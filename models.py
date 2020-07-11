from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ArrowType
from sqlalchemy import create_engine 
import arrow
from flask import Flask, render_template, redirect, request, flash, abort, session, jsonify
from datetime import datetime, timezone


db = SQLAlchemy()
app = Flask(__name__)
app.secret_key 'Paira'

class animals(db.Model):
    """animal""" 
    __table__ = 'animals'

    species = db.Column(db.String(100), nullable = False, primary_key = True)
    temperament = db.Column(db.String(100),  nullable=True) 
    age = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(300), nullable=False)
    guide = db.Column(db.String(1500), nullable=False)  

#class cases(db.Model):
#    """List of cases""" 
#    animal name 
#    age
#    photo 
#    responder 
#    species 
#    injury 
#    location

class experts(db.Model):
    """List of experts""" 
    __table__ = 'experts'
    expert_id = db.Column(db.String(100), nullable = False, primary_key=True)
    firstName = db.Column(db.String(100), nullable = False)
    lastName = db.Column(db.String(100), nullable = False)
    animal = db.relationship("animals", backref = 'experts')
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

class user(db.Model):
    """List of users"""
    
    email = db.Column(db.String(100), nullable=False, unique=True)
    userid = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

class visitor(db.Model):
    userid = db.Column(db.String(100), nullable=False, unique=True)
    


def connect_to_db(app, database='postgresql://postgres:'):
    """Connect the database to flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.app_context().push()
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
