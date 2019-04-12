from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flaskApp import app, db, bcrypt
from flaskApp.main_algorithm import call_algorithm

auth = HTTPBasicAuth


@app.route("/", methods=['GET'])
def index():
    return "<h1>hello, world</h1>"

@app.route("/classdemo", methods=['GET'])
def classDemo():
    if not request.json or not 'title' in request.json:
        abort(404)
    sample_output_schedule = call_algorithm()

    return jsonify(sample_output_schedule), 201
