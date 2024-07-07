import requests

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

def search_recipes(query, number):
    '''
    Search for recipes based on the query and app_id and app_key
    returns a list of recipes.
    '''
    base_url = "https://api.edamam.com/search"
    params = {
        'q': query,
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'from': 0,
        'to': number
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['hits']
    else:
        print(f"Error: {response.status_code}")
        return None