# 🧠 GenAI Gym Coach  

**GenAI Gym Coach** is a CLI-based AI-powered workout planning system built with Python.  

It generates personalized workout programs based on user goals and experience level, adapts to injuries and fatigue, validates plans with safety constraints, stores semantic memory using embeddings, and learns from real-world training outcomes.

---

# ✨ Features

## 🏋️ Intelligent Workout Generation
- Goal-based planning (muscle_gain / fat_loss)
- Experience-aware logic (beginner / intermediate / advanced)
- Progressive overload strategy
- Recovery-aware scheduling

## 🩹 Injury Adaptation
- Accepts injury input
- Automatically substitutes risky movements
- Adjusts volume and intensity accordingly

## 🧠 Multi-Layer AI System
- LLM-generated base workout
- Self-reflection refinement pass
- Rule-based validation engine
- Semantic validation layer
- Confidence scoring before finalization

## 📊 Training Feedback & Outcome Tracking
- User feedback (easy / good / hard)
- Fatigue inference
- Adherence tracking
- Progress evaluation (improved / stalled / regressed)
- Long-term learning from results

## 🧬 Semantic Memory
- Vector embedding storage of plans
- Retrieval of similar past plans
- Context-aware future plan generation

---

# 🛠 Tech Stack

- **Python**
- **Typer (CLI framework)**
- **SQLAlchemy**
- **MySQL**
- **Sentence Transformers**
- **Chroma (Vector Store)**
- **OpenAI API**

---

# 🚀 How To Run The Project

---

## 1️⃣ Clone The Repository

```bash
git clone https://github.com/your-username/gen-ai-gym-coach.git
cd gen-ai-gym-coach
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

### Windows
```bash
venv\Scripts\activate
```

### Mac / Linux
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Setup Environment Variables

Create a `.env` file in the root directory and add:

```
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/gym_coach
GROQAI_API_KEY=your_openai_api_key
```

Replace:
- `username`
- `password`
- `gym_coach`
- `your_GROQAI_api_key`

---

## 5️⃣ Initialize The Database

```bash
python -m coach.db.init_db
```

This command creates all required database tables.

---

# 💻 CLI Commands

---

## 👤 Onboard A New User

```bash
python -m coach.main onboard
```

---

## 🏋️ Generate Workout Plan

```bash
python -m coach.main plan
```

---

## 💬 Submit Workout Feedback

```bash
python -m coach.main feedback
```

Options:
- easy  
- good  
- hard  

---

## 🩹 Add Injury Note

```bash
python -m coach.main injury
```

---

## 📊 Record Training Outcome

```bash
python -m coach.main outcome
```

You will be prompted for:
- adherence (full / partial / skipped)
- soreness (none / mild / high)
- progress (improved / stalled / regressed)
- notes (optional)

---

## 📜 View Workout History

```bash
python -m coach.main history
```

---

# 🧠 System Architecture (High-Level)

1. User inputs profile data  
2. System retrieves past plans  
3. Fatigue and injury states are inferred  
4. Semantic memory retrieves similar plans  
5. LLM generates base plan  
6. Self-reflection refines plan  
7. Rule-based validator enforces constraints  
8. Semantic validator checks contextual appropriateness  
9. Confidence layer ensures sufficient information  
10. Final plan stored in SQL + Vector DB  

---

# 🎯 Why This Project Is Different

This is not a basic workout generator.  

It includes:
- Multi-pass LLM reasoning  
- Deterministic rule validation  
- Semantic retrieval memory  
- Confidence-based gating  
- Outcome-driven learning loop  

It behaves closer to an **AI coaching system** than a static plan generator.

---

# 📌 Requirements

- Python 3.10+
- MySQL running locally
- OpenAI API key
- Internet connection (for embeddings & LLM calls)

---

# 📄 License

This project is for educational and portfolio demonstration purposes.

---

**Built as an advanced AI system design project focused on reasoning pipelines, validation layers, and adaptive memory.**
