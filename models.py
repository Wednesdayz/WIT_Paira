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

class cases(db.Model):
    """List of cases""" 
    responder 
    species 
    injury 
    expert

class experts(db.Model):
    """List of experts""" 

class user(db.Model):
    """List of users""" 

class posts(db.Model):
    """List of posts""" 

class comments(db.Model):
    """List of comment""" 



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
