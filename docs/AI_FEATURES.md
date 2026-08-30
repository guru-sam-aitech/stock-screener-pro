# AI Analytics Features

## Overview

Market Mind Pro includes a comprehensive AI analytics engine that provides explainable, research-oriented insights for stock analysis. All AI features are designed to be transparent, educational, and supportive of your investment research process.

**Important**: AI analytics are for educational and research purposes only. They do not constitute investment advice, recommendations, or predictions of future performance.

---

## Core Features

### 1. AI Quality Score

**Purpose**: Evaluate stock quality based on fundamental metrics using an explainable rule-based system.

**Scoring Factors**:
- **Valuation** (P/E, P/B ratios): Reasonable valuations add points; elevated valuations reduce score
- **Profitability** (ROE): High return on equity indicates quality
- **Financial Health** (Debt-to-Equity): Conservative leverage is preferred
- **Growth** (Revenue & Profit Growth): Healthy growth rates are rewarded
- **Momentum** (Price Change): Recent positive momentum adds modest points

**Output**:
- Score: 0-100
- Stance: STRONG RESEARCH, POSITIVE RESEARCH, RESEARCH, or CAUTION
- Strengths: List of positive factors
- Risk Flags: List of concerning factors

**Example**:
```json
{
  "symbol": "AAPL",
  "ai_score": 78.5,
  "stance": "STRONG RESEARCH",
  "strengths": [
    "Reasonable earnings valuation",
    "Strong return on equity",
    "Conservative leverage",
    "Healthy revenue growth"
  ],
  "risk_flags": []
}
```

---

### 2. Risk Assessment

**Purpose**: Identify and explain key risk factors for a stock.

**Risk Factors Analyzed**:
- **Debt Risk**: High debt-to-equity ratios increase risk
- **Profitability Risk**: Low or negative ROE signals concern
- **Valuation Risk**: Extreme P/E ratios (very high or negative) add risk
- **Volatility Risk**: Large recent price swings increase risk
- **Size Risk**: Small-cap stocks carry additional liquidity risk

**Output**:
- Risk Score: 0-100 (lower is safer)
- Risk Level: LOW, MODERATE, HIGH, or VERY HIGH
- Risk Factors: Specific concerns identified

**Risk Levels**:
- LOW: < 35
- MODERATE: 35-54
- HIGH: 55-74
- VERY HIGH: ≥ 75

---

### 3. Sentiment Analysis

**Purpose**: Analyze news headline sentiment using a transparent keyword baseline.

**Method**:
- Positive keywords: beat, bullish, gain, growth, improve, outperform, profit, rally, record, strong, surge, upgrade
- Negative keywords: bearish, crash, cut, decline, downgrade, drop, fall, loss, miss, risk, warning, weak
- Each headline is classified as positive, negative, or neutral
- Overall sentiment score ranges from -1 to +1

**Output**:
- Sentiment: POSITIVE, NEUTRAL, or NEGATIVE
- Sentiment Score: -1 to +1
- Counts: positive, negative, neutral headlines

---

### 4. Pattern Detection

**Purpose**: Identify simple, explainable technical patterns from price history.

**Patterns Detected**:
- **Trend**: UPTREND, DOWNTREND, or SIDEWAYS based on recent price direction
- **Support/Resistance**: 20-period high and low levels
- **Key Levels**: Alerts when price is near support or resistance

**Signals**:
- BULLISH: Uptrend confirmed
- BEARISH: Downtrend confirmed
- BULLISH_WATCH: Near support level
- BEARISH_WATCH: Near resistance level
- NEUTRAL: No clear signal or insufficient data

**Requirements**: At least 20 price points for meaningful analysis

---

### 5. Smart Alerts

**Purpose**: Generate actionable monitoring alerts based on AI analysis.

**Alert Types**:
- **PRICE_DROP**: Stock down ≥5% (HIGH severity if ≥10%)
- **PRICE_SURGE**: Stock up ≥5% (MEDIUM severity)
- **VOLUME_SPIKE**: Volume ≥2x average (when average volume provided)
- **RSI_OVERSOLD**: RSI < 30 (LOW severity)
- **RSI_OVERBOUGHT**: RSI > 70 (LOW severity)

**Output**: List of alerts with type, severity, and actionable message

---

### 6. Portfolio Optimization

**Purpose**: Provide diversification-oriented rebalance suggestions.

**Method**:
- Calculate current portfolio weights
- Compare against illustrative maximum position limits based on risk tolerance:
  - LOW: 10% max per position
  - MODERATE: 15% max per position
  - HIGH: 25% max per position
- Flag positions exceeding limits for review

**Output**:
- Portfolio value
- Risk tolerance setting
- Illustrative max single position %
- Suggestions: List of overweight positions to review

---

## API Endpoints

Base URL: `http://localhost:8000/api/ai`

### POST /score

Get AI quality score for a stock.

**Request**:
```json
{
  "symbol": "AAPL",
  "pe_ratio": 28.5,
  "pb_ratio": 45.2,
  "roe": 147.5,
  "debt_to_equity": 1.73,
  "revenue_growth": 8.5,
  "profit_growth": 10.2,
  "price_change_percent": 1.5,
  "market_cap": 2800000
}
```

**Response**:
```json
{
  "symbol": "AAPL",
  "ai_score": 72.0,
  "stance": "POSITIVE RESEARCH",
  "confidence": "EXPLAINABLE_RULE_BASED",
  "strengths": ["Strong return on equity", "Healthy revenue growth"],
  "risk_flags": ["Elevated book-value valuation"],
  "disclaimer": "Educational research signal only; not investment advice."
}
```

---

### POST /risk

Assess stock risk level.

**Request**: Same as /score

**Response**:
```json
{
  "symbol": "AAPL",
  "risk_score": 32.0,
  "risk_level": "LOW",
  "risk_factors": ["No material rule-based risk flags found"],
  "disclaimer": "Risk score is informational and does not measure all risks."
}
```

---

### POST /sentiment

Analyze news sentiment.

**Request**:
```json
{
  "headlines": [
    "Apple beats earnings expectations with strong iPhone sales",
    "Tech sector faces headwinds amid rate concerns",
    "Apple announces record services revenue"
  ]
}
```

**Response**:
```json
{
  "sentiment": "POSITIVE",
  "sentiment_score": 0.33,
  "headline_count": 3,
  "positive": 2,
  "negative": 0,
  "neutral": 1,
  "method": "transparent_keyword_baseline"
}
```

---

### POST /patterns

Detect chart patterns.

**Request**:
```json
{
  "prices": [150.2, 151.5, 149.8, 152.3, 153.1, ...]
}
```

**Response**:
```json
{
  "signal": "BULLISH",
  "trend": "UPTREND",
  "support": 148.5,
  "resistance": 155.2,
  "patterns": ["Short-term uptrend"],
  "disclaimer": "Technical signals are probabilistic and not trading instructions."
}
```

---

### POST /alerts

Generate smart alerts.

**Request**:
```json
{
  "symbol": "AAPL",
  "price_change_percent": -6.5,
  "volume": 125000000,
  "rsi": 28.5
}
```

**Response**:
```json
[
  {
    "type": "PRICE_DROP",
    "severity": "HIGH",
    "message": "Price is down -6.50% today; review news and risk."
  },
  {
    "type": "RSI_OVERSOLD",
    "severity": "LOW",
    "message": "RSI is below 30; monitor for confirmation rather than acting automatically."
  }
]
```

---

### POST /portfolio/optimize

Get portfolio rebalance suggestions.

**Request**:
```json
{
  "holdings": [
    {"symbol": "AAPL", "current_value": 50000},
    {"symbol": "GOOGL", "current_value": 30000},
    {"symbol": "MSFT", "current_value": 20000}
  ],
  "risk_tolerance": "MODERATE"
}
```

**Response**:
```json
{
  "risk_tolerance": "MODERATE",
  "portfolio_value": 100000.0,
  "illustrative_max_single_position_pct": 15,
  "suggestions": [
    {
      "symbol": "AAPL",
      "current_weight": 50.0,
      "target_max_weight": 15,
      "insight": "Position concentration exceeds the illustrative limit; review diversification."
    }
  ],
  "disclaimer": "Allocation suggestions are educational, not personalized investment advice."
}
```

---

### GET /health

Health check endpoint.

**Response**:
```json
{
  "status": "ok",
  "service": "ai-analytics"
}
```

---

## Frontend Component

### AIAnalytics Component

Location: `frontend/src/components/AIAnalytics.tsx`

**Features**:
- Stock analysis input form with all fundamental fields
- AI Quality Score display with color coding
- Risk Assessment meter
- Smart Alerts panel
- Responsive grid layout
- Error handling and loading states

**Usage**:
```tsx
import AIAnalytics from './components/AIAnalytics';

function App() {
  return (
    <div>
      <AIAnalytics />
    </div>
  );
}
```

**Styling**: Uses Tailwind CSS classes. Ensure Tailwind is configured in your project.

---

## Best Practices

1. **Use AI scores as research inputs, not decisions**: Combine AI analytics with your own fundamental analysis and market research.

2. **Consider multiple factors**: Look at AI score, risk level, and alerts together for a complete picture.

3. **Review risk flags carefully**: Even high-scoring stocks may have important risk factors to consider.

4. **Monitor alerts proactively**: Set up regular checks for smart alerts to stay informed about significant moves.

5. **Diversify based on risk tolerance**: Use portfolio optimization suggestions to maintain appropriate diversification.

6. **Understand limitations**: AI analytics are based on historical and current data. They cannot predict future events or black swan occurrences.

---

## Technical Architecture

### Backend
- **Service**: `backend/app/services/ai_service.py`
  - Pure Python implementation
  - No external ML dependencies required
  - Explainable rule-based logic
  - Stateless and thread-safe

- **API**: `backend/app/api/ai_router.py`
  - FastAPI router
  - Pydantic validation
  - Error handling
  - OpenAPI documentation

### Frontend
- **Component**: `frontend/src/components/AIAnalytics.tsx`
  - React with TypeScript
  - Tailwind CSS styling
  - Async API calls
  - Responsive design

---

## Future Enhancements

Potential improvements for the AI analytics engine:

1. **Machine Learning Integration**: Train models on historical data for pattern recognition
2. **NLP Sentiment**: Use transformer models for deeper news sentiment analysis
3. **Peer Comparison**: Compare stocks against sector peers automatically
4. **Factor Analysis**: Decompose returns into style factors (value, growth, momentum, quality)
5. **Scenario Analysis**: Model impact of different economic scenarios
6. **Backtesting Framework**: Test AI signals against historical performance
7. **Custom Scoring**: Allow users to weight factors based on their preferences

---

## Disclaimer

**All AI analytics features are for educational and informational purposes only.**

- Not investment advice or recommendations
- Not predictions of future performance
- Do not consider all risks or personal circumstances
- Past performance does not guarantee future results
- Always conduct your own research
- Consult with qualified financial professionals before making investment decisions

By using these AI features, you acknowledge and accept these limitations.
