# Production Deployment Guide

## Overview

This guide covers deploying the AI Analytics system to production.

---

## Prerequisites

- Docker (optional, for containerized deployment)
- Python 3.9+ environment
- Node.js 16+ environment
- Domain name (for production)
- SSL certificate

---

## Backend Deployment

### 1. Environment Variables

Create `.env` file in backend directory:

```env
# Server
HOST=0.0.0.0
PORT=8000

# CORS
ALLOWED_ORIGINS=["https://yourdomain.com"]

# Security
SECRET_KEY=your-secret-key-here

# Optional: Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### 2. Update CORS Settings

In `backend/app/main.py`, update CORS configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "https://api.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run with Gunicorn (Production)

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### 5. Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]
```

Build and run:

```bash
docker build -t stock-screener-backend .
docker run -p 8000:8000 stock-screener-backend
```

---

## Frontend Deployment

### 1. Environment Variables

Create `.env.production`:

```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_AI_ENABLED=true
```

### 2. Build for Production

```bash
cd frontend
npm install
npm run build
```

### 3. Deploy to Static Host

Deploy the `build` folder to:
- **Vercel**: `vercel deploy`
- **Netlify**: Drag and drop build folder
- **AWS S3**: Upload to S3 bucket with CloudFront
- **Nginx**: Copy to `/var/www/html`

### 4. Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Security Hardening

### 1. Add Authentication

Protect AI endpoints with JWT authentication:

```python
from app.api.auth import get_current_user

@router.post("/score")
def score_stock(stock: StockInput, current_user = Depends(get_current_user)):
    # Endpoint protected
```

### 2. Rate Limiting

Install slowapi:

```bash
pip install slowapi
```

Add to `main.py`:

```python
from slowapi import SlowAPILimiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()
app.add_middleware(SlowAPIMiddleware)
limiter = SlowAPILimiter(app=app)

@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

@router.post("/score")
@limiter.limit("10/minute")
def score_stock(stock: StockInput):
    ...
```

### 3. Input Validation

Add additional validation in production:

```python
from pydantic import validator

class StockInput(BaseModel):
    symbol: str
    
    @validator('symbol')
    def validate_symbol(cls, v):
        if not v.isalpha() or len(v) > 5:
            raise ValueError('Invalid symbol')
        return v.upper()
```

---

## Monitoring

### 1. Health Checks

Add monitoring endpoint:

```bash
curl https://api.yourdomain.com/api/ai/health
```

### 2. Logging

Configure logging in production:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### 3. Error Tracking

Integrate with error tracking services:
- **Sentry**: For error tracking
- **LogRocket**: For frontend monitoring
- **New Relic**: For performance monitoring

---

## Performance Optimization

### 1. Caching

Add Redis caching for AI results:

```python
import redis
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_ai_score(stock_data_hash):
    # Cached result
```

### 2. Database (Optional)

Store AI scores for historical tracking:

```python
# Add to database models
class AIScore(Base):
    symbol = Column(String)
    score = Column(Float)
    timestamp = Column(DateTime)
```

### 3. CDN

Use CDN for static assets:
- Cloudflare
- AWS CloudFront
- Fastly

---

## Testing Before Deployment

### 1. Run Test Suite

```bash
cd backend
python scripts/test_ai_endpoints.py
```

### 2. Load Testing

Use Apache Bench or similar:

```bash
ab -n 1000 -c 10 http://localhost:8000/api/ai/health
```

### 3. Security Scanning

- Run OWASP ZAP scan
- Check for vulnerabilities
- Review CORS settings

---

## Rollback Plan

### 1. Version Control

Keep previous versions tagged:

```bash
git tag v1.0.0-ai-release
git push --tags
```

### 2. Database Backups

If storing AI scores:

```bash
pg_dump your_db > backup.sql
```

### 3. Quick Rollback

```bash
git checkout previous-version
# Redeploy
```

---

## Post-Deployment Checklist

- [ ] All AI endpoints responding
- [ ] CORS configured correctly
- [ ] HTTPS enabled
- [ ] Rate limiting active
- [ ] Error tracking configured
- [ ] Monitoring dashboard set up
- [ ] Backups scheduled
- [ ] Documentation updated
- [ ] Team notified

---

## Support

For issues:
1. Check logs: `docker logs <container>` or `journalctl -u your-service`
2. Review error tracking dashboard
3. Check API health endpoint
4. Test endpoints manually

---

## Cost Estimates

**Small Scale** (1000 users/day):
- Backend: $5-10/month (DigitalOcean/Heroku)
- Frontend: Free (Vercel/Netlify)
- Total: ~$10/month

**Medium Scale** (10,000 users/day):
- Backend: $20-40/month (2-4 workers)
- Frontend: $19/month (Pro plan)
- Database: $15/month (if needed)
- Total: ~$50-75/month

**Large Scale** (100,000+ users/day):
- Backend: $100-200/month (auto-scaling)
- Frontend: Custom hosting
- CDN: $50-100/month
- Total: ~$200-400/month

---

## Contact

For deployment assistance, refer to:
- `docs/AI_SETUP_GUIDE.md` - Setup instructions
- `docs/AI_FEATURES.md` - Feature documentation
- `docs/AI_QUICK_REFERENCE.md` - Quick reference
