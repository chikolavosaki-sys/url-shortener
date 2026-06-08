from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Connection pool: reuse up to 10 open connections, refresh every hour
engine = create_engine(
    settings.database_url,
    pool_size=10,
    pool_recycle=3600,
    echo=False,  # set True to print every SQL query (good for debugging)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# FastAPI dependency — inject into routes with: db: Session = Depends(get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db          #  route handler runs here, with db available
    finally:
        db.close()        #  always runs after, returns connection to pool