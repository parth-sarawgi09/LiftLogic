from typing import List
from coach.db.models import WorkoutPlan, UserProfile


def progression_instruction(
    user: UserProfile,
    previous_plans: List[WorkoutPlan]
) -> str:
    """
    Decide how the workout should progress
    """

    if not previous_plans:
        return "Create a balanced foundational workout plan."

    if len(previous_plans) == 1:
        return (
            "Progress slightly from the previous plan. "
            "Increase either reps or weight by a small margin."
        )

    instruction = (
        "Progress the workout plan compared to previous weeks. "
        "Increase training intensity or volume. "
        "Avoid repeating the same exercises exactly."
    )

    if user.experience == "advanced":
        instruction += (
            " Include advanced techniques like supersets, drop sets, or tempo control."
        )

    if user.goal == "fat_loss":
        instruction += (
            " Increase calorie expenditure with short rest periods or conditioning work."
        )

    return instruction
