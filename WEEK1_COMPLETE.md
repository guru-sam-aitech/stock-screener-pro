# 🎉 Week 1 Complete! - Database & Data Models

## ✅ What's Been Built

### Database Models
- **Company Model** (`backend/app/models/company.py`)
  - Stock symbol, name, exchange, sector, industry
  - Market data: market cap, current price, currency
  - Fundamentals: P/E, P/B, ROE, ROA, debt ratios
  - Growth metrics: revenue, profit, EPS growth

- **FinancialData Model**
  - Annual/quarterly financial statements
  - Income statement, balance sheet, cash flow
  - 5+ years of historical data

### Data Ingestion
- **FMP API Integration** (`backend/app/utils/data_ingestion.py`)
  - Fetches company profiles from Financial Modeling Prep
  - Parses and stores in PostgreSQL
  - Pre-configured with 40 stocks (20 Indian + 20 US)

---

## 🚀 How to Run Data Ingestion

### Step 1: Setup Environment

```bash
# Clone and navigate
git clone https://github.com/guru-sam-aitech/stock-screener-pro.git
cd stock-screener-pro

# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env
```

### Step 2: Get FREE API Keys

#### Financial Modeling Prep (Required)
1. Go to: https://site.financialmodelingprep.com/developer/docs
2. Click "Get Your Free API Key"
3. Sign up (no credit card needed)
4. Copy your API key
5. Add to `.env`:
```bash
FMP_API_KEY=your_api_key_here
```

#### Twelve Data (Optional - for later)
1. Go to: https://twelvedata.com/pricing
2. Sign up for free tier (800 requests/day)
3. Add to `.env`:
```bash
TWELVE_DATA_API_KEY=your_api_key_here
```

### Step 3: Start Database

**Option A: Using Docker (Recommended)**
```bash
docker-compose up -d db
# Wait 10 seconds for PostgreSQL to start
docker-compose logs -f db
```

**Option B: Local PostgreSQL**
```bash
# Install PostgreSQL 15+ if not already installed
# Create database
createdb marketmind

# Update .env with your local connection
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/marketmind
```

### Step 4: Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 5: Run Data Ingestion

```bash
# From backend directory
python app/utils/data_ingestion.py
```

**Expected Output:**
```
Processing RELIANCE.NS...
✓ Saved RELIANCE.NS: Reliance Industries Limited
Processing TCS.NS...
✓ Saved TCS.NS: Tata Consultancy Services Limited
...
✓ Ingested 40 stocks
```

### Step 6: Verify Data

```bash
# Connect to database
docker-compose exec db psql -U postgres -d marketmind

# Query companies
SELECT symbol, name, exchange, pe_ratio, roe FROM companies LIMIT 10;

# Should show:
#  symbol   | name                          | exchange | pe_ratio |  roe
# ----------+-------------------------------+----------+----------+--------
# AAPL      | Apple Inc.                    | NASDAQ   | 28.5     | 0.145
# MSFT      | Microsoft Corporation         | NASDAQ   | 32.1     | 0.198
# RELIANCE.NS| Reliance Industries Limited | NSE      | 24.3     | 0.089
```

---

## 📊 Stocks Included

### Indian Stocks (20)
RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, HINDUNILVR, ITC, SBIN, BHARTIARTL, BAJFINANCE, KOTAKBANK, LT, AXISBANK, ASIANPAINT, MARUTI, TITAN, WIPRO, ULTRACEMCO, NESTLEIND, BAJAJFINSV

### US Stocks (20)
AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, BRK.B, JPM, V, JNJ, WMT, PG, MA, UNH, HD, DIS, PYPL, BAC, NFLX

---

## 🎯 What's Next? (Week 2)

### Build Stock Screener API

**Files to Create:**
- `backend/app/api/screener.py` - Screening endpoints
- `backend/app/services/screener_service.py` - Filter logic
- `backend/app/schemas/screener.py` - Request/Response schemas

**Endpoints:**
```python
GET /api/v1/screener?market_cap_min=1000000000&pe_max=25&roe_min=15
GET /api/v1/company/{symbol}
GET /api/v1/company/{symbol}/financials
```

**Example Query:**
```bash
curl "http://localhost:8000/api/v1/screener?market_cap_min=50000&roe_min=15&pe_max=30"
```

---

## 🐛 Troubleshooting

### API Key Issues
```bash
# Test FMP API directly
curl "https://financialmodelingprep.com/api/v3/profile/AAPL?apikey=your_key"

# Should return JSON with company data
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### Import Errors
```bash
# Make sure you're in backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📈 Progress

- [x] Database models (Company, FinancialData)
- [x] Data ingestion from FMP API
- [x] 40 stocks loaded (India + US)
- [ ] Stock screener API endpoints
- [ ] Frontend UI for screening
- [ ] Company profile pages

**Next Milestone**: Week 2 - Stock Screener API 🎯

---

## 💡 Tips

1. **API Rate Limits**: FMP free tier = 250 requests/day
   - 40 stocks = ~40 requests
   - Run once daily to stay within limits

2. **Add More Stocks**: Edit `data_ingestion.py` and add symbols:
```python
more_stocks = ["ADANIENT.NS", "TATAMOTORS.NS", "COALINDIA.NS"]
asyncio.run(ingest_stocks(more_stocks))
```

3. **Database Backup**:
```bash
docker-compose exec db pg_dump -U postgres marketmind > backup.sql
```

---

**Ready for Week 2?** Let's build the screener API! 🚀
