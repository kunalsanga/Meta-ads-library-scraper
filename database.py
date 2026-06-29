import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base

logger = logging.getLogger(__name__)

# Create the synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database schema if it does not exist."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
