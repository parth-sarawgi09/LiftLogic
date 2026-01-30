import typer
from coach.db.session import get_session
from coach.db.models import UserProfile, WorkoutPlan
from coach.ai.llm_client import generate_workout_plan
from coach.ai.prompts import workout_plan_prompt

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
    Generate a workout plan using Gemini AI
    """
    session = get_session()

    user = session.query(UserProfile).first()

    if not user:
        print("❌ No user found. Please run onboard first.")
        session.close()
        return

    prompt = workout_plan_prompt(user)

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
