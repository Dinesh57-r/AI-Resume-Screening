"""
extractor.py – NLP entity extraction from resume text.
Extracts: name, email, phone, skills, education, experience years.
"""
import re
from typing import Dict, List, Any


# ── Comprehensive skills keyword bank ─────────────────────────────────────────
SKILLS_DB = {
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go", "Golang",
    "Rust", "R", "Swift", "Kotlin", "Ruby", "PHP", "Scala", "MATLAB",
    "Perl", "Shell", "Bash", "PowerShell", "Dart", "Julia", "HTML", "HTML5", "CSS", "CSS3", "Sass", "SQL", "NoSQL",

    # Web Frameworks & Frontend/Backend
    "React", "React.js", "Angular", "Vue", "Vue.js", "Next.js", "Node.js", "Express.js",
    "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET", "Laravel",
    "Rails", "Svelte", "Nuxt.js", "Remix", "Gatsby", "Tailwind", "Tailwind CSS", "Bootstrap",
    "GraphQL", "REST", "REST API", "RESTful API", "Microservices", "WebSockets", "gRPC",

    # AI / ML / Data Science / MLOps
    "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "OpenCV",
    "Hugging Face", "LangChain", "LlamaIndex", "BERT", "GPT", "LLM", "LLMs",
    "Transformers", "XGBoost", "LightGBM", "CatBoost", "Random Forest",
    "Neural Networks", "CNN", "RNN", "LSTM", "GAN", "Reinforcement Learning",
    "Transfer Learning", "Feature Engineering", "Data Mining", "MLOps", "Generative AI",
    "Prompt Engineering", "RAG", "Vector DB", "Pinecone", "ChromaDB", "FAISS", "Milvus",

    # Data Engineering & Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
    "Elasticsearch", "Apache Spark", "Spark", "PySpark", "Hadoop", "Hive", "Kafka", "Airflow",
    "dbt", "Snowflake", "BigQuery", "Redshift", "DynamoDB", "Databricks", "ETL", "Data Pipeline",

    # Cloud & DevOps
    "AWS", "Amazon Web Services", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "K8s",
    "Terraform", "Ansible", "Jenkins", "GitHub Actions", "CI/CD", "Linux", "Unix", "Nginx",
    "Prometheus", "Grafana", "CloudFormation", "Lambda", "AWS Lambda", "EC2", "S3",

    # Data Analytics & BI
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Tableau",
    "Power BI", "Excel", "Advanced Excel", "Statistics", "Data Visualization",
    "A/B Testing", "Time Series", "Time Series Analysis", "DAX", "Power Query",

    # Testing & QA
    "Selenium", "Cypress", "PyTest", "Jest", "JUnit", "Unit Testing", "Integration Testing", "Automation Testing",

    # Soft Skills & Management
    "Leadership", "Communication", "Problem Solving", "Team Player",
    "Agile", "Scrum", "Kanban", "Project Management", "Critical Thinking",
    "Collaboration", "Mentoring", "System Design", "OOP", "Object-Oriented Programming",

    # Tools & Software
    "Git", "GitHub", "GitLab", "Jira", "Confluence", "Figma",
    "Postman", "VS Code", "IntelliJ", "Jupyter", "Notion", "Linux",
}

# Degree keywords for education extraction
DEGREE_KEYWORDS = [
    r"B\.Tech\.?|Bachelor(?:'s)? (?:of )?(?:Engineering|Technology|Science|Arts|Commerce)",
    r"M\.Tech\.?|Master(?:'s)? (?:of )?(?:Engineering|Technology|Science|Arts|Commerce|Business Administration)",
    r"\bMBA\b|\bMCA\b|\bBCA\b|\bBBA\b|B\.Sc\.?|M\.Sc\.?",
    r"Ph\.?D\.?|Doctorate|Doctor of Philosophy",
    r"Diploma|Associate(?:'s)? Degree|High School|12th|10th|\bSSC\b|\bHSC\b",
]

# Experience patterns
EXP_PATTERNS = [
    r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)",
    r"(?:experience|exp)\s*(?:of\s+)?(\d+)\+?\s*(?:years?|yrs?)",
    r"(\d+)\s*-\s*\d+\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)",
]


def extract_email(text: str) -> str:
    """Extract the first email address found in text."""
    pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    """Extract the first phone number found in text."""
    patterns = [
        r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        r"\b\d{10}\b",
        r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return ""


def extract_name(text: str) -> str:
    """
    Heuristic name extraction: first non-empty line that looks like a name.
    Formats ALL-CAPS names into Title Case.
    """
    skip_words = {
        "resume", "cv", "curriculum", "vitae", "profile", "summary",
        "objective", "experience", "education", "skills", "contact",
        "references", "projects", "achievements", "certifications",
        "awards", "address", "email", "phone", "linkedin", "github",
        "academic", "declaration", "personal", "details",
    }
    lines = text.split("\n")
    for line in lines[:20]:  # Check first 20 lines
        line = line.strip()
        if not line or len(line) < 2 or len(line) > 60:
            continue
        words = line.split()
        if not (1 <= len(words) <= 5):
            continue
        if any(char.isdigit() for char in line):
            continue
        if any(skip in line.lower() for skip in skip_words):
            continue
        if any(char in line for char in ["@", ":", "|", "/", "\\", "http"]):
            continue

        # Clean name
        clean_line = re.sub(r"[^\w\s.]", "", line).strip()
        if len(clean_line) >= 2:
            # Title Case if ALL CAPS
            if clean_line.isupper():
                return clean_line.title()
            return clean_line
    return "Unknown Candidate"


def extract_skills(text: str, jd_skills: List[str] = None) -> List[str]:
    """
    Extract skills from resume text by matching against SKILLS_DB.
    Optionally also checks against extracted JD skills.
    """
    found = set()
    text_lower = text.lower()

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)

    if jd_skills:
        for skill in jd_skills:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text_lower):
                found.add(skill)

    return sorted(found)


def extract_education(text: str) -> List[str]:
    """Extract degree, institution, and grade mentions from resume text."""
    found = []
    lines = text.split("\n")

    # 1. Regex degree pattern search
    degree_patterns = [
        r"\bB\.?E\.?\b|\bB\.?Tech\.?\b|\bBachelor(?:'s)? (?:of )?(?:Engineering|Technology|Science|Arts|Commerce|Computer Applications)\b",
        r"\bM\.?E\.?\b|\bM\.?Tech\.?\b|\bMaster(?:'s)? (?:of )?(?:Engineering|Technology|Science|Arts|Commerce|Business Administration|Computer Applications)\b",
        r"\bMBA\b|\bMCA\b|\bBCA\b|\bBBA\b|\bB\.Sc\.?\b|\bM\.Sc\.?\b|\bB\.Com\.?\b|\bM\.Com\.?\b",
        r"\bPh\.?D\.?\b|\bDoctorate\b|\bDoctor of Philosophy\b",
        r"\bDiploma\b|\bAssociate(?:'s)? Degree\b|\bHigh School\b|\b12th\b|\b10th\b|\bSSLC\b|\bHSC\b|\bCBSE\b|\bICSE\b",
    ]

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        for pat in degree_patterns:
            if re.search(pat, line_str, re.IGNORECASE):
                # Clean line length
                if len(line_str) <= 100:
                    found.append(line_str)
                else:
                    m = re.search(pat, line_str, re.IGNORECASE)
                    if m:
                        found.append(m.group(0))
                break

    # 2. Also search lines containing CGPA / GPA / College / University if degree wasn't captured
    if not found:
        for line in lines:
            line_str = line.strip()
            if any(k in line_str.lower() for k in ["cgpa", "gpa", "university", "college", "institute"]):
                if 5 <= len(line_str) <= 90:
                    found.append(line_str)

    # Deduplicate preserving order
    seen = set()
    result = []
    for item in found:
        item_clean = item.strip()
        if item_clean.lower() not in seen:
            seen.add(item_clean.lower())
            result.append(item_clean)

    return result if result else ["Higher Education / Technical Degree"]


def extract_experience_years(text: str) -> int:
    """Extract total years of experience or compute from date ranges in text."""
    max_years = 0

    # 1. Explicit pattern search
    for pattern in EXP_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                years = int(match)
                if years < 50:
                    max_years = max(max_years, years)
            except ValueError:
                pass

    if max_years > 0:
        return max_years

    # 2. Compute from date ranges (e.g. 2021 - 2024 or 2022 - Present)
    current_year = 2026
    date_ranges = re.findall(r"\b(20\d{2})\s*[-–to]+\s*(Present|Current|Now|20\d{2})\b", text, re.IGNORECASE)
    total_months = 0
    for start_str, end_str in date_ranges:
        try:
            start_yr = int(start_str)
            end_yr = current_year if end_str.lower() in ["present", "current", "now"] else int(end_str)
            if 1990 <= start_yr <= end_yr <= current_year:
                total_months += (end_yr - start_yr) * 12
        except ValueError:
            pass

    if total_months >= 12:
        return total_months // 12

    return 0


def extract_linkedin(text: str) -> str:
    """Extract LinkedIn URL or handle from resume text."""
    pattern = r"(?:https?://)?(?:www\.)?linkedin\.com/(?:in|pub|profile)/[\w\-\_]+"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        url = match.group(0)
        return url if url.startswith("http") else "https://" + url

    # Look for linkedin: handle
    h_match = re.search(r"linkedin\s*:\s*([\w\-\_]+)", text, re.IGNORECASE)
    if h_match:
        return f"https://linkedin.com/in/{h_match.group(1)}"
    return ""


def extract_github(text: str) -> str:
    """Extract GitHub URL or handle from resume text."""
    pattern = r"(?:https?://)?(?:www\.)?github\.com/[\w\-\_]+"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        url = match.group(0)
        return url if url.startswith("http") else "https://" + url

    # Look for github: handle
    h_match = re.search(r"github\s*:\s*([\w\-\_]+)", text, re.IGNORECASE)
    if h_match:
        return f"https://github.com/{h_match.group(1)}"
    return ""


def extract_summary(text: str) -> str:
    """Extract candidate profile summary / objective if present."""
    lines = text.split("\n")
    capturing = False
    summary_lines = []

    for line in lines:
        line_str = line.strip()
        if any(h in line_str.lower() for h in ["summary", "objective", "profile", "about me"]):
            capturing = True
            continue
        if capturing:
            if any(h in line_str.lower() for h in ["education", "experience", "skills", "projects", "certifications", "contact"]):
                break
            if line_str:
                summary_lines.append(line_str)
                if len(summary_lines) >= 4:
                    break

    return " ".join(summary_lines) if summary_lines else ""


def extract_projects(text: str) -> List[str]:
    """Extract key projects mentioned in resume."""
    lines = text.split("\n")
    projects = []
    capturing = False

    for line in lines:
        line_str = line.strip()
        if any(h in line_str.lower() for h in ["projects", "key projects", "academic projects"]):
            capturing = True
            continue
        if capturing:
            if any(h in line_str.lower() for h in ["education", "experience", "skills", "certifications", "contact", "declaration"]):
                break
            if line_str and (line_str.startswith("•") or line_str.startswith("-") or len(line_str) > 15):
                projects.append(line_str.lstrip("•- "))
                if len(projects) >= 5:
                    break

    return projects


def extract_all(text: str, filename: str = "", jd_skills: List[str] = None) -> Dict[str, Any]:
    """
    Run all extractors on resume text and return a structured dict.

    Returns:
        dict with keys: name, email, phone, skills, education,
                        experience_years, linkedin, github, summary, projects, filename, raw_text
    """
    cleaned = text.strip()
    return {
        "filename": filename,
        "name": extract_name(cleaned),
        "email": extract_email(cleaned),
        "phone": extract_phone(cleaned),
        "skills": extract_skills(cleaned, jd_skills),
        "education": extract_education(cleaned),
        "experience_years": extract_experience_years(cleaned),
        "linkedin": extract_linkedin(cleaned),
        "github": extract_github(cleaned),
        "summary": extract_summary(cleaned),
        "projects": extract_projects(cleaned),
        "raw_text": cleaned,
    }


def extract_keywords_from_jd(jd_text: str) -> List[str]:
    """
    Extract meaningful keywords and technical terms from a job description.
    Used for skill gap analysis.
    """
    found = set()
    jd_lower = jd_text.lower()

    # 1. Match against SKILLS_DB
    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, jd_lower):
            found.add(skill)

    # 2. Extract technical terms / capitalized acronyms (e.g. PySpark, REST, MLOps)
    tech_words = re.findall(r"\b[A-Z][A-Za-z0-9+#./-]{1,15}\b", jd_text)
    skip_common = {
        "We", "The", "Our", "Must", "Have", "With", "And", "For", "You", "Are", "Will",
        "Role", "Job", "Team", "Work", "Requirements", "Responsibilities", "Qualifications",
        "Candidate", "Company", "Experience", "Years", "Strong", "Good", "Knowledge", "Ability",
        "Skills", "Degree", "Position", "Full", "Senior", "Junior", "Lead", "Principal",
        "Manager", "Engineer", "Developer", "Analyst", "Seeking", "Looking", "Need", "Plus",
        "Must-have", "Nice-to-have", "Environment", "Project", "Products", "Solutions",
        "Nice", "Table", "Clear", "High", "Low", "Data", "Learning", "Machine", "Science", "Tech",
    }
    for tw in tech_words:
        tw_clean = tw.strip(".,;:()")
        if tw_clean not in skip_common and len(tw_clean) >= 2:
            found.add(tw_clean)

    return sorted(found, key=lambda x: x.lower())
