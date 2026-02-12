def determine_training_phase(user, previous_plans):
    total_plans = len(previous_plans)

    if total_plans < 3:
        return "foundation"

    if total_plans < 6:
        return "hypertrophy"

    if total_plans < 9:
        return "intensification"

    if total_plans % 4 == 0:
        return "deload"

    return "progressive_overload"


def phase_instruction(phase):
    mapping = {
        "foundation": "Focus on movement quality, moderate volume, controlled tempo, and technique mastery.",
        "hypertrophy": "Increase total weekly volume, target 8-15 rep ranges, emphasize muscle tension.",
        "intensification": "Lower reps (4-8), increase load, prioritize compound lifts.",
        "deload": "Reduce volume by 30-40% and decrease intensity. Prioritize recovery.",
        "progressive_overload": "Progress load gradually while maintaining good recovery balance."
    }

    return mapping.get(phase, "Maintain structured progression.")
