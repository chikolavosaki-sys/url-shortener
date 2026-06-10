# URL Shortener API

A production-grade URL shortener built with FastAPI, PostgreSQL, and Redis caching.

## Tech Stack

- **FastAPI** — async Python web framework
- **PostgreSQL** — persistent storage via SQLAlchemy ORM
- **Redis** — caching layer (TTL 1 hour) for fast redirects
- **Pydantic v2** — request/response validation
- **Docker Compose** — one-command local setup

## System Design

```
Client
  │
  ▼
FastAPI (Routers → Services → Schemas)
  │                    │
  ▼                    ▼
Redis              PostgreSQL
(cache HIT)        (cache MISS → write to Redis)
  │                    │
  └────────────────────┘
           │
           ▼
   Response to client
   307 redirect / JSON / 404
```

**POST /shorten** — writes directly to PostgreSQL  
**GET /{code}** — checks Redis first, falls back to PostgreSQL on miss  
**GET /stats/{code}** — reads click analytics from PostgreSQL  

## Getting Started

### Prerequisites

- Python 3.11+
- Docker Desktop running

### Run locally

```bash
git clone https://github.com/chikolavosaki-sys/url-shortener
cd url-shortener

cp .env.example .env

pip install -r requirements.txt

docker compose up -d

python -c "from app.database import engine; from app.models.url import URL; from app.database import Base; Base.metadata.create_all(engine)"

uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** to test all endpoints interactively.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/shorten` | Create a short URL |
| `GET` | `/{short_code}` | Redirect to original URL |
| `GET` | `/stats/{short_code}` | Get click analytics |

### Example

**Create a short URL:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://github.com"}'
```

```json
{
  "short_code": "aB3xZ9",
  "short_url": "http://localhost:8000/aB3xZ9",
  "original_url": "https://github.com/",
  "clicks": 0,
  "created_at": "2026-06-10T10:00:00"
}
```

**Create with custom code:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://youtube.com", "custom_code": "yt"}'
```

**Check analytics:**
```bash
curl http://localhost:8000/stats/aB3xZ9
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | required |
| `REDIS_URL` | Redis connection string | required |
| `BASE_URL` | Base URL for short links | `http://localhost:8000` |
| `SECRET_KEY` | App secret key | `change_me_in_production` |
| `SHORT_CODE_LENGTH` | Length of generated codes | `6` |

## Project Structure

```
url-shortener/
├── app/
│   ├── core/
│   │   ├── config.py       # Settings from .env
│   │   └── redis.py        # Async Redis client
│   ├── models/
│   │   └── url.py          # SQLAlchemy URL model
│   ├── schemas/
│   │   └── url.py          # Pydantic request/response schemas
│   ├── services/
│   │   ├── url_service.py  # Business logic
│   │   └── cache_service.py# Redis cache operations
│   ├── routers/
│   │   ├── url.py          # POST /shorten, GET /{code}
│   │   └── analytics.py    # GET /stats/{code}
│   ├── database.py         # SQLAlchemy engine + session
│   └── main.py             # FastAPI app entry point
├── tests/
├── docker-compose.yml
├── requirements.txt
└── .env.example
```
