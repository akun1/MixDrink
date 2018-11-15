from flask import Flask, jsonify, request
app = Flask(__name__)

import requests
import json

drink_details = {}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommendation')
def recommendation():
    input = request.json
    favorite_drinks = ['Cuba Libre', 'Gin and Tonic', 
        'Long Island Ice Tea', 'Espresso Martini', 'Lemon Drop',
        'Manhattan', 'Negroni', 'Mulled Wine', 'Mimosa', 'Tennessee Mud']

    resp = []
    for drink in drink_details:
        if drink['strDrink'] in favorite_drinks:
            resp.append(drink)
    return jsonify(resp)

if __name__ == "__main__":

    response = requests.get('http://54.186.197.36/drinks')
    drink_details = response.json()
    print('Cataloged ' + str(len(drink_details)) + ' drinks')
    # for drink in drink_details:
    #     print(drink['strDrink'])
    app.run(host="0.0.0.0", port=80)