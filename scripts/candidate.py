from pydantic import BaseModel
from typing import List, Optional

class Education(BaseModel):
    degree: str
    university: str
    start_year: int
    end_year: int

class Experience(BaseModel):
    job_title: str
    company: str
    start_date: str
    end_date: str
    description: str

class Certification(BaseModel):
    certificate_name: str
    organization: str

class CandidateIn(BaseModel):
    full_name: str
    email: str
    phone: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
    certifications: List[Certification] 
    languages: List[str]

class CandidateOut(CandidateIn):
    id: int

