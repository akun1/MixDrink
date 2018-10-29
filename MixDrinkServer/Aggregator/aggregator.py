from flask import Flask
app = Flask(__name__)

import requests

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/stats')
def stats():
    return ''

if __name__ == "__main__":

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

    print('Cataloged ' + str(len(all_drinks)) + ' drinks')

    app.run(host="0.0.0.0", port=80)