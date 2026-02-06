# coach/ai/substitutions.py

def substitution_instruction(injury_note: str | None) -> str:
    if not injury_note:
        return "No exercise substitutions needed."

    injury = injury_note.lower()

    rules = []

    if "knee" in injury:
        rules.append(
            "- Avoid barbell back squats and deep knee flexion\n"
            "- Prefer leg press, step-ups, split squats, hamstring-dominant work"
        )

    if "shoulder" in injury:
        rules.append(
            "- Avoid overhead pressing and wide-grip bench press\n"
            "- Prefer landmine press, incline dumbbell press, lateral raises"
        )

    if "lower back" in injury or "back" in injury:
        rules.append(
            "- Avoid conventional deadlifts and bent-over rows\n"
            "- Prefer hip thrusts, chest-supported rows, RDLs with light load"
        )

    if "elbow" in injury:
        rules.append(
            "- Avoid heavy skull crushers and straight-bar curls\n"
            "- Prefer rope pushdowns, neutral-grip curls"
        )

    if "wrist" in injury:
        rules.append(
            "- Avoid barbell-heavy wrist extension\n"
            "- Prefer neutral-grip dumbbells or machines"
        )

    if not rules:
        return "Minor discomfort noted. Maintain exercises but reduce load if needed."

    return (
        "Apply the following exercise substitutions strictly:\n"
        + "\n".join(rules)
    )
