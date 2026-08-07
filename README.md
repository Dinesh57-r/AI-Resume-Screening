# 🤖 AI Resume Screening & Candidate Ranking System

An intelligent **AI-powered Resume Screening & Candidate Ranking System** developed using **Streamlit**, **Scikit-learn**, and **Natural Language Processing (NLP)** techniques. The application automates resume parsing, candidate information extraction, job description matching, and candidate ranking, enabling recruiters to identify the most suitable applicants efficiently.

---

## 📖 Overview

The AI Resume Screening System simplifies the recruitment process by automatically analyzing resumes, extracting key candidate information, comparing resumes against job descriptions, and generating ranked candidate recommendations.

The application supports multiple resume formats, performs semantic similarity matching using **TF-IDF Vectorization** and **Cosine Similarity**, identifies skill gaps, and provides interactive dashboards for recruitment analytics.

---

## ✨ Features

- Bulk Resume Upload (PDF, DOCX, TXT)
- AI-based Resume Ranking
- TF-IDF & Cosine Similarity Matching
- Automatic Skill Extraction
- Candidate Information Extraction
- Skill Gap Analysis
- Experience Evaluation
- Interactive Analytics Dashboard
- Candidate Leaderboard
- CSV & JSON Export
- Dark Theme User Interface
- Modular Project Architecture

---

## 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Frontend | Streamlit |
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| NLP | NLTK, Regular Expressions |
| Document Parsing | pdfplumber, PyPDF, python-docx |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Export | CSV, JSON |

---

## 🏗 System Workflow

```text
Resume Upload
      │
      ▼
Document Parsing
(PDF • DOCX • TXT)
      │
      ▼
Text Extraction
      │
      ▼
Candidate Information Extraction
      │
      ▼
Job Description Processing
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Cosine Similarity Matching
      │
      ▼
Skill Gap Analysis
      │
      ▼
Experience Evaluation
      │
      ▼
Composite Score Calculation
      │
      ▼
Candidate Ranking
      │
      ▼
Analytics Dashboard
      │
      ▼
CSV / JSON Export
```

---

## 📂 Project Structure

```text
AI-Resume-Screening/
│
├── app.py
├── requirements.txt
├── README.md
├── test_app.py
│
├── sample_resumes/
│   ├── john_smith_data_scientist.txt
│   ├── priya_sharma_fullstack.txt
│   └── alex_johnson_ml_junior.txt
│
└── utils/
    ├── __init__.py
    ├── parser.py
    ├── extractor.py
    ├── scorer.py
    └── visualizer.py
```

---

# 📋 Modules

## app.py

Main Streamlit application responsible for

- Resume Upload
- Job Description Input
- Candidate Ranking
- Analytics Dashboard
- Export Functionality

---

## parser.py

Responsible for parsing resume documents.

Supported formats:

- PDF
- DOCX
- TXT

PDF extraction uses:

- pdfplumber
- PyPDF (Fallback)

---

## extractor.py

Extracts candidate information using NLP techniques.

### Extracted Information

- Candidate Name
- Email Address
- Phone Number
- LinkedIn Profile
- GitHub Profile
- Technical Skills
- Soft Skills
- Education
- Experience
- Projects
- Professional Summary

---

## scorer.py

Implements the AI ranking engine.

### Functions

- TF-IDF Vectorization
- Cosine Similarity
- Skill Matching
- Experience Matching
- Composite Score Calculation
- Candidate Ranking

---

## visualizer.py

Creates interactive Plotly visualizations.

Available charts include

- Candidate Ranking
- Score Distribution
- Skill Frequency
- Skill Gap Analysis
- Experience Distribution
- Radar Comparison

---

# 🎯 Candidate Scoring

Each resume is evaluated using a weighted scoring model.

| Metric | Weight |
|---------|---------|
| Content Similarity | 50% |
| Skill Match | 40% |
| Experience Match | 10% |

### Composite Score

```
Composite Score =
(Content Similarity × 50%)
+
(Skill Match × 40%)
+
(Experience Match × 10%)
```

---

## 📊 Analytics Dashboard

The application provides interactive recruitment analytics including:

- Candidate Ranking
- Score Distribution
- Skill Frequency Analysis
- Skill Gap Visualization
- Experience Distribution
- Candidate Comparison Dashboard

---

## 📤 Export

The screening results can be exported in:

- CSV
- JSON

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/your-username/AI-Resume-Screening.git
```

Navigate to the project directory

```bash
cd AI-Resume-Screening
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

Open your browser

```
http://localhost:8501
```

---

## 🧪 Testing

Run the automated test suite.

```bash
python test_app.py
```

The test validates

- Resume Parsing
- Entity Extraction
- AI Scoring
- Candidate Ranking
- Visualization Modules

---

## 📌 Future Enhancements

- Resume Parsing using Transformer Models
- BERT-based Semantic Matching
- OCR Support for Scanned PDFs
- Resume Recommendation Engine
- Recruiter Authentication
- Candidate Feedback System
- PostgreSQL Integration
- Cloud Deployment using AWS

---

## 📄 License

This project is developed for educational and portfolio purposes.

---

## 👨‍💻 Author

**Dinesh R**

**B.E. Computer Science and Engineering (Artificial Intelligence & Machine Learning)**

Sri Eshwar College of Engineering

GitHub: https://github.com/your-username

LinkedIn: https://linkedin.com/in/your-profile
