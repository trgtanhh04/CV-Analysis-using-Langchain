from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from dotenv import load_dotenv
load_dotenv()  # sẽ tìm và load .env từ thư mục hiện tại
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List
from models import Candidate, Education, Experience, Certification, Skill, Language
from candidate import CandidateIn, CandidateOut
from info_extract import extract_text_from_pdf, extract_info
from embedding import get_embedding
from database import init_db, SessionLocal # Make sure SessionLocal is imported


# app = FastAPI() # Keep FastAPI app commented if only testing DB
init_db() # Initialize the database

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

# @app.post("/candidates/", response_model=CandidateOut)
# async def create_candidate(
#     file : UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     temp_path = f\"\"



# python scripts/main.py

if __name__ == "__main__":
    print("Running database test...")
    db_session = SessionLocal() # Changed from get_db() to SessionLocal() for direct use
    try:
        # Test 1: Create a new skill
        skill_name_to_test = "TestSkill123"
        print(f"Attempting to create skill: {skill_name_to_test}")
        
        # Check if skill already exists
        existing_skill = db_session.query(Skill).filter(Skill.name == skill_name_to_test).first()
        if existing_skill:
            print(f"Skill '{skill_name_to_test}' already exists. Deleting it for a clean test.")
            db_session.delete(existing_skill)
            db_session.commit()

        new_skill = Skill(name=skill_name_to_test)
        db_session.add(new_skill)
        db_session.commit()
        db_session.refresh(new_skill)
        print(f"Skill '{new_skill.name}' created with ID: {new_skill.id}")

        # Test 2: Retrieve the skill
        retrieved_skill = db_session.query(Skill).filter(Skill.name == skill_name_to_test).first()
        if retrieved_skill:
            print(f"Successfully retrieved skill: {retrieved_skill.name} (ID: {retrieved_skill.id})")
            print("Database test successful: Data was written and read.")
            
            # Clean up: Delete the test skill
            # print(f"Cleaning up: Deleting skill '{skill_name_to_test}'")
            # db_session.delete(retrieved_skill)
            # db_session.commit()
            # print("Test skill deleted.")
        else:
            print(f"Error: Could not retrieve skill '{skill_name_to_test}'.")
            print("Database test failed.")

    except Exception as e:
        print(f"An error occurred during the database test: {e}")
    finally:
        db_session.close()
        print("Database session closed.")