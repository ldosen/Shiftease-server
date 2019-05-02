from flask import request, jsonify, abort, Response
from flaskApp import app, db, ma, bcrypt
from flaskApp.models import Users, Employee, Manager, Available_For, Scheduled_For, Shift, Scheduled_For_Schema, Employee_Schema, Available_For_Schema
from flaskApp.main_algorithm import call_algorithm


employee_schema = Employee_Schema(many=True)


@app.route("/")
def index():
    return "<h1> hello, world </h1>"


@app.route("/register", methods=['POST'])
def register():
    # get the request as JSON, get the required fields, then create a new user with those fields
    request_data = request.get_json(force=True)
    if request_data is not None:
        username = request_data['username']
        email = request_data['email']
        password = request_data['password']
        user_type = request_data['user_type']

        user = Users(username=username, email=email, password=password, user_type=user_type)

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


@app.route("/available_for/<employee_id>", methods=['GET'])
def get_employee_availability(employee_id):
    available_for_schema = Available_For_Schema(many=True)
    results = Available_For.query.filter(Available_For.employee_id==employee_id)
    curr_user_availability = available_for_schema.dump(results)
    return jsonify(curr_user_availability.data)


@app.route("/create_scheduled_for", methods=['POST'])
def create_scheduled_for():
    request_data = request.get_json(force=True)
    employee_id = request_data['employee_id']
    shift_id = request_data['shift_id']

    scheduled_for = Scheduled_For(employee_id=employee_id, shift_id=shift_id)
    db.session.add(scheduled_for)
    db.session.commit()
    return Response(status=200)


@app.route("/scheduled_for/<employee_id>/<shift_id>/delete", methods=['POST'])
def delete_scheduled_for(employee_id, shift_id):
    scheduled_for = Scheduled_For.query.filter_by(employee_id=employee_id).filter_by(shift_id=shift_id)
    db.session.delete(scheduled_for)
    db.session.commit()
    return Response(status=200)


@app.route("/user/<id>/update_email", methods=['POST'])
def update_user_email(id):

    curr_user = Users.query.get(id)
    curr_email = curr_user.email
    request_data = request.get_json(force=True)
    new_email = request_data['email']

    if curr_email != new_email:
        curr_user.email = new_email
        db.session.commit()
        return Response(status=200)

    else:
        return Response(status=400)


@app.route("/shift/count", methods=['GET'])
def get_count_filled_shifts():
    count = Shift.query.filter_by(filled=False).count()
    return jsonify(count)


@app.route("/available_for/<timeslot>/<day>", methods=['GET'])
def get_free_guide_names_by_timeslot(timeslot, day):
    employee_schema = Employee_Schema(many=True)
    results = Employee.query.join(Available_For, Employee.id == Available_For.employee_id).join(Shift, Available_For.shift_id == Shift.id).filter(Shift.day==day).filter(Shift.time==timeslot)
    employees_for_timeslot = employee_schema.dump(results)
    return jsonify(employees_for_timeslot.data)
