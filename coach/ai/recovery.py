def recovery_instruction(training_state: str) -> str:
    if training_state == "overreached":
        return (
            "User appears overreached. "
            "Generate a deload-style week with reduced volume (40–50%), "
            "lower intensity, extra rest days, mobility work, and recovery focus."
        )

    if training_state == "fatigued":
        return (
            "User shows signs of fatigue. "
            "Reduce total volume by ~20%, avoid failure sets, "
            "prioritize recovery and technique."
        )

    if training_state == "fresh":
        return (
            "User is fresh and underloaded. "
            "Slightly increase volume or intensity while maintaining good form."
        )

    return (
        "User is progressing normally. "
        "Maintain structure and apply conservative progressive overload."
    )
