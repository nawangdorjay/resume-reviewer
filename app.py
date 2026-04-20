"""
Resume Reviewer — Streamlit Web Interface
Upload your resume, get instant AI-powered analysis with visual scorecards.
"""

import streamlit as st
import tempfile
import json
from pathlib import Path

from reviewer.parser import parse_resume
from reviewer.analyzer import analyze_resume
from reviewer.scorer import score_resume


# ── Page Config ────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Resume Reviewer 📄",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────

st.markdown("""
<style>
    .score-big {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        line-height: 1;
    }
    .score-label {
        text-align: center;
        font-size: 1.1rem;
        color: #888;
        margin-top: -0.5rem;
    }
    .grade-excellent { color: #22c55e; }
    .grade-good { color: #eab308; }
    .grade-needs-work { color: #f97316; }
    .grade-poor { color: #ef4444; }
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .strength { color: #22c55e; }
    .improvement { color: #f97316; }
    div[data-testid="stMetric"] {
        background-color: rgba(28, 131, 225, 0.05);
        border: 1px solid rgba(28, 131, 225, 0.1);
        border-radius: 10px;
        padding: 10px 15px;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────

st.title("📄 AI Resume Reviewer")
st.caption("Upload your resume → get instant scores and improvement suggestions")


# ── File Upload ────────────────────────────────────────────────────

col_upload, col_job = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "doc", "txt"],
        help="Supports PDF, DOCX, and plain text files",
    )

with col_job:
    job_file = st.file_uploader(
        "Job description (optional)",
        type=["pdf", "docx", "doc", "txt"],
        help="Upload a job description for keyword matching",
    )


# ── Analysis ───────────────────────────────────────────────────────

if uploaded_file:
    
    # Save uploaded file to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = Path(tmp.name)
    
    # Parse
    with st.spinner("📄 Parsing resume..."):
        text = parse_resume(tmp_path)
    
    if not text.strip():
        st.error("❌ Could not extract text from this file. Is it corrupted or image-only?")
        st.stop()
    
    # Parse job description
    job_text = ""
    if job_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(job_file.name).suffix) as tmp_j:
            tmp_j.write(job_file.getbuffer())
            job_text = parse_resume(Path(tmp_j.name))
    
    # Analyze
    with st.spinner("🔍 Analyzing your resume..."):
        analysis = analyze_resume(text, job_text)
        scores = score_resume(analysis)
    
    # Cleanup
    tmp_path.unlink(missing_ok=True)
    
    # ── Overall Score ──────────────────────────────────────────────
    
    overall = scores["overall"]
    
    if overall >= 80:
        grade_class = "grade-excellent"
        grade_text = "🟢 Excellent"
    elif overall >= 65:
        grade_class = "grade-good"
        grade_text = "🟡 Good"
    elif overall >= 50:
        grade_class = "grade-needs-work"
        grade_text = "🟠 Needs Work"
    else:
        grade_class = "grade-poor"
        grade_text = "🔴 Needs Major Improvement"
    
    st.markdown("---")
    
    col_score, col_empty = st.columns([1, 2])
    with col_score:
        st.markdown(
            f'<div class="score-big {grade_class}">{overall}</div>'
            f'<div class="score-label">out of 100</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"<div style='text-align:center;font-size:1.2rem;'>{grade_text}</div>", unsafe_allow_html=True)
    
    # ── Category Breakdown ─────────────────────────────────────────
    
    st.markdown("### 📊 Score Breakdown")
    
    cols = st.columns(3)
    for i, (name, data) in enumerate(scores["categories"].items()):
        with cols[i % 3]:
            score_val = data["score"]
            bar_color = "🟢" if score_val >= 7 else ("🟡" if score_val >= 5 else "🔴")
            st.metric(
                label=f"{bar_color} {name}",
                value=f"{score_val}/10",
                help=data["detail"],
            )
    
    # ── Strengths & Improvements ───────────────────────────────────
    
    st.markdown("---")
    col_s, col_i = st.columns(2)
    
    with col_s:
        if scores["strengths"]:
            st.markdown("### ✅ Strengths")
            for s in scores["strengths"]:
                st.success(s)
    
    with col_i:
        if scores["improvements"]:
            st.markdown("### ⚠️ Improvements")
            for imp in scores["improvements"]:
                st.warning(imp)
    
    # ── Detailed Stats ─────────────────────────────────────────────
    
    st.markdown("---")
    st.markdown("### 📈 Detailed Stats")
    
    stat_cols = st.columns(4)
    
    with stat_cols[0]:
        st.metric("📝 Word Count", analysis["length"]["word_count"])
    
    with stat_cols[1]:
        st.metric("📊 Metrics Found", analysis["quantification"]["metric_count"])
    
    with stat_cols[2]:
        st.metric("• Bullet Points", analysis["bullet_points"]["count"])
    
    with stat_cols[3]:
        st.metric("💪 Strong Verbs", analysis["action_verbs"]["strong_count"])
    
    # Contact info
    contact = analysis["contact_info"]
    if contact["missing"]:
        st.warning(f"Missing contact info: **{', '.join(contact['missing'])}**")
    else:
        st.success("✅ All contact info present")
    
    # Sections detected
    sections = analysis["sections"]["found"]
    detected = [s for s, v in sections.items() if v]
    missing = [s for s, v in sections.items() if not v]
    
    st.markdown("### 📑 Sections Detected")
    if detected:
        st.write("Found: " + " · ".join(f"`{s}`" for s in detected))
    if missing:
        st.write("Missing: " + " · ".join(f"`{s}`" for s in missing))
    
    # Keyword match (if job description provided)
    keywords = analysis["keywords"]
    if not keywords.get("note"):
        st.markdown("---")
        st.markdown("### 🎯 Keyword Match")
        
        match_pct = keywords["match_percentage"]
        st.progress(match_pct / 100)
        st.write(f"**{match_pct}%** match with job description")
        
        kw_cols = st.columns(2)
        with kw_cols[0]:
            if keywords["matched"]:
                st.write("**✅ Matched:**")
                st.write(", ".join(keywords["matched"][:15]))
        with kw_cols[1]:
            if keywords["missing"]:
                st.write("**❌ Missing:**")
                st.write(", ".join(keywords["missing"][:15]))
    
    # Weak phrases
    weak = analysis["action_verbs"]["weak_verbs"]
    if weak:
        st.markdown("---")
        st.markdown("### 🚫 Weak Phrases to Replace")
        for w in weak:
            st.code(w, language=None)
    
    # Too-short bullets
    short_bullets = analysis["bullet_points"].get("too_short", [])
    if short_bullets:
        st.markdown("### ✏️ Bullet Points Too Short (< 5 words)")
        for b in short_bullets:
            st.code(b, language=None)
    
    # ── Export ──────────────────────────────────────────────────────
    
    st.markdown("---")
    
    export_data = {
        "file": uploaded_file.name,
        "overall_score": overall,
        "grade": grade_text,
        "categories": {
            name: {"score": d["score"], "detail": d["detail"]}
            for name, d in scores["categories"].items()
        },
        "strengths": scores["strengths"],
        "improvements": scores["improvements"],
    }
    
    st.download_button(
        label="📥 Download Report (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name=f"resume-review-{uploaded_file.name}.json",
        mime="application/json",
    )

else:
    # ── Landing State ──────────────────────────────────────────────
    
    st.markdown("---")
    st.markdown("""
    ### How it works
    
    1. **Upload** your resume (PDF, DOCX, or TXT)
    2. **Optionally** upload a job description for keyword matching
    3. **Get instant scores** across 7 categories
    4. **Follow suggestions** to improve your resume
    
    ### What we analyze
    
    | Category | What we check |
    |---|---|
    | Section Completeness | Education, experience, skills, projects, etc. |
    | Content Quality | Strong vs weak action verbs, passive voice |
    | Keyword Optimization | Match against job description keywords |
    | Quantification | Metrics, numbers, and measurable results |
    | Length & Readability | Optimal word count for your experience level |
    | Contact Information | Email, phone, LinkedIn, GitHub |
    | Bullet Point Quality | Length, detail, and impact of bullet points |
    
    ---
    
    *Built by [Nawang Dorjay](https://github.com/nawangdorjay) — B.Tech CSE (Data Science), Leh, Ladakh*
    """)
