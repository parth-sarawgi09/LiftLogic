def strategic_adaptation_instruction(trend):
    mapping = {
        "regression_pattern": "Reduce intensity by 10-15%, prioritize recovery and technique refinement.",
        "plateau_pattern": "Change stimulus: modify rep ranges, tempo, or introduce new compound variations.",
        "fatigue_pattern": "Implement a deload week with 30% reduced volume.",
        "adherence_problem": "Simplify program structure and reduce weekly session difficulty.",
        "positive_adaptation": "Progress load by 2-5% and slightly increase intensity.",
        "neutral": "Maintain progression cautiously.",
        "no_data": "Generate a standard progressive plan."
    }

    return mapping.get(trend, "Maintain conservative progression.")
    