from flask_security import RegisterForm
from flask_security.forms import *

class registerForm(RegisterForm):
    username=StringField("Username", get_form_field_label('username'))
    name=StringField("Name", get_form_field_label('name'))