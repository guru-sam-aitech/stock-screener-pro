# 🌍 Multi-Source Stock Data Service Guide

## Overview

The new data service provides **real-time stock data** for:
- 🇮🇳 **Indian Markets** (NSE, BSE)
- 🇺🇸 **US Markets** (NYSE, NASDAQ)
- 🌏 **Global Markets** (50+ countries)

With **auto-detection**, **smart caching**, and **fallback** support.

---

## 🚀 Quick Start

### 1. Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test with Indian Stocks

```bash
# Get quote for Reliance (NSE)
curl http://localhost:8000/api/data/quote/RELIANCE.NS

# Get fundamentals for TCS (NSE)
curl -X POST http://localhost:8000/api/data/fundamentals \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TCS.NS"}'

# Get historical data for HDFC Bank
curl -X POST http://localhost:8000/api/data/historical \
  -H "Content-Type: application/json" \
  -d '{"symbol": "HDFCBANK.NS", "period": "1mo", "interval": "1d"}'
```

### 3. Test with US Stocks

```bash
# Get quote for Apple
curl http://localhost:8000/api/data/quote/AAPL

# Get fundamentals for Tesla
curl -X POST http://localhost:8000/api/data/fundamentals \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA"}'
```

---

## 📡 API Endpoints

### GET `/api/data/quote/{symbol}`

Get quick real-time quote.

**Examples:**
```bash
# Indian stock
curl http://localhost:8000/api/data/quote/RELIANCE.NS

# US stock
curl http://localhost:8000/api/data/quote/AAPL

# UK stock
curl http://localhost:8000/api/data/quote/BP.L
```

**Response:**
```json
{
  "symbol": "RELIANCE.NS",
  "name": "Reliance Industries Limited",
  "price": 2456.75,
  "change": 32.50,
  "change_percent": 1.34,
  "volume": 8542000,
  "market_cap": 16623450000000,
  "timestamp": "2026-08-30T10:45:00"
}
```

---

### POST `/api/data/fundamentals`

Get comprehensive fundamentals.

**Request:**
```json
{
  "symbol": "RELIANCE.NS",
  "market": "NSE"
}
```

**Response:**
```json
{
  "symbol": "RELIANCE.NS",
  "name": "Reliance Industries Limited",
  "market": "NSE",
  "current_price": 2456.75,
  "pe_ratio": 28.5,
  "pb_ratio": 2.1,
  "roe": 12.5,
  "debt_to_equity": 0.45,
  "revenue_growth": 15.2,
  "profit_margin": 8.9,
  "market_cap": 16623450000000,
  "dividend_yield": 0.35,
  "sector": "Energy",
  "industry": "Oil & Gas Refining",
  ...
}
```

---

### POST `/api/data/historical`

Get historical price data (OHLCV).

**Request:**
```json
{
  "symbol": "AAPL",
  "period": "1mo",
  "interval": "1d"
}
```

**Response:**
```json
[
  {
    "date": "2026-08-01",
    "open": 225.50,
    "high": 228.75,
    "low": 224.20,
    "close": 227.30,
    "volume": 52340000
  },
  {
    "date": "2026-08-02",
    "open": 227.30,
    "high": 230.10,
    "low": 226.50,
    "close": 229.80,
    "volume": 48920000
  }
]
```

---

### GET `/api/data/search`

Search for stocks by name or symbol.

**Example:**
```bash
curl "http://localhost:8000/api/data/search?q=reliance&market=NSE"
```

**Response:**
```json
[
  {
    "symbol": "RELIANCE.NS",
    "name": "Reliance Industries Limited",
    "market": "NSE"
  }
]
```

---

### GET `/api/data/markets`

Get list of supported markets.

**Response:**
```json
{
  "markets": [
    {"code": "NSE", "name": "National Stock Exchange (India)", "suffix": ".NS"},
    {"code": "BSE", "name": "Bombay Stock Exchange (India)", "suffix": ".BO"},
    {"code": "NYSE", "name": "New York Stock Exchange (US)", "suffix": ""},
    {"code": "NASDAQ", "name": "NASDAQ (US)", "suffix": ""},
    {"code": "LSE", "name": "London Stock Exchange (UK)", "suffix": ".L"},
    ...
  ]
}
```

---

## 🌍 Supported Markets

### Indian Markets
- **NSE** (National Stock Exchange) - Suffix: `.NS`
  - Examples: RELIANCE.NS, TCS.NS, HDFCBANK.NS
- **BSE** (Bombay Stock Exchange) - Suffix: `.BO`
  - Examples: TCS.BO, INFY.BO, WIPRO.BO

### US Markets
- **NYSE** (New York Stock Exchange)
  - Examples: AAPL, TSLA, GOOGL, MSFT
- **NASDAQ** (NASDAQ)
  - Examples: AMZN, META, NVDA

### Other Global Markets
- **LSE** (London) - `.L`: BP.L, HSBA.L
- **TSE** (Tokyo) - `.T`: 7203.T, 9984.T
- **TSX** (Toronto) - `.TO`: RY.TO, TD.TO
- **ASX** (Australia) - `.AX`: BHP.AX, CBA.AX
- **XETRA** (Germany) - `.DE`: VOW3.DE, SIE.DE
- **EURONEXT** (Europe) - `.PA`: MC.PA, OR.PA

---

## 🔧 Usage Examples

### Python Example

```python
import requests

# Get quote for Indian stock
response = requests.get('http://localhost:8000/api/data/quote/RELIANCE.NS')
quote = response.json()
print(f"Price: ₹{quote['price']}")

# Get fundamentals
response = requests.post(
    'http://localhost:8000/api/data/fundamentals',
    json={'symbol': 'TCS.NS'}
)
fundamentals = response.json()
print(f"P/E: {fundamentals['pe_ratio']}")
print(f"ROE: {fundamentals['roe']}%")

# Get historical data
response = requests.post(
    'http://localhost:8000/api/data/historical',
    json={'symbol': 'AAPL', 'period': '3mo', 'interval': '1d'}
)
prices = response.json()
print(f"Got {len(prices)} days of data")
```

### JavaScript/React Example

```javascript
// Get stock quote
const getQuote = async (symbol) => {
  const response = await fetch(`http://localhost:8000/api/data/quote/${symbol}`);
  const data = response.json();
  return data;
};

// Usage
const appleQuote = await getQuote('AAPL');
console.log(`Apple: $${appleQuote.price}`);

const relianceQuote = await getQuote('RELIANCE.NS');
console.log(`Reliance: ₹${relianceQuote.price}`);
```

---

## 🎯 Auto-Detection Examples

The system automatically detects markets:

| Input | Detected Market | Formatted Symbol |
|-------|----------------|------------------|
| `RELIANCE` | NSE (by default for Indian) | RELIANCE.NS |
| `RELIANCE.NS` | NSE | RELIANCE.NS |
| `TCS.BO` | BSE | TCS.BO |
| `AAPL` | US | AAPL |
| `TSLA` | US | TSLA |
| `BP.L` | LSE | BP.L |

You can also specify market explicitly:

```python
# Force NSE
stock_data_service.fetch_stock_data('RELIANCE', market='NSE')

# Force US
stock_data_service.fetch_stock_data('AAPL', market='US')
```

---

## 💾 Caching

### How It Works

- **TTL**: 15 minutes (configurable)
- **Cache Key**: MD5 hash of symbol
- **Auto-Refresh**: Expired data is refetched automatically

### Check Cache Stats

```bash
curl http://localhost:8000/api/data/cache/stats
```

**Response:**
```json
{
  "cached_items": 25,
  "ttl_minutes": 15
}
```

### Clear Cache

```bash
curl -X POST http://localhost:8000/api/data/cache/clear
```

---

## 📊 Data Coverage

### Indian Stocks (NSE/BSE)

**Available Data:**
- ✅ Real-time price
- ✅ OHLCV data
- ✅ Company fundamentals
- ✅ Financial ratios
- ✅ Sector & industry
- ⚠️ Some metrics may be limited for smaller stocks

**Popular Indian Stocks:**
- RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS
- ICICIBANK.NS, HINDUNILVR.NS, BHARTIARTL.NS
- SBIN.NS, BAJFINANCE.NS, ASIANPAINT.NS

### US Stocks

**Available Data:**
- ✅ Real-time price
- ✅ OHLCV data
- ✅ Full fundamentals
- ✅ All financial ratios
- ✅ Analyst estimates
- ✅ Earnings data

**Popular US Stocks:**
- AAPL, TSLA, GOOGL, MSFT, AMZN
- META, NVDA, JPM, V, JNJ

---

## 🔄 Integration with AI System

The AI system now **auto-fetches data**!

### Before (Manual Input)
Users had to manually enter P/E, ROE, debt, etc.

### After (Auto-Fetch)
Just enter the symbol - system fetches everything!

**Example Flow:**
1. User enters: `RELIANCE.NS`
2. System fetches: P/E, P/B, ROE, debt, growth, etc.
3. AI analyzes automatically
4. Shows score and recommendations

---

## 🛠️ Troubleshooting

### Problem: "Could not fetch data"

**Solutions:**
1. Check if symbol is correct (e.g., RELIANCE.NS not just RELIANCE)
2. Verify market suffix (.NS for NSE, .BO for BSE)
3. Check if market is open (Indian markets: 9:15 AM - 3:30 PM IST)
4. Try US stocks for testing (AAPL, TSLA)

### Problem: Limited data for Indian stocks

**Explanation:**
- yfinance has better coverage for large-cap Indian stocks
- Small-cap/mid-cap may have limited data
- Consider adding Twelve Data API for better coverage (see Advanced section)

### Problem: Slow response

**Solutions:**
1. Check cache stats - should be using cache for repeated requests
2. Reduce TTL if data freshness is critical
3. Consider adding premium API for production

---

## 🚀 Advanced: Adding Premium APIs

### Twelve Data Integration

1. **Get API Key**: https://twelvedata.com/pricing
2. **Add to environment**:
   ```bash
   export TWELVE_DATA_API_KEY=your_key_here
   ```
3. **Update data_service.py** to use Twelve Data API

**Benefits:**
- Better Indian market coverage
- Real-time data
- 800 requests/day free tier

### Alpha Vantage Integration

1. **Get API Key**: https://www.alphavantage.co/support/#api-key
2. **Add to environment**:
   ```bash
   export ALPHA_VANTAGE_API_KEY=your_key_here
   ```

**Benefits:**
- Full fundamentals
- 25 requests/day free
- 500 requests/month free

---

## 📈 Performance Tips

1. **Use Cache**: Repeated requests use cached data (15 min TTL)
2. **Batch Requests**: Fetch multiple stocks in parallel
3. **Use Quotes**: For just price, use `/quote` endpoint (faster)
4. **Historical Data**: Use appropriate period (don't fetch 10y if you need 1mo)

---

## 📝 Next Steps

1. ✅ Test with Indian stocks (RELIANCE.NS, TCS.NS)
2. ✅ Test with US stocks (AAPL, TSLA)
3. ✅ Integrate with frontend AI dashboard
4. ✅ Add auto-fetch to AI analysis form
5. ✅ Consider premium APIs for production

---

## 📞 Support

For issues:
1. Check API docs: `http://localhost:8000/docs`
2. Review logs for error messages
3. Test with known working symbols (AAPL, RELIANCE.NS)
4. Check cache stats

---

**Happy Data Fetching! 🚀📊**
