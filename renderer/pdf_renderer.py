import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT


TEMPLATE_STYLES = {
    "single_page": {
        "font": "Helvetica",
        "heading_color": colors.HexColor("#1a2e4a"),
        "accent_color": colors.HexColor("#e8a020"),
        "font_size": 10,
        "heading_size": 13,
    },
    "two_page": {
        "font": "Helvetica",
        "heading_color": colors.HexColor("#1a2e4a"),
        "accent_color": colors.HexColor("#e8a020"),
        "font_size": 11,
        "heading_size": 14,
    },
    "ats_plain": {
        "font": "Times-Roman",
        "heading_color": colors.black,
        "accent_color": colors.black,
        "font_size": 11,
        "heading_size": 13,
    },
    "executive": {
        "font": "Helvetica",
        "heading_color": colors.HexColor("#8b6914"),
        "accent_color": colors.HexColor("#8b6914"),
        "font_size": 11,
        "heading_size": 14,
    },
}


def render_to_pdf(content: str, output_path: str, template: str = "single_page") -> str:
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "output", exist_ok=True)

    style = TEMPLATE_STYLES.get(template, TEMPLATE_STYLES["single_page"])

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name",
        fontName=style["font"] + "-Bold",
        fontSize=20,
        textColor=style["heading_color"],
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    section_style = ParagraphStyle(
        "Section",
        fontName=style["font"] + "-Bold",
        fontSize=style["heading_size"] - 2,
        textColor=style["heading_color"],
        spaceBefore=10,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "Body",
        fontName=style["font"],
        fontSize=style["font_size"],
        textColor=colors.HexColor("#2c2c2c"),
        spaceAfter=3,
        leading=14,
    )

    contact_style = ParagraphStyle(
        "Contact",
        fontName=style["font"],
        fontSize=9,
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    story = []
    lines = content.split("\n")
    first_line = True

    for line in lines:
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
            continue

        # First non-empty line = name
        if first_line:
            story.append(Paragraph(stripped, name_style))
            story.append(HRFlowable(width="100%", thickness=2, color=style["heading_color"]))
            first_line = False
            continue

        # Detect section headers (all caps or ends with :)
        if stripped.isupper() or (len(stripped) < 40 and stripped.endswith(":")):
            story.append(Spacer(1, 6))
            story.append(Paragraph(stripped.rstrip(":"), section_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=style["accent_color"]))
            continue

        # Contact line (has @ or phone pattern)
        if "@" in stripped or ("|" in stripped and len(stripped) < 120):
            story.append(Paragraph(stripped, contact_style))
            continue

        # Bullet points
        if stripped.startswith(("•", "-", "*", "–")):
            bullet_text = "• " + stripped.lstrip("•-*– ").strip()
            story.append(Paragraph(bullet_text, body_style))
            continue

        story.append(Paragraph(stripped, body_style))

    doc.build(story)
    return output_path
