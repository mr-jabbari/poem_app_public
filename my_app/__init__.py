# Jabbari79
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import boto3, os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'
password = "password"
my_db = "my_db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{password}@localhost/{my_db}'

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
db = SQLAlchemy(app)

from my_app import functions
from my_app import models
from my_app import forms
from my_app import routs_web
from my_app import routes_api
from my_app import routes_functions