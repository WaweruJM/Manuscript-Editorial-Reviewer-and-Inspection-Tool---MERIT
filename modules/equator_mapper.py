def map_equator_items(text):

    issues = []
    lower = text.lower()

    if "trial registration" not in lower:
        issues.append("CONSORT: Trial registration missing.")

    if "ethics approval" not in lower:
        issues.append("Ethical approval not stated.")

    if "funding" not in lower:
        issues.append("Funding statement missing.")

    return {"issues": issues}