from flask import Flask, jsonify, request
app = Flask(__name__)

import requests
import json

drink_details = {}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    input = request.json
    print(input)
    favorite_drinks = ['Cuba Libre', 'Gin and Tonic', 
        'Long Island Ice Tea', 'Espresso Martini', 'Lemon Drop',
        'Manhattan', 'Negroni', 'Mulled Wine', 'Mimosa', 'Tennessee Mud']

    drink_scores = {
        'Cuba Libre' : 5.0,
        'Gin and Tonic' : 4.5,
        'Long Island Ice Tea' : 4.6,
        'Espresso Martini' : 3.2,
        'Lemon Drop' : 2.9,
        'Manhattan' : 3.8,
        'Negroni' : 4.1,
        'Mulled Wine' : 1.8,
        'Mimosa' : 3.5,
        'Tennessee Mud' : 4.9
    }

    resp = []
    for drink in drink_details:
        if drink['strDrink'] in favorite_drinks:
            drink['rating'] = drink_scores[drink['strDrink']]
            resp.append(drink)
    return jsonify(resp)

if __name__ == "__main__":

    response = requests.get('http://54.186.197.36/drinks')
    drink_details = response.json()
    print('Cataloged ' + str(len(drink_details)) + ' drinks')
    # for drink in drink_details:
    #     print(drink['strDrink'])
    app.run(host="0.0.0.0", port=80)