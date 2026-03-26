"""
app.py — AI Shark Tank Investor Agent — Streamlit Frontend
A polished UI for presenting the project at college.
"""

import streamlit as st
import json
from main import analyze_startup

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Shark Tank Investor",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Shark Tank Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* ── Header ── */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 50%, #0d0d1a 100%);
    border-radius: 16px;
    border: 1px solid #2a1f4a;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 50% 50%, rgba(99, 55, 255, 0.08) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.8rem;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #ffffff 0%, #a78bfa 50%, #6337ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1;
}
.hero-subtitle {
    font-size: 1rem;
    color: #8b7fc7;
    margin-top: 0.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 500;
}
.hero-badge {
    display: inline-block;
    background: rgba(99, 55, 255, 0.15);
    border: 1px solid rgba(99, 55, 255, 0.4);
    color: #a78bfa;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 0.8rem;
    font-weight: 600;
}

/* ── Input Area ── */
.stTextArea textarea {
    background-color: #12121f !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 1rem !important;
    transition: border-color 0.2s ease;
}
.stTextArea textarea:focus {
    border-color: #6337ff !important;
    box-shadow: 0 0 0 2px rgba(99, 55, 255, 0.15) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #6337ff 0%, #9b59ff 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2.5rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(99, 55, 255, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(99, 55, 255, 0.5) !important;
}

/* ── Cards ── */
.card {
    background: #12121f;
    border-radius: 14px;
    border: 1px solid #1e1e36;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: #3a2a6a; }

.card-title {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #6b6b9a;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

/* ── Decision Banner ── */
.decision-yes {
    background: linear-gradient(135deg, #0d2b1a, #0d3a1f);
    border: 2px solid #22c55e;
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
}
.decision-no {
    background: linear-gradient(135deg, #2b0d0d, #3a0d0d);
    border: 2px solid #ef4444;
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
}
.decision-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    letter-spacing: 4px;
    line-height: 1;
}
.decision-sub {
    font-size: 0.85rem;
    color: #8b8baa;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ── Question Cards ── */
.question-item {
    background: #0f0f1e;
    border-left: 3px solid #6337ff;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.95rem;
    line-height: 1.5;
    color: #c8c8e8;
}
.question-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    color: #6337ff;
    letter-spacing: 1px;
    display: block;
    margin-bottom: 0.3rem;
}

/* ── Valuation ── */
.valuation-block {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
}
.val-box {
    flex: 1;
    background: #0f0f1e;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.val-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2px; color: #6b6b9a; }
.val-amount { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; color: #a78bfa; letter-spacing: 1px; }
.val-unit { font-size: 0.7rem; color: #8b7fc7; text-transform: uppercase; }

/* ── Historical Cases ── */
.case-chip {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px 4px 3px 0;
    letter-spacing: 0.5px;
}
.case-deal { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.case-nodeal { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.25); }

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a1f4a, transparent);
    margin: 1.5rem 0;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6337ff !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0d0d1a !important;
    border-right: 1px solid #1e1e36 !important;
}

/* ── Label styles ── */
.stTextArea label {
    color: #8b7fc7 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🦈 AI SHARK TANK</div>
    <div class="hero-subtitle">Investor Intelligence Agent</div>
    <div class="hero-badge">⚡ Powered by Gemini + RAG</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown("""
    <div class="card-title" style="margin-bottom: 0.4rem;">🎯 YOUR STARTUP PITCH</div>
    """, unsafe_allow_html=True)

    pitch_text = st.text_area(
        label="Your Startup Pitch",
        placeholder=(
            "Describe your startup here...\n\n"
            "Include:\n"
            "• What your product/service does\n"
            "• Your target market\n"
            "• Current revenue & traction\n"
            "• How much funding you're seeking and for what equity\n"
            "• What makes you different from competitors\n\n"
            "Example: 'My startup EcoRide is an EV two-wheeler rental platform...'"
        ),
        height=280,
        label_visibility="collapsed",
    )

    analyze_btn = st.button("🦈 Analyze My Startup", use_container_width=True)

    # ── Architecture Info Card ──
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="card-title">⚙️ How It Works — RAG Pipeline</div>
        <div style="font-size:0.85rem; line-height:1.8; color:#8b8baa;">
            <span style="color:#a78bfa; font-weight:600;">1. Pitch Input</span> → You describe your startup<br>
            <span style="color:#a78bfa; font-weight:600;">2. Retrieval</span> → System finds similar historical cases<br>
            <span style="color:#a78bfa; font-weight:600;">3. Context Build</span> → Cases are formatted as reference<br>
            <span style="color:#a78bfa; font-weight:600;">4. Gemini Reasoning</span> → LLM acts as Shark Tank investor<br>
            <span style="color:#a78bfa; font-weight:600;">5. Structured Output</span> → JSON → Clean UI display
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">📚 Dataset Coverage</div>
        <div style="font-size: 0.82rem; color: #8b8baa; line-height: 1.7;">
            <span style="color:#e8e8f0;">15 startup cases</span> across sectors:<br>
            🍔 Food &nbsp;|&nbsp; 🏥 HealthTech &nbsp;|&nbsp; 🌱 AgriTech<br>
            📚 EdTech &nbsp;|&nbsp; 💰 FinTech &nbsp;|&nbsp; ⚡ EV/CleanTech<br>
            👗 Fashion &nbsp;|&nbsp; 💼 HRTech &nbsp;|&nbsp; 🏋️ Fitness
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RESULTS PANEL
# ─────────────────────────────────────────────
with right_col:
    # Default placeholder state
    if not analyze_btn:
        st.markdown("""
        <div style="
            height: 420px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #0d0d1a;
            border: 1px dashed #2a1f4a;
            border-radius: 14px;
            text-align: center;
            padding: 2rem;
        ">
            <div style="font-size:3.5rem; margin-bottom:1rem;">🦈</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; 
                        letter-spacing:3px; color:#3a2a6a;">
                AWAITING YOUR PITCH
            </div>
            <div style="font-size:0.85rem; color:#4a3a7a; margin-top:0.5rem;
                        max-width: 300px; line-height:1.6;">
                Enter your startup pitch on the left and hit<br>
                <strong style="color:#6337ff;">Analyze My Startup</strong> to get an AI investor decision
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Analysis Flow ──
    if analyze_btn:
        if not pitch_text or not pitch_text.strip():
            st.markdown("""
            <div style="background:#1a0a0a; border:1px solid #7f1d1d; border-radius:12px;
                        padding:1.2rem; color:#fca5a5; text-align:center;">
                ⚠️ <strong>Please enter your startup pitch</strong> before clicking Analyze.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🦈  The Shark is reviewing your pitch..."):
                try:
                    result = analyze_startup(pitch_text)
                except Exception as e:
                    st.markdown(f"""
                    <div style="background:#1a0a0a; border:1px solid #7f1d1d;
                                border-radius:12px; padding:1.2rem; color:#fca5a5;">
                        ❌ <strong>Error:</strong> {str(e)}<br><br>
                        <span style="font-size:0.85rem;">
                        Please check your <code>.env</code> file and ensure 
                        <code>GEMINI_API_KEY</code> is set correctly.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.stop()

            # ── 1. INVESTMENT DECISION ──
            decision = result.get("investment_decision", "NO").upper()
            if decision == "YES":
                st.markdown("""
                <div class="decision-yes">
                    <div class="decision-label" style="color:#22c55e;">✅ I'M IN — DEAL!</div>
                    <div class="decision-sub">The Shark wants to invest</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="decision-no">
                    <div class="decision-label" style="color:#ef4444;">❌ I'M OUT — NO DEAL</div>
                    <div class="decision-sub">The Shark passed on this opportunity</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

            # ── 2. VALUATION RANGE ──
            val = result.get("valuation_range", {})
            low = val.get("low", 0)
            high = val.get("high", 0)
            currency = val.get("currency", "INR crore")

            st.markdown(f"""
            <div class="card">
                <div class="card-title">💰 Estimated Valuation Range</div>
                <div class="valuation-block">
                    <div class="val-box">
                        <div class="val-label">Conservative</div>
                        <div class="val-amount">₹{low}</div>
                        <div class="val-unit">{currency}</div>
                    </div>
                    <div style="display:flex;align-items:center;color:#4a3a7a;
                                font-size:1.5rem;font-weight:300;">—</div>
                    <div class="val-box">
                        <div class="val-label">Optimistic</div>
                        <div class="val-amount">₹{high}</div>
                        <div class="val-unit">{currency}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── 3. INVESTOR QUESTIONS ──
            questions = result.get("investor_questions", [])
            if questions:
                st.markdown("""
                <div class="card">
                    <div class="card-title">🔥 Tough Investor Questions</div>
                """, unsafe_allow_html=True)
                for i, q in enumerate(questions[:3], 1):
                    st.markdown(f"""
                    <div class="question-item">
                        <span class="question-number">Q{i}</span>
                        {q}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # ── 4. REASONING ──
            reasoning = result.get("reasoning", "No reasoning provided.")
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🧠 Investor Reasoning</div>
                <div style="font-size:0.92rem; line-height:1.75; color:#b0b0cc;">
                    {reasoning}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── 5. RETRIEVED CASES ──
            cases = result.get("retrieved_cases", [])
            if cases:
                chips_html = ""
                for c in cases:
                    outcome = c.get("outcome", "unknown")
                    chip_class = "case-deal" if outcome == "deal" else "case-nodeal"
                    icon = "✅" if outcome == "deal" else "❌"
                    name = c.get("name", "Unknown")
                    rev = c.get("revenue", "N/A")
                    chips_html += f"""
                    <span class="case-chip {chip_class}" 
                          title="Revenue: ₹{rev}cr | Valuation: ₹{c.get('valuation','N/A')}cr">
                        {icon} {name}
                    </span>
                    """
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📂 Historical Cases Used for RAG Context</div>
                    <div>{chips_html}</div>
                    <div style="font-size:0.72rem; color:#4a3a7a; margin-top:0.6rem;">
                        Hover over chips to see revenue & valuation details
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── 6. RAW JSON Expander ──
            with st.expander("🔧 View Raw JSON Output (for debugging / demo)"):
                clean_result = {k: v for k, v in result.items() if k != "retrieved_cases"}
                st.code(json.dumps(clean_result, indent=2, ensure_ascii=False), language="json")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#2a1f4a; font-size:0.75rem; 
            padding: 0.5rem 0 1rem; letter-spacing:1px; text-transform:uppercase;">
    🦈 AI Shark Tank Investor Agent &nbsp;|&nbsp; 
    Built with Gemini + RAG &nbsp;|&nbsp; 
    College AI Project
</div>
""", unsafe_allow_html=True)
