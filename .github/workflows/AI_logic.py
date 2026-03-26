import json
import os
import google.generativeai as genai


genai.configure(api_key="AIzaSyBS_xWJR2_5tbaT-Rn5s2xY-WLmBNMm5k8")

model = genai.GenerativeModel("gemini-2.5-flash")


# 📂 Load dataset ONCE
with open("dataset.json", "r") as file:
    DATASET = json.load(file)


# 🔍 RAG retrieval
def retrieve_relevant_data(pitch, dataset):
    pitch = pitch.lower()
    relevant = []

    for data in dataset:
        if data["sector"] in pitch:
            relevant.append(data)

    if not relevant:
        relevant = dataset[:2]

    return relevant[:2]  # limit


# 🧩 Build context
def build_context(relevant_data):
    context = "Past Shark Tank Cases:\n"

    for d in relevant_data:
        context += (
            f"- {d['startup']} | Sector: {d['sector']} | "
            f"Revenue: {d['revenue']} | Ask: {d['ask']} | "
            f"Outcome: {d['outcome']}\n"
        )

    return context


# 🤖 AI call
def call_ai(pitch, context):
    prompt = f"""
You are a Shark Tank investor.

Be brutally honest. No fluff. Keep answers concise.

Startup Pitch:
{pitch}

{context}

Tasks:
1. Ask exactly 3 tough questions
2. Give investment decision (YES or NO)
3. Estimate fair valuation (in ₹ crore)
4. Give reasoning using BOTH:
   - current startup numbers
   - past cases

Return output in EXACTLY this format:

Startup: <name>
Decision: <invest/pass>
Score: <0-10>

Strengths:
- point 1
- point 2
- point 3

Weaknesses:
- point 1
- point 2
- point 3

Risks:
- point 1
- point 2
- point 3

Valuation:
<short comment>

Final Verdict:
<sharp reasoning>

Rules:
- Follow this format EXACTLY
- No extra text before or after
- Keep it clean and readable
"""

    response = model.generate_content(prompt)
    return response.text


# 🧠 MAIN FUNCTION 
def analyze_startup(pitch: str):
    relevant_data = retrieve_relevant_data(pitch, DATASET)
    context = build_context(relevant_data)

    raw_output = call_ai(pitch, context)

    
    return raw_output
    
