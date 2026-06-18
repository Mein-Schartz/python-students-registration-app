#import email
from datetime import datetime
import csv
import os

from colorama import Fore, Style, init
from tabulate import tabulate


COURSES_FILE = "courses.csv"
STUDENTS_FILE = "students.csv"


class Course:
    def __init__(self, code, name, fee, duration):
        self.code = code
        self.name = name
        self.fee = fee
        self.duration = duration



class Student:
    def __init__(self, student_id, name, age, phone, email, date_registered="", registered_courses=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email

        # Store the date as simple text so it is easy to save in a CSV file.
        if date_registered == "":
            self.date_registered = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.date_registered = date_registered

        # This list stores course codes, for example: ["PY101", "WD201"].
        if registered_courses is None:
            self.registered_courses = []
        else:
            self.registered_courses = registered_courses

    def add_course(self, course_code):
        if course_code in self.registered_courses:
            print(Fore.YELLOW + "Student has already registered for this course." + Style.RESET_ALL)
            return False

        self.registered_courses.append(course_code)
        return True

    def calculate_total_fees(self):
        total = 0

        for course_code in self.registered_courses:
            if course_code in courses:
                total = total + courses[course_code].fee

        return total

    def display_student_details(self):
        print("\nStudent Details")
        print("-" * 30)
        print(f"Student ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"Registered On: {self.date_registered}")

        print("\nRegistered Courses:")

        if len(self.registered_courses) == 0:
            print("No courses registered yet.")
        else:
            for course_code in self.registered_courses:
                if course_code in courses:
                    course = courses[course_code]
                    print(f"- {course.name} - GHS {course.fee}")
                else:
                    print(f"- Unknown course code: {course_code}")

        print(f"\nTotal Fees: GHS {self.calculate_total_fees()}")
        print("-" * 30)


# The courses dictionary stores Course objects while the program is running.
# Key = course code, Value = Course object
courses = {}

# The students dictionary stores Student objects while the program is running.
# Key = student ID, Value = Student object
students = {}


def create_default_courses():
    courses["PY101"] = Course("PY101", "Python Basics", 300, "4 weeks")
    courses["WD201"] = Course("WD201", "Web Development", 500, "6 weeks")
    courses["DB301"] = Course("DB301", "Database Fundamentals", 400, "5 weeks")
    courses["JS401"] = Course("JS401", "JavaScript Basics", 350, "4 weeks")
    courses["DB305"] = Course("DB305", "Data Structure Fundamentals", 400, "5 weeks")
    courses["JS406"] = Course("JS406", "Java Basics", 350, "4 weeks")
    courses["REM509"] = Course("REM509", "Research Methods", 200, "1 year")


def save_courses():
    # A CSV file stores rows, so each course becomes one row in the file.
    with open(COURSES_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["code", "name", "fee", "duration"])

        for course_code in courses:
            course = courses[course_code]
            writer.writerow([course.code, course.name, course.fee, course.duration])


def fetch_courses():
    global courses
    courses = {}

    if os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the heading row.

            # Convert each CSV row back into a Course object.
            for row in reader:
                if len(row) == 4:
                    course_code = row[0]
                    course_name = row[1]
                    course_fee = int(row[2])
                    course_duration = row[3]

                    courses[course_code] = Course(course_code, course_name, course_fee, course_duration)

        if len(courses) == 0:
            create_default_courses()
            save_courses()
    else:
        # If the file does not exist yet, create it with the starter courses.
        create_default_courses()
        save_courses()


def save_students():
    # A student can have many courses, so we join the course codes with | before saving.
    with open(STUDENTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["student_id", "name", "age", "phone","email", "date_registered", "registered_courses"])

        for student_id in students:
            student = students[student_id]
            course_codes = "|".join(student.registered_courses)

            writer.writerow([
                student.student_id,
                student.name,
                student.age,
                student.phone,
                student.email,
                student.date_registered,
                course_codes
            ])


def fetch_students():
    global students
    students = {}

    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the heading row.

            # Convert each CSV row back into a Student object.
            for row in reader:
                if len(row) == 7:
                    student_id = row[0]
                    name = row[1]
                    age = int(row[2])
                    phone = row[3]
                    email = row[4]
                    date_registered = row[5]

                    if row[6] == "":
                        registered_courses = []
                    else:
                        registered_courses = row[6].split("|")

                    students[student_id] = Student(
                        student_id,
                        name,
                        age,
                        phone,
                        email,
                        date_registered,
                        registered_courses
                    )
    else:
        # Create an empty file the first time the app runs.
        save_students()


def generate_student_id():
    number = 1

    while True:
        student_id = "STU" + str(number).zfill(3)

        if student_id not in students:
            return student_id

        number = number + 1


def get_required_input(message):
    value = input(message).strip()

    while value == "":
        print(Fore.RED + "This field is required." + Style.RESET_ALL)
        value = input(message).strip()

    return value

def get_valid_email():
    while True:
        email = input("Enter your email: ").strip()

        if email.count("@") != 1:
            print("Invalid email. Email must contain exactly one '@'.")
            continue

        username, domain = email.split("@")

        if not username:
            print("Invalid email. Username cannot be empty.")
            continue

        if "." not in domain:
            print("Invalid email. Domain must contain a '.'.")
            continue

        if domain.startswith(".") or domain.endswith("."):
            print("Invalid email. '.' cannot be at the beginning or end of the domain.")
            continue

        return email


def get_positive_age():
    while True:
        try:
            age = int(input("Enter age: "))

            if age > 0:
                return age

            print(Fore.RED + "Age must be greater than zero." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid age. Please enter a number." + Style.RESET_ALL)


def view_courses():
    table = []

    for course_code in courses:
        course = courses[course_code]
        table.append([course.code, course.name, "GHS " + str(course.fee), course.duration])

    print(tabulate(table, headers=["Course Code", "Course", "Fee", "Duration"], tablefmt="grid"))


def add_student():
    print("\nAdd New Student")

    name = get_required_input("Enter student name: ")
    phone = get_required_input("Enter phone number: ")
    email = get_valid_email()
    age = get_positive_age()

    student_id = generate_student_id()
    new_student = Student(student_id, name, age, phone, email)
    students[student_id] = new_student

    # Save immediately so the student is still available after the program closes.
    save_students()

    print(Fore.GREEN + f"Student added successfully. Student ID: {student_id}" + Style.RESET_ALL)


def register_student_for_course():
    student_id = get_required_input("Enter student ID: ").upper()

    if student_id not in students:
        print(Fore.RED + "Student not found." + Style.RESET_ALL)
        return

    view_courses()
    course_code = get_required_input("Enter course code: ").upper()

    if course_code not in courses:
        print(Fore.RED + "Course not found." + Style.RESET_ALL)
        return

    course_added = students[student_id].add_course(course_code)

    if course_added:
        # Save immediately so the course registration is not lost.
        save_students()
        print(Fore.GREEN + "Course registered successfully." + Style.RESET_ALL)


def view_student_details():
    student_id = get_required_input("Enter student ID: ").upper()

    if student_id in students:
        students[student_id].display_student_details()
    else:
        print(Fore.RED + "Student not found." + Style.RESET_ALL)


def view_all_students():
    print("\nAll Students")
    print("-" * 30)

    if len(students) == 0:
        print("No students added yet.")
    else:
        table = []

        for student_id in students:
            student = students[student_id]
            table.append([
                student.student_id,
                student.name,
                student.age,
                student.phone,
                student.email,
                len(student.registered_courses)
            ])

        print(tabulate(table, headers=["Student ID", "Name", "Age", "Phone", "Courses"], tablefmt="grid"))


def show_menu():
    print("\nWelcome to Python Training Center")
    print("1. View Available Courses")
    print("2. Add Student")
    print("3. Register Student for Course")
    print("4. View Student Details")
    print("5. View All Students")
    print("6. Exit")


def main():
    init(autoreset=True)

    # Fetch saved data before showing the menu.
    fetch_courses()
    fetch_students()

    while True:
        show_menu()
        print("-" * 30)

        try:
            choice = int(input("Choose an option: "))

            if choice == 1:
                view_courses()
            elif choice == 2:
                add_student()
            elif choice == 3:
                register_student_for_course()
            elif choice == 4:
                view_student_details()
            elif choice == 5:
                view_all_students()
            elif choice == 6:
                print("Thank you for using the app. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid option. Please choose from 1 to 6." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)
        except EOFError:
            print("\nInput ended. Goodbye!")
            break


if __name__ == "__main__":
    main()
