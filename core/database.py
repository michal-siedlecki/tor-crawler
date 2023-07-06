from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(settings.DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()
