# AI Analytics Quick Reference

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ai/score` | POST | Get AI quality score (0-100) |
| `/api/ai/risk` | POST | Get risk assessment |
| `/api/ai/sentiment` | POST | Analyze news sentiment |
| `/api/ai/patterns` | POST | Detect chart patterns |
| `/api/ai/alerts` | POST | Generate smart alerts |
| `/api/ai/portfolio/optimize` | POST | Portfolio optimization |
| `/api/ai/health` | GET | Health check |

**Base URL**: `http://localhost:8000`

---

## Score Ranges

| Score | Stance | Meaning |
|-------|--------|---------|
| 75-100 | STRONG RESEARCH | High quality fundamentals |
| 60-74 | POSITIVE RESEARCH | Good fundamentals |
| 40-59 | RESEARCH | Average fundamentals |
| 0-39 | CAUTION | Weak fundamentals |

---

## Risk Levels

| Score | Level | Suitability |
|-------|-------|-------------|
| 0-34 | LOW | Conservative investors |
| 35-54 | MODERATE | Balanced portfolios |
| 55-74 | HIGH | Aggressive investors |
| 75-100 | VERY HIGH | High risk tolerance only |

---

## Sentiment Scores

| Score | Sentiment |
|-------|-----------|
| > 0.15 | POSITIVE |
| -0.15 to 0.15 | NEUTRAL |
| < -0.15 | NEGATIVE |

---

## Pattern Signals

- **BULLISH**: Uptrend confirmed
- **BEARISH**: Downtrend confirmed
- **BULLISH_WATCH**: Near support level
- **BEARISH_WATCH**: Near resistance level
- **NEUTRAL**: No clear signal

---

## Alert Types

- **PRICE_DROP**: Down ≥5% (HIGH if ≥10%)
- **PRICE_SURGE**: Up ≥5%
- **VOLUME_SPIKE**: Volume ≥2x average
- **RSI_OVERSOLD**: RSI < 30
- **RSI_OVERBOUGHT**: RSI > 70

---

## Example Request (Score)

```bash
curl -X POST http://localhost:8000/api/ai/score \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "pe_ratio": 28.5,
    "roe": 147.5,
    "debt_to_equity": 1.73,
    "revenue_growth": 8.5,
    "profit_growth": 10.2
  }'
```

---

## Example Response

```json
{
  "symbol": "AAPL",
  "ai_score": 72.0,
  "stance": "POSITIVE RESEARCH",
  "strengths": ["Strong return on equity"],
  "risk_flags": ["Elevated valuation"]
}
```

---

## Frontend Component

```tsx
import AIAnalytics from './components/AIAnalytics';

function App() {
  return <AIAnalytics />;
}
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `backend/app/services/ai_service.py` | Core AI logic |
| `backend/app/api/ai_router.py` | API endpoints |
| `backend/app/main.py` | App configuration |
| `frontend/src/components/AIAnalytics.tsx` | Dashboard UI |
| `frontend/src/pages/AIAnalyticsPage.tsx` | Page wrapper |
| `docs/AI_FEATURES.md` | Full documentation |
| `docs/AI_SETUP_GUIDE.md` | Setup instructions |

---

## Quick Tips

1. **Batch requests** for multiple stocks using `Promise.all()`
2. **Cache results** to avoid redundant API calls
3. **Check risk flags** even for high-scoring stocks
4. **Use alerts** for proactive monitoring
5. **Combine signals** (score + risk + alerts) for complete picture

---

## Disclaimer

Educational use only. Not investment advice.
