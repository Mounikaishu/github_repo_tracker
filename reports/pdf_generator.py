from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(username, repos):
    filename = f"reports/{username}_report.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph(f"GitHub Report for {username}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Table data with header
    data = [["Project Name", "Number of Commits", "Last Commit Date", "URL"]]
    
    # Add repo data
    for repo in repos:
        data.append([
            Paragraph(repo.get("name", "N/A"), styles['Normal']),
            Paragraph(str(repo.get("commits_count", "N/A")), styles['Normal']),
            Paragraph(repo.get("last_commit", "N/A"), styles['Normal']),
            Paragraph(repo.get("html_url", "N/A"), styles['Normal'])
        ])
    
    # Adjust column widths (make URL wider)
    col_widths = [150, 100, 120, 220]  # Increase the last one
    
    table = Table(data, colWidths=col_widths)
    
    # Style table
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ])
    table.setStyle(style)
    
    elements.append(table)
    
    doc.build(elements)
    print(f"✅ PDF generated: {filename}")
