"""
Pydantic Schemas for Stock Screener
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class StockResponse(BaseModel):
    """Individual stock response."""
    
    symbol: str
    name: str
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    
    # Market Data
    market_cap: Optional[float] = None
    current_price: Optional[float] = None
    
    # Valuation
    pe_ratio: Optional[float] = Field(None, description="Price to Earnings ratio")
    pb_ratio: Optional[float] = Field(None, description="Price to Book ratio")
    
    # Profitability
    roe: Optional[float] = Field(None, description="Return on Equity %")
    roa: Optional[float] = Field(None, description="Return on Assets %")
    
    # Debt & Liquidity
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    
    # Growth
    revenue_growth: Optional[float] = None
    profit_growth: Optional[float] = None
    
    # Dividends
    dividend_yield: Optional[float] = None
    
    class Config:
        from_attributes = True


class ScreenerResponse(BaseModel):
    """Screener results with pagination."""
    
    total: int = Field(..., description="Total number of matching stocks")
    limit: int = Field(..., description="Results per page")
    offset: int = Field(..., description="Current offset")
    results: List[StockResponse]


class ScreenerRequest(BaseModel):
    """Request schema for complex screening (POST)."""
    
    # Market Cap
    market_cap_min: Optional[float] = None
    market_cap_max: Optional[float] = None
    
    # Valuation
    pe_min: Optional[float] = None
    pe_max: Optional[float] = None
    pb_min: Optional[float] = None
    pb_max: Optional[float] = None
    
    # Profitability
    roe_min: Optional[float] = None
    roa_min: Optional[float] = None
    
    # Debt
    debt_to_equity_max: Optional[float] = None
    
    # Growth
    revenue_growth_min: Optional[float] = None
    profit_growth_min: Optional[float] = None
    
    # Filters
    exchange: Optional[str] = None
    sector: Optional[str] = None
    country: str = "IN"
    
    # Pagination
    limit: int = 50
    offset: int = 0
