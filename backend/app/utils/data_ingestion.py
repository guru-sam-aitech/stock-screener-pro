"""
Data Ingestion Module
Fetch company data and financials from Financial Modeling Prep API
"""

import httpx
from typing import List, Dict, Optional
from datetime import datetime

from app.core.config import settings
from app.core.database import SessionLocal, engine, Base
from app.models.company import Company, FinancialData

# Create tables
Base.metadata.create_all(bind=engine)


class FMPDataIngestion:
    """Fetch and store data from Financial Modeling Prep."""
    
    def __init__(self):
        self.api_key = settings.FMP_API_KEY
        self.base_url = "https://financialmodelingprep.com/api/v3"
    
    async def fetch_company_profile(self, symbol: str) -> Optional[Dict]:
        """Fetch company profile data."""
        url = f"{self.base_url}/profile/{symbol}"
        params = {"apikey": self.api_key}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                return data[0] if data else None
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                return None
    
    async def fetch_financials(self, symbol: str, limit: int = 5) -> List[Dict]:
        """Fetch annual financial statements."""
        url = f"{self.base_url}/financials/{symbol}"
        params = {
            "apikey": self.api_key,
            "limit": limit,
            "period": "annual"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                return response.json().get("financials", [])
            except Exception as e:
                print(f"Error fetching financials for {symbol}: {e}")
                return []
    
    def parse_company_data(self, profile: Dict) -> Dict:
        """Parse FMP profile into Company model data."""
        return {
            "symbol": profile.get("symbol"),
            "name": profile.get("companyName"),
            "exchange": profile.get("exchange"),
            "sector": profile.get("sector"),
            "industry": profile.get("industry"),
            "country": profile.get("country"),
            "market_cap": profile.get("mktCap"),
            "current_price": profile.get("price"),
            "currency": profile.get("currency"),
            "pe_ratio": profile.get("price") / profile.get("eps") if profile.get("eps") else None,
            "pb_ratio": profile.get("price") / profile.get("bookPrice") if profile.get("bookPrice") else None,
            "dividend_yield": profile.get("dividendYield"),
            "roe": profile.get("returnOnEquity"),
            "roa": profile.get("returnOnAssets"),
            "debt_to_equity": profile.get("debtToEquity"),
            "current_ratio": profile.get("currentRatio"),
            "quick_ratio": profile.get("quickRatio"),
        }
    
    def save_company(self, company_data: Dict) -> Company:
        """Save company to database."""
        db = SessionLocal()
        try:
            # Check if exists
            existing = db.query(Company).filter(
                Company.symbol == company_data["symbol"]
            ).first()
            
            if existing:
                # Update
                for key, value in company_data.items():
                    setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
                company = existing
            else:
                # Create new
                company = Company(**company_data)
                db.add(company)
            
            db.commit()
            db.refresh(company)
            return company
        finally:
            db.close()
    
    async def ingest_stock(self, symbol: str) -> Optional[Company]:
        """Complete ingestion for one stock."""
        print(f"Processing {symbol}...")
        
        # Fetch profile
        profile = await self.fetch_company_profile(symbol)
        if not profile:
            return None
        
        # Parse and save
        company_data = self.parse_company_data(profile)
        company = self.save_company(company_data)
        
        print(f"✓ Saved {symbol}: {company.name}")
        return company


async def ingest_stocks(symbols: List[str]):
    """Ingest multiple stocks."""
    ingestion = FMPDataIngestion()
    
    for symbol in symbols:
        await ingestion.ingest_stock(symbol)
    
    print(f"\n✓ Ingested {len(symbols)} stocks")


if __name__ == "__main__":
    import asyncio
    
    # Sample Indian stocks
    indian_stocks = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", 
        "ICICIBANK.NS", "HINDUNILVR.NS", "ITC.NS", "SBIN.NS",
        "BHARTIARTL.NS", "BAJFINANCE.NS", "KOTAKBANK.NS", "LT.NS",
        "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "TITAN.NS",
        "WIPRO.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "BAJAJFINSV.NS"
    ]
    
    # Sample US stocks
    us_stocks = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", 
        "TSLA", "BRK.B", "JPM", "V", "JNJ", "WMT", "PG", 
        "MA", "UNH", "HD", "DIS", "PYPL", "BAC", "NFLX"
    ]
    
    # Run ingestion
    asyncio.run(ingest_stocks(indian_stocks + us_stocks))
