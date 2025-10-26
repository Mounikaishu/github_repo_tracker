import csv
from pathlib import Path

# ----------------------------
# Students CSV
# ----------------------------
STUDENTS_CSV = Path("students/students.csv")

def load_students():
    """
    Loads students from students.csv.
    Returns a dictionary: { regno: username }
    """
    students = {}
    if not STUDENTS_CSV.exists():
        return students

    with open(STUDENTS_CSV, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            regno = row.get("RegNo", "").strip()
            username = row.get("Username", "").strip()
            if regno and username:
                students[regno] = username
    return students

def get_username_by_regno(regno):
    """
    Returns the GitHub username for a given registration number.
    """
    students = load_students()
    return students.get(regno)

# ----------------------------
# Summary CSV generation
# ----------------------------
SUMMARY_CSV = Path("reports/summary_report.csv")

def generate_summary_csv(all_student_data):
    """
    all_student_data: list of dicts
        Each dict contains:
        { "regno": ..., "username": ..., "repos_count": ..., "total_commits": ... }
    """
    # Ensure reports folder exists
    SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(SUMMARY_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["RegNo", "Username", "No. of Projects", "Total Commits"])
            for student in all_student_data:
                writer.writerow([
                    student.get("regno", ""),
                    student.get("username", ""),
                    student.get("repos_count", 0),
                    student.get("total_commits", 0)
                ])
        print(f"✅ Summary CSV saved: {SUMMARY_CSV}")
    except PermissionError:
        print(f"❌ Permission denied: cannot write to {SUMMARY_CSV}. Close the file if it is open.")
