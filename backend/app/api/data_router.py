"""FastAPI router for stock data endpoints."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services.data_service import stock_data_service


router = APIRouter(prefix="/api/data", tags=["stock-data"])


class StockDataRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol (e.g., RELIANCE, AAPL)")
    market: Optional[str] = Field(None, description="Market hint (NSE, BSE, US, etc.)")


class HistoricalDataRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
    period: str = Field("1y", description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")
    interval: str = Field("1d", description="Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)")


@router.get("/quote/{symbol}")
def get_quote(symbol: str) -> Dict[str, Any]:
    """
    Get quick real-time quote for a stock.
    
    Examples:
    - /api/data/quote/AAPL → US stock
    - /api/data/quote/RELIANCE.NS → Indian NSE stock
    - /api/data/quote/TCS.BO → Indian BSE stock
    """
    try:
        quote = stock_data_service.get_quote(symbol)
        if 'error' in quote:
            raise HTTPException(status_code=404, detail=quote['error'])
        return quote
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fundamentals")
def get_fundamentals(request: StockDataRequest) -> Dict[str, Any]:
    """
    Get comprehensive fundamentals for a stock.
    
    Returns:
    - Valuation metrics (P/E, P/B, P/S, etc.)
    - Profitability (ROE, ROA, margins)
    - Financial health (debt, cash, ratios)
    - Growth metrics (revenue, earnings growth)
    - Size metrics (market cap, shares)
    - Dividends
    - Technical indicators
    - Sector & industry info
    """
    try:
        data = stock_data_service.fetch_stock_data(request.symbol, request.market)
        if 'error' in data:
            raise HTTPException(status_code=404, detail=data['error'])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/historical")
def get_historical_data(request: HistoricalDataRequest) -> List[Dict[str, Any]]:
    """
    Get historical price data (OHLCV).
    
    Returns list of price points with:
    - date
    - open, high, low, close
    - volume
    """
    try:
        prices = stock_data_service.fetch_historical_prices(
            request.symbol, 
            request.period, 
            request.interval
        )
        if not prices:
            raise HTTPException(status_code=404, detail=f"No data found for {request.symbol}")
        return prices
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
def search_stocks(
    q: str = Query(..., description="Search query"),
    market: Optional[str] = Query(None, description="Filter by market")
) -> List[Dict[str, str]]:
    """
    Search for stocks by name or symbol.
    
    Example: /api/data/search?q=reliance&market=NSE
    """
    try:
        results = stock_data_service.search_stocks(q, market)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats")
def get_cache_stats() -> Dict[str, int]:
    """Get cache statistics."""
    return stock_data_service.get_cache_stats()


@router.post("/cache/clear")
def clear_cache() -> Dict[str, str]:
    """Clear all cached data."""
    stock_data_service.clear_cache()
    return {"status": "ok", "message": "Cache cleared"}


@router.get("/markets")
def get_supported_markets() -> Dict[str, List[str]]:
    """Get list of supported markets and their suffixes."""
    return {
        "markets": [
            {"code": "NSE", "name": "National Stock Exchange (India)", "suffix": ".NS"},
            {"code": "BSE", "name": "Bombay Stock Exchange (India)", "suffix": ".BO"},
            {"code": "NYSE", "name": "New York Stock Exchange (US)", "suffix": ""},
            {"code": "NASDAQ", "name": "NASDAQ (US)", "suffix": ""},
            {"code": "LSE", "name": "London Stock Exchange (UK)", "suffix": ".L"},
            {"code": "TSE", "name": "Tokyo Stock Exchange (Japan)", "suffix": ".T"},
            {"code": "TSX", "name": "Toronto Stock Exchange (Canada)", "suffix": ".TO"},
            {"code": "ASX", "name": "Australian Securities Exchange", "suffix": ".AX"},
            {"code": "XETRA", "name": "Frankfurt Stock Exchange (Germany)", "suffix": ".DE"},
            {"code": "EURONEXT", "name": "Euronext (Europe)", "suffix": ".PA"},
        ]
    }
