from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

app = Flask(__name__)
"""
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://niuenxjulkpxav:09f3c861d5df0e5e06235f8a73fc54c2665864942b2459f9c96ff496d0cdcbb0@ec2-50-17-246-114.compute-1.amazonaws.com:5432/d688gbqp26k5fr'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskApp import routes
from flaskApp import models

models.db.create_all()
"""
