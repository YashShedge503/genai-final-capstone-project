from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from src.config import Config

Base = declarative_base()

class LogRecord(Base):
    __tablename__ = 'log_records'

    id = Column(Integer, primary_key=True)
    log_id = Column(String, unique=True, index=True)  # Cloud Provider ID
    timestamp = Column(DateTime, default=datetime.utcnow)
    service_name = Column(String)
    severity = Column(String)
    message = Column(Text)
    
    # AI Analysis Fields
    is_resolved = Column(Boolean, default=False)
    ai_root_cause = Column(Text, nullable=True)
    ai_suggested_fix = Column(Text, nullable=True)
    ai_generated_code = Column(Text, nullable=True)

# Database Setup
engine = create_engine(Config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()