"""
app.py – AI Resume Screening Application (Streamlit)

A full-featured, premium AI-powered resume screening tool.
Pages: Home / Upload → Job Description → Results → Analytics → Export
"""

import io
import os
import json
import time
import datetime
import pandas as pd
import streamlit as st
from typing import List, Dict, Any

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal imports ─────────────────────────────────────────────────────────
from utils.parser import parse_resume, clean_text
from utils.extractor import extract_all, extract_keywords_from_jd
from utils.scorer import rank_candidates, get_tier
from utils.visualizer import (
    score_bar_chart,
    score_distribution,
    skill_frequency_chart,
    skill_gap_sunburst,
    radar_chart,
    experience_distribution,
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Root & Reset ── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #1a1040 40%, #24243e 100%);
            min-height: 100vh;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: rgba(15, 12, 41, 0.85);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(99, 102, 241, 0.25);
        }
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: #a5b4fc;
        }

        /* ── Main content ── */
        .main .block-container {
            padding-top: 1.5rem;
            max-width: 1400px;
        }

        /* ── Card component ── */
        .card {
            background: rgba(30, 27, 75, 0.6);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
        }

        /* ── Hero Banner ── */
        .hero-banner {
            background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(168,85,247,0.15) 100%);
            border: 1px solid rgba(99,102,241,0.3);
            border-radius: 20px;
            padding: 2.5rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        .hero-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(99,102,241,0.08) 0%, transparent 60%);
            animation: pulse 4s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 1; }
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #818cf8, #c084fc, #e879f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 0.5rem 0;
            line-height: 1.2;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #94a3b8;
            margin: 0;
        }

        /* ── Metric cards ── */
        .metric-card {
            background: rgba(30, 27, 75, 0.7);
            border: 1px solid rgba(99,102,241,0.25);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            text-align: center;
        }
        .metric-number {
            font-size: 2.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 0.25rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        /* ── Score badge ── */
        .score-badge {
            display: inline-block;
            padding: 0.3rem 0.9rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        /* ── Skill chip ── */
        .chip-matched {
            display: inline-block;
            background: rgba(34,197,94,0.2);
            color: #4ade80;
            border: 1px solid rgba(34,197,94,0.35);
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.78rem;
            margin: 0.2rem;
            font-weight: 500;
        }
        .chip-missing {
            display: inline-block;
            background: rgba(239,68,68,0.2);
            color: #f87171;
            border: 1px solid rgba(239,68,68,0.35);
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.78rem;
            margin: 0.2rem;
            font-weight: 500;
        }
        .chip-extra {
            display: inline-block;
            background: rgba(99,102,241,0.2);
            color: #a5b4fc;
            border: 1px solid rgba(99,102,241,0.35);
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.78rem;
            margin: 0.2rem;
            font-weight: 500;
        }

        /* ── Candidate row ── */
        .candidate-row {
            background: rgba(30,27,75,0.55);
            border: 1px solid rgba(99,102,241,0.18);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.6rem;
            transition: all 0.2s ease;
        }
        .candidate-row:hover {
            border-color: rgba(99,102,241,0.5);
            background: rgba(30,27,75,0.75);
        }

        /* ── Progress bar ── */
        .progress-wrap {
            background: rgba(255,255,255,0.08);
            border-radius: 999px;
            height: 8px;
            overflow: hidden;
            margin-top: 4px;
        }
        .progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #6366f1, #a855f7);
            transition: width 0.8s ease;
        }

        /* ── Section heading ── */
        .section-heading {
            font-size: 1.4rem;
            font-weight: 700;
            color: #e2e8f0;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(99,102,241,0.25);
        }

        /* ── Upload zone ── */
        [data-testid="stFileUploader"] {
            border: 2px dashed rgba(99,102,241,0.4) !important;
            border-radius: 14px !important;
            background: rgba(99,102,241,0.05) !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: rgba(99,102,241,0.7) !important;
            background: rgba(99,102,241,0.1) !important;
        }

        /* ── Buttons ── */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.55rem 1.5rem !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
        }

        /* ── Selectbox, text_area etc ── */
        .stTextArea textarea, .stTextInput input, .stSelectbox select {
            background: rgba(30,27,75,0.7) !important;
            border: 1px solid rgba(99,102,241,0.3) !important;
            color: #e2e8f0 !important;
            border-radius: 10px !important;
        }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(30,27,75,0.6) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(99,102,241,0.2) !important;
            gap: 4px;
            padding: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            color: #94a3b8 !important;
            font-weight: 500 !important;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
        }

        /* ── Expander ── */
        .streamlit-expanderHeader {
            background: rgba(30,27,75,0.6) !important;
            border: 1px solid rgba(99,102,241,0.2) !important;
            border-radius: 10px !important;
            color: #e2e8f0 !important;
        }

        /* ── Slider ── */
        .stSlider [data-testid="stThumb"] {
            background: #6366f1 !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
        ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.5); border-radius: 3px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Session state helpers ────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "upload",
        "candidates": [],
        "jd_text": "",
        "jd_keywords": [],
        "ranked": [],
        "required_exp": 0,
        "weights": {"tfidf": 0.50, "skill": 0.40, "experience": 0.10},
        "selected_candidate": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ── Sidebar ──────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div style="text-align:center;padding:1rem 0;">'
            '<span style="font-size:2.5rem;">🤖</span><br>'
            '<span style="font-size:1.1rem;font-weight:700;color:#a5b4fc;">AI Resume Screener</span><br>'
            '<span style="font-size:0.75rem;color:#64748b;">Powered by NLP & TF-IDF</span>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown("### 📍 Navigation")
        pages = {
            "📤 Upload Resumes": "upload",
            "📋 Job Description": "jd",
            "🏆 Results & Ranking": "results",
            "📊 Analytics Dashboard": "analytics",
            "💾 Export Data": "export",
        }
        for label, page_key in pages.items():
            is_active = st.session_state.page == page_key
            if st.button(
                label,
                key=f"nav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.page = page_key
                st.rerun()

        st.divider()

        # Stats in sidebar
        if st.session_state.candidates:
            st.markdown("### 📈 Session Stats")
            st.markdown(
                f"""
                <div style="display:flex;flex-direction:column;gap:0.5rem;">
                  <div class="metric-card">
                    <div class="metric-number">{len(st.session_state.candidates)}</div>
                    <div class="metric-label">Resumes Loaded</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.session_state.ranked:
                top = st.session_state.ranked[0]
                st.markdown(
                    f"""
                    <div class="metric-card" style="margin-top:0.5rem;">
                      <div class="metric-number">{top['percentage_score']:.0f}%</div>
                      <div class="metric-label">Top Score</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()
        st.markdown(
            '<p style="font-size:0.72rem;color:#475569;text-align:center;">'
            "AI Resume Screener v1.0<br>Built with Streamlit & scikit-learn"
            "</p>",
            unsafe_allow_html=True,
        )


# ── Page: Upload ─────────────────────────────────────────────────────────────
def page_upload():
    st.markdown(
        '<div class="hero-banner">'
        '<h1 class="hero-title">AI Resume Screener</h1>'
        '<p class="hero-subtitle">Upload resumes, define a job description,<br>'
        "and let AI rank your candidates intelligently.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    stats = [
        ("🧠", "AI-Powered", "TF-IDF + Cosine Similarity"),
        ("📄", "Multi-Format", "PDF, DOCX & TXT support"),
        ("⚡", "Instant Results", "Bulk screening in seconds"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3], stats):
        col.markdown(
            f'<div class="card" style="text-align:center;">'
            f'<div style="font-size:2rem;">{icon}</div>'
            f'<div style="font-weight:700;color:#a5b4fc;margin:0.4rem 0;">{title}</div>'
            f'<div style="color:#64748b;font-size:0.85rem;">{desc}</div>'
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<div class="section-heading">📤 Upload Resume Files</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Drag and drop resumes here (PDF, DOCX, TXT)",
        type=["pdf", "docx", "doc", "txt"],
        accept_multiple_files=True,
        help="Upload one or more resume files. All formats supported.",
    )

    if uploaded_files:
        progress_bar = st.progress(0, text="Processing resumes…")
        candidates = []
        errors = []

        for i, uf in enumerate(uploaded_files):
            try:
                raw_text = parse_resume(uf)
                raw_text = clean_text(raw_text)
                candidate = extract_all(raw_text, filename=uf.name)
                candidates.append(candidate)
            except Exception as e:
                errors.append((uf.name, str(e)))
            progress_bar.progress(
                (i + 1) / len(uploaded_files),
                text=f"Processing: {uf.name}",
            )

        progress_bar.empty()

        if errors:
            for fname, err in errors:
                st.warning(f"⚠️ Could not parse **{fname}**: {err}")

        if candidates:
            st.session_state.candidates = candidates
            st.success(f"✅ Successfully parsed **{len(candidates)}** resume(s)!")

            # Preview cards
            st.markdown("### 👤 Parsed Candidates Preview")
            cols = st.columns(min(3, len(candidates)))
            for i, c in enumerate(candidates):
                col = cols[i % len(cols)]
                col.markdown(
                    f'<div class="candidate-row">'
                    f'<div style="font-weight:700;color:#a5b4fc;font-size:1rem;">{c["name"]}</div>'
                    f'<div style="color:#64748b;font-size:0.8rem;margin-top:2px;">{c["filename"]}</div>'
                    f'<div style="margin-top:0.5rem;font-size:0.82rem;color:#94a3b8;">'
                    f'📧 {c["email"] or "—"} &nbsp;|&nbsp; 📱 {c["phone"] or "—"}</div>'
                    f'<div style="margin-top:0.35rem;font-size:0.8rem;color:#94a3b8;">'
                    f'🎓 {", ".join(c["education"][:2]) if c["education"] else "—"} &nbsp;|&nbsp; '
                    f'💼 {c["experience_years"]} yrs exp</div>'
                    f'<div style="margin-top:0.5rem;">'
                    + "".join(
                        f'<span class="chip-extra">{s}</span>'
                        for s in c["skills"][:5]
                    )
                    + ("..." if len(c["skills"]) > 5 else "")
                    + "</div></div>",
                    unsafe_allow_html=True,
                )

            st.markdown("---")
            col_btn1, col_btn2 = st.columns([1, 4])
            with col_btn1:
                if st.button("➡️ Next: Add Job Description", type="primary"):
                    st.session_state.page = "jd"
                    st.rerun()

    elif st.session_state.candidates:
        st.info(
            f"ℹ️ {len(st.session_state.candidates)} resume(s) already loaded. "
            "Upload new files to replace them or proceed to the next step."
        )
        if st.button("➡️ Go to Job Description", type="primary"):
            st.session_state.page = "jd"
            st.rerun()


# ── Page: Job Description ────────────────────────────────────────────────────
def page_jd():
    st.markdown('<div class="section-heading">📋 Job Description Configuration</div>', unsafe_allow_html=True)

    if not st.session_state.candidates:
        st.warning("⚠️ Please upload resumes first.")
        if st.button("⬅️ Go to Upload"):
            st.session_state.page = "upload"
            st.rerun()
        return

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("#### ✍️ Enter Job Description")
        jd_text = st.text_area(
            label="Job Description",
            value=st.session_state.jd_text,
            height=380,
            placeholder=(
                "Paste the full job description here…\n\n"
                "Example:\nWe are looking for a Senior Data Scientist with 5+ years of experience in Python, "
                "Machine Learning, TensorFlow, and SQL. The candidate should have strong knowledge of NLP, "
                "deep learning, and cloud platforms like AWS or GCP…"
            ),
            help="Paste the complete job description. The AI will extract keywords and match against resumes.",
            label_visibility="collapsed",
        )

        # Sample JDs
        with st.expander("💡 Load a Sample Job Description"):
            sample_jds = {
                "Data Scientist": (
                    "We are looking for an experienced Data Scientist with 4+ years of experience. "
                    "Required skills: Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, "
                    "SQL, Pandas, NumPy, Data Visualization, Statistics, A/B Testing. "
                    "Experience with NLP, Computer Vision, and cloud platforms (AWS, GCP, Azure) is a plus. "
                    "Strong communication and collaboration skills required. Agile methodology experience preferred."
                ),
                "Full Stack Developer": (
                    "We need a Full Stack Developer with 3+ years of experience. "
                    "Must have: JavaScript, TypeScript, React, Node.js, Express.js, REST API, SQL, MongoDB, Git. "
                    "Nice to have: Docker, Kubernetes, AWS, CI/CD, GraphQL. "
                    "Strong problem-solving skills and ability to work in an Agile team environment."
                ),
                "ML Engineer": (
                    "Seeking an ML Engineer with 5+ years building production ML systems. "
                    "Requirements: Python, TensorFlow, PyTorch, Kubernetes, Docker, AWS, MLflow, "
                    "Apache Spark, Kafka, SQL, C++, Transformers, BERT. "
                    "Experience with distributed computing and model deployment is essential."
                ),
                "DevOps Engineer": (
                    "DevOps Engineer with 3+ years of experience required. "
                    "Core skills: Linux, Docker, Kubernetes, Terraform, Ansible, Jenkins, GitHub Actions, "
                    "AWS or Azure or GCP, Python, Bash, Prometheus, Grafana, CI/CD pipelines. "
                    "Strong background in microservices architecture."
                ),
            }
            sample_choice = st.selectbox("Choose a template:", ["— Select —"] + list(sample_jds.keys()))
            if sample_choice != "— Select —":
                if st.button("Load Template", type="primary"):
                    st.session_state.jd_text = sample_jds[sample_choice]
                    st.rerun()

    with col_right:
        st.markdown("#### ⚙️ Screening Parameters")

        st.markdown(
            '<div class="card">'
            '<div style="font-weight:600;color:#a5b4fc;margin-bottom:0.5rem;">⏱️ Required Experience</div>',
            unsafe_allow_html=True,
        )
        required_exp = st.slider(
            "Minimum years of experience",
            min_value=0,
            max_value=20,
            value=st.session_state.required_exp,
            step=1,
            format="%d years",
            help="Set 0 to ignore experience in scoring.",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("#### 🎯 Scoring Weights")
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )
        w_tfidf = st.slider(
            "Content Match (TF-IDF)", 0, 100,
            int(st.session_state.weights["tfidf"] * 100), 5,
            help="Weight for overall text similarity between resume and JD."
        )
        w_skill = st.slider(
            "Skill Match", 0, 100,
            int(st.session_state.weights["skill"] * 100), 5,
            help="Weight for matched skills vs. required JD keywords."
        )
        w_exp = st.slider(
            "Experience Match", 0, 100,
            int(st.session_state.weights["experience"] * 100), 5,
            help="Weight for years of experience (requires non-zero Required Experience)."
        )
        st.markdown("</div>", unsafe_allow_html=True)

        total_w = w_tfidf + w_skill + w_exp
        if total_w == 0:
            st.error("⚠️ All weights are 0. Please set at least one weight > 0.")
        else:
            st.markdown(
                f'<div class="card" style="text-align:center;">'
                f'<div style="color:#64748b;font-size:0.8rem;margin-bottom:0.5rem;">Effective Weights (normalized)</div>'
                f'<div style="color:#a5b4fc;">Content: <b>{w_tfidf/total_w*100:.0f}%</b> &nbsp;|&nbsp; '
                f'Skills: <b>{w_skill/total_w*100:.0f}%</b> &nbsp;|&nbsp; '
                f'Exp: <b>{w_exp/total_w*100:.0f}%</b></div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    # Extract JD keywords preview
    if jd_text.strip():
        kws = extract_keywords_from_jd(jd_text)
        if kws:
            st.markdown("#### 🔍 Extracted JD Keywords")
            chip_html = "".join(f'<span class="chip-extra">{k}</span>' for k in kws)
            st.markdown(
                f'<div class="card">{chip_html}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        run_disabled = not jd_text.strip() or total_w == 0 if "total_w" in dir() else True
        if st.button("🚀 Screen Candidates", type="primary", disabled=not jd_text.strip()):
            with st.spinner("🤖 AI is analysing all resumes…"):
                kws = extract_keywords_from_jd(jd_text)
                weights = {
                    "tfidf": w_tfidf,
                    "skill": w_skill,
                    "experience": w_exp,
                }
                ranked = rank_candidates(
                    candidates=[dict(c) for c in st.session_state.candidates],
                    jd_text=jd_text,
                    jd_keywords=kws,
                    required_experience=required_exp,
                    weights=weights,
                )
                # Attach tier labels
                for c in ranked:
                    label, color = get_tier(c["composite_score"])
                    c["tier_label"] = label
                    c["tier_color"] = color

                st.session_state.jd_text = jd_text
                st.session_state.jd_keywords = kws
                st.session_state.ranked = ranked
                st.session_state.required_exp = required_exp
                st.session_state.weights = {
                    "tfidf": w_tfidf / max(total_w, 1),
                    "skill": w_skill / max(total_w, 1),
                    "experience": w_exp / max(total_w, 1),
                }
                time.sleep(0.5)

            st.success("✅ Screening complete! Redirecting to results…")
            time.sleep(0.8)
            st.session_state.page = "results"
            st.rerun()


# ── Page: Results ────────────────────────────────────────────────────────────
def page_results():
    st.markdown('<div class="section-heading">🏆 Candidate Rankings</div>', unsafe_allow_html=True)

    if not st.session_state.ranked:
        st.warning("⚠️ No screening results yet. Please complete the Job Description step first.")
        if st.button("⬅️ Go to Job Description"):
            st.session_state.page = "jd"
            st.rerun()
        return

    ranked = st.session_state.ranked

    # ── Summary metrics ──
    total = len(ranked)
    excellent = sum(1 for c in ranked if c["percentage_score"] >= 75)
    good = sum(1 for c in ranked if 55 <= c["percentage_score"] < 75)
    avg_score = sum(c["percentage_score"] for c in ranked) / total if total else 0
    top_candidate = ranked[0]

    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        (m1, str(total), "Total Candidates"),
        (m2, str(excellent), "Excellent Matches"),
        (m3, str(good), "Good Matches"),
        (m4, f"{avg_score:.1f}%", "Average Score"),
        (m5, top_candidate["name"], "Top Candidate"),
    ]
    for col, num, lbl in metrics:
        col.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-number" style="font-size:1.6rem;">{num}</div>'
            f'<div class="metric-label">{lbl}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Filter & Search ──
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_term = st.text_input("🔍 Search by name or file", placeholder="Type to filter…")
    with col_filter:
        tier_filter = st.selectbox(
            "Filter by tier",
            ["All", "🏆 Excellent", "✅ Good", "⚠️ Average", "❌ Below Average"],
        )

    filtered = ranked
    if search_term:
        filtered = [
            c for c in filtered
            if search_term.lower() in c["name"].lower()
            or search_term.lower() in c["filename"].lower()
        ]
    if tier_filter != "All":
        filtered = [c for c in filtered if c.get("tier_label", "") == tier_filter]

    # ── Candidate List ──
    if not filtered:
        st.info("No candidates match your current filters.")
    else:
        st.markdown(f"**Showing {len(filtered)} of {total} candidates**")
        for c in filtered:
            col_main, col_detail = st.columns([5, 1])
            with col_main:
                pct = c["percentage_score"]
                tier_label = c.get("tier_label", "")
                tier_color = c.get("tier_color", "#6366f1")

                matched_chips = "".join(
                    f'<span class="chip-matched">{s}</span>'
                    for s in c.get("matched_skills", [])[:4]
                )
                missing_chips = "".join(
                    f'<span class="chip-missing">{s}</span>'
                    for s in c.get("missing_skills", [])[:3]
                )

                st.markdown(
                    f'<div class="candidate-row">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'  <div>'
                    f'    <span style="font-size:1.1rem;font-weight:700;color:#e2e8f0;">#{c["rank"]} {c["name"]}</span>'
                    f'    <span style="font-size:0.78rem;color:#64748b;margin-left:0.5rem;">{c["filename"]}</span>'
                    f'  </div>'
                    f'  <div>'
                    f'    <span style="font-size:1.3rem;font-weight:800;color:{tier_color};">{pct:.1f}%</span>'
                    f'    <span style="font-size:0.75rem;color:{tier_color};margin-left:0.3rem;">{tier_label}</span>'
                    f'  </div>'
                    f'</div>'
                    f'<div class="progress-wrap"><div class="progress-fill" style="width:{pct}%;"></div></div>'
                    f'<div style="display:flex;gap:1.5rem;margin-top:0.6rem;font-size:0.8rem;color:#94a3b8;">'
                    f'  <span>📧 {c["email"] or "—"}</span>'
                    f'  <span>📱 {c["phone"] or "—"}</span>'
                    f'  <span>💼 {c["experience_years"]} yrs</span>'
                    f'  <span>🧠 {len(c["skills"])} skills</span>'
                    f'  <span>🎓 {", ".join(c["education"][:1]) if c["education"] else "—"}</span>'
                    f'</div>'
                    f'<div style="margin-top:0.5rem;">{matched_chips}'
                    + (f' <span style="color:#64748b;font-size:0.78rem;">Missing: </span>{missing_chips}' if missing_chips else "")
                    + "</div></div>",
                    unsafe_allow_html=True,
                )
            with col_detail:
                st.write("")
                if st.button("🔍 Details", key=f"detail_{c['rank']}"):
                    st.session_state.selected_candidate = c
                    st.session_state.page = "detail"
                    st.rerun()

    # ── Score Chart ──
    st.markdown("---")
    st.markdown("#### 📊 Score Overview")
    st.plotly_chart(score_bar_chart(filtered or ranked), use_container_width=True)


# ── Page: Candidate Detail ───────────────────────────────────────────────────
def page_detail():
    c = st.session_state.selected_candidate
    if not c:
        st.session_state.page = "results"
        st.rerun()
        return

    if st.button("⬅️ Back to Results"):
        st.session_state.page = "results"
        st.rerun()

    tier_label = c.get("tier_label", "")
    tier_color = c.get("tier_color", "#6366f1")

    st.markdown(
        f'<div class="hero-banner" style="padding:1.5rem;">'
        f'<h2 style="color:#e2e8f0;font-size:1.8rem;font-weight:700;margin:0;">'
        f'#{c["rank"]} — {c["name"]}</h2>'
        f'<p style="color:#94a3b8;margin:0.3rem 0 0 0;">{c["filename"]}</p>'
        f'<div style="margin-top:0.8rem;font-size:2rem;font-weight:800;color:{tier_color};">'
        f'{c["percentage_score"]:.1f}% &nbsp;'
        f'<span style="font-size:1rem;">{tier_label}</span>'
        f"</div></div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "🧠 Skills Analysis", "📊 Score Breakdown", "📄 Raw Text"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**Contact & Social Links**")

            email = c.get("email") or "—"
            phone = c.get("phone") or "—"
            linkedin = c.get("linkedin") or ""
            github = c.get("github") or ""

            st.markdown(f"📧 **Email:** `{email}`")
            st.markdown(f"📱 **Phone:** `{phone}`")
            if linkedin:
                st.markdown(f"🔗 **LinkedIn:** [{linkedin}]({linkedin})")
            else:
                st.markdown("🔗 **LinkedIn:** —")
            if github:
                st.markdown(f"🐙 **GitHub:** [{github}]({github})")
            else:
                st.markdown("🐙 **GitHub:** —")

            if c.get("summary"):
                st.markdown("---")
                st.markdown("**📝 Profile Summary / Objective**")
                st.info(c["summary"])

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**Education & Experience**")
            edu_list = c.get("education", []) or ["Higher Education / Degree"]
            for edu in edu_list[:5]:
                st.markdown(f"🎓 {edu}")

            exp_yrs = c.get("experience_years", 0)
            if exp_yrs == 0:
                st.markdown("💼 **0 years of experience** *(Fresher / Student / Entry Level)*")
            else:
                st.markdown(f"💼 **{exp_yrs} years** of professional experience")

            if c.get("projects"):
                st.markdown("---")
                st.markdown("**🚀 Key Projects Detected**")
                for proj in c["projects"][:4]:
                    st.markdown(f"• {proj}")

            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.plotly_chart(skill_gap_sunburst(c), use_container_width=True)

        col_m, col_miss, col_extra = st.columns(3)
        with col_m:
            st.markdown("**✅ Matched Skills**")
            matched = c.get("matched_skills", [])
            if matched:
                chips = "".join(f'<span class="chip-matched">{s}</span>' for s in matched)
                st.markdown(f'<div class="card">{chips}</div>', unsafe_allow_html=True)
            else:
                st.info("No matched skills found.")

        with col_miss:
            st.markdown("**❌ Missing Skills**")
            missing = c.get("missing_skills", [])
            if missing:
                chips = "".join(f'<span class="chip-missing">{s}</span>' for s in missing)
                st.markdown(f'<div class="card">{chips}</div>', unsafe_allow_html=True)
            else:
                st.success("No missing skills! 🎉")

        with col_extra:
            st.markdown("**💡 Extra Skills**")
            extra = c.get("extra_skills", [])
            if extra:
                chips = "".join(f'<span class="chip-extra">{s}</span>' for s in extra[:15])
                st.markdown(f'<div class="card">{chips}</div>', unsafe_allow_html=True)
            else:
                st.info("No extra skills detected.")

    with tab3:
        col_g, col_b = st.columns(2)
        scores = {
            "Content Match (TF-IDF)": c.get("tfidf_score", 0),
            "Skill Match": c.get("skill_score", 0),
            "Experience Match": c.get("experience_score", 0),
            "Overall Score": c.get("composite_score", 0),
        }
        for i, (label, score) in enumerate(scores.items()):
            col = col_g if i % 2 == 0 else col_b
            pct = score * 100
            col.markdown(
                f'<div class="metric-card" style="margin-bottom:0.5rem;">'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-number">{pct:.1f}%</div>'
                f'<div class="progress-wrap"><div class="progress-fill" style="width:{pct}%;"></div></div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    with tab4:
        raw = c.get("raw_text", "")
        st.text_area("Extracted Resume Text", value=raw, height=400, disabled=True)


# ── Page: Analytics ──────────────────────────────────────────────────────────
def page_analytics():
    st.markdown('<div class="section-heading">📊 Analytics Dashboard</div>', unsafe_allow_html=True)

    if not st.session_state.ranked:
        st.warning("⚠️ No data to analyse. Please screen resumes first.")
        if st.button("⬅️ Go to Job Description"):
            st.session_state.page = "jd"
            st.rerun()
        return

    ranked = st.session_state.ranked

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Score Overview", "🧠 Skills Insights", "🎯 Radar Comparison", "📋 Summary Table"]
    )

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(score_distribution(ranked), use_container_width=True)
        with col2:
            st.plotly_chart(experience_distribution(ranked), use_container_width=True)
        st.plotly_chart(score_bar_chart(ranked), use_container_width=True)

    with tab2:
        st.plotly_chart(skill_frequency_chart(ranked, top_n=20), use_container_width=True)

        # JD keywords coverage
        jd_kws = st.session_state.jd_keywords
        if jd_kws:
            st.markdown("#### JD Keyword Coverage Across All Candidates")
            coverage_data = []
            for kw in jd_kws:
                count = sum(
                    1 for c in ranked if kw in c.get("matched_skills", [])
                )
                coverage_data.append({"Keyword": kw, "Coverage": count, "Pct": count / len(ranked) * 100})

            coverage_df = pd.DataFrame(coverage_data).sort_values("Coverage", ascending=False)
            import plotly.express as px
            fig = px.bar(
                coverage_df,
                x="Keyword",
                y="Pct",
                title="Keyword Coverage (% of candidates who have this skill)",
                color="Pct",
                color_continuous_scale="Purp",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"),
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(tickangle=-35),
                yaxis=dict(title="Coverage (%)"),
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if len(ranked) == 1:
            st.info("ℹ️ Showing radar chart comparison for 1 candidate. Upload/screen more candidates to compare multiple candidates.")
            st.plotly_chart(radar_chart(ranked, top_n=1), use_container_width=True)
        else:
            max_val = min(10, len(ranked))
            default_val = min(5, max_val)
            top_n = st.slider("Number of candidates to compare", min_value=2, max_value=max_val, value=default_val)
            st.plotly_chart(radar_chart(ranked, top_n=top_n), use_container_width=True)

    with tab4:
        df = pd.DataFrame(
            [
                {
                    "Rank": c["rank"],
                    "Name": c["name"],
                    "File": c["filename"],
                    "Score (%)": c["percentage_score"],
                    "Tier": c.get("tier_label", ""),
                    "Skills Matched": len(c.get("matched_skills", [])),
                    "Skills Missing": len(c.get("missing_skills", [])),
                    "Total Skills": len(c.get("skills", [])),
                    "Experience (yrs)": c.get("experience_years", 0),
                    "Email": c.get("email", ""),
                    "Phone": c.get("phone", ""),
                }
                for c in ranked
            ]
        )
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


# ── Page: Export ─────────────────────────────────────────────────────────────
def page_export():
    st.markdown('<div class="section-heading">💾 Export Results</div>', unsafe_allow_html=True)

    if not st.session_state.ranked:
        st.warning("⚠️ No results to export. Please screen resumes first.")
        if st.button("⬅️ Go to Job Description"):
            st.session_state.page = "jd"
            st.rerun()
        return

    ranked = st.session_state.ranked

    col1, col2 = st.columns(2)

    with col1:
        # CSV Export
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Export as CSV")
        st.markdown(
            "Download a spreadsheet with all candidate scores, skills, and contact info.",
            unsafe_allow_html=True,
        )
        df = pd.DataFrame(
            [
                {
                    "Rank": c["rank"],
                    "Name": c["name"],
                    "File": c["filename"],
                    "Email": c.get("email", ""),
                    "Phone": c.get("phone", ""),
                    "LinkedIn": c.get("linkedin", ""),
                    "GitHub": c.get("github", ""),
                    "Overall Score (%)": c["percentage_score"],
                    "TF-IDF Score": c.get("tfidf_score", 0),
                    "Skill Score": c.get("skill_score", 0),
                    "Experience Score": c.get("experience_score", 0),
                    "Tier": c.get("tier_label", ""),
                    "Skills Found": ", ".join(c.get("skills", [])),
                    "Matched Skills": ", ".join(c.get("matched_skills", [])),
                    "Missing Skills": ", ".join(c.get("missing_skills", [])),
                    "Education": ", ".join(c.get("education", [])),
                    "Experience (years)": c.get("experience_years", 0),
                }
                for c in ranked
            ]
        )
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_bytes,
            file_name=f"resume_screening_{timestamp}.csv",
            mime="text/csv",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # JSON Export
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🗂️ Export as JSON")
        st.markdown("Download structured JSON data for integration with other systems.")

        export_data = [
            {
                "rank": c["rank"],
                "name": c["name"],
                "filename": c["filename"],
                "email": c.get("email", ""),
                "phone": c.get("phone", ""),
                "linkedin": c.get("linkedin", ""),
                "github": c.get("github", ""),
                "scores": {
                    "overall_pct": c["percentage_score"],
                    "tfidf": c.get("tfidf_score", 0),
                    "skill": c.get("skill_score", 0),
                    "experience": c.get("experience_score", 0),
                },
                "tier": c.get("tier_label", ""),
                "skills": {
                    "all": c.get("skills", []),
                    "matched": c.get("matched_skills", []),
                    "missing": c.get("missing_skills", []),
                    "extra": c.get("extra_skills", []),
                },
                "education": c.get("education", []),
                "experience_years": c.get("experience_years", 0),
            }
            for c in ranked
        ]
        json_bytes = json.dumps(export_data, indent=2).encode("utf-8")
        st.download_button(
            label="⬇️ Download JSON",
            data=json_bytes,
            file_name=f"resume_screening_{timestamp}.json",
            mime="application/json",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Preview
    st.markdown("---")
    st.markdown("#### 👁️ Data Preview")
    st.dataframe(df, use_container_width=True, hide_index=True)


# ── Router ───────────────────────────────────────────────────────────────────
def main():
    inject_css()
    init_state()
    render_sidebar()

    page = st.session_state.page

    if page == "upload":
        page_upload()
    elif page == "jd":
        page_jd()
    elif page == "results":
        page_results()
    elif page == "detail":
        page_detail()
    elif page == "analytics":
        page_analytics()
    elif page == "export":
        page_export()
    else:
        st.session_state.page = "upload"
        st.rerun()


if __name__ == "__main__":
    main()
