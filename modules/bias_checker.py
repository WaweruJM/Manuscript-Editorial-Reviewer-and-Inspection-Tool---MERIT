def detect_bias(text):

    issues = []
    lower = text.lower()

    if "random" not in lower:
        issues.append("Potential selection bias: randomization not described.")

    if "blinding" not in lower:
        issues.append("Performance bias risk: blinding not reported.")

    return {"issues": issues}