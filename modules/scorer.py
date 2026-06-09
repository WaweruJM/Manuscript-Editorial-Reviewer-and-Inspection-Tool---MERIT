# modules/scorer.py

def generate_scores(methodology_report, coherence):

    """
    Generates two editorial reviewer scores

    Score 1:
    Coherence with standard methodological principles

    Score 2:
    Coherence with manuscript's declared methods

    Returns:
       score1, score2
    """


    # ------------------------------
    # TOTAL POSSIBLE CHECKPOINTS
    # ------------------------------

    TOTAL_METHOD_RULES = 20

    TOTAL_COHERENCE_RULES = 20


    # ------------------------------
    # PENALTIES
    # ------------------------------

    method_penalties = len(
       methodology_report["issues"]
    )

    coherence_penalties = len(
       coherence
    )


    # ------------------------------
    # SCORE 1
    # Standard methodological coherence
    # ------------------------------

    score1 = (
      (TOTAL_METHOD_RULES - method_penalties)
      / TOTAL_METHOD_RULES
    ) * 100


    # ------------------------------
    # SCORE 2
    # Declared methods coherence
    # ------------------------------

    score2 = (
      (TOTAL_COHERENCE_RULES - coherence_penalties)
      / TOTAL_COHERENCE_RULES
    ) * 100


    # ------------------------------
    # Prevent negative values
    # ------------------------------

    if score1 < 0:
        score1 = 0

    if score2 < 0:
        score2 = 0


    # Round nicely
    score1 = round(score1,1)
    score2 = round(score2,1)


    return score1, score2