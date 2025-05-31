from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from dotenv import load_dotenv
load_dotenv()  # sẽ tìm và load .env từ thư mục hiện tại
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
from typing import List
from models import Candidate, Education, Experience, Certification, Skill, Language
from candidate import CandidateIn, CandidateOut
from info_extract import extract_text_from_pdf, extract_info
from embedding import get_embedding
from database import init_db, SessionLocal # Make sure SessionLocal is imported


app = FastAPI() 
init_db()

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
    
    skill_text = ", ".join(info.get('skills', []))
    exp_text = "\n".join([e.get('description', '') for e in info.get('experience', [])])
    embedding = get_embedding(f"{skill_text}\n{exp_text}")

    # Add candidate 
    candidate = Candidate(
        full_name=info['full_name'],
        email=info.get('email', ''),
        phone=info.get('phone', ''),
        embedding=embedding
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # Add education
    for edu in info.get('education', []):
        db.add(Education(
            candidate_id=candidate.id,
            degree=edu.get('degree', ''),
            university=edu.get('university', ''),
            start_year=edu.get('start_year'),
            end_year=edu.get('end_year')
        ))
    
    # Add experience
    for exp in info.get('experience', []):
        db.add(Experience(
            candidate_id=candidate.id,
            job_title=exp.get('job_title', ''),
            company=exp.get('company', ''),
            start_date=exp.get('start_date'),
            end_date=exp.get('end_date'),
            description=exp.get('description')
        ))

    # Add certifications
    for cert in info.get('certifications', []):
        db.add(Certification(
            candidate_id=candidate.id,
            certificate_name=cert.get('certificate_name', ''),
            organization=cert.get('organization', '')
        ))
    
    # Add skills
    for skill_name in info.get('skills', []):
        skill = create_or_get_skill(db, skill_name)
        candidate.skills.append(skill)

    # Add languages
    for lang_name in info.get('languages', []):
        lang = create_or_get_language(db, lang_name)
        candidate.languages.append(lang)

    db.commit()  # Commit all changes at once
    db.refresh(candidate)

    output = CandidateOut(
        id=candidate.id,
        full_name=candidate.full_name,
        email=candidate.email,
        phone=candidate.phone,
        education=[e for e in info.get('education', [])],
        experience=[e for e in info.get('experience', [])],
        skills=[s.name for s in candidate.skills],
        certifications=[c for c in info.get('certifications', [])],
        languages=[l.name for l in info.get('languages', [])],
    )
    return output


# uvicorn scripts.main:app --reload
# Note: nếu chạy bị lỗi postgresql -> mở task bar -> kill postgresql server (do nó chiểm dụng cổng 5432)
