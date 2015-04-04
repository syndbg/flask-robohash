# flask-robohash

[![Coverage Status](https://coveralls.io/repos/syndbg/flask-robohash/badge.svg)](https://coveralls.io/r/syndbg/flask-robohash)
[![Build Status](https://travis-ci.org/syndbg/flask-robohash.svg)](https://travis-ci.org/syndbg/flask-robohash)

![Flask Robohash](https://robohash.org/robohash?size=200x200 "Flask Robohash")

Cause Gravatar ain't got nothing on robots avatars!


## Installation


```
pip install flask-robohash
```

If you want to contribute and run the tests:

```
pip install flask-robohash
pip install -r requirements/developing.pip
```

## Usage

### Always instantiate `Robohash`


**The verbose way**
```python
from flask import Flask
from flask.ext.robohash import Robohash


awesome_app = Flask()
robohash = Robohash()
robohash.init_app(awesome_app)
```

**or just**
```python
robohash = Robohash(app=awesome_app)
```
**but if you want default app-wide options**
```python
robohash = Robohash(app=awesome_app,
                    x=128,
                    y=128,
                    hash_algorithm='sha256')
```

**In views(controllers)**

```python
@app.route('/profile/<int:id>')
def profile_by(id):
    profile = Profile.query.get(id)
    return render_template('profile.html', profile=profile)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    method_type = request.method
    form = ProfileCreationForm()
    if method_type == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        photo = request.files.get('photo') or robohash(first_name)
        new_profile = Profile(first_name=first_name,
                              last_name=form.last_name.data,
                              photo=photo)
        db.session.add(new_profile)
        db.session.commit()
        flash('Registration successfull!')
        return redirect(url_for('profile_by', id=new_profile.id))
    return render_template('profiles.html')
```


**In templates as a filter**

 ```python
 {{ user.first_name | robohash }}
 ```

 Or with args

 ```python
 {{ user.first_name | robohash(x=200, y=200) }}
 ```


## Robohash parameters

Robohash.org doesn't reveal all of its parameters clearly, but I managed to gather them from the source code and add a bit more to my liking.


| Type  |  Name       |   Notes |   Default |   Optional |
|:-:	|:-:	      |:-:	|:-:	|:-:	|
|   STR |   text      |Used to generate a random robot/zombie/head by `robohash.org`. Should be provided to the Robohash class constructor only if you want a default image. When used with template filters, you still provide a `text` as seen in the `Usage` section.  |   flask-robohash	|   ✗	|
|   INT |   x         |Image horizontal size|   300	|   ✔	|
|   INT |   y         |Image vertical size  |  300 	|  ✔ 	|
|   STR | size        |Image size as WxH. `x` and `y` are prioritized over `size` if supplied.	|  None 	|   ✔	|
|   STR	| format      |Image format. Options are `png`, `jpg`, `bmp`   	|   None	|  ✔ 	|
|   STR	| bgset       |Image background. Options are `any`, `1`, `2`, `3`|   None |   ✔	|
|   STR	|creature_type|Options are `robots`, `zombies`, `heads` or just `1`, `2`, `3`.|   None|  ✔ 	|
|   STR |   color     |Creature's color. `red`, `green`, `blue` and etc.  	|   None|   ✔	|
|   STR	| force_hash  | To hash the provided `text` or not. Recommended left default to hide user info.  	|   True|   ✔	|
|   STR	|hash_algorithm| The algorithm to use when hashing `text`. Supported algos are those in `hashlib.algorithms_available`  	|   md5	|   ✔	|
|   STR	|use_gravatar| If provided `text` is a recognized Gravatar user email. Generated `robohash.org` URL will redirect to that user's Gravatar img.	|   False	|   ✔	|
|   STR	|gravatar_hashed| If provided `text` is a recognized and already MD5 hashed as mentioned in https://en.gravatar.com/site/implement/images/ , generated robohash.org URL will redirect to that user's Gravatar img. 	|   False	|   ✔	|
