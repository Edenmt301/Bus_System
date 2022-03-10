from wtforms import Form , StringField , PasswordField , SubmitField , validators
from busSystem.models import User

class LoginForm(Form) :
    uname = StringField("Username" , validators=[
        validators.DataRequired() ,
        validators.Length(min=4 , max=20)
    ])
    password = PasswordField("Password" , validators=[
        validators.DataRequired() ,
        validators.Length(min=4 , max=20)
    ])
    submit = SubmitField("Login")