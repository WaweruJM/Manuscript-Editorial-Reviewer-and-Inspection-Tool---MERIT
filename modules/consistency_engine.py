import re


def extract_section(text, section_name):
    """
    Extract approximate section text using regex.
    """

    pattern = rf"{section_name}(.+?)(introduction|methods|results|discussion|conclusion|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).lower()

    return ""


def check_consistency(text):
    """
    Performs internal manuscript consistency checks.
    """

    issues = []
    lower = text.lower()

    # ---------------------------------------
    # SECTION EXTRACTION
    # ---------------------------------------

    methods = extract_section(lower, "methods")
    results = extract_section(lower, "results")
    conclusion = extract_section(lower, "conclusion")

    # ---------------------------------------
    # 1. METHODS vs RESULTS ALIGNMENT
    # ---------------------------------------

    if methods and results:

        if "regression" in methods and "regression" not in results:
            issues.append(
                "Statistical inconsistency: Regression analysis described in methods but not reported in results."
            )

        if "chi-square" in methods and "chi-square" not in results:
            issues.append(
                "Statistical inconsistency: Chi-square test mentioned in methods but absent in results."
            )

    # ---------------------------------------
    # 2. SAMPLE SIZE CONSISTENCY
    # ---------------------------------------

    sample_sizes = re.findall(r"n\s*=\s*(\d+)", lower)

    if len(set(sample_sizes)) > 1:
        issues.append(
            "Inconsistent sample size reporting across manuscript sections."
        )

    # ---------------------------------------
    # 3. OBJECTIVE vs CONCLUSION ALIGNMENT
    # ---------------------------------------

    if "objective" in lower and conclusion:

        if "significant" in conclusion and "p value" not in lower:
            issues.append(
                "Conclusion claims statistical significance without supporting p-values."
            )

    # ---------------------------------------
    # 4. METHODS vs VARIABLES REPORTED
    # ---------------------------------------

    if "independent variable" in methods and "independent variable" not in results:
        issues.append(
            "Variables defined in methods not reflected in results."
        )

    # ---------------------------------------
    # 5. TABLE / RESULT CROSS-REFERENCE
    # ---------------------------------------

    if "table" in results and "table" not in methods:
        issues.append(
            "Tables referenced in results but not described in methods."
        )

    # ---------------------------------------
    # 6. TEMPORAL CONSISTENCY
    # ---------------------------------------

    if "prospective" in methods and "retrospective" in results:
        issues.append(
            "Study design inconsistency: Prospective design in methods but retrospective indicated in results."
        )

    # ---------------------------------------
    # 7. MISSING LINK BETWEEN RESULTS AND CONCLUSION
    # ---------------------------------------

    if results and conclusion:

        if len(results.strip()) > 0 and len(conclusion.strip()) > 0:

            if "therefore" not in conclusion and "thus" not in conclusion:
                issues.append(
                    "Weak logical linkage between results and conclusion (missing inferential transition)."
                )

    # ---------------------------------------
    # RETURN STRUCTURED OUTPUT
    # ---------------------------------------

    return {
        "issues": issues
    }