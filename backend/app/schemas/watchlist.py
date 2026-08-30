"""
Watchlist Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class WatchlistStockBase(BaseModel):
    symbol: str
    notes: Optional[str] = None
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None


class WatchlistStockCreate(WatchlistStockBase):
    pass


class WatchlistStockResponse(WatchlistStockBase):
    id: int
    watchlist_id: int
    added_at: datetime
    
    class Config:
        from_attributes = True


class WatchlistBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class WatchlistResponse(WatchlistBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    stocks: List[WatchlistStockResponse] = []
    
    class Config:
        from_attributes = True
