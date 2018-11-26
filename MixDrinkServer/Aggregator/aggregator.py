from flask import Flask, jsonify
app = Flask(__name__)

import requests
import json
import operator

all_drinks = []
save_file = 'catalog.json'
ingredient_file = 'ingredients.json'
ingredient_frequency = {}
detail_list = {}

ingredient_names = ['strIngredient1','strIngredient2',
    'strIngredient3','strIngredient4','strIngredient5',
    'strIngredient6','strIngredient7','strIngredient8',
    'strIngredient9','strIngredient10','strIngredient11',
    'strIngredient12','strIngredient13','strIngredient14',
    'strIngredient15']

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/stats')
def stats():
    return 'I have cataloged ' + str(len(all_drinks)) + ' drinks'

@app.route('/ingredient_stats')
def ingredient_stats():
    results = ''
    results += 'Ingredients: ' + str(len(ingredient_frequency)) + '<br></br>'
    results += ' Top 10<br></br>'
    sorted_ing_freqs = list(reversed(sorted(ingredient_frequency.items(), key=operator.itemgetter(1))))
    for i in range(0, 10):
        results += str(sorted_ing_freqs[i]) + '<br></br>'

    return results

@app.route('/drinks')
def drinks():
    return jsonify(detail_list)

@app.route('/ingredients')
def ingredients():
    return jsonify(ingredient_frequency)


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

        ingredient_list = []
        for key in ingredient_names:
            if details[key]:
                ingredient_list.append(details[key])
        details['allIngredients'] = ingredient_list
        drink_details.append(details)

    return drink_details

def get_ingredient_frequencies(drink_details):

    freq = {}
    for drink in drink_details:
        for name in ingredient_names:
            ingredient = drink[name]
            if ingredient:
                ingredient = ingredient.lower()
                if ingredient in freq:
                    freq[ingredient] += 1
                else:
                    freq[ingredient] = 1
    

    return freq


if __name__ == "__main__":

    update_catalog = False

    if update_catalog:
        detail_list = get_all_cocktaildb()
        with open(save_file, 'w') as fout:
            json.dump(detail_list, fout)

    else:
        with open(save_file, 'r') as fin:
            detail_list = json.load(fin)

    ingredient_frequency = get_ingredient_frequencies(detail_list)
    with open(ingredient_file, 'w') as fout:
        json.dump(ingredient_frequency, fout)

    print('Cataloged ' + str(len(detail_list)) + ' drinks')

    app.run(host="0.0.0.0", port=80)