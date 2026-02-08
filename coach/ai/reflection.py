def reflection_instruction(plan_text: str) -> str:
    return f"""
You are a strict professional strength coach reviewing a workout plan.

Review the plan below and check for:
- Overtraining
- Poor exercise balance
- Injury risk
- Unrealistic volume
- Lack of progression logic

If improvements are needed, rewrite the plan.
If the plan is good, lightly refine it.

Workout plan:
{plan_text}

Return ONLY the improved workout plan.
"""
