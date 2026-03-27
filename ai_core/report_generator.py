from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

def generate_report(plan: dict, output_path: str = "data/finora_report.pdf"):
    """Generates a professional PDF financial report from coordinator output"""
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # --- Custom Styles ---
    title_style = ParagraphStyle(
        "Title", fontSize=24, textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6, alignment=TA_CENTER, fontName="Helvetica-Bold"
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", fontSize=12, textColor=colors.HexColor("#f0a500"),
        spaceAfter=4, alignment=TA_CENTER, fontName="Helvetica"
    )
    section_style = ParagraphStyle(
        "Section", fontSize=14, textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6, spaceBefore=12, fontName="Helvetica-Bold"
    )
    normal_style = ParagraphStyle(
        "Normal2", fontSize=10, textColor=colors.HexColor("#333333"),
        spaceAfter=4, fontName="Helvetica", leading=16
    )

    user = plan["user"]
    tax = plan["tax"]
    inv = plan["investment"]
    advice = plan["ai_advice"]

    # --- Header ---
    elements.append(Paragraph("FINORA", title_style))
    elements.append(Paragraph("Your AI-Powered Financial Advisor", subtitle_style))
    elements.append(Paragraph(
        f"Personal Financial Report — {datetime.now().strftime('%d %B %Y')}",
        ParagraphStyle("date", fontSize=9, textColor=colors.grey, 
                      alignment=TA_CENTER, fontName="Helvetica")
    ))
    elements.append(HRFlowable(width="100%", thickness=2, 
                               color=colors.HexColor("#f0a500")))
    elements.append(Spacer(1, 12))

    # --- User Profile ---
    elements.append(Paragraph("👤 User Profile", section_style))
    profile_data = [
        ["Name", user["name"]],
        ["Age", str(user["age"])],
        ["Annual Income", f"₹{user['annual_income']:,}"],
        ["Risk Profile", user["risk_profile"].upper()],
        ["Goal", user["goal"].title()],
    ]
    profile_table = Table(profile_data, colWidths=[2*inch, 4*inch])
    profile_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0,0), (0,-1), colors.white),
        ("BACKGROUND", (1,0), (1,-1), colors.HexColor("#f5f5f5")),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS", (1,0), (1,-1), 
         [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("PADDING", (0,0), (-1,-1), 8),
    ]))
    elements.append(profile_table)
    elements.append(Spacer(1, 12))

    # --- Tax Summary ---
    elements.append(HRFlowable(width="100%", thickness=1, 
                               color=colors.HexColor("#eeeeee")))
    elements.append(Paragraph("📊 Tax Analysis", section_style))
    
    tax_data = [
        ["Metric", "Amount"],
        ["Annual Income", f"₹{tax['annual_income']:,}"],
        ["Total Deductions", f"₹{tax['total_deductions']:,}"],
        ["Tax Without Deductions", f"₹{tax['tax_before']:,.0f}"],
        ["Tax After Deductions", f"₹{tax['tax_after']:,.0f}"],
        ["💰 Total Tax Saved", f"₹{tax['tax_saved']:,.0f}"],
    ]
    tax_table = Table(tax_data, colWidths=[3*inch, 3*inch])
    tax_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS", (0,1), (-1,-2), 
         [colors.HexColor("#f9f9f9"), colors.white]),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#e8f5e9")),
        ("TEXTCOLOR", (0,-1), (-1,-1), colors.HexColor("#2e7d32")),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("PADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (1,0), (1,-1), "RIGHT"),
    ]))
    elements.append(tax_table)
    elements.append(Spacer(1, 12))

    # --- Deduction Breakdown ---
    elements.append(Paragraph("Deduction Breakdown:", 
                              ParagraphStyle("sub", fontSize=11, 
                              fontName="Helvetica-Bold", 
                              textColor=colors.HexColor("#333333"))))
    ded_data = [["Section", "Amount"]]
    for section, amount in tax["deduction_breakdown"].items():
        ded_data.append([f"Section {section}", f"₹{amount:,}"])
    
    ded_table = Table(ded_data, colWidths=[3*inch, 3*inch])
    ded_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f0a500")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("PADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (1,0), (1,-1), "RIGHT"),
    ]))
    elements.append(ded_table)
    elements.append(Spacer(1, 12))

    # --- Investment Plan ---
    elements.append(HRFlowable(width="100%", thickness=1, 
                               color=colors.HexColor("#eeeeee")))
    elements.append(Paragraph("💼 Investment Plan", section_style))
    
    port_data = [["Instrument", "Allocation", "Monthly SIP"]]
    for instrument, details in inv["portfolio"].items():
        port_data.append([
            instrument,
            details["percentage"],
            f"₹{details['monthly_amount']:,}"
        ])
    
    port_table = Table(port_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    port_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), 
         [colors.HexColor("#f9f9f9"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("PADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (1,0), (-1,-1), "CENTER"),
    ]))
    elements.append(port_table)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        f"🏆 Estimated Corpus after {inv['years']} years: "
        f"₹{inv['total_corpus']:,.0f}",
        ParagraphStyle("corpus", fontSize=12, fontName="Helvetica-Bold",
                      textColor=colors.HexColor("#2e7d32"),
                      backColor=colors.HexColor("#e8f5e9"),
                      borderPad=8, spaceAfter=12)
    ))

    # --- AI Advice ---
    elements.append(HRFlowable(width="100%", thickness=1, 
                               color=colors.HexColor("#eeeeee")))
    elements.append(Paragraph("🤖 Finora AI Recommendations", section_style))
    
    for line in advice.split("\n"):
        if line.strip():
            clean = line.replace("**", "").strip()
            elements.append(Paragraph(clean, normal_style))
    
    elements.append(Spacer(1, 12))

    # --- Disclaimer ---
    elements.append(HRFlowable(width="100%", thickness=1, 
                               color=colors.HexColor("#eeeeee")))
    elements.append(Paragraph(
        "⚠️ Disclaimer: This report is generated by an AI system for "
        "educational purposes only. It does not constitute financial advice. "
        "Please consult a certified financial advisor before making investment decisions.",
        ParagraphStyle("disclaimer", fontSize=8, textColor=colors.grey,
                      fontName="Helvetica", leading=12, spaceBefore=8)
    ))

    # --- Build PDF ---
    doc.build(elements)
    print(f"\n✅ Report generated: {output_path}")
    return output_path


# --- Test ---
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ai_core.coordinator_agent import run_coordinator

    user = {
        "name": "Rahul Sharma",
        "age": 30,
        "annual_income": 800000,
        "monthly_savings": 15000,
        "risk_profile": "medium",
        "goal": "retirement",
        "investments": {
            "ELSS": 50000,
            "PPF": 30000,
            "health_insurance": 15000
        }
    }

    plan = run_coordinator(user)
    generate_report(plan)