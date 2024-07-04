import requests

def search_recipes(query, number,app_id, app_key):
    '''
    Search for recipes based on the query and app_id and app_key
    returns a list of recipes.
    '''
    base_url = "https://api.edamam.com/search"
    params = {
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
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