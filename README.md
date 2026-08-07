# 🤖 AI Resume Screening & Candidate Ranking System

A **fully-featured AI-powered Resume Screening & Candidate Ranking Application** built using **Streamlit**, **Scikit-learn**, **NLTK**, **pdfplumber**, **PyPDF**, **python-docx**, and **Plotly**. The application automates resume screening by extracting candidate information, matching resumes against job descriptions, ranking applicants, and providing interactive analytics.

---

# 📌 Project Overview

The AI Resume Screening System is designed to simplify the recruitment process by automatically analyzing resumes, extracting important candidate information, calculating job relevance scores, and ranking candidates based on AI-powered matching algorithms.

The application supports bulk resume uploads, multiple document formats, NLP-based entity extraction, TF-IDF similarity scoring, skill gap analysis, and interactive dashboards for HR professionals.

---

# 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Frontend** | Streamlit, HTML, CSS |
| **Machine Learning** | Scikit-learn, NLTK |
| **Document Parsing** | pdfplumber, PyPDF, python-docx |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly |
| **Storage & Export** | CSV, JSON |

---

# ✨ Features

- 📤 Bulk Resume Upload (PDF, DOCX, TXT)
- 📄 Dual PDF Parsing (pdfplumber + PyPDF fallback)
- 🧠 NLP-based Candidate Information Extraction
- 🤖 TF-IDF & Cosine Similarity Resume Scoring
- 🎯 Skill Gap Analysis
- 🏆 Candidate Ranking System
- 👤 Detailed Candidate Profile Viewer
- 📊 Interactive Analytics Dashboard
- 💾 Export Results to CSV & JSON

---

# 📋 Functional Modules

## 📤 Resume Upload

- Upload multiple resumes simultaneously
- Supports PDF, DOCX, and TXT formats
- Preview uploaded candidate resumes

---

## 📄 Resume Parser

The parser extracts text from different document formats.

### Supported Formats

- PDF
- DOCX
- TXT

### PDF Parsing

- Primary Engine: **pdfplumber**
- Fallback Engine: **PyPDF**

---

## 🧠 NLP Entity Extraction

Automatically extracts:

- Candidate Name
- Email Address
- Phone Number
- LinkedIn Profile
- GitHub Profile
- Technical Skills
- Soft Skills
- Education Details
- Experience
- Projects
- Professional Summary

### Supported Education Detection

- B.E.
- B.Tech
- M.Tech
- M.Sc
- BCA
- MCA
- MBA
- Diploma
- HSC
- SSLC

---

## 🤖 AI Resume Scoring

Each resume is compared against the Job Description using TF-IDF Vectorization and Cosine Similarity.

### Composite Score Formula

```
Composite Score =
(Content Match × TF-IDF Weight)
+ (Skill Match × Skill Weight)
+ (Experience Match × Experience Weight)
```

### Default Weight Distribution

| Metric | Weight |
|---------|--------|
| TF-IDF Content Match | 50% |
| Skill Match | 40% |
| Experience Match | 10% |

---

## 🎯 Skill Gap Analysis

The system automatically identifies:

- ✅ Matched Skills
- ❌ Missing Skills
- ➕ Additional Skills

---

## 🏆 Candidate Ranking

Candidates are ranked based
