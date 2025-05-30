from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Candidate, Education, Experience, Certification, Skill, Language
from candidate import CandidateIn, CandidateOut
from info_extract import extract_text_from_pdf, extract_info
from embedding import get_embedding
from database import init_db, SessionLocal

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
    temp_path = f""