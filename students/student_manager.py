import csv
from pathlib import Path

STUDENTS_CSV = Path("students/students.csv")  # Make sure this CSV exists

def load_students():
    """Load all students from CSV into a dictionary {regno: github_username}"""
    students = {}
    if not STUDENTS_CSV.exists():
        print(f"❌ {STUDENTS_CSV} not found!")
        return students

    with open(STUDENTS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students[row["regno"].strip()] = row["github_username"].strip()
    return students

def get_username_by_regno(regno):
    """Return GitHub username for a given registration number"""
    students = load_students()
    return students.get(regno, None)
