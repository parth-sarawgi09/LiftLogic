def adaptation_instruction(outcome_analysis):
    return f"""
The following insights were derived from the user's recent training outcomes:

{outcome_analysis}

Adjust the upcoming workout plan accordingly while keeping it safe, effective, and aligned with the user's goal.
"""
