# modules/coherence_engine.py

def check_coherence(text, stat_report):
    """
    Evaluates internal consistency between methods, results,
    and statistical reporting.

    Returns:
        dict: {"issues": [...]}
    """

    issues = []

    if not text:
        return {"issues": ["No manuscript text available for coherence analysis."]}

    text_lower = text.lower()

    # -----------------------------------
    # STATISTICAL BURDEN CHECK
    # -----------------------------------

    if isinstance(stat_report, dict):
        stat_issues = stat_report.get("issues", [])
    else:
        stat_issues = stat_report  # fallback if still list

    if len(stat_issues) > 3:
        issues.append(
            "High number of statistical issues detected, reducing overall coherence."
        )

    # -----------------------------------
    # OBJECTIVE vs CONCLUSION CHECK
    # -----------------------------------

    if "objective" in text_lower and "conclusion" not in text_lower:
        issues.append(
            "Study objective stated but no clear conclusion found."
        )

    # -----------------------------------
    # METHODS vs RESULTS CHECK
    # -----------------------------------

    if "methods" in text_lower and "results" not in text_lower:
        issues.append(
            "Methods described without corresponding results section."
        )

    # -----------------------------------
    # INTERNAL LOGIC CHECK
    # -----------------------------------

    if "significant" in text_lower and "p value" not in text_lower:
        issues.append(
            "Claims of significance made without supporting statistical evidence."
        )

    # -----------------------------------
    # NO ISSUES CASE
    # -----------------------------------

    if len(issues) == 0:
        issues.append("No major coherence issues detected.")

    return {"issues": issues}   # ✅ CRITICAL FIX