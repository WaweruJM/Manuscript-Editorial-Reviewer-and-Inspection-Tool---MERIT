# modules/highlighter.py

import os
from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX
import tempfile


# ----------------------------------------
# HELPER: Highlight keyword in paragraph
# ----------------------------------------

def highlight_keyword(paragraph, keyword):

    for run in paragraph.runs:
        if keyword.lower() in run.text.lower():
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW


# ----------------------------------------
# HELPER: Add inline reviewer comment
# ----------------------------------------

def add_inline_comment(paragraph, comment, level="major"):

    run = paragraph.add_run(f"\n[Reviewer Comment: {comment}]")

    if level == "major":
        run.font.color.rgb = RGBColor(0, 0, 255)   # Blue

    elif level == "minor":
        run.font.color.rgb = RGBColor(0, 128, 0)   # Green


# ----------------------------------------
# MAIN FUNCTION
# ----------------------------------------

def annotate_document(file, method_report, stat_report):

    """
    Creates an annotated manuscript with:

    - GREEN highlight → good practices
    - YELLOW highlight → flagged areas
    - Inline reviewer comments
    - End-of-document summary

    Returns:
        output file path
    """

    doc = Document(file)

    # ----------------------------------------
    # SAFE EXTRACTION OF ISSUES
    # ----------------------------------------

    method_issues = method_report.get("issues", []) if isinstance(method_report, dict) else method_report
    stat_issues = stat_report.get("issues", []) if isinstance(stat_report, dict) else stat_report

    # ----------------------------------------
    # GOOD PRACTICE TERMS (GREEN)
    # ----------------------------------------

    correct_terms = [
        "randomization",
        "sample size calculation",
        "power analysis",
        "confidence interval",
        "95% ci",
        "p-value",
        "logistic regression",
        "odds ratio",
        "anova",
        "f-statistic",
        "hazard ratio",
        "intention to treat"
    ]

    # ----------------------------------------
    # SIMPLE ISSUE → KEYWORD MAPPING
    # ----------------------------------------

    def map_issue_to_keyword(issue):

        issue = issue.lower()

        if "random" in issue:
            return "random"

        if "confidence interval" in issue:
            return "confidence"

        if "p-value" in issue or "p value" in issue:
            return "p"

        if "sample size" in issue:
            return "sample"

        if "bias" in issue:
            return "bias"

        if "regression" in issue:
            return "regression"

        return None


    # ----------------------------------------
    # PROCESS DOCUMENT PARAGRAPHS
    # ----------------------------------------

    for paragraph in doc.paragraphs:

        text_lower = paragraph.text.lower()

        # ---- Highlight GOOD PRACTICES (GREEN)
        for run in paragraph.runs:
            for term in correct_terms:
                if term in run.text.lower():
                    run.font.highlight_color = WD_COLOR_INDEX.BRIGHT_GREEN

        # ---- Apply METHOD issues (MAJOR → BLUE)
        for issue in method_issues:

            keyword = map_issue_to_keyword(issue)

            if keyword and keyword in text_lower:

                highlight_keyword(paragraph, keyword)
                add_inline_comment(paragraph, issue, level="major")
                break  # avoid duplicate comments per paragraph

        # ---- Apply STAT issues (MINOR → GREEN)
        for issue in stat_issues:

            keyword = map_issue_to_keyword(issue)

            if keyword and keyword in text_lower:

                highlight_keyword(paragraph, keyword)
                add_inline_comment(paragraph, issue, level="minor")
                break


    # ----------------------------------------
    # ADD SUMMARY SECTION
    # ----------------------------------------

    doc.add_page_break()

    doc.add_heading("Editorial Review Summary", 0)

    # ---- Methodology
    doc.add_heading("Major Methodological Concerns", level=1)

    for issue in method_issues:
        p = doc.add_paragraph(issue)
        p.runs[0].font.color.rgb = RGBColor(0, 0, 255)

    # ---- Statistics
    doc.add_heading("Minor Statistical Concerns", level=1)

    for issue in stat_issues:
        p = doc.add_paragraph(issue)
        p.runs[0].font.color.rgb = RGBColor(0, 128, 0)


    # ----------------------------------------
    # SAVE FILE SAFELY
    # ----------------------------------------

    temp_path = tempfile.mktemp(suffix=".docx")
    doc.save(temp_path)

    return temp_path