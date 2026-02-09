def confidence_prompt(user, plan_text, context):
    return f"""
You are an expert fitness coach.

User profile:
- Goal: {user.goal}
- Experience: {user.experience}
- Training state: {context['training_state']}
- Injury note: {context.get('injury_note')}

Workout plan:
{plan_text}

Do you have enough information to confidently recommend this plan?

Answer ONLY in this format:
CONFIDENCE: high/low
MISSING_INFO:
- item 1 (if any)
- item 2 (if any)
"""

def parse_confidence(text):
    confidence = "confidence: high" in text.lower()
    missing = []

    if "missing_info:" in text.lower():
        lines = text.splitlines()
        missing = [l.strip("- ").strip() for l in lines if l.strip().startswith("-")]

    return confidence, missing
