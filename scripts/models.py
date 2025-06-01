from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Text,
    JSON,
    Table,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

candidate_skills = Table(
    'candidate_skills',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

candidate_languages = Table(
    'candidate_languages',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)


class Education(Base):
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    degree = Column(String, nullable=True)
    university = Column(String, nullable=True)
    start_year = Column(String, nullable=True)
    end_year = Column(String, nullable=True)

    candidate = relationship('Candidate', back_populates='education')


class Experience(Base):
    __tablename__ = 'experience'

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    start_date = Column(String, nullable=True) 
    end_date = Column(String, nullable=True)   
    description = Column(Text, nullable=True)

    candidate = relationship('Candidate', back_populates='experience')


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    certificate_name = Column(String, nullable=True)  
    organization = Column(String, nullable=True)  

    candidate = relationship('Candidate', back_populates='certifications')


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    candidates = relationship('Candidate', secondary=candidate_skills, back_populates='skills')


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    candidates = relationship('Candidate', secondary=candidate_languages, back_populates='languages')


class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)  
    email = Column(String, nullable=True, unique=True) 
    phone = Column(String, nullable=True)
    embedding = Column(JSON, nullable=True)

    education = relationship('Education', back_populates='candidate', cascade='all, delete-orphan')
    experience = relationship('Experience', back_populates='candidate', cascade='all, delete-orphan')
    certifications = relationship('Certification', back_populates='candidate', cascade='all, delete-orphan')
    skills = relationship('Skill', secondary=candidate_skills, back_populates='candidates')
    languages = relationship('Language', secondary=candidate_languages, back_populates='candidates')
