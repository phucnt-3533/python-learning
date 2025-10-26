"""
Exercise 1: Student Grade Management System
Manage student grades for math, literature, and English
"""

class Student:
    """Class to represent a student with their grades"""

    def __init__(self, name, math_grade, literature_grade, english_grade):
        self.name = name
        self.math_grade = math_grade
        self.literature_grade = literature_grade
        self.english_grade = english_grade

    def calculate_average(self):
        """Calculate the average grade of the student"""
        return (self.math_grade + self.literature_grade + self.english_grade) / 3

    def __str__(self):
        """String representation of the student"""
        avg = self.calculate_average()
        return f"name: {self.name}, toan: {self.math_grade}, van: {self.literature_grade}, anh: {self.english_grade}, avg: {avg:.1f}"


class ClassRoom:
    """Class to manage a list of students"""

    def __init__(self):
        self.students = []

    def add_student(self, student):
        """Add a student to the class"""
        self.students.append(student)

    def get_highest_average(self):
        """Get the highest average grade in the class"""
        if not self.students:
            return None
        return max(student.calculate_average() for student in self.students)

    def print_all_students(self):
        """Print information of all students"""
        for student in self.students:
            print(student)

    def get_top_students(self):
        """Get list of students with the highest average grade"""
        if not self.students:
            return []

        max_avg = self.get_highest_average()
        top_students = [student.name for student in self.students
                       if student.calculate_average() == max_avg]
        return top_students


def main():
    """Main function to run the program"""
    classroom = ClassRoom()

    # Input number of students
    try:
        n = int(input("Enter number of students: "))

        # Input student information
        for i in range(n):
            print(f"\nStudent {i+1}:")
            name = input("Name: ")
            math = float(input("Math grade: "))
            literature = float(input("Literature grade: "))
            english = float(input("English grade: "))

            student = Student(name, math, literature, english)
            classroom.add_student(student)

        # b) Print highest average grade
        print(f"\n--- Highest average grade in class ---")
        highest_avg = classroom.get_highest_average()
        print(f"Highest average: {highest_avg:.1f}")

        # c) Print all students information
        print(f"\n--- All students information ---")
        classroom.print_all_students()

        # d) Print list of students with highest average
        print(f"\n--- Students with highest average ---")
        top_students = classroom.get_top_students()
        print(f"Top students: {', '.join(top_students)}")

    except ValueError:
        print("Error: Invalid input! Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
