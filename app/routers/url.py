from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services import url_service
from app.core.config import settings

router = APIRouter()

@router.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    try:
        url_obj = url_service.create_short_url(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return URLResponse(
        short_code=url_obj.short_code,
        short_url=f"{settings.base_url}/{url_obj.short_code}",
        original_url=url_obj.original_url,
        clicks=url_obj.clicks,
        created_at=url_obj.created_at,
    )

@router.get("/{short_code}")
async def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url_obj = await url_service.resolve_url(db, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=url_obj.original_url, status_code=307)