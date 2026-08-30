"""
Screener Service - Business Logic for Stock Screening
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List, Dict

from app.models.company import Company


class ScreenerService:
    """Business logic for stock screening."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def screen_stocks(
        self,
        market_cap_min: Optional[float] = None,
        market_cap_max: Optional[float] = None,
        pe_min: Optional[float] = None,
        pe_max: Optional[float] = None,
        pb_min: Optional[float] = None,
        pb_max: Optional[float] = None,
        roe_min: Optional[float] = None,
        roa_min: Optional[float] = None,
        debt_to_equity_max: Optional[float] = None,
        current_ratio_min: Optional[float] = None,
        revenue_growth_min: Optional[float] = None,
        profit_growth_min: Optional[float] = None,
        dividend_yield_min: Optional[float] = None,
        exchange: Optional[str] = None,
        sector: Optional[str] = None,
        country: str = "IN",
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "market_cap",
        sort_order: str = "desc"
    ) -> Dict:
        """
        Screen stocks based on fundamental criteria.
        Returns dict with total count and list of stocks.
        """
        
        # Build query
        query = self.db.query(Company)
        filters = []
        
        # Apply all filters
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
        
        # Apply filters
        if filters:
            query = query.filter(and_(*filters))
        
        # Count total
        total = query.count()
        
        # Sort
        if hasattr(Company, sort_by):
            sort_column = getattr(Company, sort_by)
            if sort_order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        
        # Paginate
        stocks = query.offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "stocks": stocks
        }
    
    def get_top_stocks(
        self,
        by: str = "market_cap",
        limit: int = 10,
        exchange: Optional[str] = None
    ) -> List[Company]:
        """Get top stocks by specified metric."""
        
        query = self.db.query(Company)
        
        if exchange:
            query = query.filter(Company.exchange == exchange)
        
        if hasattr(Company, by):
            sort_column = getattr(Company, by)
            query = query.order_by(sort_column.desc())
        
        return query.limit(limit).all()
    
    def get_sector_summary(self) -> List[Dict]:
        """Get summary statistics by sector."""
        
        from sqlalchemy import func
        
        summary = self.db.query(
            Company.sector,
            func.count(Company.id).label("count"),
            func.avg(Company.pe_ratio).label("avg_pe"),
            func.avg(Company.roe).label("avg_roe"),
            func.avg(Company.market_cap).label("avg_market_cap")
        ).group_by(Company.sector).all()
        
        return [
            {
                "sector": s.sector,
                "count": s.count,
                "avg_pe": round(s.avg_pe, 2) if s.avg_pe else None,
                "avg_roe": round(s.avg_roe, 2) if s.avg_roe else None,
                "avg_market_cap": round(s.avg_market_cap, 2) if s.avg_market_cap else None
            }
            for s in summary
        ]
