🧠 GenAI Gym Coach
An Adaptive AI Workout Coaching System with Memory, Validation & Outcome Learning
🚀 Overview

GenAI Gym Coach is an intelligent workout planning system powered by Large Language Models (LLMs).

Unlike static workout generators, this system:

Generates personalized training programs

Adapts to injuries and fatigue

Learns from user feedback

Validates plans using rule-based guardrails

Uses semantic memory retrieval

Tracks real training outcomes

Implements a full closed-loop adaptive learning system

This project demonstrates advanced AI system design beyond simple prompt engineering.

🧩 Core Capabilities
1️⃣ Personalized Workout Generation

Goal-aware (muscle_gain / fat_loss)

Experience-aware (beginner / intermediate / advanced)

Progressive overload logic

Recovery strategy integration

2️⃣ Injury-Aware Adaptation

Stores injury notes

Suggests safe substitutions

Automatically modifies unsafe exercises

3️⃣ Feedback & Fatigue Modeling

After each workout:

User rates difficulty (easy / good / hard)

System infers training state:

recovering

progressing

fatigued

Future plans adapt accordingly

4️⃣ Semantic Memory (Vector Database)

Stores past workout plans as embeddings

Retrieves similar past training scenarios

Injects contextual memory into new plan generation

5️⃣ Rule-Based Guardrails

Strict enforcement of:

Volume constraints

Recovery constraints

Beginner safety rules

Plans violating constraints are auto-corrected.

6️⃣ LLM Self-Reflection

Each workout plan goes through:

Draft generation

Self-critique pass

Plan refinement

Improves structure, realism, and safety.

7️⃣ Semantic Validation Layer

A second LLM acts as a judge to verify:

Plan appropriateness

Injury compatibility

Recovery alignment

If invalid → plan is rewritten.

8️⃣ Confidence Estimation

Before finalizing, the system checks:

Is enough information available?

Is user context sufficient?

If not, it asks clarifying questions instead of guessing.

9️⃣ Training Outcome Tracking

After completing a plan, the user records:

Adherence: full / partial / skipped

Soreness: none / mild / high

Progress: improved / stalled / regressed

Optional notes

This enables true adaptive coaching based on real outcomes.

🏗️ System Architecture (High-Level)
User Profile
     ↓
Plan Generation
     ↓
Self Reflection
     ↓
Rule Validation
     ↓
Semantic Validation
     ↓
Confidence Check
     ↓
Final Plan
     ↓
Workout Execution
     ↓
Outcome Recording
     ↓
Fatigue Inference
     ↓
Next Adaptive Plan


This is a closed-loop AI coaching system, not a one-shot generator.

🛠 Tech Stack

Python 3.10+

Typer (CLI framework)

SQLAlchemy ORM

MySQL

Sentence Transformers

Vector Store (Chroma)

OpenAI / LLM API

HuggingFace embeddings

📁 Project Structure
coach/
│
├── main.py
│
├── db/
│   ├── models.py
│   ├── session.py
│   └── init_db.py
│
├── ai/
│   ├── prompts.py
│   ├── progression.py
│   ├── fatigue.py
│   ├── recovery.py
│   ├── injury.py
│   ├── substitutions.py
│   ├── reflection.py
│   ├── validator.py
│   ├── semantic_validator.py
│   ├── confidence.py
│   └── constraints.py
│
└── memory/
    ├── vector_store.py
    └── embedder.py

⚙️ Setup Guide
1️⃣ Clone the Repository
git clone https://github.com/your-username/gen-ai-gym-coach.git
cd gen-ai-gym-coach

2️⃣ Create Virtual Environment
python -m venv venv


Activate:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in root:

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/gym_coach
OPENAI_API_KEY=your_api_key_here


Replace:

username

password

gym_coach

your_api_key_here

5️⃣ Initialize Database
python -m coach.db.init_db


This creates:

user_profile

workout_plan

training_outcome

🖥 How to Run

All commands are CLI-based.

👤 Onboard a New User
python -m coach.main onboard

🏋️ Generate Workout Plan
python -m coach.main plan


Includes:

Memory retrieval

Fatigue modeling

Constraint enforcement

Semantic validation

Self-reflection

Vector storage

💬 Submit Workout Feedback
python -m coach.main feedback


Options:

1 → Easy

2 → Good

3 → Hard

🩹 Record Injury
python -m coach.main injury

📊 Record Training Outcome
python -m coach.main outcome

📜 View Workout History
python -m coach.main history

🧠 Why This Project Is Impressive

This is not a basic LLM wrapper.

It demonstrates:

Multi-stage LLM pipelines

AI validation architecture

Guardrail enforcement

Memory-augmented generation

Outcome-driven adaptation

Human-in-the-loop feedback modeling

Confidence estimation systems

This reflects real-world AI system design, not tutorial-level prompt engineering.

🔮 Future Enhancements

Web dashboard (FastAPI + React)

Reinforcement-style weight progression

Analytics visualization

Dockerized deployment

Cloud-hosted API

Multi-user scaling