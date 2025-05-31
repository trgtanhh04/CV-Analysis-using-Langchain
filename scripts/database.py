from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Base
from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)  # Bỏ connect_args
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(bind=engine)