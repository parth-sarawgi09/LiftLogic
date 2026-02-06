def injury_instruction(injury: str | None) -> str:
    if not injury or injury == "none":
        return "User reports no pain or injuries."

    return (
        f"User reports {injury} pain. "
        "Avoid exercises that stress this area. "
        "Suggest safe alternatives, reduce intensity if needed, "
        "and prioritize joint-friendly movements."
    )
