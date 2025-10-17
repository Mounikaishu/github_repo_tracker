from students.student_manager import load_students, get_username_by_regno, generate_summary_csv
from github_api.github_fetcher import fetch_github_data_for_user
from reports.pdf_report import generate_student_pdf

def main():
    print("Select an option:")
    print("1️⃣ Generate summary CSV for all students")
    print("2️⃣ Generate PDF for a single student")
    
    choice = input("Enter 1 or 2: ").strip()
    
    students = load_students()
    if not students:
        print("❌ No students found in students.csv")
        return

    if choice == "1":
        all_data = []
        for regno, username in students.items():
            print(f"Processing {regno} -> {username} ...")
            data = fetch_github_data_for_user(username)
            if data.get("error"):
                print(f"⚠️ Unexpected data for {username}, skipping...")
                continue
            repos = data.get("repos", [])
            total_commits = sum(repo.get("commits_count", 0) for repo in repos)
            all_data.append({
                "regno": regno,
                "username": username,
                "repos_count": len(repos),
                "total_commits": total_commits
            })
        generate_summary_csv(all_data)
    
    elif choice == "2":
        regno = input("Enter the registration number: ").strip()
        username = get_username_by_regno(regno)
        if not username:
            print(f"❌ No student found with RegNo {regno}")
            return
        print(f"Processing {regno} -> {username} ...")
        data = fetch_github_data_for_user(username)
        if data.get("error"):
            print(f"❌ Error for {username}: {data['error']}")
            return
        generate_student_pdf(username, data.get("repos", []))
    
    else:
        print("❌ Invalid option")

if __name__ == "__main__":
    main()
