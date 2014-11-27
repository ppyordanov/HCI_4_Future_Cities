from flask.ext.wtf import form
from werkzeug.utils import secure_filename
from wtforms import Form, BooleanField, TextField, PasswordField, validators, SelectField
from wtforms.validators import Required
from flask_wtf.file import FileField

WEATHER = [('sunny', "Sunny"), ('hot', "Hot"),( 'rainy', "Rainy"),('cloudy', "Cloudy"),('snowy', "Snowy"),('foggy', "Foggy"),('hail', "Hail")]

class UploadForm(Form):
    title = TextField('Title', [validators.Length(min=4, max=25)])
    description = TextField('Description', [validators.Length(min=6, max=35)])
    square = TextField('Square', [validators.Length(min=1, max=3)])
    weather = SelectField(u'Weather',coerce=str, choices = WEATHER, validators = [Required()])
    photo = FileField('Your photo')
