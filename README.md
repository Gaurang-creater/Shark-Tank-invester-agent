# 🦈 AI Shark Tank Investor Agent

> An AI system that analyzes startup pitches and responds like a Shark Tank investor.
> Built with **Google Gemini API** (free tier) + **Retrieval-Augmented Generation (RAG)** + **Streamlit**.

---

## 📁 Project Structure

```
shark_ai_project/
├── main.py          ← Backend: RAG pipeline + Gemini API logic
├── app.py           ← Frontend: Streamlit UI
├── dataset.json     ← 15 historical startup cases (RAG knowledge base)
├── requirements.txt ← Python dependencies
├── .env             ← Your Gemini API key (fill this in)
└── README.md        ← This file
```

---

## ⚡ Quick Start

### Step 1 — Get a Free Gemini API Key

1. Go to → https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key

### Step 2 — Set Up the Project

```bash
# Navigate to the project folder
cd shark_ai_project

# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3 — Add Your API Key

Open `.env` and replace `your_api_key_here`:

```
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

### Step 4 — Run the App

```bash
streamlit run app.py
```

The app will open at → **http://localhost:8501**

---

## 🧪 Test the Backend Alone

```bash
python main.py
```

This runs a sample pitch through the full pipeline and prints the JSON output.

---

## 🏗️ Architecture — How RAG Works Here

```
User Pitch
    │
    ▼
┌─────────────────────────────────┐
│  RETRIEVAL (RAG Step)           │
│  • Detect sector from pitch     │
│  • Match against dataset.json   │
│  • Return top 3 similar cases   │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  CONTEXT CONSTRUCTION           │
│  • Format cases into text block │
│  • Include revenue, outcome,    │
│    metrics, red flags           │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  GEMINI LLM REASONING           │
│  • System persona: Shark Tank   │
│  • Pitch + context in prompt    │
│  • Enforced JSON output schema  │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  STRUCTURED JSON OUTPUT         │
│  • 3 tough investor questions   │
│  • Investment decision YES/NO   │
│  • Valuation range (₹ crore)    │
│  • Grounded reasoning           │
└─────────────────────────────────┘
```

---

## 📊 Dataset

`dataset.json` contains 15 startup cases across:

| Sector     | Examples                          |
|------------|-----------------------------------|
| Food       | FreshKart, TiffinBox              |
| HealthTech | MediLink, NeuroCare               |
| AgriTech   | AgroSmart, GreenField             |
| EdTech     | EduLeap, CodeMentor               |
| FinTech    | LoanDost, SafeHome                |
| EV         | CleanCharge                       |
| HRTech     | QuickHire                         |
| Fashion    | StyleDNA                          |
| CleanTech  | WasteWise                         |
| Fitness    | UrbanFit                          |

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `GEMINI_API_KEY not found` | Check your `.env` file is in the same folder as `main.py` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `JSON parse error` | Retry — Gemini occasionally returns malformed JSON; the app has a fallback |
| `quota exceeded` | Free tier has limits; wait a minute and retry |

---

## 🎓 Academic Concepts Demonstrated

- **RAG (Retrieval-Augmented Generation)** — grounding LLM responses with a local dataset
- **LLM Prompting** — persona injection, schema enforcement, few-shot context
- **AI Agent Workflow** — multi-step pipeline: retrieve → build → reason → output
- **Structured Output** — enforcing JSON schema from an unstructured LLM

---

*Built for college AI course project presentation.*
