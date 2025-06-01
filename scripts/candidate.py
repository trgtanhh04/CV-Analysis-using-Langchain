from pydantic import BaseModel
from typing import List, Optional

class Education(BaseModel):
    degree: Optional[str] = None
    university: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None

class Experience(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class Certification(BaseModel):
    certificate_name: Optional[str] = None
    organization: Optional[str] = None

class CandidateIn(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    education: List[Education] = []
    experience: List[Experience] = []
    skills: List[str] = []
    certifications: List[Certification] = []
    languages: List[str] = []

class CandidateOut(CandidateIn):
    id: int
