import queue
# from flaskApp.models import Employee, Shift, Available_For

# TODO: Convert this into a function so it can be called form another script file
# TODO: Make the algorithm return something, preferably a dictionary but we cna jsonify anything

# The actual scheduling algorithm
# __________________________________

# Step 1.1: Query the database for the pertinent availability into a list.

"""
Luke is going to take care of querying the database. The following code is an example return from database queries -
a 1d list, probably in the order of the database itself. The order I expect is list[0] through
list[x] is the elements for all of the availability slots for person 1. Person 2's availability then
is list[x+1] through list[2x], and so on.

4/10/19:
Here is a sample query using SQLAlchemy that we would use in this kind of scenario:

saturday_results = Employee.query.join(Available_For, Employee.id == Available_For.employeeId).add_columns
(Employee.lname, Employee.fname).join(Shift, Shift.id == Available_For.id).add_columns(Shift.time, Shift.day)
.filter_by(day='saturday')

saturday_results = Employee.query.join(Available_For, Employee.id == Available_For.employeeId).add_columns
(Employee.lname, Employee.fname).join(Shift, Shift.id == Available_For.id).add_columns(Shift.time, Shift.day)
.filter_by(day='sunday')

those queries together will get you who is available for saturday and who is available for sunday. You can append
._asdict() to have these results returned in Python dictionary format. 

to search for slots to be filled, you can query like this:
slots_to_be_filled_saturday = Shift.query.filter_by(day='saturday').filer_by(filled = False)
slots_to_be_filled_sunday = Shift.query.filter_by(day='sunday').filter_by(filled = False)
"""

# In this example list, we are trying to schedule 3 people over 2 days, with 2 possible shifts on each day.
# As such we have 12 data points, 4 per person ie 2 per person per day (I recognize there are really no Sunday tours)
raw_availabilities = [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0]

slots_to_fill = ["Saturday: 10:15am - 11:30am", "Saturday: 11:45am - 1pm",
                 "Sunday: 10:15am - 11:30am", "Sunday: 11:45am - 1pm"]

# Greatest amount of timeslots to be filled in any given day in the selected time period.
# TO-DO: Count this while querying database.
max_slots = 2

# Total amount of shifts to be scheduled in the selected time period.
total_shifts = 4

# Headings from the table so we can have something to output into the schedule
employees = ["Luke", "George", "Zac"]

# As well as the target number of shifts per time period per person. in a realistic scenario, this would be
# a larger number given the context would be a week instead 2 days/a weekend.
# Also, realistically, there would be conflicts in target shift # per week for each employee, ie not everyone's
# ideal number can be met. We ain't there yet, so for beginning dev purposes this one happens to fit perfectly.

target_shifts = [2, 1, 1]


def make_schedule(raw_availabilities, slots_to_fill, max_slots, total_shifts, employees, target_shifts):
    employees_dict = create_employees_dict(
        employees, target_shifts, raw_availabilities)
    employees_queue = create_employees_queue(employees_dict)
    return schedule(total_shifts, employees_queue, employees_dict, slots_to_fill)

# Step 1.2: Sort the employees into a priority queue based primarily on target number of shifts
# and secondarily (if two employees have same target number of shifts) on number of available slots per person.


def create_employees_dict(employees, target_shifts, raw_availabilities):
    employees_dict = {}
    avbl_index = 0
    emp_index = 0
    for employee in employees:
        employees_dict[employee] = [target_shifts[emp_index], sum(raw_availabilities[avbl_index: avbl_index + total_shifts]),
                                    raw_availabilities[avbl_index: avbl_index + total_shifts]]
        avbl_index += total_shifts
        emp_index += 1
    return employees_dict


def create_employees_queue(employees_dict):
    ordered_employees = sorted(
        employees_dict, key=lambda k: (employees_dict[k][0], employees_dict[k][1]))
    employees_queue = queue.Queue(maxsize=len(employees))
    for emp in ordered_employees:
        employees_queue.put(emp)
    return employees_queue

# Step 2: Step through the schedule and try to schedule someone, checking the constraints to see if its possible.


print("scheduling algorithm:")


def schedule(total_shifts, employees_queue, employees_dict, slots_to_fill):
    schedule_list = [None for x in range(total_shifts)]

    while not employees_queue.empty():
        current_employee = employees_queue.get()
        print("current_employee:")
        print(current_employee)
        for shift_index in range(total_shifts):
            print("shift_index:")
            print(shift_index)
            if schedule_list[shift_index] == None and employees_dict[current_employee][2][shift_index] == 1:
                schedule_list[shift_index] = current_employee
                print("employee scheduled for shift")
                employees_dict[current_employee][0] -= 1
                print("employee remaining shifts after scheduling:")
                print(employees_dict[current_employee][0])
                if employees_dict[current_employee][0] > 0:
                    employees_queue.put(current_employee)
                    print("employee re-added to queue")
                break
            else:
                shift_index += 1

    schedule_dict = {}
    for i in range(len(schedule_list)):
        schedule_dict[slots_to_fill[i]] = schedule_list[i]
        i += 1

    return schedule_dict


# Step 3: Remove the guide from the queue if they can be scheduled
# Step 4: Keep track of how many times people have been scheduled to enforce fairness
# Step 5: Update the database with the new schedule information
# Step 6: ML to make it good


def main():
    print("schedule_dict:")
    print(make_schedule(raw_availabilities, slots_to_fill, max_slots, total_shifts, employees, target_shifts))


if __name__ == '__main__':
    main()
