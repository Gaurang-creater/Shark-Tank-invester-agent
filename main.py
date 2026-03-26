"""
main.py — AI Shark Tank Investor Agent Backend
Uses Retrieval-Augmented Generation (RAG) with Google Gemini API
"""

import json
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# ─────────────────────────────────────────────
# 1. CONFIGURATION
# ─────────────────────────────────────────────
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError(
        "❌ GEMINI_API_KEY not found. Please set it in your .env file."
    )

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")   # free-tier model

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.json")


# ─────────────────────────────────────────────
# 2. LOAD DATASET
# ─────────────────────────────────────────────
def load_dataset() -> list[dict]:
    """Load the startup cases from dataset.json."""
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} startup cases from dataset.")
        return data
    except FileNotFoundError:
        print("⚠️  dataset.json not found. Using empty dataset.")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️  Invalid JSON in dataset.json: {e}")
        return []


# ─────────────────────────────────────────────
# 3. RETRIEVAL — Find Similar Cases (RAG Step)
# ─────────────────────────────────────────────
SECTOR_KEYWORDS: dict[str, list[str]] = {
    "food":       ["food", "restaurant", "grocery", "delivery", "meal", "kitchen", "tiffin", "cafe", "snack"],
    "healthtech": ["health", "medical", "doctor", "hospital", "diagnostic", "medicine", "clinic", "mental", "wellness"],
    "fitness":    ["fitness", "gym", "workout", "exercise", "yoga", "sport", "training"],
    "agritech":   ["agri", "farm", "crop", "soil", "agriculture", "harvest", "irrigation", "organic"],
    "edtech":     ["edu", "learn", "course", "school", "college", "student", "tutor", "coaching", "skill"],
    "hrtech":     ["hr", "hire", "recruit", "talent", "employee", "resume", "job", "workforce"],
    "ev":         ["ev", "electric vehicle", "charging", "battery", "mobility", "e-scooter", "e-bike"],
    "fintech":    ["finance", "loan", "payment", "insurance", "banking", "credit", "invest", "wallet", "lending"],
    "fashion":    ["fashion", "clothing", "apparel", "style", "outfit", "wardrobe", "beauty", "cosmetic"],
    "cleantech":  ["clean", "waste", "recycl", "green", "solar", "environment", "carbon", "sustainable"],
}


def detect_sector(pitch: str) -> str:
    """
    Detect the primary sector from the pitch text using keyword matching.
    Returns the best-matching sector name or 'general'.
    """
    pitch_lower = pitch.lower()
    scores: dict[str, int] = {}

    for sector, keywords in SECTOR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in pitch_lower)
        if score > 0:
            scores[sector] = score

    if not scores:
        return "general"
    return max(scores, key=scores.get)


def retrieve_similar_cases(pitch: str, dataset: list[dict], top_k: int = 3) -> list[dict]:
    """
    RAG Retrieval Step:
    Match pitch to historical startup cases using sector detection.
    Returns top_k most relevant cases.
    """
    detected_sector = detect_sector(pitch)
    print(f"🔍 Detected sector: {detected_sector}")

    # Primary match: same sector
    matched = [s for s in dataset if s.get("sector", "").lower() == detected_sector]

    # Fallback: if fewer than top_k found, pad with other cases
    if len(matched) < top_k:
        others = [s for s in dataset if s not in matched]
        matched += others[: top_k - len(matched)]

    return matched[:top_k]


# ─────────────────────────────────────────────
# 4. CONTEXT CONSTRUCTION
# ─────────────────────────────────────────────
def build_context(cases: list[dict]) -> str:
    """
    Format retrieved startup cases into a readable context block
    that Gemini can use to ground its reasoning.
    """
    if not cases:
        return "No historical cases found for this sector."

    lines = ["📂 HISTORICAL STARTUP CASES (for reference):\n"]
    for i, c in enumerate(cases, 1):
        outcome_label = "✅ DEAL" if c.get("outcome") == "deal" else "❌ NO DEAL"
        lines.append(
            f"Case {i}: {c.get('startup_name', 'Unknown')} ({outcome_label})\n"
            f"  Sector       : {c.get('sector', 'N/A')}\n"
            f"  Description  : {c.get('description', 'N/A')}\n"
            f"  Revenue      : ₹{c.get('revenue_inr_crore', 'N/A')} crore\n"
            f"  Ask          : ₹{c.get('ask_inr_crore', 'N/A')} crore "
            f"for {c.get('equity_offered_percent', 'N/A')}% equity\n"
            f"  Valuation    : ₹{c.get('valuation_inr_crore', 'N/A')} crore\n"
            f"  Key Metric   : {c.get('key_metric', 'N/A')}\n"
            f"  Red Flag     : {c.get('red_flag', 'N/A')}\n"
        )
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 5. PROMPT CONSTRUCTION
# ─────────────────────────────────────────────
SYSTEM_PERSONA = """You are a seasoned Shark Tank India investor with 20+ years of experience.
You have backed over 50 startups and have a sharp eye for business potential.
You are direct, analytical, and data-driven. You ask tough but fair questions.
Your decisions are based on: market size, revenue traction, unit economics,
defensibility, founder credibility, and comparable deals.
You always respond in INR (₹ crore) for valuations."""

JSON_SCHEMA = """{
  "investor_questions": [
    "Question 1 here",
    "Question 2 here",
    "Question 3 here"
  ],
  "investment_decision": "YES" or "NO",
  "valuation_range": {
    "low": <number in crore>,
    "high": <number in crore>,
    "currency": "INR crore"
  },
  "reasoning": "Detailed 3-5 sentence reasoning referencing both the pitch and historical cases."
}"""


def build_prompt(pitch: str, context: str) -> str:
    """Build the full prompt to send to Gemini."""
    return f"""{SYSTEM_PERSONA}

---

{context}

---

🚀 NEW STARTUP PITCH TO EVALUATE:

{pitch}

---

TASK:
Analyze this startup pitch like a Shark Tank investor. Use the historical cases above to calibrate your judgment.

Respond with ONLY a valid JSON object matching this exact schema (no markdown, no extra text):

{JSON_SCHEMA}

Rules:
- investor_questions: exactly 3 tough, specific questions an investor would ask
- investment_decision: exactly "YES" or "NO"
- valuation_range: realistic low and high in ₹ crore based on revenue multiples seen in similar cases
- reasoning: must reference at least one historical case by name
"""


# ─────────────────────────────────────────────
# 6. GEMINI API CALL
# ─────────────────────────────────────────────
def call_gemini(prompt: str) -> str:
    """
    Send the prompt to Gemini and return raw text response.
    """
    generation_config = genai.types.GenerationConfig(
        temperature=0.4,       # slightly creative but mostly deterministic
        max_output_tokens=1024,
    )
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )
    return response.text.strip()


# ─────────────────────────────────────────────
# 7. JSON PARSING WITH FALLBACK
# ─────────────────────────────────────────────
def parse_json_response(raw: str) -> dict:
    """
    Attempt to parse Gemini's response as JSON.
    Handles common issues like markdown code fences.
    """
    # Strip markdown code fences if present
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()

    # Try to extract JSON object if there's surrounding text
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parse error: {e}")
        print(f"Raw response was:\n{raw}\n")
        # Return a structured error response so the UI doesn't crash
        return {
            "investor_questions": [
                "What is your current Monthly Recurring Revenue (MRR)?",
                "How do you plan to achieve profitability in the next 18 months?",
                "Who are your top 3 competitors and what is your moat against them?"
            ],
            "investment_decision": "NO",
            "valuation_range": {
                "low": 0,
                "high": 0,
                "currency": "INR crore"
            },
            "reasoning": (
                "⚠️ Analysis could not be fully generated due to a formatting error "
                "in the AI response. Please try again with a more detailed pitch. "
                f"Raw response snippet: {raw[:200]}..."
            )
        }


# ─────────────────────────────────────────────
# 8. MAIN AGENT FUNCTION
# ─────────────────────────────────────────────
def analyze_startup(pitch: str) -> dict:
    """
    Full RAG + LLM pipeline:
    1. Retrieve similar historical cases
    2. Build context
    3. Build prompt
    4. Call Gemini
    5. Parse and return structured JSON
    
    Args:
        pitch (str): The startup pitch text from the user.
    
    Returns:
        dict: Structured JSON with questions, decision, valuation, and reasoning.
    """
    if not pitch or not pitch.strip():
        return {
            "investor_questions": [],
            "investment_decision": "NO",
            "valuation_range": {"low": 0, "high": 0, "currency": "INR crore"},
            "reasoning": "❌ No pitch was provided. Please describe your startup."
        }

    print("\n" + "="*60)
    print("🦈 AI SHARK TANK INVESTOR AGENT — Processing Pitch")
    print("="*60)

    # Step 1: Load dataset
    dataset = load_dataset()

    # Step 2: Retrieve relevant historical cases (RAG)
    similar_cases = retrieve_similar_cases(pitch, dataset, top_k=3)
    print(f"📋 Retrieved {len(similar_cases)} similar cases: "
          f"{[c.get('startup_name') for c in similar_cases]}")

    # Step 3: Build context
    context = build_context(similar_cases)

    # Step 4: Build prompt
    prompt = build_prompt(pitch, context)
    print("📡 Sending prompt to Gemini...")

    # Step 5: Call Gemini
    raw_response = call_gemini(prompt)
    print("✅ Received response from Gemini.")
    print(f"📝 Raw response:\n{raw_response}\n")

    # Step 6: Parse JSON
    result = parse_json_response(raw_response)

    # Step 7: Attach metadata for UI
    result["retrieved_cases"] = [
        {
            "name": c.get("startup_name"),
            "sector": c.get("sector"),
            "outcome": c.get("outcome"),
            "revenue": c.get("revenue_inr_crore"),
            "valuation": c.get("valuation_inr_crore"),
        }
        for c in similar_cases
    ]

    print("🎯 Analysis complete!")
    return result


# ─────────────────────────────────────────────
# 9. STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    sample_pitch = """
    My startup is called QuickDoc. We are a healthtech company building an AI-powered 
    telemedicine platform that connects patients in rural India to verified doctors within 
    5 minutes. We currently have 12,000 monthly active users, 150 partner doctors, and 
    generate ₹1.5 crore in annual revenue through consultation fees. 
    We are asking for ₹4 crore for 12% equity. Our technology uses NLP to triage 
    patients and recommend the right specialist, reducing misdiagnosis by 40%.
    """

    result = analyze_startup(sample_pitch)
    print("\n📊 FINAL STRUCTURED OUTPUT:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
