def analyze_outcomes(outcomes):
    if not outcomes:
        return "No outcome history available."

    adherence = [o.adherence for o in outcomes]
    soreness = [o.soreness for o in outcomes]
    progress = [o.progress for o in outcomes]

    insights = []

    if adherence.count("skipped") >= 2:
        insights.append("Reduce weekly volume and simplify workouts.")

    if soreness.count("high") >= 2:
        insights.append("Reduce intensity and add recovery emphasis.")

    if progress.count("stalled") >= 2:
        insights.append("Increase progressive overload or exercise variation.")

    if progress.count("improved") >= 2:
        insights.append("Maintain current structure with slight progression.")

    if not insights:
        insights.append("Maintain current training strategy.")

    return "\n".join(insights)
