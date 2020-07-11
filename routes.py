from flask import Flask, render_template, redirect, request, flash, abort, session, send_from_directory, abort
from flask.json import jsonify
import json
from flask_mail import Mail, Message
import os
from jinja2 import StrictUndefined
from passlib.hash import pbkdf2_sha256
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'paira'

@app.route('/')
def homepage():
    """Display Homepage"""
    
    return render_template("homepage.html")


if __name__ == "__main__":
    # Change app.debug to False before launch
    app.debug = True
    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")