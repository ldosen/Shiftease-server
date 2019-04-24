import queue
# from flaskApp.models import Employee, Shift, Available_For

# The actual scheduling algorithm
# __________________________________

# Query the database for the pertinent availability into a list.

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

#slots_to_fill = ["Saturday: 10:15am - 11:30am", "Saturday: 11:45am - 1pm",
 #                "Sunday: 10:15am - 11:30am", "Sunday: 11:45am - 1pm"]

# version 2
slots_to_fill = {2019: {4:{23:{"9am": None,"10am": None}, 24:{"9am": None,"10am": None}}}}

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


def call_algorithm():
    raw_availabilities = [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0]
    slots_to_fill = {2019: {4:{23:{"9am": None,"10am": None}, 24:{"9am": None,"10am": None}}}}
    max_slots = 2
    total_shifts = 4
    employees = ["Luke", "George", "Zac"]
    target_shifts = [2, 1, 1]
    return make_schedule(raw_availabilities, slots_to_fill, max_slots, total_shifts, employees, target_shifts)

# ______________________________________________________________________________________________
# Division between pseudo-testing setup (above) and actual algorithm methods (below)
# _______________________________________________________________________________________________


# Call methods below to process data into the necessary inputs for the scheduling algorithm itself, then calls
# that algorithm. Returns the final schedule output
# This is the method the server will call
def make_schedule(raw_availabilities, slots_to_fill, max_slots, total_shifts, employees, target_shifts):
    employees_dict = create_employees_dict(
        employees, target_shifts, raw_availabilities)
    employees_queue = create_employees_queue(employees_dict)
    return schedule(total_shifts, employees_queue, employees_dict, slots_to_fill)

# Create employees dict, effectively mapping each employee to all their relevant information in the format
# Employee: [target shifts, total shifts they are available for, list of all their availabilities]


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

# Sort the employees into a priority queue based primarily on target number of shifts
# and secondarily (if two employees have same target number of shifts) on number of available slots per person.


def create_employees_queue(employees_dict):
    ordered_employees = sorted(
        employees_dict, key=lambda k: (employees_dict[k][0], employees_dict[k][1]))
    employees_queue = queue.Queue(maxsize=len(employees))
    for emp in ordered_employees:
        employees_queue.put(emp)
    return employees_queue

# Scheduling algorithm


def schedule(total_shifts, employees_queue, employees_dict, slots_to_fill):
    # List of employees (empty, filled below) in the order of shifts in given time period
    schedule_list = [None for x in range(total_shifts)]
    # List of employees who could not be scheduled by the algorithm
    unschedulable = {}

    # Iterate through employees queue
    while not employees_queue.empty():
        current_employee = employees_queue.get()
        current_target_shifts = employees_dict[current_employee][0]
        # Try to schedule current employee for each shift
        for shift_index in range(total_shifts):
            # Schedule current employee for current shift if shift is unfilled and employee is available
            if schedule_list[shift_index] == None and employees_dict[current_employee][2][shift_index] == 1:
                schedule_list[shift_index] = current_employee
                # Decrement amount of remaining shifts to fill for current employee
                employees_dict[current_employee][0] -= 1
                # Add employee back into queue if they have any remaining shifts to be scheduled for (target shifts)
                if employees_dict[current_employee][0] > 0:
                    employees_queue.put(current_employee)
                break
        # If employee cannot fill any shift after iterating through all shifts, add to
        # list of unschedulable employees to be manually handled by manager
        # Output is a dict of each unschedulable employee to a list for which index 0
        # is their currently remaining shifts and index 1 is their initial # of target shifts
        if employees_dict[current_employee][0] > 0:
            unschedulable[current_employee] = [employees_dict[current_employee][0], current_target_shifts]

    # Dictionary mapping shifts to employees that have filled them
    # schedule_dict = {}
    """for i in range(len(schedule_list)):
        schedule_dict[slots_to_fill[0]] = slots_to_fill[1]
        schedule_dict[slots_to_fill[i]] = schedule_list[i]
        i += 1"""
    i = 0
    for year in slots_to_fill:
        for month in slots_to_fill[year]:
            for day in slots_to_fill[year][month]:
                for shift in slots_to_fill[year][month][day]:
                    slots_to_fill[year][month][day][shift] = schedule_list[i]
                    i+=1

    result = {"schedule":slots_to_fill, "unschedulable": unschedulable}

    return result
