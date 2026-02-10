import typer
from coach.db.session import get_session
from coach.db.models import UserProfile, WorkoutPlan, TrainingOutcome

from coach.ai.llm_client import generate_workout_plan
from coach.ai.prompts import workout_plan_prompt
from coach.ai.progression import progression_instruction
from coach.ai.feedback import feedback_instruction
from coach.ai.fatigue import infer_training_state
from coach.ai.recovery import recovery_instruction
from coach.ai.injury import injury_instruction
from coach.ai.substitutions import substitution_instruction

# DAY 12
from coach.ai.reflection import reflection_instruction

# DAY 13
from coach.memory.vector_store import store_plan, find_similar_plans

# DAY 16–19
from coach.ai.constraints import (
    volume_constraints,
    recovery_constraints,
    beginner_rules,
)
from coach.ai.validator import validate_plan
from coach.ai.semantic_validator import (
    semantic_validation_prompt,
    parse_semantic_result,
)
from coach.ai.confidence import confidence_prompt, parse_confidence

from coach.ai.outcome_analysis import analyze_outcomes
from coach.ai.adaptation import adaptation_instruction


app = typer.Typer()


# -------------------------------------------------
# Helper: Select User
# -------------------------------------------------
def select_user(session):
    users = session.query(UserProfile).all()

    if not users:
        return None

    if len(users) == 1:
        return users[0]

    print("\nSelect a user:")
    for idx, user in enumerate(users, start=1):
        print(f"{idx}. {user.name} ({user.goal}, {user.experience})")

    while True:
        try:
            choice = int(input("\nEnter user number: "))
            if 1 <= choice <= len(users):
                return users[choice - 1]
        except ValueError:
            pass

        print("❌ Invalid selection. Try again.")


# -------------------------------------------------
# Command: Onboard
# -------------------------------------------------
@app.command()
def onboard():
    session = get_session()

    user = UserProfile(
        name=input("Name: "),
        age=int(input("Age: ")),
        height_cm=int(input("Height (cm): ")),
        weight_kg=int(input("Weight (kg): ")),
        goal=input("Goal (muscle_gain / fat_loss): "),
        experience=input("Experience (beginner / intermediate / advanced): "),
        days_per_week=int(input("Workout days per week: ")),
    )

    session.add(user)
    session.commit()
    session.close()

    print("✅ User onboarded successfully!")


# -------------------------------------------------
# Command: Generate Plan (DAY 19)
# -------------------------------------------------
@app.command()
def plan():
    session = get_session()
    user = select_user(session)

    if not user:
        print("❌ No users found.")
        session.close()
        return

    previous_plans = (
        session.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .limit(3)
        .all()
    )

    # -------- Derived State --------
    training_state = infer_training_state(previous_plans)
    injury_note = previous_plans[0].injury_note if previous_plans else None
    latest_feedback = previous_plans[0].feedback if previous_plans else None

    # -------- Semantic Memory --------
    similar_plans = find_similar_plans(
        f"{user.goal} {user.experience} {training_state}"
    )

    semantic_text = ""
    if similar_plans:
        semantic_text = "\n\nRelevant past experiences:\n"
        for plan in similar_plans:
            semantic_text += f"\n{plan}\n"

    # -------- Constraints --------
    volume_rules = volume_constraints(user)
    recovery_rules = recovery_constraints(training_state)
    beginner_guardrails = beginner_rules(user)

    # -------- Base Prompt --------
    prompt = (
        workout_plan_prompt(user)
        + semantic_text
        + "\n\nTraining state:\n"
        + training_state
        + "\n\nInjury considerations:\n"
        + injury_instruction(injury_note)
        + "\n\nExercise substitutions:\n"
        + substitution_instruction(injury_note)
        + "\n\nFeedback analysis:\n"
        + feedback_instruction(latest_feedback)
        + "\n\nRecovery strategy:\n"
        + recovery_instruction(training_state)
        + "\n\nProgression strategy:\n"
        + progression_instruction(user, previous_plans)
        + "\n\nCOACHING CONSTRAINTS (MANDATORY):\n"
        + f"Volume rules: {volume_rules}\n"
        + f"Recovery rules: {recovery_rules}\n"
        + beginner_guardrails
    )

    print(f"\n🤖 Generating workout plan for {user.name}...")
    draft_plan = generate_workout_plan(prompt)

    # -------------------------------------------------
    # DAY 12: SELF-REFLECTION
    # -------------------------------------------------
    reflection_prompt = reflection_instruction(draft_plan)
    final_plan = generate_workout_plan(reflection_prompt)

    # -------------------------------------------------
    # RULE VALIDATION
    # -------------------------------------------------
    errors = validate_plan(final_plan, volume_rules)

    if errors:
        correction_prompt = (
            "The following workout plan violates coaching rules:\n"
            + "\n".join(f"- {e}" for e in errors)
            + "\n\nFix the plan while keeping it safe and effective:\n\n"
            + final_plan
        )
        final_plan = generate_workout_plan(correction_prompt)

    # -------------------------------------------------
    # SEMANTIC VALIDATION
    # -------------------------------------------------
    context = {
        "training_state": training_state,
        "injury_note": injury_note,
    }

    judge_prompt = semantic_validation_prompt(user, final_plan, context)
    judgement = generate_workout_plan(judge_prompt)

    is_valid, reasons = parse_semantic_result(judgement)

    if not is_valid:
        correction_prompt = (
            "The plan is NOT appropriate:\n"
            + "\n".join(f"- {r}" for r in reasons)
            + "\n\nRewrite the plan to fix these issues:\n\n"
            + final_plan
        )
        final_plan = generate_workout_plan(correction_prompt)

    # -------------------------------------------------
    # CONFIDENCE GATE
    # -------------------------------------------------
    confidence_prompt_text = confidence_prompt(user, final_plan, context)
    confidence_result = generate_workout_plan(confidence_prompt_text)

    is_confident, missing_info = parse_confidence(confidence_result)

    if not is_confident:
        print("\n⚠️ More information required before finalizing:")
        for item in missing_info:
            print(f"- {item}")
        session.close()
        return

    # -------------------------------------------------
    # SAVE PLAN
    # -------------------------------------------------
    workout_plan = WorkoutPlan(
        user_id=user.id,
        plan_text=final_plan,
    )

    session.add(workout_plan)
    session.commit()

    # -------------------------------------------------
    # DAY 13: VECTOR MEMORY
    # -------------------------------------------------
    store_plan(workout_plan.id, final_plan)

    session.close()

    print("\n✅ Workout plan generated, validated, judged, and remembered!\n")
    print(final_plan)


# -------------------------------------------------
# Command: Injury
# -------------------------------------------------
@app.command()
def injury():
    session = get_session()
    user = select_user(session)

    if not user:
        print("❌ No users found.")
        session.close()
        return

    last_plan = (
        session.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    if not last_plan:
        print("❌ No workout plans found.")
        session.close()
        return

    note = input("\nDescribe any injury or pain (Enter for none): ").strip()
    last_plan.injury_note = note if note else None

    session.commit()
    session.close()

    print("✅ Injury note saved.")


# -------------------------------------------------
# Command: Feedback
# -------------------------------------------------
@app.command()
def feedback():
    session = get_session()
    user = select_user(session)

    if not user:
        print("❌ No users found.")
        session.close()
        return

    last_plan = (
        session.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    if not last_plan:
        print("❌ No workout plans found.")
        session.close()
        return

    print("\nHow did the last workout feel?")
    print("1. Easy\n2. Good\n3. Hard")

    mapping = {"1": "easy", "2": "good", "3": "hard"}
    feedback = mapping.get(input("Enter choice: ").strip())

    if not feedback:
        print("❌ Invalid input.")
        session.close()
        return

    last_plan.feedback = feedback
    session.commit()
    session.close()

    print("✅ Feedback saved.")


# -------------------------------------------------
# Command: History
# -------------------------------------------------
@app.command()
def history():
    session = get_session()
    user = select_user(session)

    plans = (
        session.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .all()
    )

    if not plans:
        print("❌ No workout history.")
        session.close()
        return

    print(f"\n📜 Workout history for {user.name}\n")
    for idx, plan in enumerate(plans, start=1):
        print(f"--- Plan {idx} ---")
        print(plan.plan_text)
        if plan.feedback:
            print(f"Feedback: {plan.feedback}")
        if plan.injury_note:
            print(f"Injury: {plan.injury_note}")
        print("-" * 40)

    session.close()


# -------------------------------------------------
# Command: Outcome (DAY 14)
# -------------------------------------------------
@app.command()
def outcome():
    session = get_session()
    user = select_user(session)

    last_plan = (
        session.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    if not last_plan:
        print("❌ No workout plan found.")
        session.close()
        return

    outcome = TrainingOutcome(
        user_id=user.id,
        plan_id=last_plan.id,
        adherence=input("Adherence (full/partial/skipped): "),
        soreness=input("Soreness (none/mild/high): "),
        progress=input("Progress (improved/stalled/regressed): "),
        notes=input("Notes (optional): ") or None,
    )

    session.add(outcome)
    session.commit()
    session.close()

    print("✅ Training outcome saved.")


if __name__ == "__main__":
    app()
