from pathlib import Path
from students.student_manager import load_students
from github_api.github_fetcher import fetch_github_data_for_user
from reports.pdf_generator import generate_pdf

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def process_all_students():
    students = load_students()
    if not students:
        print("❌ No students found in students/students.csv")
        return

    for regno, username in students.items():
        print(f"Processing {regno} -> {username} ...")
        data = fetch_github_data_for_user(username)
        
        if data.get("error"):
            print(f"  ❌ Error for {username}: {data['error']}")
            continue
        
        pdf_filename = REPORTS_DIR / f"{regno}_{username}_report.pdf"
        generate_pdf(username, data["repos"])
        print(f"  ✅ PDF saved: {pdf_filename}")

if __name__ == "__main__":
    process_all_students()
