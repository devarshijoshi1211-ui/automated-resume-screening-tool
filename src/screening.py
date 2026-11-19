from pathlib import Path
import pandas as pd
from .extractor import extract_text, SUPPORTED
from .matcher import load_skills, score_resume

def screen_resumes(resume_dir, jd_path, skills_path, threshold=60.0):
    resume_dir = Path(resume_dir)
    jd = Path(jd_path).read_text(encoding="utf-8")
    required_skills = load_skills(skills_path)
    rows = []

    for path in sorted(resume_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        try:
            resume_text = extract_text(path)
            if not resume_text.strip():
                raise ValueError("No text extracted; this may be a scanned PDF.")
            metrics = score_resume(jd, resume_text, required_skills)
            # Score threshold creates a review shortlist only; it is not a hiring decision.
            decision = "SHORTLIST" if metrics["score"] >= threshold else "REVIEW"
            rows.append({
                "candidate": path.stem,
                "file_name": path.name,
                **metrics,
                "decision": decision,
                "notes": "Human review required; score is a matching aid only."
            })
        except Exception as exc:
            rows.append({
                "candidate": path.stem, "file_name": path.name, "score": 0.0,
                "text_similarity": 0.0, "skill_coverage": 0.0,
                "matched_skills": "None", "missing_skills": ", ".join(required_skills),
                "matched_count": 0, "required_count": len(required_skills),
                "decision": "ERROR", "notes": str(exc)
            })

    if not rows:
        return pd.DataFrame(columns=["candidate", "file_name", "score", "text_similarity",
            "skill_coverage", "matched_skills", "missing_skills", "decision", "notes"])
    return pd.DataFrame(rows).sort_values(["score", "candidate"], ascending=[False, True]).reset_index(drop=True)
