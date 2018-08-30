import datetime
import os
import dicttoxml
from dicttoxml import dicttoxml
import requests
from flask_restful import Resource, Api
from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)
api = Api(app)  # api is a collection of objects, where each object contains a specific functionality (GET, POST, etc)

# My own API with google script and GoogleSheets
API_URL_BASE = 'https://script.google.com/macros/s/AKfycbwjnEMw_u8Ph6dypWX_JWlDz77j9Qv8aSLiE8uKYfYc68FgrZSM/exec'

@app.route('/finance/api/v1/stocks')
def AllStocks():
    response = requests.get(API_URL_BASE)

    if response.status_code == 200:
        return response.content  # json.loads(response.content.JSONDecoder('utf-8'))
    else:
        return None

@app.route('/xml')
def AllStocksXML():
    response = requests.get(API_URL_BASE)

    try:
        xml = dicttoxml.dicttoxml(response.content)
    except Exception as e:
        return json.loads(e)

    if response.status_code == 200:
        return xml
    else:
        return xml

@app.route('/finance/api/v1/stocks/<string:ticker>')
def Ticker(ticker):
    response = requests.get(API_URL_BASE + '?ticker=' + ticker)

    if response.status_code == 200:
        return response.content  # json.loads(response.content.JSONDecoder('utf-8'))
    else:
        return None

class NewTicker(Resource):
    def post(self, ticker):  # param is pulled from url string

        response = requests.post(API_URL_BASE + '?ticker=' + ticker)

        if response.status_code == 200:
            return response.content #json.loads(response.content)
        else:
            return None

@app.route('/')
@app.route('/home')
@app.route('/finance')
@app.route('/finance/api')
@app.route('/finance/api/v1')
def index():
    return render_template(
        'index.html',
        title='Home Page'
    )

# once we've defined our api functionalities, add them to the master API object
#api.add_resource(Home, '/home')
#api.add_resource(AllStocks, '/finance/api/v1/stocks')
#api.add_resource(Ticker, '/finance/api/v1/stocks/<string:ticker>')
api.add_resource(NewTicker, '/finance/api/v1/newTicker/<string:ticker>')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

################# Study this case ##########################################
#REF: https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12 ###############
