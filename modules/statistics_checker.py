# modules/statistics_checker.py

import re


def validate_statistics(text):
    """
    Checks whether statistical methods reported in a manuscript
    are coherent with standard statistical principles.

    Returns:
        dict: {"issues": list of identified problems}
    """

    issues = []

    if not text:
        return {"issues": ["No text provided for statistical analysis."]}

    text = text.lower()


    # -----------------------------------
    # P VALUES CHECK
    # -----------------------------------

    if "p value" in text or "p-value" in text or "p<" in text:

        if not re.search(r"p\s*[<=>]\s*0\.\d+", text):

            issues.append(
                "P-values mentioned but improperly formatted."
            )


    # -----------------------------------
    # CONFIDENCE INTERVAL CHECK
    # -----------------------------------

    if "odds ratio" in text or "relative risk" in text:

        if "confidence interval" not in text and "95% ci" not in text:

            issues.append(
                "Effect measures reported without confidence intervals."
            )


    # -----------------------------------
    # T-TEST ASSUMPTION CHECK
    # -----------------------------------

    if "t-test" in text or "student t test" in text:

        if "normality" not in text:

            issues.append(
                "T-test reported but normality assumption not mentioned."
            )


    # -----------------------------------
    # CHI-SQUARE CHECK
    # -----------------------------------

    if "chi-square" in text:

        if "expected frequency" not in text:

            issues.append(
                "Chi-square reported without expected frequency assumption."
            )


    # -----------------------------------
    # LOGISTIC REGRESSION CHECK
    # -----------------------------------

    if "logistic regression" in text:

        if "odds ratio" not in text:

            issues.append(
                "Logistic regression reported without odds ratios."
            )

        if "multicollinearity" not in text:

            issues.append(
                "No assessment of multicollinearity reported."
            )


    # -----------------------------------
    # LINEAR REGRESSION CHECK
    # -----------------------------------

    if "linear regression" in text:

        if "residual" not in text:

            issues.append(
                "Linear regression without residual diagnostics."
            )


    # -----------------------------------
    # SAMPLE SIZE / POWER CHECK
    # -----------------------------------

    if "sample size" not in text and "power analysis" not in text:

        issues.append(
            "Sample size calculation or power analysis missing."
        )


    # -----------------------------------
    # MULTIPLE COMPARISON CHECK
    # -----------------------------------

    if "anova" in text:

        if "post hoc" not in text:

            issues.append(
                "ANOVA reported without post hoc testing."
            )


    # -----------------------------------
    # NO PROBLEMS
    # -----------------------------------

    if len(issues) == 0:

        issues.append(
            "No major statistical problems detected."
        )


    # ✅ FIX: return standardized structure
    return {"issues": issues}