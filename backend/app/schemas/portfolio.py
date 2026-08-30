"""
Portfolio Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PortfolioHoldingBase(BaseModel):
    symbol: str
    quantity: float
    avg_price: float
    notes: Optional[str] = None


class PortfolioHoldingCreate(PortfolioHoldingBase):
    pass


class PortfolioHoldingResponse(PortfolioHoldingBase):
    id: int
    portfolio_id: int
    total_invested: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class PortfolioResponse(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    holdings: List[PortfolioHoldingResponse] = []
    
    class Config:
        from_attributes = True


class PortfolioWithPnL(PortfolioResponse):
    total_invested: float = 0
    current_value: float = 0
    total_pnl: float = 0
    total_pnl_percent: float = 0
    
    class Config:
        from_attributes = True
