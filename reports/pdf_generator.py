from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

def generate_pdf(username, repo_list):
    pdf_file = Path("reports") / f"{username}_report.pdf"
    c = canvas.Canvas(str(pdf_file), pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"GitHub Report: {username}")
    
    y = height - 100
    c.setFont("Helvetica", 12)

    if not repo_list:
        c.drawString(50, y, "No repositories found.")
    else:
        for repo in repo_list:
            c.drawString(50, y, f"Repo: {repo['name']}")
            c.drawString(60, y - 15, f"URL: {repo['html_url']}")
            c.drawString(60, y - 30, f"Commits: {repo['commits']} | Last commit: {repo['last_commit']}")
            y -= 60
            if y < 100:
                c.showPage()
                y = height - 50

    c.save()
