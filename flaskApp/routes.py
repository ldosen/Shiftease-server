from flask import request, jsonify, abort, Response
from flaskApp import app, db, bcrypt
from flaskApp.models import Users, Employee, Manager, Available_For, Scheduled_For, Shift
# import flaskApp.main_algorithm

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
    request_data = request.get_json()
    if request_data is not None:
        username = request_data.json['username']
        email = request_data.json['email']
        password = request_data.json['password']
        usertype = request_data.json['usertype']
        fname = request_data.json['fname']
        lname = request_data.json['lname']

        user = Users(username=username, email=email, password=password, usertype=usertype)

        db.session.add(user)
        db.session.commit()
        return Response(status=200)
    else:
        abort(400)



@app.route("/calendar/<id>", methods=['GET'])
def get_employee_calendar(id):
    results = Employee.query.filter_by(id=id).join(Scheduled_For, Employee.id == Scheduled_For.employeeId)\
        .add_columns(Employee.fname)\
        .join(Shift, Scheduled_For.shiftId == Shift.id).add_columns(Shift.time, Shift.day, Shift.month)
    dict_results = list()
    for row in results:
        rowDict = row._asdict()
        dict_results.append(rowDict)
    return str(dict_results)

