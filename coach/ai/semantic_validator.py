def semantic_validation_prompt(user, plan_text, context):
    return f"""
You are an experienced strength coach.

User profile:
- Goal: {user.goal}
- Experience: {user.experience}
- Training state: {context['training_state']}
- Injury note: {context.get('injury_note')}

Workout plan:
{plan_text}

Evaluate whether this plan is appropriate.

Answer ONLY in this format:
VALID: yes/no
REASONS:
- reason 1
- reason 2 (if any)
"""


def parse_semantic_result(text):
    valid = "VALID: yes" in text.lower()
    reasons = []

    if "reasons:" in text.lower():
        lines = text.splitlines()
        reasons = [l.strip("- ").strip() for l in lines if l.strip().startswith("-")]

    return valid, reasons
