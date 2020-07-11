from flask import Flask, render_template, redirect, request, flash, abort, session, send_from_directory, abort
from flask.json import jsonify
import json
from flask_mail import Mail, Message
import os
from jinja2 import StrictUndefined
from passlib.hash import pbkdf2_sha256
from werkzeug import secure_filename
from models import *

app = Flask(__name__)
app.secret_key = 'paira'

UPLOAD_FOLDER = os.path.join('static/img')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.secret_key = 'Bbklct321'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

@app.route('/')
def homepage():
    """Display Homepage"""

    return render_template("homepage.html")

@app.route('/register')
def show_register():
    """Show registration form"""

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def process_registration():
    """Process user registration"""

    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    password = request.form.get("password")
    password = pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=16)
    phone = request.form.get("phone")

    curr = user(firstName=firstName, lastName=lastName, email=email, password=password)
    
    db.session.add(curr)
    db.session.commit()

    session['email'] = email
    if session.get('email'):
        flash("Registration successful! Welcome to animal shelter!")
    else:
        flash("Please enable cookies to log in")

    return redirect("/")

@app.route('/logout')
def process_logout():
    """Log user out, redirect to /products"""

    del session['email']

    flash("You have been logged out.")

    return redirect("/")

@app.route('/login', methods=['POST'])
def process_login():
    """Process login data. Add user_id to session"""

    email = request.form.get('email')
    password = request.form.get('password')

    curr = db.session.query(user).filter(user.email == email).first()

    if curr and pbkdf2_sha256.verify(password, curr.password):

        session['email'] = email
        if session.get('email'):
            flash("Login successful!")
            return redirect("/")  
        else:
            return "CookieFail"

    else:

        return "Fail"

@app.route('/whoAreWe')
def who_are_we():
    """Who are we""" 
    return render_template("whoAreWe.html")

@app.route('/guides')
def guides():
    """guides"""
    return render_template("guides.html")

@app.route('/experts')
def experts():
    """experts"""
    return render_template("experts.html")

@app.route('/donate')
def donate():
    """donation"""
    return render_template("donateNow.html")

@app.route('/emergency')
def emergency():
    """emergency"""
    return render_template("emergency.html")

@app.route('/addGuide')
def add_guide():
    """add guide"""
    return render_template("add guide")

if __name__ == "__main__":
    # Change app.debug to False before launch
    app.debug = True
    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0")