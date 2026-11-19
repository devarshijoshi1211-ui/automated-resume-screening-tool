# System Architecture

## Project Overview

The Automated Resume Screening Tool helps recruiters organize,
analyze and rank resumes against a job description.

## Main Components

- Frontend: Next.js recruiter dashboard.
- Backend: FastAPI REST API.
- Database: SQLite.
- Resume extraction: PDF, DOCX and TXT support.
- Semantic matching: Sentence Transformers.
- Ranking: Semantic similarity, skill coverage and experience.

## Workflow

1. Recruiter creates a job.
2. Job details are saved in SQLite.
3. Recruiter uploads candidate resumes.
4. Resume text is extracted.
5. Candidate information and parsed details are stored.
6. The ranking API compares resumes with the job description.
7. Candidates are ranked by their calculated scores.
8. Recruiter reviews the results and makes the final decision.

## Database Tables

- jobs
- candidates
- resumes
- features
- rankings

## API Endpoints

- GET /
- GET /health
- POST /api/job/create
- POST /api/resume/upload/{candidate_id}
- POST /api/rank/{job_id}
