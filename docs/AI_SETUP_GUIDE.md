# AI Analytics Setup Guide

## Quick Start

This guide will help you set up and use the AI analytics features in Market Mind Pro.

---

## Prerequisites

- Python 3.9+ (for backend)
- Node.js 16+ (for frontend)
- Existing Market Mind Pro installation

---

## Backend Setup

### 1. Verify Installation

The AI service files should already be in place:
```
backend/app/services/ai_service.py
backend/app/api/ai_router.py
backend/app/main.py (updated with AI router)
```

### 2. Install Dependencies (if needed)

The AI service uses only standard Python libraries. No additional dependencies required.

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Verify AI Endpoints

Visit the API documentation at: `http://localhost:8000/docs`

Look for the "ai-analytics" tag to see all AI endpoints.

Test the health endpoint:
```bash
curl http://localhost:8000/api/ai/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "ai-analytics"
}
```

---

## Frontend Setup

### 1. Verify Component Files

Ensure these files exist:
```
frontend/src/components/AIAnalytics.tsx
frontend/src/pages/AIAnalyticsPage.tsx
```

### 2. Configure Environment

Create or update `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000
```

### 3. Add Routing (if using React Router)

In your `App.tsx` or routing file:

```tsx
import { Routes, Route } from 'react-router-dom';
import AIAnalyticsPage from './pages/AIAnalyticsPage';

function App() {
  return (
    <Routes>
      {/* ... other routes */}
      <Route path="/ai-analytics" element={<AIAnalyticsPage />} />
    </Routes>
  );
}
```

### 4. Add Navigation Link

In your navigation component:

```tsx
<Link to="/ai-analytics" className="nav-link">
  AI Analytics
</Link>
```

### 5. Start Frontend

```bash
cd frontend
npm install
npm start
```

### 6. Access AI Dashboard

Navigate to: `http://localhost:3000/ai-analytics`

---

## Testing the AI Features

### Test AI Scoring

```bash
curl -X POST http://localhost:8000/api/ai/score \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "pe_ratio": 28.5,
    "pb_ratio": 45.2,
    "roe": 147.5,
    "debt_to_equity": 1.73,
    "revenue_growth": 8.5,
    "profit_growth": 10.2,
    "price_change_percent": 1.5,
    "market_cap": 2800000
  }'
```

### Test Risk Assessment

```bash
curl -X POST http://localhost:8000/api/ai/risk \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "pe_ratio": 28.5,
    "roe": 147.5,
    "debt_to_equity": 1.73,
    "price_change_percent": 1.5,
    "market_cap": 2800000
  }'
```

### Test Smart Alerts

```bash
curl -X POST http://localhost:8000/api/ai/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "price_change_percent": -6.5,
    "volume": 125000000,
    "rsi": 28.5
  }'
```

---

## Using the AI Dashboard

### Step 1: Enter Stock Data

Fill in the form with stock fundamentals:
- **Symbol**: Stock ticker (e.g., AAPL, GOOGL)
- **P/E Ratio**: Price-to-earnings ratio
- **P/B Ratio**: Price-to-book ratio
- **ROE**: Return on equity (%)
- **Debt to Equity**: Debt-to-equity ratio
- **Revenue Growth**: Year-over-year revenue growth (%)
- **Profit Growth**: Year-over-year profit growth (%)
- **Price Change**: Today's price change (%)
- **RSI**: Relative Strength Index (0-100)

### Step 2: Click "Analyze Stock"

The dashboard will display:
- **AI Quality Score** (0-100) with strengths and risk flags
- **Risk Assessment** with risk level and factors
- **Smart Alerts** for significant events

### Step 3: Interpret Results

**AI Score Guide**:
- 75-100: STRONG RESEARCH - High quality fundamentals
- 60-74: POSITIVE RESEARCH - Good fundamentals
- 40-59: RESEARCH - Average fundamentals
- 0-39: CAUTION - Weak fundamentals

**Risk Level Guide**:
- LOW: Suitable for conservative investors
- MODERATE: Suitable for balanced portfolios
- HIGH: Suitable for aggressive investors
- VERY HIGH: High risk, use caution

---

## Integration with Existing Features

### Add AI Score to Stock Cards

```tsx
import { fetchAIScore } from '../api/ai';

// In your stock card component
const score = await fetchAIScore(stockData);
<div className={`score ${score.ai_score >= 70 ? 'high' : 'low'}`}>
  {score.ai_score}
</div>
```

### Add Risk Badge to Watchlist

```tsx
const risk = await fetchRisk(stockData);
<div className={`badge risk-${risk.risk_level.toLowerCase()}`}>
  {risk.risk_level}
</div>
```

### Show Alerts in Notifications

```tsx
const alerts = await fetchAlerts(stockData);
alerts.forEach(alert => {
  showNotification(alert.message, alert.severity);
});
```

---

## Troubleshooting

### Backend Issues

**Problem**: AI endpoints not found
- **Solution**: Verify `main.py` imports `ai_router` and includes it with `app.include_router(ai_router)`

**Problem**: Import errors
- **Solution**: Ensure you're in the `backend` directory and running from the correct Python environment

### Frontend Issues

**Problem**: Component not rendering
- **Solution**: Check browser console for errors, verify Tailwind CSS is configured

**Problem**: API calls failing
- **Solution**: Verify `REACT_APP_API_URL` is set correctly in `.env`

**Problem**: CORS errors
- **Solution**: Backend CORS is configured to allow all origins in development. For production, update `main.py` CORS settings.

---

## Performance Tips

1. **Batch API Calls**: When analyzing multiple stocks, use `Promise.all()` to parallelize requests
2. **Cache Results**: Store AI scores in local state or cache to avoid redundant API calls
3. **Lazy Load**: Load the AI analytics page only when needed to reduce initial bundle size
4. **Debounce Input**: Add debouncing to form inputs if making real-time API calls

---

## Security Considerations

### Production Deployment

1. **Update CORS**: Restrict origins in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Add Authentication**: Protect AI endpoints with your existing auth middleware

3. **Rate Limiting**: Implement rate limiting to prevent abuse

4. **Input Validation**: The API already validates inputs with Pydantic, but add additional checks for production use

---

## Next Steps

### Enhancements to Consider

1. **Auto-fetch Fundamentals**: Integrate with financial data APIs to auto-populate form fields
2. **Historical Tracking**: Store AI scores over time to track changes
3. **Custom Weighting**: Allow users to customize scoring weights
4. **Export Reports**: Generate PDF reports of AI analysis
5. **Backtesting**: Test AI signals against historical performance

### Learning Resources

- Review `docs/AI_FEATURES.md` for detailed feature documentation
- Check API docs at `http://localhost:8000/docs`
- Examine `ai_service.py` to understand scoring logic

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Examine backend logs for error messages
4. Check browser console for frontend errors

---

## Disclaimer

AI analytics are for educational and research purposes only. They do not constitute investment advice, recommendations, or predictions of future performance. Always conduct your own research and consult with qualified financial professionals before making investment decisions.
