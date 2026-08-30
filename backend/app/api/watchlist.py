"""
Watchlist API - CRUD operations
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import Watchlist, WatchlistStock, User
from app.schemas.watchlist import WatchlistCreate, WatchlistResponse, WatchlistStockCreate, WatchlistStockResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[WatchlistResponse])
def get_watchlists(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Get all watchlists for current user."""
    watchlists = db.query(Watchlist).filter(Watchlist.user_id == user.id).all()
    return watchlists


@router.post("/", response_model=WatchlistResponse)
def create_watchlist(
    watchlist: WatchlistCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Create new watchlist."""
    db_watchlist = Watchlist(**watchlist.dict(), user_id=user.id)
    db.add(db_watchlist)
    db.commit()
    db.refresh(db_watchlist)
    return db_watchlist


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
def get_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get specific watchlist with stocks."""
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user.id
    ).first()
    
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    return watchlist


@router.put("/{watchlist_id}", response_model=WatchlistResponse)
def update_watchlist(
    watchlist_id: int,
    watchlist_update: WatchlistCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Update watchlist."""
    db_watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user.id
    ).first()
    
    if not db_watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    update_data = watchlist_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_watchlist, field, value)
    
    db.commit()
    db.refresh(db_watchlist)
    return db_watchlist


@router.delete("/{watchlist_id}")
def delete_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Delete watchlist."""
    db_watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user.id
    ).first()
    
    if not db_watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    db.delete(db_watchlist)
    db.commit()
    return {"message": "Watchlist deleted successfully"}


@router.post("/{watchlist_id}/stocks", response_model=WatchlistStockResponse)
def add_stock_to_watchlist(
    watchlist_id: int,
    stock: WatchlistStockCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Add stock to watchlist."""
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user.id
    ).first()
    
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Check if stock already in watchlist
    existing = db.query(WatchlistStock).filter(
        WatchlistStock.watchlist_id == watchlist_id,
        WatchlistStock.symbol == stock.symbol
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Stock already in watchlist")
    
    db_stock = WatchlistStock(
        watchlist_id=watchlist_id,
        symbol=stock.symbol,
        notes=stock.notes,
        target_price=stock.target_price,
        stop_loss=stock.stop_loss
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


@router.delete("/{watchlist_id}/stocks/{symbol}")
def remove_stock_from_watchlist(
    watchlist_id: int,
    symbol: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Remove stock from watchlist."""
    stock = db.query(WatchlistStock).filter(
        WatchlistStock.watchlist_id == watchlist_id,
        WatchlistStock.symbol == symbol
    ).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found in watchlist")
    
    db.delete(stock)
    db.commit()
    return {"message": f"Stock {symbol} removed from watchlist"}
