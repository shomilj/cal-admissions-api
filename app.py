from flask import Flask 
from flask import request, jsonify
from utils import *

app = Flask(__name__) 

@app.route("/api", methods=['POST']) 
def api(): 
    if request.json and 'columns' in request.json and 'filters' in request.json:
        columns = request.json['columns']
        filters = request.json['filters']
        return jsonify(query(columns, filters).to_csv())
    else:
        return jsonify('hello')
