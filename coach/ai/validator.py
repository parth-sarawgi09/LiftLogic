import re

def extract_set_counts(plan_text):
    """
    Returns list of set counts found in plan text
    Example matches: '4 sets', '5 sets of'
    """
    return [int(x) for x in re.findall(r'(\d+)\s*sets', plan_text.lower())]


def count_exercises(plan_text):
    """
    Heuristic: count numbered exercise lines
    """
    return len(re.findall(r'\n\d+\.', plan_text))


def validate_plan(plan_text, constraints):
    errors = []

    # Volume checks
    max_sets = constraints.get("max_sets_per_exercise")
    max_exercises = constraints.get("max_exercises_per_day")

    set_counts = extract_set_counts(plan_text)
    if max_sets and any(s > max_sets for s in set_counts):
        errors.append("Too many sets per exercise.")

    exercise_count = count_exercises(plan_text)
    if max_exercises and exercise_count > max_exercises * constraints.get("max_training_days", 1):
        errors.append("Too many exercises overall.")

    # Beginner deadlift rule
    if "deadlift" in plan_text.lower():
        if plan_text.lower().count("deadlift") > 1:
            errors.append("Deadlift appears more than once.")

    return errors
