from fpdf import FPDF


def generate_pdf(
    total,
    normal,
    slow,
    aggressive,
    score,
    grade,
    recommendation
):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 18)

    pdf.cell(0, 12, "Driver Activity Monitoring Report", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Total Windows : {total}", ln=True)
    pdf.cell(0, 10, f"Normal : {normal}", ln=True)
    pdf.cell(0, 10, f"Slow : {slow}", ln=True)
    pdf.cell(0, 10, f"Aggressive : {aggressive}", ln=True)

    pdf.ln(5)

    pdf.cell(0, 10, f"Driver Safety Score : {score:.1f}/100", ln=True)
    pdf.cell(0, 10, f"Driver Grade : {grade}", ln=True)

    pdf.ln(5)

    pdf.multi_cell(
        0,
        10,
        f"AI Recommendation:\n{recommendation}"
    )

    filename = "Driver_Report.pdf"

    pdf.output(filename)

    return filename