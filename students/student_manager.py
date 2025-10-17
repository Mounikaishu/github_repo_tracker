import csv
from pathlib import Path

STUDENTS_CSV = Path("students/students.csv")
SUMMARY_CSV = Path("reports/summary_report.csv")

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

def generate_summary_csv(all_student_data):
    """
    Generates summary CSV for all students.
    all_student_data: list of dicts
        Each dict contains:
        { "regno": ..., "username": ..., "repos_count": ..., "total_commits": ... }
    """
    SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    
    if not all_student_data:
        print("⚠️ No data available to generate summary report.")
        return
    
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
