import smartcar
from flask import Flask, redirect, request, jsonify, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return jsonify({"you sent": json.dumps(request.json)})

    else:
        response = jsonify({"about": "Hello World!"})
        return response
