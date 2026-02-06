import typer
from coach.db.session import get_session
from coach.db.models import UserProfile, WorkoutPlan

from coach.ai.llm_client import generate_workout_plan
from coach.ai.prompts import workout_plan_prompt
from coach.ai.progression import progression_instruction
from coach.ai.feedback import feedback_instruction
from coach.ai.fatigue import infer_training_state
from coach.ai.recovery import recovery_instruction
from coach.ai.injury import injury_instruction

app = typer.Typer()


# -------------------------
# Helper: Select User
# -------------------------
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


# -------------------------
# Command: Onboard
# -------------------------
@app.command()
def onboard():
    name = input("Name: ")
    age = int(input("Age: "))
    height = int(input("Height (cm): "))
    weight = int(input("Weight (kg): "))
    goal = input("Goal (muscle_gain / fat_loss): ")
    experience = input("Experience (beginner / intermediate / advanced): ")
    days = int(input("Workout days per week: "))

    session = get_session()

    user = UserProfile(
        name=name,
        age=age,
        height_cm=height,
        weight_kg=weight,
        goal=goal,
        experience=experience,
        days_per_week=days,
    )

    session.add(user)
    session.commit()
    session.close()

    print("✅ User onboarded successfully!")


# -------------------------
# Command: Generate Plan
# -------------------------
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

    history_text = ""
    if previous_plans:
        history_text = "\n\nPrevious workout plans:\n"
        for idx, plan in enumerate(previous_plans, start=1):
            history_text += f"\nPlan {idx}:\n{plan.plan_text}\n"

    latest_feedback = previous_plans[0].feedback if previous_plans else None
    feedback_text = feedback_instruction(latest_feedback)

    training_state = infer_training_state(previous_plans)
    recovery_text = recovery_instruction(training_state)

    injury_note = previous_plans[0].injury_note if previous_plans else None
    injury_text = injury_instruction(injury_note)

    progression_text = progression_instruction(user, previous_plans)

    prompt = (
        workout_plan_prompt(user)
        + history_text
        + "\n\nTraining state:\n"
        + training_state
        + "\n\nInjury considerations:\n"
        + injury_text
        + "\n\nFeedback analysis:\n"
        + feedback_text
        + "\n\nRecovery strategy:\n"
        + recovery_text
        + "\n\nProgression strategy:\n"
        + progression_text
    )

    print(f"\n🤖 Generating workout plan for {user.name}...")
    plan_text = generate_workout_plan(prompt)

    workout_plan = WorkoutPlan(
        user_id=user.id,
        plan_text=plan_text,
    )

    session.add(workout_plan)
    session.commit()
    session.close()

    print("✅ Workout plan generated and saved!\n")
    print(plan_text)


# -------------------------
# Command: Injury Input (DAY 10)
# -------------------------
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
        print("❌ No workout plan found.")
        session.close()
        return

    print("\nAny pain or injury?")
    print("1. None")
    print("2. Shoulder")
    print("3. Knee")
    print("4. Lower back")
    print("5. Elbow")
    print("6. Wrist")

    mapping = {
        "1": "none",
        "2": "shoulder",
        "3": "knee",
        "4": "lower back",
        "5": "elbow",
        "6": "wrist",
    }

    choice = input("Enter choice: ").strip()
    injury = mapping.get(choice)

    if not injury:
        print("❌ Invalid input.")
        session.close()
        return

    last_plan.injury_note = injury
    session.commit()
    session.close()

    print("✅ Injury information saved!")


# -------------------------
# Command: Feedback
# -------------------------
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
    print("1. Easy")
    print("2. Good")
    print("3. Hard")

    mapping = {"1": "easy", "2": "good", "3": "hard"}
    feedback = mapping.get(input("Enter choice: ").strip())

    if not feedback:
        print("❌ Invalid input.")
        session.close()
        return

    last_plan.feedback = feedback
    session.commit()
    session.close()

    print("✅ Feedback saved successfully!")


# -------------------------
# Command: History
# -------------------------
@app.command()
def history():
    session = get_session()
    user = select_user(session)

    if not user:
        print("❌ No users found.")
        session.close()
        return

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


if __name__ == "__main__":
    app()
