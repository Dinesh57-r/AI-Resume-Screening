# 🤖 AI Resume Screening App — Streamlit

A **fully-featured, AI-powered Resume Screening & Candidate Ranking Application** built with **Streamlit**, **scikit-learn**, **pdfplumber**, **pypdf**, and **Plotly**.

---

## 📌 Implementation Plan & Overview

This project provides an automated, intelligent HR screening system. It parses bulk resumes in multiple formats, extracts key candidate entities using NLP, scores candidates against job descriptions using TF-IDF vectorization and weighted composite matching, and presents actionable insights via a premium animated dark UI.

### 🛠️ Tech Stack
- **Frontend / UI**: Streamlit with custom dark glassmorphism CSS theming
- **NLP / AI Engine**: `scikit-learn` (TF-IDF vectorizer + Cosine Similarity), `nltk`, RegEx entity extractors
- **Dual-Engine Document Parsers**: `pdfplumber` + `pypdf` (PDF fallback engine), `python-docx` (DOCX & tables), plain text (`TXT`)
- **Analytics & Visualizations**: `Plotly` (interactive dark-theme charts), `pandas` (data tables & exports)
- **Data Export & Storage**: CSV and JSON export modules, Streamlit session state management

---

## ✨ Features & Functional Highlights

| Feature | Description |
|---|---|
| 📤 **Bulk Resume Upload** | Drag & drop multiple `PDF`, `DOCX`, and `TXT` resume files simultaneously |
| 📄 **Dual-Engine Parsing** | High-precision text extraction with `pdfplumber` + `pypdf` fallback for layout-heavy PDFs |
| 🧠 **Smart NLP Entity Extraction** | Extracts Candidate Name, Email, Phone Number, 100+ Technical & Soft Skills, Education Degrees, Experience (years/date-ranges), Profile Summaries, and Projects |
| 🤖 **AI TF-IDF Scoring** | TF-IDF (1-2 n-grams) cosine similarity scoring between candidate resumes and Job Descriptions |
| 🎯 **Skill Gap Analysis** | Automatic comparison generating **Matched Skills**, **Missing Skills**, and **Extra Skills** lists |
| 🏆 **Ranked Leaderboard** | Sortable candidate ranking table with tier badges (🏆 Excellent, ✅ Good, ⚠️ Average, ❌ Below Average) |
| 👤 **Detailed Candidate Drill-down** | Interactive profile viewer with Contact Cards, Education, Experience, Skill Gap Sunbursts, Score Breakdown, and Raw Text |
| 📊 **Analytics Dashboard** | Score Distribution Histogram, Skill Frequency Chart, Keyword Coverage Bar Chart, Experience Pie Chart, Radar Comparison, and Summary Dataframes |
| 💾 **Multi-Format Export** | One-click export of complete screening evaluation to **CSV** and **JSON** |

---

## 🗂️ Project Structure & Module Description

```
f:\AI-Resume-Screening (2)\AI-Resume-Screening\AI-Resume-Screening\
├── app.py                  # Main Streamlit app (Routing, UI layout, Custom CSS)
├── requirements.txt        # Core dependencies list
├── README.md               # Complete project documentation & guide
├── test_app.py             # End-to-end unit test & validation script
├── sample_resumes/         # Sample candidate resumes for testing
│   ├── john_smith_data_scientist.txt
│   ├── priya_sharma_fullstack.txt
│   └── alex_johnson_ml_junior.txt
└── utils/
    ├── __init__.py         # Package initialization
    ├── parser.py           # Dual-engine PDF (pdfplumber + pypdf), DOCX, and TXT parser
    ├── extractor.py        # NLP entity extraction (Name, Email, Phone, Skills, Education, Exp, Projects)
    ├── scorer.py           # TF-IDF Cosine Similarity & Weighted Composite Scoring Engine
    └── visualizer.py       # Plotly chart factory (6 dark-themed interactive charts)
```

### 📄 Key Files Explained

1. **`app.py`**: Controls Streamlit navigation across 5 primary pages:
   - **Upload Resumes**: Upload drag & drop files + candidate preview cards.
   - **Job Description**: Text area input, sample templates (Data Scientist, Full Stack, ML Engineer, DevOps), weight sliders, and experience requirements.
   - **Results & Ranking**: Interactive leaderboard, search bar, tier filters, and detailed candidate modal drill-downs.
   - **Analytics Dashboard**: Comprehensive chart gallery and radar comparison slider.
   - **Export Data**: CSV and JSON download triggers with interactive preview tables.

2. **`utils/parser.py`**:
   - `parse_pdf()`: Extracts text using `pdfplumber` with layout support; falls back to `pypdf` if needed.
   - `parse_docx()`: Extracts paragraphs and embedded tables from Microsoft Word documents.
   - `parse_txt()`: Decodes UTF-8 plain text files.

3. **`utils/extractor.py`**:
   - `SKILLS_DB`: Dictionary of 100+ technologies across AI/ML, Web, Cloud, Databases, DevOps, Data Engineering, and Soft Skills.
   - `extract_name()`: Cleans and formats candidate names into Title Case.
   - `extract_email()` & `extract_phone()`: Regex contact detail matching.
   - `extract_education()`: Captures degrees (`B.E.`, `B.Tech`, `M.Tech`, `M.Sc`, `BCA`, `MCA`, `MBA`, `Diploma`, `HSC`, `SSLC`), colleges, universities, and CGPA/GPA scores.
   - `extract_experience_years()`: Computes total years explicitly or from date ranges (`2021 - 2025`).
   - `extract_linkedin()` & `extract_github()`: Social profile link extractors.
   - `extract_summary()` & `extract_projects()`: Extracts candidate summary and key academic/professional projects.

4. **`utils/scorer.py`**:
   - `compute_tfidf_score()`: Calculates n-gram TF-IDF cosine similarity between resume and JD text.
   - `skill_gap_analysis()`: Computes matched vs missing skill sets without duplicate case variations.
   - `score_resume()`: Generates composite score based on customizable weights:
     $$\text{Composite Score} = (w_{\text{tfidf}} \times \text{TF-IDF}) + (w_{\text{skill}} \times \text{Skill Match}) + (w_{\text{exp}} \times \text{Experience Match})$$
   - `rank_candidates()`: Ranks candidates in descending order and assigns tier badges.

5. **`utils/visualizer.py`**:
   - `score_bar_chart()`: Horizontal candidate ranking bar chart.
   - `score_distribution()`: Score frequency histogram.
   - `skill_frequency_chart()`: Top skills bar chart across all resumes.
   - `skill_gap_sunburst()`: Sunburst hierarchy chart of matched vs missing skills per candidate.
   - `radar_chart()`: Polar radar comparison chart across scoring dimensions.
   - `experience_distribution()`: Experience breakdown pie chart.

---

## ⚙️ How Scoring Works

The default scoring model allocates weights as follows (configurable in UI):

| Metric | Weight | Description |
|---|---|---|
| **Content Match (TF-IDF)** | 50% | Cosine similarity between TF-IDF text vectors of resume and JD |
| **Skill Match** | 40% | Percentage of extracted JD keywords present in the candidate's resume |
| **Experience Match** | 10% | Candidate experience relative to required minimum years |

---

## 🧪 Testing & Verification

Run the automated test script to verify all parser, extractor, scorer, and visualizer functions:

```bash
python test_app.py
```

---

## 🚀 Quick Start & Commands to Run

### 1. Navigate to Project Directory

```powershell
cd "f:\AI-Resume-Screening (2)\AI-Resume-Screening\AI-Resume-Screening"
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run Streamlit Application

```powershell
streamlit run app.py
```

### 4. Open in Browser

Navigate to **`http://localhost:8501`** in your browser.
