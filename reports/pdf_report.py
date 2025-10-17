from fpdf import FPDF
from pathlib import Path

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_student_pdf(username, repos_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)  # We'll handle page breaks manually

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"GitHub Report for {username}", ln=True, align='C')
    pdf.ln(10)

    # Table headers
    headers = ["Project Name", "Commits", "Last Commit Date", "URL"]
    col_widths = [60, 25, 45, 70]
    row_line_height = 8  # height per line

    def draw_table_header():
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(200, 220, 255)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align='C', fill=True)
        pdf.ln()

    draw_table_header()
    pdf.set_font("Arial", '', 11)

    for repo in repos_data:
        # Determine number of lines needed for each cell
        def get_num_lines(text, width):
            lines = pdf.multi_cell(width, row_line_height, str(text), border=0, align='L', split_only=True)
            return len(lines)

        lines_needed = [
            get_num_lines(repo.get("name", ""), col_widths[0]),
            get_num_lines(str(repo.get("commits_count", 0)), col_widths[1]),
            get_num_lines(repo.get("last_commit", "N/A"), col_widths[2]),
            get_num_lines(repo.get("url", ""), col_widths[3])
        ]
        row_height = max(lines_needed) * row_line_height

        # Check if page break is needed
        if pdf.get_y() + row_height > pdf.h - pdf.b_margin:
            pdf.add_page()
            draw_table_header()
            pdf.set_font("Arial", '', 11)

        x_start = pdf.get_x()
        y_start = pdf.get_y()

        # Draw each cell
        pdf.multi_cell(col_widths[0], row_height / lines_needed[0], str(repo.get("name", "")), border=1)
        x1 = x_start + col_widths[0]
        pdf.set_xy(x1, y_start)
        pdf.multi_cell(col_widths[1], row_height / lines_needed[1], str(repo.get("commits_count", 0)), border=1, align='C')
        x2 = x1 + col_widths[1]
        pdf.set_xy(x2, y_start)
        pdf.multi_cell(col_widths[2], row_height / lines_needed[2], repo.get("last_commit", "N/A"), border=1, align='C')
        x3 = x2 + col_widths[2]
        pdf.set_xy(x3, y_start)
        pdf.multi_cell(col_widths[3], row_height / lines_needed[3], str(repo.get("url", "")), border=1)

        # Move cursor to next row
        pdf.set_xy(x_start, y_start + row_height)

    # Save PDF
    filename = REPORTS_DIR / f"{username}_report.pdf"
    pdf.output(filename)
    print(f"✅ PDF saved: {filename}")
