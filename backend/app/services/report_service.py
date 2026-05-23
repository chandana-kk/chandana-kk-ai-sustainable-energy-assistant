"""PDF report generation for monthly energy summary."""
import os
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.config import get_settings
from app.services.energy_simulator import get_simulator
from app.services.ml_service import ml_service


def generate_pdf_report(user_id: str, user_name: str) -> str:
    reports_dir = Path(__file__).resolve().parents[2] / "reports"
    reports_dir.mkdir(exist_ok=True)
    filename = f"energy_report_{user_id[:8]}_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = reports_dir / filename

    reading = get_simulator(user_id).next_reading()
    recs = ml_service.get_recommendations(user_id)
    settings = get_settings()

    doc = SimpleDocTemplate(str(filepath), pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>Smart Energy AI — Monthly Report</b>", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"User: {user_name}", styles["Normal"]),
        Paragraph(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]),
        Spacer(1, 20),
    ]

    data = [
        ["Metric", "Value"],
        ["Daily Usage", f"{reading['daily_kwh']} kWh"],
        ["Monthly Usage", f"{reading['monthly_kwh']} kWh"],
        ["Estimated Bill", f"₹{reading['estimated_bill']:.2f}"],
        ["Carbon Footprint", f"{reading['carbon_kg']:.1f} kg CO₂"],
        ["Tariff", f"₹{settings.tariff_per_kwh}/kWh"],
    ]
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Top Recommendations</b>", styles["Heading2"]))
    for r in recs[:5]:
        story.append(Paragraph(f"• {r['title']}: {r['description']}", styles["Normal"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    return str(filepath)
