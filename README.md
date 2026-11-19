# Automated Resume Screening Tool

A beginner-friendly Python project that simulates an Applicant Tracking System (ATS) workflow. It extracts text from PDF, DOCX, and TXT resumes, matches resumes against a job description, calculates transparent matching scores, ranks candidates, and exports CSV reports.

> **Important:** This is an educational screening simulator. Scores indicate textual and configured-skill overlap; they do not measure a person's ability or predict job performance. Do not use it as an automated hiring/rejection system. Recruiters must review original resumes and make decisions with appropriate human oversight.

## Problem statement

Recruiters may receive many resumes for one vacancy. Manually comparing every resume with job requirements can be repetitive. This project demonstrates how Python can automate document ingestion, text preprocessing, skill matching, similarity scoring, ranking, and report generation.

## Features

- Read `.pdf`, `.docx`, and `.txt` resumes.
- Read a job description from a text file.
- Configure required skills in a plain text file.
- Normalize text using regular expressions.
- Identify required skills using phrase-aware matching.
- Compare job description and resume with TF-IDF and cosine similarity.
- Calculate a weighted score and rank candidates.
- Export overall, shortlisted, and review CSV reports.
- Explain matched and missing skills for each resume.

## Technology stack

Python 3.11+, Pandas, NumPy, pdfplumber, python-docx, Scikit-learn, TF-IDF, Sentence Transformers, FastAPI, SQLite, Next.js, React, and Cloudflare Quick Tunnels.

## Folder structure

    Automated-Resume-Screening-Tool/
        ├── api/
            │   ├── app.py
                │   └── uploads/
                    ├── data/
                        │   ├── job_description.txt
                            │   ├── required_skills.txt
                                │   └── resume_screening.db
                                    ├── docs/
                                        │   ├── architecture.md
                                            │   ├── scoring-methodology.md
                                                │   └── responsible-ai.md
                                                    ├── frontend/
                                                        │   ├── app/
                                                            │   └── package.json
                                                                ├── images/
                                                                    ├── outputs/
                                                                        ├── resumes/
                                                                            ├── src/
                                                                                │   ├── extractor.py
                                                                                    │   ├── matcher.py
                                                                                        │   ├── preprocessing.py
                                                                                            │   ├── screening.py
                                                                                                │   └── semantic_matcher.py
                                                                                                    ├── main.py
                                                                                                        ├── requirements.txt
                                                                                                            ├── .gitignore
                                                                                                                └── README.md

                                                                                                                ## Installation

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python main.py
```

Customize the threshold or input paths:

```bash
python main.py --resumes resumes --jd data/job_description.txt --skills data/required_skills.txt --threshold 40 --output outputs
```

## Scoring method

The project uses:

`final_score = (0.60 * tfidf_cosine_similarity + 0.40 * required_skill_coverage) * 100`

Both component values are between 0 and 1. The command-line entry point (`main.py`) uses a default threshold of 40 points. The underlying `screen_resumes()` function has a default of 60 when called directly without a threshold. Records at or above the supplied threshold are labeled `SHORTLIST`; others are labeled `REVIEW`. This is a configurable demonstration rule, not a validated hiring standard.

## Generated reports

- `outputs/screening_results.csv` — all processed resumes.
- `outputs/shortlisted_candidates.csv` — candidates at or above the configured score threshold.
- `outputs/review_candidates.csv` — candidates below the threshold.

Each row includes score, text similarity, skill coverage, matched skills, missing skills, decision, and notes.

## Sample data

The `resumes/` folder contains three synthetic TXT resumes for demonstration. Add your own synthetic or consented sample PDF/DOCX files to test document extraction. Scanned/image-only PDFs require OCR and are not supported by this version.

## Screenshots

After running the project, capture:
1. Project folder in your editor.
2. Sample resumes and job description.
3. Terminal output showing ranked results.
4. `screening_results.csv` opened in a spreadsheet.
5. Shortlisted and review CSV files.
6. GitHub repository home page.

Save screenshots in `images/` and add them here, for example:

```markdown
![Terminal results](images/terminal-output.png)
```

## Limitations and responsible use

- Skill extraction uses a manually maintained dictionary; it can miss synonyms and context.
- TF-IDF measures word/phrase overlap, not deep semantic understanding.
- Resume layouts and extraction quality vary.
- Scanned PDFs need OCR.
- The original CLI scoring formula does not include experience. The advanced API uses an estimated experience value extracted with regular expressions; this estimate may be inaccurate.
- Names, age, gender, caste, religion, disability, photo, and other sensitive/protected attributes must not be used for ranking.
- Do not infer candidate quality from missing keywords alone.
- Keep personal data secure, obtain permission for test data, and delete it when no longer needed.
- Every candidate must receive human review; the tool should assist, not replace, recruiters.

## Learning outcomes

- Python modules and functions.
- File handling and document parsing.
- Text cleaning with regular expressions.
- Data processing with Pandas.
- NLP feature extraction with TF-IDF.
- Similarity measurement with cosine similarity.
- Ranking and CSV report generation.
- Git/GitHub project documentation.

## Future enhancements

- Streamlit recruiter dashboard.
- FastAPI endpoints and SQLite persistence.
- Synonym-aware skill normalization and RapidFuzz.
- Sentence Transformer semantic similarity.
- OCR for scanned resumes.
- Unit tests and labeled-dataset evaluation.
- Human feedback and fairness monitoring.

## License

Choose a license appropriate for your intended use before publishing.


## Advanced architecture

The project also includes an advanced recruiter workflow:

- **FastAPI:** REST API for job creation, resume upload and candidate ranking.
- **Next.js:** Web-based recruiter dashboard.
- **SQLite:** Persistent storage for jobs, candidates, resumes, extracted features and rankings.
- **Resume parsing:** Extracts skills, estimated years of experience and education.
- **RapidFuzz:** Tested separately for fuzzy skill matching; it is not currently integrated into the active ranking API.
- **Sentence Transformers:** Uses the all-MiniLM-L6-v2 model for semantic similarity.
- **Evaluation:** Demonstrates ROC-AUC, PR-AUC, precision, recall, F1-score and Top-K precision.

### API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Check API and database |
| POST | `/api/job/create` | Create a job |
| POST | `/api/resume/upload/{candidate_id}` | Upload and parse a resume |
| POST | `/api/rank/{job_id}` | Rank candidates for a job |

### Advanced scoring method

The advanced ranking API uses:

`score = 0.55 × semantic_similarity + 0.35 × skill_coverage + 0.10 × experience_score − gap_penalty`

The gap penalty is calculated as:

`gap_penalty = 0.10 × (required_skill_count − matched_skill_count)`

This is a demonstration scoring formula. Scores are not probabilities or validated measures of candidate quality.

The original command-line screening pipeline separately uses TF-IDF similarity and required-skill coverage.

### Database

SQLite stores five tables:

- `jobs`
- `candidates`
- `resumes`
- `features`
- `rankings`

### Evaluation results

A small synthetic demonstration dataset was used to test the ranking evaluation pipeline. The initial three-candidate evaluation produced ROC-AUC and PR-AUC values of 1.0.

These results are illustrative only. The dataset is too small and its relevance labels are manually assigned, so these metrics do not establish real-world model performance.

## Deployment and demonstration

The FastAPI backend and Next.js dashboard were run in Google Colab for demonstration. Cloudflare Quick Tunnels were used to expose the local development servers for browser testing.

Quick Tunnels are temporary development links and are not a production deployment.

For production use, add authentication, authorization, secure file storage, upload limits, HTTPS, logging, monitoring and appropriate data-retention controls.

## Responsible AI and privacy

- Use synthetic or consented resumes for testing.
- Collect only information needed for the screening task.
- Do not use protected or sensitive personal attributes in scoring.
- Keep recruiters responsible for all hiring decisions.
- Provide explanations of matched and missing job skills.
- Secure candidate information and delete it when no longer required.
- Treat automated rankings as decision-support information only.

## Updated future enhancements

- OCR support for scanned resumes.
- More robust employment-date and experience calculation.
- Improved synonym-aware skill extraction and contextual matching.
- Unit and integration testing.
- Evaluation on a larger, representative and independently labelled dataset.
- Production deployment with authentication and secure storage.
- Fairness testing and ongoing monitoring.
- Recruiter feedback and audit capabilities.
