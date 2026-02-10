def rank_questions_prompt(missing_info, user):
    return f"""
You are an expert fitness coach.

User:
- Goal: {user.goal}
- Experience: {user.experience}

Missing information:
{chr(10).join(f"- {m}" for m in missing_info)}

Rank these questions by importance for making a SAFE and EFFECTIVE workout plan.

Return ONLY the most important question.
"""
