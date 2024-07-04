#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, render_template, request
import random
import concurrent.futures
import api

app = Flask(__name__)

APP_ID = "0b16882d"
APP_KEY = "9a04913ab5bb2dfa66bf19ae617b1624"

foods_and_snacks = [
    "Apple","Banana","Orange","Grapes","Strawberry","Blueberry","Raspberry","Blackberry","Watermelon","Pineapple",
    "Mango","Papaya","Kiwi","Peach","Plum","Cherry","Apricot","Nectarine","Pomegranate","Cantaloupe",
    "Honeydew","Tomato","Cucumber","Carrot","Celery","Wheat","Barley","Rye","Juice", "Jelly","Yogurt",
    "Bell Pepper","Broccoli","Cauliflower","Spinach","Kale","Lettuce","Cabbage","Brussels Sprouts","Asparagus","Green Beans",
    "Peas","Corn","Potato","Sweet Potato","Pumpkin","Zucchini","Eggplant","Mushroom","Onion","Garlic",
    "Ginger","Beetroot","Radish","Turnip","Parsnip","Artichoke","Avocado","Olives","Chickpeas","Lentils",
    "Black Beans","Kidney Beans","Pinto Beans","Soybeans","Edamame","Tofu","Tempeh","Quinoa","Rice","Oats",
    "Millet","Amaranth","Buckwheat","Chia Seeds","Flax Seeds","Pumpkin Seeds","Sunflower Seeds","Almonds","Walnuts","Cashews",
    "Pistachios","Pecans","Hazelnuts","Brazil Nuts","Macadamia Nuts","Peanuts","Peanut Butter","Almond Butter","Tahini",
    "Hummus","Granola","Yogurt","Cheese","Milk","Cottage Cheese","Cream Cheese","Butter","Eggs","Chicken",
    "Beef","Pork","Lamb","Turkey","Fish","Shrimp","Crab","Lobster","Salmon","Tuna","Pizza","Pasta","Ravioli","Spaghetti",
    "Lasagna","Risotto","Casserole","Omelette","Pancakes","Waffles","Crepes","Custard","Cocoa","Coffee","Tea","Water", "Burger",
    "Fries", "Salad", "Soup"
]


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    """returns the index page of the project"""
    if request.method == 'POST':
        search = request.form.get('search')
        recipes = None
        if search:
            recipes = api.search_recipes(search, 20, APP_ID, APP_KEY)
        return render_template('search_results.html', recipes=recipes, results=search)
    
    choice = random.choice(foods_and_snacks)
    recipes = api.search_recipes(choice, 3, APP_ID, APP_KEY)
    return render_template('index.html', recipes=recipes)

@app.route('/browse', methods=['GET', 'POST'], strict_slashes=False)
def browse():
    """returns the browse page of the project"""
    if request.method == 'POST':
        search = request.form.get('search')
        recipes = None
        if search:
            recipes = api.search_recipes(search, 20, APP_ID, APP_KEY)
        return render_template('search_results.html', recipes=recipes, results=search)

    all_recipes = []  
    def fetch_recipes(food):
        return api.search_recipes(food, 6, APP_ID, APP_KEY)
      
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_food = {executor.submit(fetch_recipes, food): food for food in foods_and_snacks}
        for future in concurrent.futures.as_completed(future_to_food):
            food = future_to_food[future]
            try:
                recipes = future.result()
                all_recipes.extend(recipes)
            except Exception as exc:
                print(f'Food {food} generated an exception: {exc}')

    random.shuffle(all_recipes)
    return render_template('browse_recipes.html', recipes=all_recipes)

@app.route('/login', strict_slashes=False)
def login():
    """returns the login page of the project"""
    return render_template('login.html')

@app.route('/register', strict_slashes=False)
def registration():
    """returns the registration page of the project"""
    return render_template('registration.html')

@app.route('/about', methods=['GET', 'POST'], strict_slashes=False)
def about():
    """returns the about page of the project"""
    if request.method == 'POST':
        search = request.form.get('search')
        recipes = None
        if search:
            recipes = api.search_recipes(search, 20, APP_ID, APP_KEY)
        return render_template('search_results.html', recipes=recipes, results=search)
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
