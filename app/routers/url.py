from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/shorten")
def shorten_url(db: Session = Depends(get_db)):
    
    return {"status": "stub"}

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    
    return {"status": "stub", "code": short_code}