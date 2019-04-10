from datetime import datetime
from flaskApp import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)


class Employee(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(20), nullable=False)
    fname = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Employee('{self.id}', '{self.lname}', '{self.fname}')"


class Shift(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(7), nullable=False)
    day = db.Column(db.String(15), nullable=False)
    month = db.Column(db.String(9), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    filled = db.Column(db.Boolean, nullable=False)


class Available_For(db.Model):
    __table_args__ = {'extend_existing': True}
    employeeId = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True, nullable=False)
    shiftId = db.Column(db.Integer, db.ForeignKey('shift.id'), primary_key=True, nullable=False)


