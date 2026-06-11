# Python Students Registration App

A command-line course registration app for managing students, available courses, and student course enrolments.

## Features

- View available courses in a formatted table
- Add students with generated student IDs
- Register students for courses
- Prevent duplicate course registration for the same student
- View individual student details and total fees
- View all saved students
- Save courses and students in CSV files

## Requirements

- Python 3.10 or newer
- `colorama`
- `tabulate`

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python CourseRegistration.py
```

You can also run the compatibility launcher:

```powershell
python script.py
```

## Notes

Courses are stored in `courses.csv`.

Students are stored in `students.csv`.

When the app starts, it fetches courses and students from those CSV files. When you add a student or register a student for a course, the app saves the updated student data back to `students.csv`.

## Project Structure

```text
.
+-- CourseRegistration.py
+-- script.py
+-- courses.csv
+-- students.csv
+-- requirements.txt
+-- .gitignore
+-- README.md
```
