from students.student_manager import get_username_by_regno
from github_api.github_fetcher import fetch_github_data_for_user
from reports.pdf_generator import generate_pdf

if __name__ == "__main__":
    regno = input("Enter Registration No: ").strip()
    username = get_username_by_regno(regno)
    
    if not username:
        print("❌ Student not found.")
    else:
        print(f"Fetching data for {username} ...")
        data = fetch_github_data_for_user(username)
        if data.get("error"):
            print(f"❌ Error: {data['error']}")
        else:
            generate_pdf(username, data["repos"])
            print(f"✅ PDF report generated for {username}")
