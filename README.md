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
from flask.ext.robohash import Robohash

robohash = Robohash()
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
