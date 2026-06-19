from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.url import URLStats
from app.services import url_service

router = APIRouter()

@router.get("/{short_code}", response_model=URLStats)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url_obj = url_service.get_url_stats(db, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return url_obj