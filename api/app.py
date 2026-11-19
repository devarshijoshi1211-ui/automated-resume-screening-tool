from fastapi import FastAPI
from pathlib import Path
import sqlite3

app = FastAPI(title='Automated Resume Screening API', version='1.0.0')
DB_PATH = Path('/content/drive/MyDrive/Resume Screening Project/Automated-Resume-Screening-Tool/data/resume_screening.db')

@app.get('/')
def home():
    return {'message': 'Automated Resume Screening API is running'}

@app.get('/health')
def health():
    conn = sqlite3.connect(DB_PATH)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    conn.close()
    return {'status': 'healthy', 'database_connected': True, 'tables': [row[0] for row in tables]}

from pydantic import BaseModel
from uuid import uuid4

class JobCreate(BaseModel):
    title: str
    jd_text: str
    must_have: str
    nice_to_have: str = ''
    min_exp_years: float = 0
    location: str = 'Remote'

@app.post('/api/job/create')
def create_job(job: JobCreate):
    job_id = 'JOB-' + str(uuid4())[:8]
    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)', (job_id, job.title, job.jd_text, job.must_have, job.nice_to_have, job.min_exp_years, job.location))
    conn.commit()
    conn.close()
    return {'message': 'Job created successfully', 'job_id': job_id}

from fastapi import UploadFile, File, Form, HTTPException
from datetime import datetime
import json, re
from pathlib import Path

@app.post('/api/resume/upload/{candidate_id}')
async def upload_resume(candidate_id: str, candidate_name: str = Form(...), file: UploadFile = File(...)):
    filename = Path(file.filename or '').name
    suffix = Path(filename).suffix.lower()
    if suffix not in ['.pdf', '.docx', '.txt']:
        raise HTTPException(status_code=400, detail='Only PDF, DOCX and TXT files are supported')
    upload_dir = Path(__file__).parent / 'uploads'
    upload_dir.mkdir(exist_ok=True)
    saved_path = upload_dir / (candidate_id + '_' + filename)
    saved_path.write_bytes(await file.read())
    from src.extractor import extract_text
    raw_text = extract_text(saved_path)
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail='No text could be extracted from this resume')
    skill_patterns = ['python', 'sql', 'excel', 'power bi', 'pandas', 'numpy', 'data visualization', 'statistics', 'machine learning', 'html', 'css', 'javascript', 'react', 'git', 'java', 'flask', 'rest api', 'scikit-learn', 'docker']
    parsed = {'skills': [s for s in skill_patterns if s in raw_text.lower()], 'years_exp': max(map(float, re.findall(r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?|y)\b', raw_text.lower())), default=None), 'education': next((e for e in ['B.Tech', 'BCA', 'MCA', 'M.Tech', 'B.Sc', 'M.Sc', 'MBA'] if e.lower() in raw_text.lower()), None)}
    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO candidates (id, name) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET name=excluded.name', (candidate_id, candidate_name))
    conn.execute('INSERT OR REPLACE INTO resumes (candidate_id, source, raw_text, parsed_json, updated_at) VALUES (?, ?, ?, ?, ?)', (candidate_id, filename, raw_text, json.dumps(parsed), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return {'message': 'Resume uploaded and parsed successfully', 'candidate_id': candidate_id, 'file_name': filename, 'parsed_data': parsed}

@app.post('/api/rank/{job_id}')
def rank_candidates(job_id: str):
    from src.semantic_matcher import semantic_similarity
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    job = conn.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
    if job is None:
        conn.close()
        raise HTTPException(status_code=404, detail='Job not found')
    must_skills = [s.strip().lower() for s in (job['must_have'] or '').split(',') if s.strip()]
    resumes = conn.execute('SELECT c.id, c.name, r.raw_text, r.parsed_json FROM candidates c JOIN resumes r ON c.id=r.candidate_id').fetchall()
    results = []
    for candidate in resumes:
        raw_text = candidate['raw_text'] or ''
        parsed = json.loads(candidate['parsed_json'] or '{}')
        matched = [s for s in must_skills if s in raw_text.lower()]
        missing = [s for s in must_skills if s not in matched]
        hits = len(matched)
        total = len(must_skills)
        years = float(parsed.get('years_exp') or 0)
        gap = 0.1 * (total - hits)
        similarity = semantic_similarity(job['jd_text'] or '', raw_text)
        coverage = hits / max(1, total)
        experience = 1.0 if float(job['min_exp_years'] or 0) <= 0 else min(1.0, years / float(job['min_exp_years']))
        score = 0.55 * similarity + 0.35 * coverage + 0.10 * experience - gap
        reasons = 'Matched: ' + ', '.join(matched) + '; Missing: ' + ', '.join(missing) + '; Experience: ' + str(years) + ' years; Human review required.'
        conn.execute('INSERT OR REPLACE INTO features VALUES (?, ?, ?, ?, ?, ?, ?)', (candidate['id'], job_id, similarity, hits, total, years, gap))
        conn.execute('INSERT OR REPLACE INTO rankings VALUES (?, ?, ?, ?, ?)', (job_id, candidate['id'], score, reasons, datetime.now().isoformat()))
        results.append({'candidate_id': candidate['id'], 'candidate_name': candidate['name'], 'score': round(score, 4), 'matched_skills': matched, 'missing_skills': missing, 'years_experience': years, 'reasons': reasons})
    conn.commit()
    conn.close()
    return sorted(results, key=lambda x: x['score'], reverse=True)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=['https://outlets-evaluate-coins-accent.trycloudflare.com'], allow_credentials=False, allow_methods=['*'], allow_headers=['*'])
