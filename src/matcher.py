from pathlib import Path
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import clean_text

def load_skills(path: str | Path) -> list[str]:
    skills = [line.strip().lower() for line in Path(path).read_text(encoding="utf-8").splitlines()]
    return sorted({s for s in skills if s and not s.startswith("#")})

def find_skills(text: str, skills: list[str]) -> list[str]:
    """Match whole skill phrases to reduce accidental substring matches."""
    normalized = clean_text(text)
    found = []
    for skill in skills:
        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, normalized):
            found.append(skill)
    return found

def similarity(jd: str, resume: str) -> float:
    docs = [clean_text(jd), clean_text(resume)]
    if not any(docs):
        return 0.0
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    try:
        matrix = vectorizer.fit_transform(docs)
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        return 0.0

def score_resume(jd: str, resume: str, required_skills: list[str]) -> dict:
    matched = find_skills(resume, required_skills)
    missing = [s for s in required_skills if s not in matched]
    coverage = len(matched) / len(required_skills) if required_skills else 0.0
    text_sim = similarity(jd, resume)
    final_score = (0.60 * text_sim + 0.40 * coverage) * 100
    return {
        "score": round(final_score, 2),
        "text_similarity": round(text_sim * 100, 2),
        "skill_coverage": round(coverage * 100, 2),
        "matched_skills": ", ".join(matched) if matched else "None",
        "missing_skills": ", ".join(missing) if missing else "None",
        "matched_count": len(matched),
        "required_count": len(required_skills),
    }
