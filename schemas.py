from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AdSchema(BaseModel):
    brand_name: str
    ad_number: int = Field(..., ge=1, le=5)
    platform: Optional[str] = None
    status: Optional[str] = None
    started_date: Optional[str] = None
    primary_text: Optional[str] = None
    headline: Optional[str] = None
    description: Optional[str] = None
    cta: Optional[str] = None
    landing_page: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    screenshot_path: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
