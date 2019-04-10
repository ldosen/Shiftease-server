from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flaskApp import app, db, bcrypt
# import flaskApp.main_algorithm


@app.route("/", methods=['GET'])
def index():
    return "<h1>hello, world</h1>"

@app.route("/classdemo", methods=['GET', 'POST'])
def classDemo():
    if not request.json or not 'title' in request.json:
        abort(404)
    sample_output_schedule = None # call the main algorithm here \
    # TODO: refactor the main algorithm to be a class so args can be passed here

    return jsonify(sample_output_schedule), 201
