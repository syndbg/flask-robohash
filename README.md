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

Robohash.org doesn't reveal all of its parameters clearly, but I managed to gather them from the source code.

* *INT* x - Image horizontal size
* *INT* y - Image vertical size
* *STR* format - 'bmp', 'jpg' or 'png'. The output of the image.
* *STR* bgset - '1', '2' or '3' or 'any'. The available background sets.
* *STR* size - '200x200'. Constructed by params `x` and `y`. Recommended that you use `x` and `y` instead of `size`.

