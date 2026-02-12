def analyze_trends(outcomes):
    if not outcomes:
        return "no_data"

    improvements = 0
    regressions = 0
    stalled = 0
    high_soreness = 0
    skipped = 0

    for o in outcomes:
        if o.progress == "improved":
            improvements += 1
        elif o.progress == "regressed":
            regressions += 1
        elif o.progress == "stalled":
            stalled += 1

        if o.soreness == "high":
            high_soreness += 1

        if o.adherence == "skipped":
            skipped += 1

    total = len(outcomes)

    if regressions >= 2:
        return "regression_pattern"

    if stalled >= 3:
        return "plateau_pattern"

    if high_soreness >= total // 2:
        return "fatigue_pattern"

    if skipped >= total // 2:
        return "adherence_problem"

    if improvements >= total // 2:
        return "positive_adaptation"

    return "neutral"
