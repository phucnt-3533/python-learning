# Python Practice Exercises - Solutions

This folder contains solutions for 5 Python practice exercises from Sun* - Talent & Product Incubator Vietnam Unit.

## Files

- `exercise_1.py` - Student Grade Management System
- `exercise_2.py` - Overtime Hours and Meal Allowances Calculator
- `exercise_3.py` - Vacation Days Calculator Based on Seniority
- `exercise_4.py` - Name Formatting with Initials
- `exercise_5.py` - Count Occurrences and Sort by Frequency

## How to Run

Each exercise can be run independently:

```bash
python exercise_1.py
python exercise_2.py
python exercise_3.py
python exercise_4.py
python exercise_5.py
```

## Exercise Descriptions

### Exercise 1: Student Grade Management System
- Create a class-based system to manage student grades
- Track math, literature, and English grades
- Calculate and display:
  - Highest average grade in class
  - All student information with averages
  - Students with the highest average

**Example Output:**
```
name: ngoc, toan: 3, van: 4, anh: 5, avg: 4.0
name: thao, toan: 6, van: 7, anh: 8, avg: 7.0
```

### Exercise 2: Overtime Calculator
- Calculate overtime hours and meal allowances
- Input: check-in and check-out times (hh:mm)
- Logic:
  - OT > 4 hours + includes lunch time (12:00-13:00): deduct 1 hour, lunch allowance = Y
  - OT > 3 hours + works past 21:00: dinner allowance = Y

**Example:**
```
Check-in: 08:00, Check-out: 12:30
Output: OT: 4.5, Lunch: N, Dinner: N
```

### Exercise 3: Vacation Days Calculator
- Calculate vacation days based on work start date
- Logic:
  - 5+ years seniority: 14 days
  - 4+ years seniority: 13 days
  - Others: 12 days
  - For current year starts: calculate based on months worked

**Example:**
```
Start date: 10/03/2020 (Current: 04/04/2020)
Output: 9.5 days
```

### Exercise 4: Name Formatter
- Format Vietnamese names with initials
- Remove extra spaces
- First name: capitalize first letter
- Last name and middle names: uppercase initials

**Example:**
```
Input: " le thi Be Nho "
Output: NhoLTB
```

### Exercise 5: Frequency Counter
- Count occurrences of elements in a list
- Sort by frequency in ascending order
- Return dictionary with element as key, count as value

**Example:**
```
Input: 10 1 2 4 5 2 4 1 6 4 3
Output: {5: 1, 6: 1, 3: 1, 1: 2, 2: 2, 4: 3}
```

## Testing

Each file includes test cases that can be uncommented in the `if __name__ == "__main__"` block:

```python
# Uncomment to run test cases
# print("\n" + "="*50 + "\n")
# test_cases()
```

## Features

- Input validation and error handling
- Clean, object-oriented design (where applicable)
- Comprehensive test cases
- Clear documentation and comments
- Following Python best practices

## Author

Solutions created for Sun* Python practice exercises.

© 2023 By Sun* - Talent & Product Incubator Vietnam Unit - All rights reserved
