def workout_plan_prompt(user):
    return f"""
You are a professional fitness coach.

Create a 7-day workout plan for the following user:

Name: {user.name}
Age: {user.age}
Height: {user.height_cm} cm
Weight: {user.weight_kg} kg
Goal: {user.goal}
Experience level: {user.experience}
Workout days per week: {user.days_per_week}

Rules:
- Gym-based workouts
- Clear day-wise split
- Mention sets and reps
- No medical advice
- Keep it concise and practical
"""
