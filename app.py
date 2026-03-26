import os
import streamlit as st
from dotenv import load_dotenv
from file_parser_mod.file_parser import extract_text
from scorer.ats_scorer import score_resume
from optimizer.resume_optimizer import optimize_resume
from renderer.pdf_renderer import render_to_pdf

load_dotenv()

st.set_page_config(
    page_title="ResumeIQ · ATS Optimizer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:        #080810;
    --surface:   #0f0f1a;
    --card:      #13131f;
    --border:    #ffffff0d;
    --border-hi: #ffffff1a;
    --text:      #f0f0ff;
    --muted:     #6b6b8a;
    --accent:    #7c6aff;
    --accent2:   #ff6a9b;
    --accent3:   #6affda;
    --green:     #00e5a0;
    --yellow:    #ffc85e;
    --red:       #ff5e7d;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .main, .block-container {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1400px !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── NOISE OVERLAY ── */
body::before {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 0; opacity: 0.4;
}

/* ── HERO ── */
.hero-wrap {
    position: relative;
    padding: 72px 0 56px;
    text-align: center;
    overflow: hidden;
}
.hero-glow {
    position: absolute;
    width: 700px; height: 700px;
    border-radius: 50%;
    background: radial-gradient(circle, #7c6aff18 0%, transparent 70%);
    top: -200px; left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
}
.hero-label {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--accent);
    border: 1px solid #7c6aff30;
    background: #7c6aff0a;
    padding: 5px 16px;
    border-radius: 999px;
    margin-bottom: 24px;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #f0f0ff 0%, #a89bff 40%, #ff6a9b 80%, #6affda 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 18px;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── CARDS ── */
.glass-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.glass-card:hover { border-color: var(--border-hi); }
.glass-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #ffffff03 0%, transparent 60%);
    pointer-events: none;
}

.card-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── STEP BADGE ── */
.step-num {
    width: 26px; height: 26px;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: white;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    flex-shrink: 0;
}

/* ── SCORE RING ── */
.score-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 20px 24px;
}
.score-ring-container {
    position: relative;
    width: 160px; height: 160px;
    margin-bottom: 20px;
}
.score-ring-container svg { transform: rotate(-90deg); }
.score-center {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.score-num {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
}
.score-denom {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 2px;
}
.score-status {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    margin-bottom: 8px;
}
.score-gap {
    color: var(--muted);
    font-size: 0.8rem;
    text-align: center;
    line-height: 1.6;
    max-width: 280px;
}

/* ── METRIC BARS ── */
.metric-item {
    margin-bottom: 14px;
}
.metric-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}
.metric-name {
    font-size: 0.8rem;
    color: var(--muted);
}
.metric-val {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: var(--text);
    font-weight: 500;
}
.bar-track {
    height: 4px;
    background: #ffffff08;
    border-radius: 999px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 1s ease;
}

/* ── TAGS ── */
.tags-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
.tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid;
    letter-spacing: 0.02em;
}
.tag-miss { color: var(--red);   border-color: #ff5e7d30; background: #ff5e7d08; }
.tag-have { color: var(--green); border-color: #00e5a030; background: #00e5a008; }

/* ── LIST ITEMS ── */
.list-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 9px 12px;
    border-radius: 10px;
    margin-bottom: 6px;
    font-size: 0.82rem;
    line-height: 1.5;
}
.list-strength { background: #00e5a008; color: #a7f3d0; border-left: 2px solid var(--green); }
.list-improve  { background: #ffc85e08; color: #fde68a; border-left: 2px solid var(--yellow); }
.list-icon { flex-shrink: 0; margin-top: 1px; }

/* ── EMPTY STATE ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px;
    text-align: center;
}
.empty-icon {
    width: 72px; height: 72px;
    border-radius: 20px;
    background: linear-gradient(135deg, #7c6aff15, #ff6a9b15);
    border: 1px solid #7c6aff20;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    margin-bottom: 20px;
}
.empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
}
.empty-sub { color: var(--muted); font-size: 0.85rem; line-height: 1.6; }

/* ── DIVIDER ── */
.divider { height: 1px; background: var(--border); margin: 20px 0; }

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stTextArea"] label { display: none; }
div[data-testid="stTextArea"] textarea {
    background: #0a0a14 !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    resize: none !important;
    padding: 14px !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px #7c6aff15 !important;
}

div[data-testid="stFileUploader"] {
    background: #0a0a14 !important;
    border: 1px dashed var(--border-hi) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}
div[data-testid="stFileUploader"] label { display: none !important; }
div[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
}
div[data-testid="stFileUploader"] button {
    background: #7c6aff15 !important;
    color: var(--accent) !important;
    border: 1px solid #7c6aff30 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 8px 32px #7c6aff25 !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 12px 40px #7c6aff40 !important;
}

div[data-testid="stDownloadButton"] > button {
    background: #00e5a010 !important;
    color: var(--green) !important;
    border: 1px solid #00e5a030 !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #00e5a018 !important;
    box-shadow: 0 0 24px #00e5a020 !important;
}

div[data-testid="stSelectbox"] label { display: none !important; }
div[data-testid="stSelectbox"] > div > div {
    background: #0a0a14 !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stSpinner"] { color: var(--accent) !important; }

.stAlert { border-radius: 12px !important; }

/* column gap */
div[data-testid="column"] { padding: 0 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-glow"></div>
    <div class="hero-label">AI-Powered Resume Intelligence</div>
    <div class="hero-title">ResumeIQ</div>
    <div class="hero-sub">Drop your resume. Paste a job description.<br>Get your ATS score and an optimized version — instantly.</div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ────────────────────────────────────────────────────────────────────
left, right = st.columns([5, 7], gap="medium")

with left:
    # JD input
    st.markdown("""
    <div class="glass-card">
        <div class="card-label"><span class="step-num">1</span> Job Description</div>
    </div>
    """, unsafe_allow_html=True)
    jd_text = st.text_area("jd", placeholder="Paste the full job description here…", height=200, label_visibility="collapsed")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Resume upload
    st.markdown("""
    <div class="glass-card">
        <div class="card-label"><span class="step-num">2</span> Your Resume</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("resume", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    if uploaded_file:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;padding:10px 14px;
                    background:#00e5a008;border:1px solid #00e5a025;border-radius:10px;margin-top:8px;">
            <span style="color:var(--green);font-size:1rem;">✓</span>
            <span style="color:#a7f3d0;font-size:0.82rem;font-family:'DM Mono',monospace;">{uploaded_file.name}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze Resume")

# ── RESULTS ──────────────────────────────────────────────────────────────────
with right:
    if analyze_btn:
        if not jd_text.strip():
            st.error("Please paste a Job Description first.")
        elif not uploaded_file:
            st.error("Please upload your resume file.")
        else:
            with st.spinner("Running ATS analysis…"):
                os.makedirs("output", exist_ok=True)
                file_path = f"output/ui_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())

                try:
                    resume_text = extract_text(file_path)
                    result = score_resume(resume_text, jd_text)
                    score = result["total_score"]

                    if score >= 75:
                        ring_color = "#00e5a0"
                        status_text = "Strong Match"
                        status_color = "#00e5a0"
                    elif score >= 55:
                        ring_color = "#ffc85e"
                        status_text = "Partial Match"
                        status_color = "#ffc85e"
                    else:
                        ring_color = "#ff5e7d"
                        status_text = "Needs Work"
                        status_color = "#ff5e7d"

                    circumference = 2 * 3.14159 * 60
                    dash = (score / 100) * circumference

                    # Score ring
                    st.markdown(f"""
                    <div class="glass-card">
                        <div class="card-label">Overall Score</div>
                        <div class="score-wrap">
                            <div class="score-ring-container">
                                <svg width="160" height="160" viewBox="0 0 160 160">
                                    <circle cx="80" cy="80" r="60" fill="none" stroke="#ffffff08" stroke-width="10"/>
                                    <circle cx="80" cy="80" r="60" fill="none" stroke="{ring_color}"
                                        stroke-width="10" stroke-linecap="round"
                                        stroke-dasharray="{dash:.1f} {circumference:.1f}"
                                        style="filter:drop-shadow(0 0 8px {ring_color}60)"/>
                                </svg>
                                <div class="score-center">
                                    <div class="score-num" style="color:{ring_color}">{score}</div>
                                    <div class="score-denom">/ 100</div>
                                </div>
                            </div>
                            <div class="score-status" style="color:{status_color}">{status_text}</div>
                            <div class="score-gap">{result.get('gap_message','')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Metrics
                    metrics = [
                        ("Keyword Match",   result.get("keyword_score", 0)),
                        ("Role Alignment",  result.get("role_alignment_score", 0)),
                        ("Format Score",    result.get("format_score", 0)),
                        ("Action Verbs",    result.get("action_verb_score", 0)),
                        ("Quantification",  result.get("quantification_score", 0)),
                    ]
                    metrics_html = '<div class="glass-card"><div class="card-label">Score Breakdown</div>'
                    for name, val in metrics:
                        metrics_html += f"""
                        <div class="metric-item">
                            <div class="metric-top">
                                <span class="metric-name">{name}</span>
                                <span class="metric-val">{val}</span>
                            </div>
                            <div class="bar-track">
                                <div class="bar-fill" style="width:{val}%"></div>
                            </div>
                        </div>"""
                    metrics_html += '</div>'
                    st.markdown(metrics_html, unsafe_allow_html=True)

                    # Keywords
                    c1, c2 = st.columns(2)
                    with c1:
                        present = result.get("present_keywords", [])[:10]
                        tags = "".join([f'<span class="tag tag-have">{k}</span>' for k in present])
                        st.markdown(f'<div class="glass-card"><div class="card-label">Present Keywords</div><div class="tags-wrap">{tags}</div></div>', unsafe_allow_html=True)
                    with c2:
                        missing = result.get("missing_keywords", [])[:10]
                        tags = "".join([f'<span class="tag tag-miss">{k}</span>' for k in missing])
                        st.markdown(f'<div class="glass-card"><div class="card-label">Missing Keywords</div><div class="tags-wrap">{tags}</div></div>', unsafe_allow_html=True)

                    # Strengths & Improvements
                    c3, c4 = st.columns(2)
                    with c3:
                        items = "".join([f'<div class="list-item list-strength"><span class="list-icon">✦</span>{s}</div>' for s in result.get("strengths", [])])
                        st.markdown(f'<div class="glass-card"><div class="card-label">Strengths</div>{items}</div>', unsafe_allow_html=True)
                    with c4:
                        items = "".join([f'<div class="list-item list-improve"><span class="list-icon">→</span>{i}</div>' for i in result.get("improvements", [])])
                        st.markdown(f'<div class="glass-card"><div class="card-label">Improvements</div>{items}</div>', unsafe_allow_html=True)

                    # Download
                    st.markdown('<div class="glass-card"><div class="card-label">Download Optimized Resume</div>', unsafe_allow_html=True)
                    fmt_choice = st.selectbox("fmt", ["Single Page", "Two Page", "ATS Plain", "Executive"], label_visibility="collapsed")
                    fmt_map = {"Single Page": "single_page", "Two Page": "two_page", "ATS Plain": "ats_plain", "Executive": "executive"}

                    with st.spinner("Generating optimized resume…"):
                        gaps = result.get("missing_keywords", [])
                        optimized = optimize_resume(resume_text, jd_text, gaps)
                        pdf_path = render_to_pdf(optimized, "output/ui_optimized.pdf", template=fmt_map[fmt_choice])

                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "⬇ Download Optimized Resume",
                            data=f,
                            file_name="optimized_resume.pdf",
                            mime="application/pdf"
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.markdown("""
        <div class="glass-card">
            <div class="empty-state">
                <div class="empty-title">Ready to analyze</div>
                <div class="empty-sub">Paste your job description,<br>upload your resume, and hit Analyze.<br><br>Your full ATS report will appear here.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)