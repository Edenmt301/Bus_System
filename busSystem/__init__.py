from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
pwd = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginpage"
login_manager.login_message = "You are mot authorised to access this page. Please login first."
login_manager.login_message_category = "danger" 

from busSystem.models import Route, User, Bus, Station, Route_Station
from busSystem import routes