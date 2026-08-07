🤖 AI Resume Screening & Candidate Ranking System

An AI-powered Resume Screening & Candidate Ranking System that automates candidate evaluation by extracting resume information, analyzing job relevance, and ranking applicants using Natural Language Processing (NLP) and Machine Learning techniques.

Built with Streamlit, Scikit-learn, Plotly, and advanced document parsing libraries, the application enables recruiters to efficiently process multiple resumes, identify the most suitable candidates, and visualize hiring insights through an interactive dashboard.

📌 Project Overview

The AI Resume Screening System streamlines the recruitment process by automatically parsing resumes, extracting candidate information, comparing resumes with job descriptions, and generating intelligent candidate rankings.

The application supports multiple resume formats, performs TF-IDF-based semantic matching, identifies skill gaps, and provides interactive analytics for data-driven hiring decisions.

✨ Key Features
Bulk Resume Processing supporting PDF, DOCX, and TXT files
Dual PDF Parsing Engine using pdfplumber with PyPDF fallback
NLP-based Entity Extraction for candidate information
AI Resume Ranking using TF-IDF Vectorization and Cosine Similarity
Skill Gap Analysis with matched, missing, and additional skills
Composite Candidate Scoring using configurable weighted metrics
Interactive Candidate Dashboard with detailed profile insights
Analytics Dashboard powered by Plotly visualizations
CSV & JSON Export for screening reports
🛠 Technology Stack
Category	Technologies
Frontend	Streamlit
Machine Learning	Scikit-learn, NLTK
NLP	Regular Expressions, TF-IDF, Cosine Similarity
Document Processing	pdfplumber, PyPDF, python-docx
Data Processing	Pandas, NumPy
Visualization	Plotly
Export	CSV, JSON
🏗 System Architecture
                  Resume Upload
                        │
                        ▼
          Multi-format Document Parser
      (PDF • DOCX • TXT Extraction)
                        │
                        ▼
             NLP Entity Extraction
                        │
                        ▼
         Candidate Information Database
                        │
                        ▼
         Job Description Processing
                        │
                        ▼
          TF-IDF Vectorization Engine
                        │
                        ▼
         Cosine Similarity Calculation
                        │
                        ▼
      Skill Gap & Experience Evaluation
                        │
                        ▼
      Weighted Composite Score Engine
                        │
                        ▼
          Candidate Ranking Module
                        │
                        ▼
      Analytics Dashboard & Export
📂 Project Structure
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
    ├── parser.py
    ├── extractor.py
    ├── scorer.py
    └── visualizer.py
📑 Module Description
app.py

The main Streamlit application responsible for managing the complete workflow, including resume uploads, job description input, candidate evaluation, analytics visualization, and report generation.

parser.py

Implements a robust document parsing engine capable of extracting textual information from multiple document formats.

Responsibilities

PDF parsing using pdfplumber
PyPDF fallback parser
DOCX parser
TXT parser
extractor.py

Performs NLP-based information extraction from resumes.

Extracted Information
Candidate Name
Email Address
Phone Number
LinkedIn Profile
GitHub Profile
Education
Technical Skills
Soft Skills
Experience
Projects
Professional Summary
scorer.py

Implements the AI scoring pipeline.

Core Functions
TF-IDF Vectorization
Cosine Similarity Matching
Skill Match Calculation
Experience Evaluation
Composite Score Generation
Candidate Ranking
visualizer.py

Generates interactive analytics using Plotly.

Available Visualizations
Candidate Ranking
Score Distribution
Skill Frequency Analysis
Skill Gap Sunburst
Experience Distribution
Candidate Radar Comparison
🎯 Candidate Scoring Methodology

The application evaluates each resume using a weighted scoring model.

Component	Weight
Content Similarity (TF-IDF)	50%
Skill Matching	40%
Experience Match	10%
Composite Score
Score=(0.50×Content Match)+(0.40×Skill Match)+(0.10×Experience Match)
📊 Analytics

The application provides comprehensive hiring analytics, including:

Candidate Score Distribution
Resume Ranking Leaderboard
Skill Frequency Analysis
Skill Gap Visualization
Experience Distribution
Candidate Performance Comparison
🚀 Installation
git clone <repository-url>

cd AI-Resume-Screening

pip install -r requirements.txt

streamlit run app.py
🧪 Testing

Execute the test suite using:

python test_app.py

The test module validates:

Resume Parsing
Entity Extraction
AI Scoring Engine
Candidate Ranking
Visualization Components
📈 Workflow
Resume Upload
      │
      ▼
Document Parsing
      │
      ▼
Information Extraction
      │
      ▼
Job Description Analysis
      │
      ▼
TF-IDF Similarity
      │
      ▼
Skill Matching
      │
      ▼
Experience Evaluation
      │
      ▼
Composite Score Generation
      │
      ▼
Candidate Ranking
      │
      ▼
Analytics & Export
