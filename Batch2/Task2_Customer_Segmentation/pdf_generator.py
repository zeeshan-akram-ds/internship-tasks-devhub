from fpdf import FPDF
from datetime import datetime

def generate_segment_pdf(segment_name, summary_text, stats_dict, filename="segment_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Customer Segmentation Report", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, txt=f"Generated on: {datetime.now().strftime('%B %d, %Y')}", ln=True)
    pdf.ln(5)

    # For all segments or one
    if segment_name == "All Segments":
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Summary for All Customer Segments", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, txt=summary_text)
        
        for seg_name, seg_stats in stats_dict.items():
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt=f"Segment: {seg_name}", ln=True)
            pdf.set_font("Arial", '', 11)
            for key, value in seg_stats.items():
                pdf.cell(0, 8, txt=f"{key}: {value}", ln=True)

    else:
        # Single segment
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"Segment: {segment_name}", ln=True)

        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, txt=summary_text)
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Statistical Overview", ln=True)

        pdf.set_font("Arial", '', 11)
        for key, value in stats_dict.items():
            pdf.cell(0, 8, txt=f"{key}: {value}", ln=True)

    pdf.output(filename)
    return filename