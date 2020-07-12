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
    guide = db.Column(db.String(1500), nullable=True) 

class Guides(db.Model):
    """animal guide"""
    __tablename__ = 'guides'
    userid = db.Column(db.Integer, nullable=False)
    guideName = db.Column(db.String(100), nullable = False)
    guideNumber = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    description = db.Column(db.String(5000), nullable = False)
    species = db.Column(db.String(100), nullable = False)
    photo = db.Column(db.String(200), nullable = False)


#class cases(db.Model):
#    """List of cases""" 
#    animal name 
#    age
#    photo 
#    responder 
#    species 
#    injury 
#    location

class Experts(db.Model):
    """List of experts""" 
    __tablename__ = 'experts'
    expert_id = db.Column(db.Integer, autoincrement=True, nullable = False, primary_key=True)
    firstName = db.Column(db.String(100), nullable = False)
    lastName = db.Column(db.String(100), nullable = False)
    animals = db.Column(db.String(100), db.ForeignKey("animals.species"), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    zipcode = db.Column(db.String(500), nullable=False)

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

def populate_db():

    animal1 = animals(species = "quokka", temperament = "happy", age = "young", photo ="./static/images/thequokka.jpg")
    animal2 = animals(species = "cats", temperament = "fluffy", age ="old", photo = "./static/images/theKoala.png")
    expert1 = Experts(expert_id = 1, firstName = "John", lastName = "Smith", animals = "quokka", email = "james@hotmail.com", password = "holo", location = "161 Sussex St, Sydney", zipcode = "2001")
    expert2 = Experts(expert_id = 2, firstName = "Smith", lastName = "John", animals = "cats", email = "smith@hotmail.com", password = "hoolo", location = "14 The Avenue, North Sydney", zipcode = "2060" )
    expert3 = Experts(expert_id = 3, firstName = "Johnny", lastName = "Sins", animals = "cats", email = "Johnnysins@hotmail.com", password = "hooo", location = "33 Macquarie St, Sydney, NSW", zipcode = "2000" )

    db.session.add(animal1)
    db.session.add(animal2)
    db.session.commit()
    db.session.add(expert1)
    db.session.add(expert2)
    db.session.add(expert3)
    db.session.commit()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    connect_to_db(app)
    db.create_all()
    populate_db()
    print("Connected to DB.")
