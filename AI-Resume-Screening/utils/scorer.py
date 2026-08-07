"""
scorer.py – AI Scoring Engine using TF-IDF + Cosine Similarity.
Scores each resume against the job description and performs skill gap analysis.
"""
from typing import List, Dict, Tuple, Any
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def compute_tfidf_score(resume_text: str, jd_text: str) -> float:
    """
    Compute TF-IDF cosine similarity between resume and JD.
    Returns a float in [0, 1].
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    corpus = [preprocess_text(jd_text), preprocess_text(resume_text)]
    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True,
        )
        tfidf_matrix = vectorizer.fit_transform(corpus)
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score), 4)
    except Exception:
        return 0.0


def skill_gap_analysis(
    resume_skills: List[str], jd_keywords: List[str]
) -> Dict[str, List[str]]:
    """
    Compare resume skills against JD keywords without case duplicate variations.

    Returns:
        dict with 'matched', 'missing', 'extra' skill lists.
    """
    resume_map = {s.lower(): s for s in resume_skills}
    jd_map = {k.lower(): k for k in jd_keywords}

    matched_keys = sorted(set(resume_map.keys()) & set(jd_map.keys()))
    missing_keys = sorted(set(jd_map.keys()) - set(resume_map.keys()))
    extra_keys = sorted(set(resume_map.keys()) - set(jd_map.keys()))

    matched = [jd_map[k] for k in matched_keys]
    missing = [jd_map[k] for k in missing_keys]
    extra = [resume_map[k] for k in extra_keys]

    return {"matched": matched, "missing": missing, "extra": extra}


def compute_skill_score(matched: List[str], jd_keywords: List[str]) -> float:
    """
    Bonus score based on skill match ratio.
    Returns a float in [0, 1].
    """
    if not jd_keywords:
        return 0.0
    return round(len(matched) / len(jd_keywords), 4)


def compute_experience_score(resume_years: int, required_years: int) -> float:
    """
    Score based on years of experience.
    Returns 1.0 if meets/exceeds requirement, scaled below.
    """
    if required_years <= 0:
        return 1.0
    return round(min(resume_years / required_years, 1.0), 4)


def score_resume(
    candidate: Dict[str, Any],
    jd_text: str,
    jd_keywords: List[str],
    required_experience: int = 0,
    weights: Dict[str, float] = None,
) -> Dict[str, Any]:
    """
    Score a single candidate resume against the JD.

    Args:
        candidate: Output dict from extractor.extract_all()
        jd_text: Raw job description text
        jd_keywords: Extracted keywords from JD
        required_experience: Minimum years required (0 = ignore)
        weights: Scoring weight dict {'tfidf': float, 'skill': float, 'experience': float}

    Returns:
        candidate dict enriched with scoring fields.
    """
    if weights is None:
        weights = {"tfidf": 0.50, "skill": 0.40, "experience": 0.10}

    # Normalize weights
    total_w = sum(weights.values())
    weights = {k: v / total_w for k, v in weights.items()}

    # Re-evaluate candidate skills including extracted JD keywords to ensure complete match
    from utils.extractor import extract_skills
    candidate["skills"] = extract_skills(candidate["raw_text"], jd_keywords)

    # Individual scores
    tfidf_score = compute_tfidf_score(candidate["raw_text"], jd_text)
    gap = skill_gap_analysis(candidate["skills"], jd_keywords)
    skill_score = compute_skill_score(gap["matched"], jd_keywords)
    exp_score = compute_experience_score(
        candidate.get("experience_years", 0), required_experience
    )

    # Weighted composite
    composite = (
        weights["tfidf"] * tfidf_score
        + weights["skill"] * skill_score
        + weights["experience"] * exp_score
    )

    candidate.update(
        {
            "tfidf_score": tfidf_score,
            "skill_score": skill_score,
            "experience_score": exp_score,
            "composite_score": round(composite, 4),
            "percentage_score": round(composite * 100, 1),
            "matched_skills": gap["matched"],
            "missing_skills": gap["missing"],
            "extra_skills": gap["extra"],
        }
    )
    return candidate


def rank_candidates(
    candidates: List[Dict[str, Any]],
    jd_text: str,
    jd_keywords: List[str],
    required_experience: int = 0,
    weights: Dict[str, float] = None,
) -> List[Dict[str, Any]]:
    """
    Score and rank all candidates by composite score (descending).

    Returns:
        List of enriched candidate dicts, sorted best → worst.
    """
    scored = [
        score_resume(c, jd_text, jd_keywords, required_experience, weights)
        for c in candidates
    ]
    ranked = sorted(scored, key=lambda x: x["composite_score"], reverse=True)

    # Add rank number
    for i, c in enumerate(ranked, start=1):
        c["rank"] = i

    return ranked


def get_tier(score: float) -> Tuple[str, str]:
    """
    Return a human-readable tier label and color for a composite score.

    Returns:
        (label, hex_color)
    """
    pct = score * 100
    if pct >= 75:
        return "🏆 Excellent", "#22c55e"
    elif pct >= 55:
        return "✅ Good", "#3b82f6"
    elif pct >= 35:
        return "⚠️ Average", "#f59e0b"
    else:
        return "❌ Below Average", "#ef4444"
