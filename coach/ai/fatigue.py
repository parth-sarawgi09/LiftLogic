from coach.db.models import WorkoutPlan

def infer_training_state(previous_plans: list[WorkoutPlan]) -> str:
    if not previous_plans:
        return "fresh"

    recent_feedback = [
        p.feedback for p in previous_plans
        if p.feedback is not None
    ][:3]

    if len(recent_feedback) < 2:
        return "progressing"

    if recent_feedback.count("hard") >= 3:
        return "overreached"

    if recent_feedback.count("hard") == 2:
        return "fatigued"

    if recent_feedback.count("easy") >= 2:
        return "fresh"

    return "progressing"
