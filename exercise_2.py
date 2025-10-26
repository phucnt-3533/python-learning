"""
Exercise 2: Calculate Overtime (OT) Hours and Meal Allowances
Calculate OT hours and determine lunch and dinner allowances
"""

from datetime import datetime, time


def parse_time(time_str):
    """Parse time string in format hh:mm"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None


def time_diff_hours(start_time, end_time):
    """Calculate time difference in hours"""
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)

    # Handle case where end time is before start time (next day)
    if end_dt < start_dt:
        return None

    diff = end_dt - start_dt
    return diff.total_seconds() / 3600


def includes_lunch_time(start_time, end_time):
    """Check if the time range includes lunch time (12:00-13:00)"""
    lunch_start = time(12, 0)
    lunch_end = time(13, 0)

    return start_time < lunch_end and end_time > lunch_start


def calculate_ot(check_in, check_out):
    """
    Calculate OT hours and meal allowances

    Logic:
    - If OT > 4 hours and includes lunch time (12:00-13:00): subtract 1 hour, lunch allowance = Y
    - If OT > 3 hours and works past 21:00: dinner allowance = Y
    - Other cases: no lunch deduction, no allowances
    """
    start_time = parse_time(check_in)
    end_time = parse_time(check_out)

    # Validate input
    if start_time is None or end_time is None:
        return None, None, None, "Invalid time format! Use hh:mm"

    ot_hours = time_diff_hours(start_time, end_time)

    if ot_hours is None:
        return None, None, None, "Invalid time range! Check-out must be after check-in"

    lunch_allowance = "N"
    dinner_allowance = "N"

    # Check if OT > 4 hours and includes lunch time
    if ot_hours > 4 and includes_lunch_time(start_time, end_time):
        ot_hours -= 1  # Subtract 1 hour for lunch
        lunch_allowance = "Y"

    # Check if OT > 3 hours and works past 21:00
    if ot_hours > 3 and end_time > time(21, 0):
        dinner_allowance = "Y"

    return ot_hours, lunch_allowance, dinner_allowance, None


def main():
    """Main function to run the program"""
    print("=== Overtime Calculator ===\n")

    check_in = input("Enter check-in time (hh:mm): ")
    check_out = input("Enter check-out time (hh:mm): ")

    ot_hours, lunch, dinner, error = calculate_ot(check_in, check_out)

    if error:
        print(f"\nError: {error}")
    else:
        print(f"\nOT: {ot_hours}, Lunch: {lunch}, Dinner: {dinner}")


def test_cases():
    """Test the function with example cases"""
    print("=== Test Cases ===\n")

    test_data = [
        ("08:00", "12:30"),  # Expected: OT = 4.5, Lunch: N, Dinner: N
        ("12:00", "16:30"),  # Expected: OT = 3.5, Lunch: Y, Dinner: N
        ("08:00", "18:00"),  # Expected: OT = 9.0, Lunch: Y, Dinner: N
        ("17:00", "22:00"),  # Expected: OT = 5.0, Lunch: N, Dinner: Y
        ("10:00", "22:30"),  # Expected: OT = 11.5, Lunch: Y, Dinner: Y
        ("14:00", "17:00"),  # Expected: OT = 3.0, Lunch: N, Dinner: N
    ]

    for check_in, check_out in test_data:
        ot_hours, lunch, dinner, error = calculate_ot(check_in, check_out)
        if error:
            print(f"Check-in = \"{check_in}\", Check-out = \"{check_out}\"")
            print(f"  Error: {error}\n")
        else:
            print(f"Check-in = \"{check_in}\", Check-out = \"{check_out}\"")
            print(f"  OT: {ot_hours}, Lunch: {lunch}, Dinner: {dinner}\n")


if __name__ == "__main__":
    # Run main program
    main()

    # Uncomment to run test cases
    # print("\n" + "="*50 + "\n")
    # test_cases()
