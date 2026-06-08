from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import url, analytics

app = FastAPI(
    title="URL Shortener API",
    description="Production-grade URL shortener with Redis caching",
    version="1.0.0",
    docs_url="/docs",    
    redoc_url="/redoc", 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url.router,       tags=["URLs"])
app.include_router(analytics.router, prefix="/stats", tags=["Analytics"])

@app.get("/")
def health_check():
    return {"status": "ok", "service": "url-shortener"}