from flask import Flask
app = Flask(__name__)

import requests
import json

all_drinks = []
save_file = 'catalog.json'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/stats')
def stats():
    return 'I have cataloged ' + str(len(all_drinks)) + ' drinks'

def get_all_cocktaildb():
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?g=list')
    data = response.json()
    drink_categories = data['drinks']
    
    print('Getting drinks from ' + str(len(drink_categories)) + ' categories')

    all_drinks = []

    for category in drink_categories:

        print('Adding drinks that go in a ' + category['strGlass'])

        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=' + category['strGlass'])
        data = response.json()
        drink_list = data['drinks']
        all_drinks = all_drinks + drink_list

    drink_details = []

    for drink in all_drinks:
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='+drink['idDrink'])
        data = response.json()
        details = data['drinks'][0]
        drink_details.append(details)

    return drink_details

if __name__ == "__main__":

    update_catalog = False

    if update_catalog:
        detail_list = get_all_cocktaildb()
        with open(save_file, 'w') as fout:
            json.dump(detail_list, fout)

    else:
        with open(save_file, 'r') as fin:
            detail_list = json.load(fin)

    print('Cataloged ' + str(len(detail_list)) + ' drinks')

    app.run(host="0.0.0.0", port=80)