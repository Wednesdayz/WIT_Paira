from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ArrowType
from sqlalchemy import create_engine 
import arrow
from flask import Flask, render_template, redirect, request, flash, abort, session, jsonify
from datetime import datetime, timezone


db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = 'Paira'

class animals(db.Model):
    """animal""" 
    __tablename__ = 'animals'

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
    __tablename__ = 'experts'
    expert_id = db.Column(db.Integer, autoincrement=True, nullable = False, primary_key=True)
    firstName = db.Column(db.String(100), nullable = False)
    lastName = db.Column(db.String(100), nullable = False)
    animals = db.Column(db.String(100), db.ForeignKey("animals.species"), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

class user(db.Model):
    """List of users"""
    __tablename__ = 'user'

    email = db.Column(db.String(100), nullable=False, unique=True)
    userid = db.Column(db.Integer, nullable=False, unique=True, autoincrement = True, primary_key = True)
    password = db.Column(db.String(500), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)

class visitor(db.Model):
    __tablename__ = 'visitor'
    userid = db.Column(db.Integer, autoincrement=True , unique=True, primary_key = True)
    


def connect_to_db(app, database='postgresql://postgres:Bbklct321@localhost:5432/postgres'):
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
