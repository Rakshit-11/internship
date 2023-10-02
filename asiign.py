import csv
from datetime import datetime, timedelta

def load_data(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def find_consecutive_days(data, consecutive_days=7):
    result = []
    for employee in data:
        name = employee['Employee Name']
        days_worked = [datetime.strptime(entry['Pay Cycle Start Date'], '%m/%d/%Y') for entry in data if entry['Employee Name'] == name and entry['Pay Cycle Start Date']]
        days_worked.sort()

        for i in range(len(days_worked) - consecutive_days + 1):
            if all((days_worked[i + j] - days_worked[i + j - 1]).days == 1 for j in range(1, consecutive_days)):
                result.append({'Name': name, 'Position': employee['Position ID']})
                break

    return result

def find_short_breaks(data, min_hours=1, max_hours=10):
    result = []
    processed_employees = set()  # Keep track of processed employees to avoid duplicates
    for employee in data:
        name = employee['Employee Name']
        if name in processed_employees:
            continue

        shifts = [datetime.strptime(date, '%m/%d/%Y %I:%M %p') for date in [entry['Time'] for entry in data if entry['Employee Name'] == name and entry['Time']]]
        shifts.sort()

        for i in range(1, len(shifts)):
            break_duration = shifts[i] - shifts[i - 1]
            if timedelta(hours=min_hours) < break_duration < timedelta(hours=max_hours):
                result.append({'Name': name, 'Position': employee['Position ID']})
                processed_employees.add(name)  # Mark this employee as processed
                break

    return result



def convert_time_to_hours(time_str):
    """
    Convert time in the format 'H:MM' to hours as float.
    """
    if ':' in time_str:
        hours, minutes = map(int, time_str.split(':'))
        return hours + minutes / 60.0
    else:
        return 0.0

def find_long_shifts(data, max_hours=14):
    result = []
    processed_employees = set() 
    for employee in data:
        name = employee['Employee Name']
        if name in processed_employees:
            continue

        shifts = [entry for entry in data if entry['Employee Name'] == name and entry['Timecard Hours (as Time)']]
        for shift in shifts:
            time_as_float = convert_time_to_hours(shift['Timecard Hours (as Time)'])
            if time_as_float > max_hours:
                result.append({'Name': name, 'Position': employee['Position ID']})
                processed_employees.add(name)  
                break

    return result



if __name__ == "__main__":
    file_path = r"C:\Users\nikhi\Downloads\Assignment_Timecard.xlsx - Sheet1.csv"  
    data = load_data(file_path)

    # employees who have worked for 7 consecutive days
    consecutive_days_result = find_consecutive_days(data)
    print("Employees who have worked for 7 consecutive days:")
    for entry in consecutive_days_result:
        print(f"{entry['Name']} - {entry['Position']}")

    # employees who have less than 10 hours of time between shifts but greater than 1 hour
    short_breaks_result = find_short_breaks(data)
    print("\n employee who have less than 10 hours of time between shifts but greater than 1 hour:")
    for entry in short_breaks_result:
        print(f"{entry['Name']} - {entry['Position']}")

    # employees who have worked for more than 14 hours in a single shift
    long_shifts_result = find_long_shifts(data)
    print("\nemployee Who has worked for more than 14 hours in a single shift:")
    for entry in long_shifts_result:
        print(f"{entry['Name']} - {entry['Position']}")
