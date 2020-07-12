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

UPLOAD_FOLDER = os.path.join('static/images')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.secret_key = 'Bbklct321'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

@app.route('/')
def homepage():
    """Display Homepage"""

    return render_template("emergency.html")

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

@app.route('/pickups.json')
def get_pickups_json():
    """Provide JSON for pickup locations"""

    pickup_json = {"locations": {}, "ids": []}
    pickups = Experts.query.filter(Experts.expert_id > 1).all()

    for pickup in pickups:
        pickup_json["locations"][pickup.firstName] = {"id": pickup.expert_id,
                                                 "name": pickup.firstName,
                                                 "description": pickup.animals,
                                                 "address": pickup.location,
                                                 "zipcode": pickup.zipcode}
        pickup_json["ids"].append(pickup.firstName)

    return jsonify(**pickup_json)

@app.route('/experts')
def experts():
    """experts"""
    pickups = db.session.query(Experts).filter(Experts.expert_id > 0).all()
    return render_template("experts.html", pickups=pickups)

@app.route('/donate')
def donate():
    """donation"""
    return render_template("donateNow.html")

@app.route('/emergency')
def emergency():
    """emergency"""
    return render_template("emergency.html")

@app.route('/guides')
def guides():
    """guides"""
    g = db.session.query(Guides)
    return render_template("guides.html", guides = g)

@app.route('/guides/<int:guideNumber>')
def show_guide_page(guideNumber):
    """Query database for product info and display results"""
    gui = Guides.query.get(guideNumber)
    co = db.session.query(user).filter(user.userid == gui.userid).one()

    return render_template("guide_page.html", guides = gui, con = co)

@app.route('/add')
def create():
    """create new guide"""
    if session.get('email'):
        use = db.session.query(user).filter(user.email == session['email']).one()
        return render_template("addGuide.html", user = use)
    else:
        flash('Please login')
        return redirect('/')

@app.route('/addGuide', methods=['GET', 'POST'])
def add_guide():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        name = secure_filename(f.filename)

    user_id = db.session.query(user).filter(user.email ==session['email']).one().userid
    guide_name = request.form.get("guideName")
    guide_description = request.form.get("description")
    specie = request.form.get("species")
    
    new_guide = Guides(userid = user_id, guideName = guide_name, description = guide_description, species = specie, photo = name)
    db.session.add(new_guide)
    db.session.commit()
    flash('New guide created')
    return redirect("/guides")



if __name__ == "__main__":
    # Change app.debug to False before launch
    app.debug = True
    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0")