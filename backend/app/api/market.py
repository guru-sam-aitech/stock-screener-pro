"""
Market Analytics API - Gainers, Losers, Trending, Dashboard
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Dict

from app.db.session import get_db
from app.models.company import Company
from app.models.user import Portfolio, Watchlist, User
from app.core.security import get_current_user

router = APIRouter()


@router.get("/gainers")
def get_top_gainers(limit: int = 10, db: Session = Depends(get_db)):
    """Get top gainers by price change percentage."""
    stocks = db.query(Company).filter(
        Company.current_price > 0,
        Company.price_change_percent.isnot(None)
    ).order_by(
        desc(Company.price_change_percent)
    ).limit(limit).all()
    
    return stocks


@router.get("/losers")
def get_top_losers(limit: int = 10, db: Session = Depends(get_db)):
    """Get top losers by price change percentage."""
    stocks = db.query(Company).filter(
        Company.current_price > 0,
        Company.price_change_percent.isnot(None)
    ).order_by(
        Company.price_change_percent
    ).limit(limit).all()
    
    return stocks


@router.get("/trending")
def get_trending_stocks(limit: int = 10, db: Session = Depends(get_db)):
    """Get trending stocks by trading volume."""
    stocks = db.query(Company).filter(
        Company.current_price > 0,
        Company.volume > 0
    ).order_by(
        desc(Company.volume)
    ).limit(limit).all()
    
    return stocks


@router.get("/sector-performance")
def get_sector_performance(db: Session = Depends(get_db)):
    """Get performance metrics by sector."""
    sectors = db.query(
        Company.sector,
        func.count(Company.id).label("count"),
        func.avg(Company.pe_ratio).label("avg_pe"),
        func.avg(Company.roe).label("avg_roe"),
        func.avg(Company.market_cap).label("avg_market_cap")
    ).filter(
        Company.sector.isnot(None)
    ).group_by(Company.sector).all()
    
    return [
        {
            "sector": s.sector,
            "count": s.count,
            "avg_pe": round(s.avg_pe, 2) if s.avg_pe else None,
            "avg_roe": round(s.avg_roe, 2) if s.avg_roe else None,
            "avg_market_cap": round(s.avg_market_cap, 2) if s.avg_market_cap else None
        }
        for s in sectors
    ]


@router.get("/dashboard/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get dashboard summary data for logged-in user."""
    
    # Portfolio stats
    portfolio_count = db.query(func.count(Portfolio.id)).filter(
        Portfolio.user_id == user.id
    ).scalar() or 0
    
    # Watchlist stats
    watchlist_count = db.query(func.count(Watchlist.id)).filter(
        Watchlist.user_id == user.id
    ).scalar() or 0
    
    # Total holdings across all portfolios
    from app.models.user import PortfolioHolding
    total_holdings = db.query(func.count(PortfolioHolding.id)).join(
        Portfolio, PortfolioHolding.portfolio_id == Portfolio.id
    ).filter(
        Portfolio.user_id == user.id
    ).scalar() or 0
    
    # Total watchlist stocks
    from app.models.user import WatchlistStock
    total_watchlist_stocks = db.query(func.count(WatchlistStock.id)).join(
        Watchlist, WatchlistStock.watchlist_id == Watchlist.id
    ).filter(
        Watchlist.user_id == user.id
    ).scalar() or 0
    
    # Market stats
    total_stocks = db.query(func.count(Company.id)).scalar() or 0
    
    gainers_count = db.query(func.count(Company.id)).filter(
        Company.price_change_percent > 0
    ).scalar() or 0
    
    losers_count = db.query(func.count(Company.id)).filter(
        Company.price_change_percent < 0
    ).scalar() or 0
    
    return {
        "user": {
            "username": user.username,
            "email": user.email,
            "is_premium": user.is_premium
        },
        "portfolio": {
            "count": portfolio_count,
            "total_holdings": total_holdings
        },
        "watchlist": {
            "count": watchlist_count,
            "total_stocks": total_watchlist_stocks
        },
        "market": {
            "total_stocks": total_stocks,
            "gainers_count": gainers_count,
            "losers_count": losers_count,
            "market_breadth": round((gainers_count / (gainers_count + losers_count) * 100) if (gainers_count + losers_count) > 0 else 50, 2)
        }
    }


@router.get("/market-stats")
def get_market_stats(db: Session = Depends(get_db)):
    """Get overall market statistics."""
    
    # Average metrics
    avg_pe = db.query(func.avg(Company.pe_ratio)).filter(
        Company.pe_ratio > 0
    ).scalar() or 0
    
    avg_roe = db.query(func.avg(Company.roe)).filter(
        Company.roe > 0
    ).scalar() or 0
    
    avg_market_cap = db.query(func.avg(Company.market_cap)).filter(
        Company.market_cap > 0
    ).scalar() or 0
    
    # Count by exchange
    exchanges = db.query(
        Company.exchange,
        func.count(Company.id).label("count")
    ).group_by(Company.exchange).all()
    
    exchange_stats = {e.exchange: e.count for e in exchanges}
    
    # Count by country
    countries = db.query(
        Company.country,
        func.count(Company.id).label("count")
    ).group_by(Company.country).all()
    
    country_stats = {c.country: c.count for c in countries}
    
    return {
        "avg_pe": round(avg_pe, 2),
        "avg_roe": round(avg_roe, 2),
        "avg_market_cap": round(avg_market_cap, 2),
        "by_exchange": exchange_stats,
        "by_country": country_stats
    }
