from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# remove these when not in a test environment
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kbrhughlcqlylc:4d8a00e22981b27d974dff2863946a8f9e4a6ff166fd1475b43a95c8f4a54be1@ec2-50-19-114-27.compute-1.amazonaws.com:5432/d699no4mvj906n'

CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskApp import routes
from flaskApp import models

models.db.create_all()

