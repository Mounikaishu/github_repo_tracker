from fpdf import FPDF
import textwrap

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "GitHub Student Report", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_student_pdf(username, repos):
    pdf = PDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 12)
    
    headers = ["Project Name", "Number of Commits", "Last Commit Date", "URL"]
    col_widths = [80, 40, 40, 120]

    # Header row
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 11)
    for repo in repos:
        x_start = pdf.get_x()
        y_start = pdf.get_y()

        # Project Name
        pdf.multi_cell(col_widths[0], 8, str(repo.get("name", "")), border=1)
        y_new = pdf.get_y()
        pdf.set_xy(x_start + col_widths[0], y_start)

        # Number of Commits
        pdf.multi_cell(col_widths[1], 8, str(repo.get("commits", 0)), border=1, align="C")
        pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)

        # Last Commit Date
        pdf.multi_cell(col_widths[2], 8, str(repo.get("last_commit_date", "N/A")), border=1, align="C")
        pdf.set_xy(x_start + col_widths[0] + col_widths[1] + col_widths[2], y_start)

        # URL — use cell instead of multi_cell
        url = str(repo.get("url", ""))
        pdf.set_text_color(0, 0, 255)
        # wrap long URLs manually
        url_lines = textwrap.wrap(url, width=50)
        for line in url_lines:
            pdf.cell(col_widths[3], 8, line, border=1, link=url)
            pdf.ln()
        pdf.set_text_color(0, 0, 0)

        pdf.set_y(max(y_new, pdf.get_y()))
        pdf.set_x(10)

    pdf_file = f"reports/{username}_report.pdf"
    pdf.output(pdf_file)
    print(f"✅ PDF saved: {pdf_file}")
