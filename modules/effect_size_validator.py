def validate_effect_sizes(text):

    issues = []
    lower = text.lower()

    if "odds ratio" not in lower and "relative risk" not in lower:
        issues.append("Effect size measures not clearly reported.")

    if "confidence interval" not in lower:
        issues.append("Effect size reported without confidence intervals.")

    return {"issues": issues}