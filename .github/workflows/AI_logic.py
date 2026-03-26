import json
import os
import google.generativeai as genai

# 🔑 Configure Gemini (use env variable later)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#For api key very simple go to google API and generate API key and copy paste absolutely free
#NO billing is required
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

Return output in STRICT JSON format:
{{
  "questions": ["", "", ""],
  "decision": "",
  "valuation_range": "",
  "reasoning": ""
}}
"""

    response = model.generate_content(prompt)
    return response.text


#  MAIN FUNCTION (Gaurang uses this)

def analyze_startup(pitch: str):
    relevant_data = retrieve_relevant_data(pitch, DATASET)
    context = build_context(relevant_data)

    raw_output = call_ai(pitch, context)

    try:
        return json.loads(raw_output)
    except:
        return {
            "error": "Invalid JSON from AI",
            "raw": raw_output
        }

#from main import analyze_startup
#result = analyze_startup(pitch)
#Put this code in AI and say have to make backend for this.
