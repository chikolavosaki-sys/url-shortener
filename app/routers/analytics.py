from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    
    return {"status": "stub", "code": short_code}