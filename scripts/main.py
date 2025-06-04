from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from dotenv import load_dotenv
load_dotenv() 
import sys
import os
from dateutil import parser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
from typing import List
from models import Candidate, Education, Experience, Certification, Skill, Language
from candidate import CandidateIn, CandidateOut
from info_extract import extract_text_from_pdf, extract_info
from vector_db import CandidateFaissIndex
from embedding import get_embedding
from database import init_db, SessionLocal 
from datetime import datetime, date


app = FastAPI() 

@app.get("/")
def read_root():
    return {"status": "API is live!"}

# Database for local
init_db()

# Database for production
faiss_index = None  
EMBED_DIM = 1536

# Procsess to handle None or empty values safely
def safe_get(value, default="Unknown"):
    if value is None:
        return default
    if isinstance(value, str) and value.strip() == "":
        return default
    return value

def parse_date(date_str):
    current_dt = datetime.now()

    if not isinstance(date_str, str) or not date_str.strip():
        return "Unknown"

    cleaned_date_str = date_str.strip().lower()

    # Handle common non-date strings
    if cleaned_date_str in ("present", "current", "now", "na", "n/a", "null", "", "unknown"):
        return "Unknown"
    
    try:
        parsed_dt = parser.parse(date_str.strip(), default=current_dt)
        return parsed_dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError, parser.ParserError):
        return "Unknown"
    except Exception:
        return "Unknown"


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_or_get_skill(db, name):
    obj = db.query(Skill).filter(Skill.name == name).first()
    if not obj:
        obj = Skill(name=name)
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj

def create_or_get_language(db, name):
    obj = db.query(Language).filter(Language.name == name).first()
    if not obj:
        obj = Language(name=name)
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj

# FastAPI route to create a candidate from a CV file
@app.post("/candidates/", response_model=CandidateOut)
async def create_candidate(
    file : UploadFile = File(...),
    db: Session = Depends(get_db)
):
    temp_path = f"data/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    text = extract_text_from_pdf(temp_path)
    info = extract_info(text)

    if not info.get('full_name'):
        raise HTTPException(status_code=400, detail="No full name found in CV")

    job_title = safe_get(info.get('job_title', 'Unknown'))
    skill_text = ", ".join(info.get('skills', []))

    embedding_input = f"Job Title: {job_title}\nSkills: {skill_text}"
    embedding = get_embedding(embedding_input)

    email = safe_get(info.get('email'), default="Unknown")
    existing_candidate = db.query(Candidate).filter(Candidate.email == email).first()

    if existing_candidate:
        raise HTTPException(status_code=400, detail="Candidate with this email already exists")

    candidate = Candidate(
        full_name=safe_get(info.get('full_name')),
        email=email,
        phone=safe_get(info.get('phone')),
        job_title=job_title,
        embedding=json.dumps(embedding.tolist()) if hasattr(embedding, 'tolist') else json.dumps(embedding) # Convert ndarray to list
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # Add education
    for edu in info.get('education', []):
        db.add(Education(
            candidate_id=candidate.id,
            degree=safe_get(edu.get('degree')),
            university=safe_get(edu.get('university')),
            start_year=str(edu.get('start_year') or 'Unknown'),
            end_year=str(edu.get('end_year') or 'Unknown')
        ))
    
    # Add experience
    for exp in info.get('experience', []):
        db.add(Experience(
            candidate_id=candidate.id,
            job_title=safe_get(exp.get('job_title')),
            company=safe_get(exp.get('company')),
            start_date=parse_date(exp.get('start_date')),
            end_date=parse_date(exp.get('end_date')),
            description=safe_get(exp.get('description'), default="Unknown")
        ))

    # Add certifications
    for cert in info.get('certifications', []):
        db.add(Certification(
            candidate_id=candidate.id,
            certificate_name=safe_get(cert.get('certificate_name')),
            organization=safe_get(cert.get('organization'))
        ))
    
    # Add skills
    for skill_name in info.get('skills', []):
        skill = create_or_get_skill(db, skill_name)
        candidate.skills.append(skill)

    # Add languages
    for lang_name in info.get('languages', []):
        lang = create_or_get_language(db, lang_name)
        candidate.languages.append(lang)

    db.commit()
    db.refresh(candidate)

    output = CandidateOut(
        id=candidate.id,
        full_name=candidate.full_name,
        email=candidate.email,
        phone=candidate.phone,
        job_title=safe_get(info.get('job_title', 'Unknown')),
        education=[
            {
                "degree": safe_get(e.get("degree")),
                "university": safe_get(e.get("university")),
                "start_year": str(e.get("start_year") or "Unknown"),
                "end_year": str(e.get("end_year") or "Unknown"),
            }
            for e in info.get('education', [])
        ],
        experience=[
            {
                "job_title": safe_get(e.get("job_title")),
                "company": safe_get(e.get("company")),
                "start_date": parse_date(e.get("start_date")),
                "end_date": parse_date(e.get("end_date")),
                "description": safe_get(e.get("description"), default="Unknown"),
            }
            for e in info.get('experience', [])
        ],
        skills=[s.name for s in candidate.skills],
        certifications=[
            {
                "certificate_name": safe_get(c.get("certificate_name")),
                "organization": safe_get(c.get("organization")),
            }
            for c in info.get('certifications', [])
        ],
        languages=[lang_obj.name for lang_obj in candidate.languages],
    )
    return output


# Searching candidates by attributes
@app.get("/candidates/search/", response_model=List[CandidateOut])
def search_candidates_semantic(
    job_title: str = None,
    skills: List[str] = None,
    db: Session = Depends(get_db),
    top_k: int = 5
):  
    
    # global faiss_index

    query_part = []
    if job_title:
        query_part.append(f"Job Title: {job_title}")
    if skills:
        query_part.append(f"Skills: {', '.join(skills)}")
    query = "\n".join(query_part).strip()

    all_candidates_ebd = db.query(Candidate).filter(Candidate.embedding.isnot(None)).all()
    if not all_candidates_ebd:
        raise HTTPException(status_code=404, detail="No candidates found")
    
    curr_faiss_index = CandidateFaissIndex(dim=EMBED_DIM)
    curr_faiss_index.add_embedding(all_candidates_ebd)

    query_embedding = get_embedding(query)
    candidates_ids = curr_faiss_index.search(query_embedding, k=top_k)
    # Erase candidates same ids
    candidates_ids = list(set(candidates_ids))

    results = db.query(Candidate).filter(Candidate.id.in_(candidates_ids)).all()
    results_dict = {c.id: c for c in results}
    sorted_candidates = [results_dict[cid] for cid in candidates_ids if cid in results_dict]


    if not sorted_candidates:
        raise HTTPException(status_code=404, detail="No candidates found")
    
    output = []
    for c in sorted_candidates:
        output.append(CandidateOut(
            id=c.id,
            full_name=c.full_name,
            email=c.email,
            phone=c.phone,
            job_title=safe_get(c.job_title, default="Unknown"),
            education=[
                {
                    "degree": safe_get(e.degree),
                    "university": safe_get(e.university),
                    "start_year": str(e.start_year or "Unknown"),
                    "end_year": str(e.end_year or "Unknown"),
                }
                for e in c.education
            ],
            experience=[
                {
                    "job_title": safe_get(e.job_title),
                    "company": safe_get(e.company),
                    "start_date": parse_date(e.start_date),
                    "end_date": parse_date(e.end_date),
                    "description": safe_get(e.description, default="Unknown"),
                }
                for e in c.experience
            ],
            skills=[s.name for s in c.skills],
            certifications=[
                {
                    "certificate_name": safe_get(cert.certificate_name),
                    "organization": safe_get(cert.organization),
                }
                for cert in c.certifications
            ],
            languages=[lang.name for lang in c.languages],
        ))
    return output
# uvicorn scripts.main:app --reload
# Note: nếu chạy bị lỗi postgresql -> mở task bar -> kill postgresql server (do nó chiểm dụng cổng 5432)

