#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
import random, jsonify
import concurrent.futures
import api
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '9a04913ab5bb2dfa66bf19ae617b1624'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///masterchef.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))
        else:
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    if form.email.data and form.password.data:
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def home():
    """returns the index page of the project"""
    global REGISTER, LOGIN, FAILED
    LOGIN = False
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        search = request.form.get('search')
        recipes = None
        if search:
            recipes = api.search_recipes(search, 20)
        return render_template('search_results.html', recipes=recipes, results=search)
    
    choice = random.choice(api.foods_and_snacks)
    recipes = api.search_recipes(choice, 3)
    return render_template('home.html', recipes=recipes)

@app.route('/browse', methods=['GET', 'POST'], strict_slashes=False)
def browse():
    """returns the browse page of the project"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        search = request.form.get('search')
        recipes = None
        if search:
            recipes = api.search_recipes(search, 20)
        return render_template('search_results.html', recipes=recipes, results=search)

    all_recipes = []  
    def fetch_recipes(food):
        return api.search_recipes(food, 6)
      
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_food = {executor.submit(fetch_recipes, food): food for food in api.foods_and_snacks}
        for future in concurrent.futures.as_completed(future_to_food):
            food = future_to_food[future]
            try:
                recipes = future.result()
                all_recipes.extend(recipes)
            except Exception as exc:
                print(f'Food {food} generated an exception: {exc}')

    random.shuffle(all_recipes)
    return render_template('browse_recipes.html', recipes=all_recipes)

@app.route('/about', methods=['GET', 'POST'], strict_slashes=False)
def about():
    """returns the about page of the project"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        search = request.form.get('search')
        recipes = None
        if search:
            recipes = api.search_recipes(search, 20)
        return render_template('search_results.html', recipes=recipes, results=search)
    return render_template('about.html')


def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port="5000")
