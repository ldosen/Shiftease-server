from flask import request, jsonify, abort, Response
from flaskApp import app, db, ma, bcrypt
from flaskApp.models import Users, Employee, Manager, Available_For, Scheduled_For, Shift, Scheduled_For_Schema, Employee_Schema
# import flaskApp.main_algorithm


employee_schema = Employee_Schema(many=True)

@app.route("/")
def index():
    return "<h1> hello, world </h1>"


@app.route("/integrationdemo", methods=['GET'])
def integration_demo():

    demo_data = {10: {"9am": "Ramsha", "10am": "Somto", "11am":"Maha"},
                 16: {"8am": "Maha", "10am": "Luke"},
                 27: {"12pm": "Jonathan"}}

    return jsonify(demo_data)


@app.route("/register", methods=['POST'])
def register():
    # get the request as JSON, get the required fields, then create a new user with those fields
    request_data = request.get_json(force=True)
    if request_data is not None:
        username = request_data.json['username']
        email = request_data.json['email']
        password = request_data.json['password']
        user_type = request_data.json['user_type']

        user = Users(username=username, email=email, password=password, usertype=user_type)

        db.session.add(user)
        db.session.commit()
        return Response(status=200)
    else:
        abort(400)


@app.route("/employee/<id>", methods=['GET'])
def get_employee_info(id):
    results = Employee.query.filter_by(id=id)
    employee_data = employee_schema.dump(results)
    return jsonify(employee_data.data)


@app.route("/scheduled_for/<employee_id>", methods=['GET'])
def get_employee_schedule(employee_id):
    scheduled_for_schema = Scheduled_For_Schema(many=True)
    results = Scheduled_For.query.filter(Scheduled_For.employee_id == employee_id)
    curr_user_schedule = scheduled_for_schema.dump(results)
    return jsonify(curr_user_schedule.data)


@app.route("/scheduled_for/", methods=['GET'])
def get_all_scheduled_shifts():
    schedule_for_schema = Scheduled_For_Schema(many=True)
    results = Scheduled_For.query.all()
    return schedule_for_schema.jsonify(results)


@app.route("/employee", methods=['POST'])
def create_new_employee():
    return None


@app.route("/scheduled_for", methods=['POST'])
def schedule_new_guide():
    return None
