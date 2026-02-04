import typer
from coach.db.session import get_session
from coach.db.models import UserProfile, WorkoutPlan
from coach.ai.llm_client import generate_workout_plan
from coach.ai.prompts import workout_plan_prompt
from coach.ai.progression import progression_instruction

app = typer.Typer()


@app.command()
def onboard():
    """
    Onboard a new user
    """
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
        days_per_week=days
    )

    session.add(user)
    session.commit()
    session.close()

    print("✅ User onboarded successfully!")


@app.command()
def plan():
    """
    Generate a workout plan using AI (Day 5: progressive overload)
    """
    session = get_session()

    user = session.query(UserProfile).first()

    if not user:
        print("❌ No user found. Please run onboard first.")
        session.close()
        return

    # 🔹 Fetch last 3 workout plans (memory)
    previous_plans = (
        session.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .limit(3)
        .all()
    )

    # 🔹 Convert history to text
    history_text = ""
    if previous_plans:
        history_text = "\n\nPrevious workout plans:\n"
        for idx, plan in enumerate(previous_plans, start=1):
            history_text += f"\nPlan {idx}:\n{plan.plan_text}\n"

    # 🔥 Day 5: rule-based progression logic
    progression_text = progression_instruction(user, previous_plans)

    # 🔹 Final prompt sent to LLM
    prompt = (
        workout_plan_prompt(user)
        + history_text
        + "\n\nProgression instructions:\n"
        + progression_text
    )

    print("🤖 Generating workout plan...")
    plan_text = generate_workout_plan(prompt)

    workout_plan = WorkoutPlan(
        user_id=user.id,
        plan_text=plan_text
    )

    session.add(workout_plan)
    session.commit()
    session.close()

    print("✅ Workout plan generated and saved!\n")
    print(plan_text)


if __name__ == "__main__":
    app()
