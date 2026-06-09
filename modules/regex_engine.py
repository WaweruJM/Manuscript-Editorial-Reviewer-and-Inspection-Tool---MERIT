# modules/regex_engine.py

import regex as re


def check_guidelines(
    text,
    consort=False,
    strobe=False,
    prisma=False,
    sampl=False
):

    """
    Checks manuscript against methodological
    reporting guideline indicators.
    """

    issues = []

    text = text.lower()


    patterns = {

      "randomization":
      r"randomi[sz]ation",

      "sample_size":
      r"sample size calculation|power analysis",

      "confidence_interval":
      r"95% ci|confidence interval",

      "p_value":
      r"p\s*[<=>]\s*0\.\d+"

    }


    for name, pattern in patterns.items():

        if not re.search(pattern, text):

            issues.append(
               f"Missing: {name}"
            )


    # Guideline-specific checks

    if consort:

        if "participant flow" not in text:

            issues.append(
               "CONSORT: participant flow missing"
            )


    if strobe:

        if "confounding" not in text:

            issues.append(
              "STROBE: confounding discussion missing"
            )


    if prisma:

        if "flow diagram" not in text:

            issues.append(
              "PRISMA: flow diagram missing"
            )


    if sampl:

        if "effect size" not in text:

            issues.append(
              "SAMPL: effect size missing"
            )


    return {

      "issues": issues,

      "matches": patterns

    }

   