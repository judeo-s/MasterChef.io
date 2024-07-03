#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """returns the index page of the project"""
    return render_template('home.html')

@app.route('/login', strict_slashes=False)
def login():
    """returns the login page of the project"""
    return render_template('login.html')

@app.route('/registration', strict_slashes=False)
def registration():
    """returns the registration page of the project"""
    return render_template('registration.html')

@app.route('/about', strict_slashes=False)
def about():
    """returns the about page of the project"""
    return render_template('about.html')

@app.route('/contact', strict_slashes=False)
def contact():
    """returns the contact page of the project"""
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
