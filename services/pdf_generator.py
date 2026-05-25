import os
from fpdf import FPDF

class AuditPDF(FPDF):
    def header(self):
        # Setting up a professional header layout
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "SimplifIQ Automated Lead Intelligence Report", ln=True, align="R")
        self.line(10, 18, 200, 18) # Decorative horizontal line
        self.ln(5)

    def footer(self):
        # Page numbers at the bottom
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_pdf(company_name: str, lead_name: str, ai_insights: str) -> str:
    """
    Takes the structured information and compiles it into a beautiful,
    clean PDF document saved directly to the root folder.
    """
    pdf = AuditPDF()
    pdf.add_page()
    
    # --- TITLE SECTION ---
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(31, 41, 55) # Dark charcoal grey
    pdf.cell(0, 12, f"Strategic Business Audit", ln=True)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(79, 70, 229) # Professional indigo accent color
    pdf.cell(0, 10, f"Prepared for: {company_name}", ln=True)
    pdf.ln(5)
    
    # --- METADATA BOX ---
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 6, f"Prepared Attn: {lead_name}", ln=True)
    pdf.cell(0, 6, "Analysis Type: Automated Digital & Operational Infrastructure Audit", ln=True)
    pdf.ln(10)
    
    # --- INTRODUCTION ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "1. Executive Summary", ln=True)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    intro_text = (
        f"This intelligence brief was generated immediately following a request by {lead_name}. "
        f"Our system analyzed public signals and digital endpoints associated with {company_name}. "
        f"Below are foundational, data-driven optimization points formulated to improve operational efficiency."
    )
    pdf.multi_cell(0, 6, intro_text)
    pdf.ln(8)
    
    # --- AI INSIGHTS SECTION ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "2. Tailored Growth & Technology Insights", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    
    # 1. Clean out lingering markdown artifacts
    clean_insights = ai_insights.replace("**", "")

    # 2. Force a break on any actual newline characters first
    clean_insights = clean_insights.replace("\n", "<br>")

    # 3. THE FIX: Find every opening bold tag (<b>) and slap line breaks in front of it!
    # This guarantees that every new section automatically drops down to a fresh line.
    clean_insights = clean_insights.replace("<b>", "<br><br><b>")

    # 4. Clean up any accidental triple breaks at the very beginning of the text
    if clean_insights.startswith("<br><br>"):
        clean_insights = clean_insights.replace("<br><br>", "", 1)

    # 5. Hand the properly spaced layout to the compiler
    pdf.set_font("Helvetica", size=11)
    pdf.write_html(clean_insights)
            
    # --- OUTPUT HANDLING ---
    # Save the output file in a clean kebab-case format
    safe_filename = f"Audit_{company_name.replace(' ', '_')}.pdf"
    pdf.output(safe_filename)
    
    print(f"[PDF Generator] Successfully compiled and exported: {safe_filename}")
    return safe_filename