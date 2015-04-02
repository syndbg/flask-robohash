# flask-robohash
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

**Always initialize in your Flask app's module (file)**

```python
from flask import Flask
from flask.ext.robohash import Robohash


app = Flask()
robohash = Robohash()
robohash.init_app(app)
```

**In backend code**

```python
@app.route('/profile/<int:id')
def profile_by(id):
    profile = Profile.query.get(id)
    return render_template('profile.html', profile=profile)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    method_type = request.method
    form = ProfileCreationForm()
    if method_type == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        form_photo = request.files.get('photo', None)
        photo = form_photo if form_photo else robohash(first_name)
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


## Robohash parameters

Robohash.org doesn't reveal all of its parameters clearly, but I managed to gather them from the source code and add a bit more to my liking.

* *INT* x (default 300) - Image horizontal size
* *INT* y (default 300) - Image vertical size
* *STR* size (default 300x300) - Constructed by params `x` and `y`. Recommended that you use `x` and `y` instead of `size`.
* *STR* format (optional) - 'bmp', 'jpg' or 'png'. The output of the image.
* *STR* bgset (optional) - 'bg1', 'bg2', 'bg3', '1', '2', '3' or 'any'. The available background sets.
* *STR* set (optional)  - 'robots', 'zombies', 'heads', 1, 2 or 3. What random creature type to generate.
* *STR* color (optional)  - The creature's color. Used to filter robots/zombies/heads by color.
* *STR* force_hash (optional and default True) - To prevent exposing user data, hash the given `text` with `md5` by default.
* *STR* hash_algorithm (optional and default md5) - Hashing algorithm to use if `force_hash`. Supports only those in `hashlib.algorithms_available`.
* *STR* use_gravatar (optional and default False) - If passed `text` is a recognized email in gravatar, built link will forward to a gravatar IMG url.
* *STR* gravatar_hashed (optional and default False) - If passed `text` is a recognized md5 email hash in gravatar, built link will forward to a gravatar IMG url.
