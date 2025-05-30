from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    Table,
    JSON,
    Date,
)

from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# relationship n-n between candidates and skills
candidate_skills = Table(
    'candidate_skills',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

# relationship n-n between candidates and languages
candidate_languages = Table(
    'candidate_languages',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)


class Education(Base):
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True, index=True)
    degree = Column(String, nullable=False)
    university = Column(String, nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)

    candidate = relationship('Candidate', back_populates='education')

class Experience(Base):
    __tablename__ = 'experience'

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)

    candidate = relationship('Candidate', back_populates='experience')


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    certificate_name = Column(String, nullable=False)
    organization = Column(String, nullable=False)

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
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    
    # 1-n relationships
    education = relationship('Education', back_populates='candidate', cascade='all, delete-orphan')
    experience = relationship('Experience', back_populates='candidate', cascade='all, delete-orphan')
    certifications = relationship('Certification', back_populates='candidate', cascade='all, delete-orphan')

    # n-n relationships
    skills = relationship('Skill', secondary=candidate_skills, back_populates='candidates')
    languages = relationship('Language', secondary=candidate_languages, back_populates='candidates')

    embedding = Column(JSON, nullable=True)  # For storing embeddings if needed
