from pathlib import Path
import argparse
import pandas as pd
from src.screening import screen_resumes

def main():
    parser = argparse.ArgumentParser(description="ATS-style resume screening simulator")
    parser.add_argument("--resumes", default="resumes", help="Folder containing PDF/DOCX/TXT resumes")
    parser.add_argument("--jd", default="data/job_description.txt", help="Job description text file")
    parser.add_argument("--skills", default="data/required_skills.txt", help="One required skill per line")
    parser.add_argument("--threshold", type=float, default=40.0, help="Shortlist score threshold (0-100)")
    parser.add_argument("--output", default="outputs", help="Output folder")
    args = parser.parse_args()

    results = screen_resumes(args.resumes, args.jd, args.skills, args.threshold)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    results.to_csv(out / "screening_results.csv", index=False)
    results[results["decision"] == "SHORTLIST"].to_csv(out / "shortlisted_candidates.csv", index=False)
    results[results["decision"] == "REVIEW"].to_csv(out / "review_candidates.csv", index=False)

    if results.empty:
        print("No supported resume files found.")
        return
    display_cols = ["candidate", "score", "skill_coverage", "matched_skills", "missing_skills", "decision"]
    print("\nRESUME SCREENING RESULTS")
    print(results[display_cols].to_string(index=False))
    print(f"\nProcessed {len(results)} resume(s).")
    print(f"Shortlisted: {(results['decision'] == 'SHORTLIST').sum()}")
    print(f"Review: {(results['decision'] == 'REVIEW').sum()}")
    print(f"Reports saved in: {out.resolve()}")

if __name__ == "__main__":
    main()
