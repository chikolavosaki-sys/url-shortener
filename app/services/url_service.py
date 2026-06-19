import random
import string
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.models.url import URL
from app.schemas.url import URLCreate
from app.core.config import settings
from app.services.cache_service import get_cached_url, set_cached_url


def _generate_code(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def create_short_url(db: Session, payload: URLCreate) -> URL:
    code = payload.custom_code

    if code:
        if db.query(URL).filter(URL.short_code == code).first():
            raise ValueError(f"Code '{code}' is already in use.")
    else:
        for _ in range(5):
            code = _generate_code(settings.short_code_length)
            if not db.query(URL).filter(URL.short_code == code).first():
                break
        else:
            raise RuntimeError("Could not generate a unique code. Try again.")

    url_obj = URL(original_url=str(payload.original_url), short_code=code)
    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)
    return url_obj


async def resolve_url(db: Session, short_code: str) -> URL | None:
    cached = await get_cached_url(short_code)
    if cached:
        db.execute(update(URL).where(URL.short_code == short_code).values(clicks=URL.clicks + 1))
        db.commit()
        return URL(short_code=short_code, original_url=cached, clicks=0)

    url_obj = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_obj:
        return None

    await set_cached_url(short_code, url_obj.original_url)
    url_obj.clicks += 1
    db.commit()
    db.refresh(url_obj)
    return url_obj


def get_url_stats(db: Session, short_code: str) -> URL | None:
    return db.query(URL).filter(URL.short_code == short_code).first()