def inspect_tables(text):

    issues = []
    lower = text.lower()

    if "table 1" not in lower:
        issues.append("Baseline characteristics table missing.")

    if "figure" not in lower:
        issues.append("No figures referenced in manuscript.")

    return {"issues": issues}