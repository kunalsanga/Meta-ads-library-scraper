from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Ad(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(255), index=True, nullable=False)
    ad_number = Column(Integer, nullable=False)
    platform = Column(String(255), nullable=True)
    status = Column(String(100), nullable=True)
    started_date = Column(String(100), nullable=True)
    primary_text = Column(Text, nullable=True)
    headline = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    cta = Column(String(100), nullable=True)
    landing_page = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    screenshot_path = Column(String(500), nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
