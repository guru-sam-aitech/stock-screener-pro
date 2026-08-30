"""
Stock Screener API Endpoints
Filter stocks by fundamentals, valuation, growth, and technical metrics
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List

from app.core.database import get_db
from app.models.company import Company
from app.schemas.screener import ScreenerRequest, StockResponse, ScreenerResponse

router = APIRouter(prefix="/api/v1/screener", tags=["Screener"])


@router.get("/", response_model=ScreenerResponse)
async def screen_stocks(
    db: Session = Depends(get_db),
    
    # Market Cap (in crores for India, billions for US)
    market_cap_min: Optional[float] = Query(None, description="Minimum market cap"),
    market_cap_max: Optional[float] = Query(None, description="Maximum market cap"),
    
    # Valuation Ratios
    pe_min: Optional[float] = Query(None, description="Minimum P/E ratio"),
    pe_max: Optional[float] = Query(None, description="Maximum P/E ratio"),
    pb_min: Optional[float] = Query(None, description="Minimum P/B ratio"),
    pb_max: Optional[float] = Query(None, description="Maximum P/B ratio"),
    
    # Profitability
    roe_min: Optional[float] = Query(None, description="Minimum ROE %"),
    roa_min: Optional[float] = Query(None, description="Minimum ROA %"),
    
    # Debt & Liquidity
    debt_to_equity_max: Optional[float] = Query(None, description="Maximum debt to equity"),
    current_ratio_min: Optional[float] = Query(None, description="Minimum current ratio"),
    
    # Growth
    revenue_growth_min: Optional[float] = Query(None, description="Minimum revenue growth %"),
    profit_growth_min: Optional[float] = Query(None, description="Minimum profit growth %"),
    
    # Dividends
    dividend_yield_min: Optional[float] = Query(None, description="Minimum dividend yield %"),
    
    # Filters
    exchange: Optional[str] = Query(None, description="Filter by exchange (NSE, BSE, NYSE, NASDAQ)"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    country: Optional[str] = Query("IN", description="Filter by country"),
    
    # Pagination
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    
    # Sorting
    sort_by: str = Query("market_cap", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc, desc)")
):
    """
    Screen stocks based on fundamental criteria.
    
    Example:
    - GET /api/v1/screener?market_cap_min=50000&roe_min=15&pe_max=25
    - GET /api/v1/screener?exchange=NSE&sector=Technology&roe_min=20
    """
    
    # Build query
    query = db.query(Company)
    
    # Apply filters
    filters = []
    
    if market_cap_min is not None:
        filters.append(Company.market_cap >= market_cap_min)
    if market_cap_max is not None:
        filters.append(Company.market_cap <= market_cap_max)
    
    if pe_min is not None:
        filters.append(Company.pe_ratio >= pe_min)
    if pe_max is not None:
        filters.append(Company.pe_ratio <= pe_max)
    
    if pb_min is not None:
        filters.append(Company.pb_ratio >= pb_min)
    if pb_max is not None:
        filters.append(Company.pb_ratio <= pb_max)
    
    if roe_min is not None:
        filters.append(Company.roe >= roe_min)
    if roa_min is not None:
        filters.append(Company.roa >= roa_min)
    
    if debt_to_equity_max is not None:
        filters.append(Company.debt_to_equity <= debt_to_equity_max)
    if current_ratio_min is not None:
        filters.append(Company.current_ratio >= current_ratio_min)
    
    if revenue_growth_min is not None:
        filters.append(Company.revenue_growth >= revenue_growth_min)
    if profit_growth_min is not None:
        filters.append(Company.profit_growth >= profit_growth_min)
    
    if dividend_yield_min is not None:
        filters.append(Company.dividend_yield >= dividend_yield_min)
    
    if exchange:
        filters.append(Company.exchange == exchange)
    if sector:
        filters.append(Company.sector == sector)
    if country:
        filters.append(Company.country == country)
    
    # Apply all filters
    if filters:
        query = query.filter(and_(*filters))
    
    # Count total results
    total = query.count()
    
    # Sorting
    if hasattr(Company, sort_by):
        sort_column = getattr(Company, sort_by)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # Pagination
    stocks = query.offset(offset).limit(limit).all()
    
    # Convert to response
    results = [
        StockResponse(
            symbol=stock.symbol,
            name=stock.name,
            exchange=stock.exchange,
            sector=stock.sector,
            industry=stock.industry,
            market_cap=stock.market_cap,
            current_price=stock.current_price,
            pe_ratio=stock.pe_ratio,
            pb_ratio=stock.pb_ratio,
            roe=stock.roe,
            roa=stock.roa,
            debt_to_equity=stock.debt_to_equity,
            dividend_yield=stock.dividend_yield,
            revenue_growth=stock.revenue_growth,
            profit_growth=stock.profit_growth,
        )
        for stock in stocks
    ]
    
    return ScreenerResponse(
        total=total,
        limit=limit,
        offset=offset,
        results=results
    )


@router.get("/{symbol}", response_model=StockResponse)
async def get_company_details(symbol: str, db: Session = Depends(get_db)):
    """
    Get detailed company information by symbol.
    
    Example:
    - GET /api/v1/screener/RELIANCE.NS
    - GET /api/v1/screener/AAPL
    """
    stock = db.query(Company).filter(Company.symbol == symbol).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    return StockResponse(
        symbol=stock.symbol,
        name=stock.name,
        exchange=stock.exchange,
        sector=stock.sector,
        industry=stock.industry,
        market_cap=stock.market_cap,
        current_price=stock.current_price,
        pe_ratio=stock.pe_ratio,
        pb_ratio=stock.pb_ratio,
        roe=stock.roe,
        roa=stock.roa,
        debt_to_equity=stock.debt_to_equity,
        dividend_yield=stock.dividend_yield,
        revenue_growth=stock.revenue_growth,
        profit_growth=stock.profit_growth,
    )


@router.get("/sectors/list")
async def get_sectors(db: Session = Depends(get_db)):
    """Get list of all sectors."""
    sectors = db.query(Company.sector).distinct().all()
    return {"sectors": [s[0] for s in sectors if s[0]]}


@router.get("/industries/list")
async def get_industries(db: Session = Depends(get_db)):
    """Get list of all industries."""
    industries = db.query(Company.industry).distinct().all()
    return {"industries": [i[0] for i in industries if i[0]]}


@router.get("/exchanges/list")
async def get_exchanges(db: Session = Depends(get_db)):
    """Get list of all exchanges."""
    exchanges = db.query(Company.exchange).distinct().all()
    return {"exchanges": [e[0] for e in exchanges if e[0]]}
