def feedback_instruction(feedback: str | None) -> str:
    if not feedback:
        return "No feedback was given for previous workouts."

    if feedback == "easy":
        return (
            "The previous workout felt easy. "
            "Increase intensity by adding weight, sets, or volume."
        )

    if feedback == "hard":
        return (
            "The previous workout felt too hard. "
            "Reduce volume slightly or add more rest."
        )

    return (
        "The previous workout felt balanced. "
        "Apply progressive overload conservatively."
    )
