def calculate_coaching_score(outcomes):
    if not outcomes:
        return 0

    score = 0
    total = len(outcomes)

    for o in outcomes:
        if o.adherence == "full":
            score += 2
        elif o.adherence == "partial":
            score += 1

        if o.soreness == "mild":
            score += 1
        elif o.soreness == "high":
            score -= 1

        if o.progress == "improved":
            score += 2
        elif o.progress == "regressed":
            score -= 2

    return round(score / total, 2)
