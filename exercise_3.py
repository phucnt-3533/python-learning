"""
Exercise 3: Calculate Vacation Days Based on Seniority
Calculate vacation days based on work start date and seniority
"""

from datetime import datetime


def parse_date(date_str):
    """Parse date string in format dd/mm/yyyy"""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None


def calculate_vacation_days(start_date_str, current_date=None):
    """
    Calculate vacation days based on seniority

    Logic:
    - If start date < current year:
      + 5+ years seniority: 14 days
      + 4+ years seniority: 13 days
      + Other cases: 12 days
    - If start date in current year:
      Calculate based on months worked until end of year:
      + Start date >= 10th: that month = 0.5 days
      + Start date < 10th: that month = 1 day
    """
    start_date = parse_date(start_date_str)

    if start_date is None:
        return None, "Invalid date format! Use dd/mm/yyyy"

    # Use current date or provided date for testing
    if current_date is None:
        current_date = datetime.now()
    else:
        current_date = parse_date(current_date)
        if current_date is None:
            return None, "Invalid current date format!"

    # Check if start date is in the future
    if start_date > current_date:
        return None, "Start date cannot be in the future!"

    # Case 1: Start date before current year
    if start_date.year < current_date.year:
        # Calculate years of seniority
        years = current_date.year - start_date.year

        if years >= 5:
            return 14.0, None
        elif years >= 4:
            return 13.0, None
        else:
            return 12.0, None

    # Case 2: Start date in current year
    else:
        vacation_days = 0.0
        start_month = start_date.month
        start_day = start_date.day

        # Calculate from start month to December
        for month in range(start_month, 13):
            if month == start_month:
                # For the start month, check the day
                if start_day >= 10:
                    vacation_days += 0.5
                else:
                    vacation_days += 1.0
            else:
                # For subsequent months, add 1 day
                vacation_days += 1.0

        return vacation_days, None


def main():
    """Main function to run the program"""
    print("=== Vacation Days Calculator ===\n")

    start_date = input("Enter start date (dd/mm/yyyy): ")

    vacation_days, error = calculate_vacation_days(start_date)

    if error:
        print(f"\nError: {error}")
    else:
        print(f"\nVacation days: {vacation_days}")


def test_cases():
    """Test the function with example cases"""
    print("=== Test Cases ===")
    print("Current date: 04/04/2020\n")

    test_data = [
        ("10/03/2020", "04/04/2020", 9.5),   # Expected: 9.5
        ("04/12/2019", "04/04/2020", 12.0),  # Expected: 12
        ("10/10/2015", "04/04/2020", 13.0),  # Expected: 13
        ("01/01/2015", "04/04/2020", 14.0),  # Expected: 14
        ("05/05/2020", "04/04/2020", None),  # Expected: Error (future date)
        ("01/01/2020", "04/04/2020", 9.0),   # Expected: 9.0
    ]

    for start_date, current_date, expected in test_data:
        vacation_days, error = calculate_vacation_days(start_date, current_date)
        if error:
            print(f"Start date: {start_date}")
            print(f"  Error: {error}\n")
        else:
            result = "✓" if vacation_days == expected else "✗"
            print(f"Start date: {start_date}")
            print(f"  Vacation days: {vacation_days} (Expected: {expected}) {result}\n")


if __name__ == "__main__":
    # Run main program
    main()

    # Uncomment to run test cases
    # print("\n" + "="*50 + "\n")
    # test_cases()
