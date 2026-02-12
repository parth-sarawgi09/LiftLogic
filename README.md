🧠 GenAI Gym Coach

GenAI Gym Coach is a CLI-based AI workout planning system built with Python.

It generates personalized workout programs, adapts to injuries and fatigue, validates plans with safety rules, stores memory using embeddings, and learns from real training outcomes.

✨ Features

Personalized workout plan generation

Goal-based training (muscle gain / fat loss)

Experience-based logic (beginner / intermediate / advanced)

Injury-aware substitutions

Fatigue modeling from feedback

Rule-based safety constraints

Semantic validation layer

LLM self-reflection refinement

Vector memory storage (semantic retrieval)

Training outcome tracking

🛠 Tech Stack

Python

Typer (CLI)

SQLAlchemy

MySQL

Sentence Transformers

Chroma (vector store)

OpenAI API

🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/gen-ai-gym-coach.git
cd gen-ai-gym-coach

2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in the root directory:

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/gym_coach
OPENAI_API_KEY=your_openai_api_key


Replace:

username

password

gym_coach

your_openai_api_key

5️⃣ Initialize the Database
python -m coach.db.init_db


This will create all required tables.

💻 CLI Commands
👤 Onboard New User
python -m coach.main onboard

🏋️ Generate Workout Plan
python -m coach.main plan

💬 Submit Feedback (Easy / Good / Hard)
python -m coach.main feedback

🩹 Add Injury Note
python -m coach.main injury

📊 Record Training Outcome
python -m coach.main outcome

📜 View Workout History
python -m coach.main history

🧠 What Makes This Different

This is not a basic workout generator.

It includes:

Multi-stage LLM refinement

Constraint validation

Semantic memory retrieval

Confidence estimation

Outcome-based adaptation

It behaves more like an intelligent coaching system than a static planner.