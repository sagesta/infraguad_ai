"""Builds a submission-ready proposal PDF from proposal_data.json."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
OUT_PATH = BASE_DIR / "InfraGuard_Pro_Project_Proposal.pdf"
DATA = json.loads((BASE_DIR / "proposal_data.json").read_text(encoding="utf-8"))


def stylesheet():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Times-Bold",
            fontSize=15,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=16,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverText",
            fontName="Times-Roman",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Chapter",
            fontName="Times-Bold",
            fontSize=16,
            leading=22,
            alignment=TA_CENTER,
            spaceBefore=12,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading",
            fontName="Times-Bold",
            fontSize=13,
            leading=17,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subheading",
            fontName="Times-BoldItalic",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyJustify",
            fontName="Times-Roman",
            fontSize=11.5,
            leading=16,
            alignment=TA_JUSTIFY,
            firstLineIndent=0,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletBody",
            fontName="Times-Roman",
            fontSize=11.2,
            leading=15,
            alignment=TA_JUSTIFY,
            leftIndent=16,
            firstLineIndent=-10,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            fontName="Times-Roman",
            fontSize=8.7,
            leading=11,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHeader",
            fontName="Times-Bold",
            fontSize=8.8,
            leading=11,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Caption",
            fontName="Times-Italic",
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            spaceBefore=5,
            spaceAfter=10,
        )
    )
    return styles


STYLES = stylesheet()


def para(text: str, style: str = "BodyJustify") -> Paragraph:
    return Paragraph(escape(text), STYLES[style])


def heading(text: str):
    return para(text, "Heading")


def subheading(text: str):
    return para(text, "Subheading")


def bullet(text: str):
    return Paragraph(f"&#8226; {escape(text)}", STYLES["BulletBody"])


def table(rows, col_widths=None):
    body = []
    for row_index, row in enumerate(rows):
        style_name = "TableHeader" if row_index == 0 else "TableCell"
        body.append([Paragraph(escape(str(cell)), STYLES[style_name]) for cell in row])
    t = Table(body, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5EDF6")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#737373")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def cover():
    story = [Spacer(1, 0.85 * inch)]
    story.append(para("MASTER OF INFORMATION TECHNOLOGY (MIT) PROFESSIONAL MASTER'S PROJECT PROPOSAL", "CoverTitle"))
    story.append(Spacer(1, 0.22 * inch))
    story.append(para(DATA["projectTitle"].upper(), "CoverTitle"))
    story.append(para(f"({DATA['projectSubtitle']})", "CoverText"))
    story.append(Spacer(1, 0.34 * inch))
    story.append(para("BY:", "CoverText"))
    story.append(para(DATA["studentName"].upper(), "CoverText"))
    story.append(para(f"({DATA['matricNumber']})", "CoverText"))
    story.append(Spacer(1, 0.38 * inch))
    story.append(para(DATA["department"].upper(), "CoverText"))
    story.append(para(DATA["school"].upper(), "CoverText"))
    story.append(para(DATA["university"].upper(), "CoverText"))
    story.append(Spacer(1, 0.32 * inch))
    story.append(para(f"SUPERVISOR: {DATA['supervisor']}", "CoverText"))
    story.append(para(DATA["proposalDate"].upper(), "CoverText"))
    story.append(PageBreak())
    return story


def add_paragraphs(story, paragraphs):
    for paragraph in paragraphs or []:
        story.append(para(paragraph))


def chapter_one(story):
    story.append(para("CHAPTER ONE", "Chapter"))
    story.append(para("INTRODUCTION", "Chapter"))
    for section in DATA["chapterOne"]:
        story.append(heading(section["heading"]))
        add_paragraphs(story, section.get("paragraphs"))
        if section.get("aim"):
            story.append(subheading("Aim"))
            story.append(para(section["aim"]))
        if section.get("objectives"):
            rows = [["Objective Area", "Objective Statement", "Expected Evidence"]]
            rows.extend([[item["area"], item["statement"], item["evidence"]] for item in section["objectives"]])
            story.append(table(rows, [1.35 * inch, 3.25 * inch, 2.05 * inch]))
            story.append(Spacer(1, 0.1 * inch))
        if section.get("questions"):
            rows = [["No.", "Research Question"]]
            rows.extend([[str(index + 1), question] for index, question in enumerate(section["questions"])])
            story.append(table(rows, [0.45 * inch, 6.2 * inch]))
            story.append(Spacer(1, 0.1 * inch))
        if section.get("withinScope"):
            story.append(subheading("Within Scope"))
            for item in section["withinScope"]:
                story.append(bullet(item))
            story.append(subheading("Out of Scope"))
            for item in section["outOfScope"]:
                story.append(bullet(item))
        if section.get("items"):
            for item in section["items"]:
                story.append(bullet(item))
        if section.get("terms"):
            story.append(table([["Term", "Definition"], *section["terms"]], [1.6 * inch, 5.05 * inch]))
            story.append(Spacer(1, 0.1 * inch))
    story.append(PageBreak())


def chapter_two(story):
    story.append(para("CHAPTER TWO", "Chapter"))
    story.append(para("PRELIMINARY LITERATURE REVIEW AND TECHNOLOGY CONTEXT", "Chapter"))
    for section in DATA["chapterTwo"]:
        story.append(heading(section["heading"]))
        add_paragraphs(story, section.get("paragraphs"))
        for gap in section.get("gaps", []):
            story.append(bullet(gap))
    story.append(PageBreak())


def chapter_three(story):
    story.append(para("CHAPTER THREE", "Chapter"))
    story.append(para("PROPOSED METHODOLOGY AND SYSTEM DESIGN", "Chapter"))
    for section in DATA["chapterThree"]:
        story.append(heading(section["heading"]))
        add_paragraphs(story, section.get("paragraphs"))
    story.append(heading("3.7 Methodology Alignment Matrix"))
    story.append(table(DATA["methodologyMatrix"], [1.65 * inch, 3.2 * inch, 1.8 * inch]))
    story.append(heading(DATA["solutionOverview"]["heading"]))
    add_paragraphs(story, DATA["solutionOverview"]["paragraphs"])
    story.append(subheading("Key System Components"))
    for component in DATA["solutionOverview"]["components"]:
        story.append(bullet(component))
    image_path = BASE_DIR / "figures" / "fig_3_1_architecture.png"
    if image_path.exists():
        story.append(Spacer(1, 0.08 * inch))
        img = Image(str(image_path), width=6.4 * inch, height=4.0 * inch)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(para("Figure 3.1: Proposed High-Level Architecture of InfraGuard Pro.", "Caption"))
    story.append(heading("3.8 Tools and Technologies to be Used"))
    story.append(table(DATA["tools"], [1.55 * inch, 5.1 * inch]))
    story.append(PageBreak())


def remaining_sections(story):
    story.append(para("FEASIBILITY CONSIDERATIONS", "Chapter"))
    for item in DATA["feasibility"]:
        story.append(heading(item["heading"]))
        story.append(para(item["text"]))
    story.append(PageBreak())

    story.append(para("PROJECT PLAN AND TIMELINE", "Chapter"))
    story.append(para("The proposed project plan is summarised below. The schedule will be refined after proposal approval and supervisor feedback."))
    story.append(table(DATA["timeline"], [1.1 * inch, 2.7 * inch, 2.85 * inch]))
    story.append(PageBreak())

    story.append(para("EXPECTED DELIVERABLES", "Chapter"))
    for deliverable in DATA["expectedDeliverables"]:
        story.append(bullet(deliverable))
    story.append(PageBreak())

    story.append(para("REFERENCES", "Chapter"))
    for index, reference in enumerate(DATA["references"], 1):
        story.append(Paragraph(f"{index}. {escape(reference)}", STYLES["BodyJustify"]))


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setFont("Times-Italic", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(width / 2, 0.45 * inch, f"Page {doc.page} | Copyright 2026 MIVA Open University. All Rights Reserved.")
    canvas.restoreState()


def main():
    doc = SimpleDocTemplate(
        str(OUT_PATH),
        pagesize=A4,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=f"{DATA['projectTitle']} - Project Proposal",
        author=DATA["studentName"],
    )
    story = []
    story.extend(cover())
    chapter_one(story)
    chapter_two(story)
    chapter_three(story)
    remaining_sections(story)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
