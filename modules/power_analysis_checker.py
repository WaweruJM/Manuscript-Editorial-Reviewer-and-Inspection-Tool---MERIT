def assess_power(text):

    issues = []
    lower = text.lower()

    if "power analysis" not in lower:
        issues.append("Power analysis not reported.")

    if "sample size calculation" not in lower:
        issues.append("Sample size calculation missing.")

    return {"issues": issues}