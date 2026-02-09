def volume_constraints(user):
    if user.experience == "beginner":
        return {
            "max_exercises_per_day": 5,
            "max_sets_per_exercise": 4,
            "max_training_days": min(user.days_per_week, 5),
            "max_core_days": 2,
        }

    if user.experience == "intermediate":
        return {
            "max_exercises_per_day": 6,
            "max_sets_per_exercise": 5,
            "max_core_days": 3,
        }

    return {}

def recovery_constraints(training_state):
    if training_state == "fatigued":
        return "Reduce total volume by 30% and remove deadlifts or squats."

    if training_state == "overreaching":
        return "Force deload week. No progression. RPE ≤ 7."

    return "Normal recovery capacity."

def beginner_rules(user):
    if user.experience != "beginner":
        return ""

    return """
Beginner safety rules:
- No more than 1 heavy compound lift per session
- No deadlifts more than once per week
- No training same muscle group on consecutive days
- Avoid failure training
"""
