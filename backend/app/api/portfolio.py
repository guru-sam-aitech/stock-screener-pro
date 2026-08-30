"""
Portfolio API - CRUD operations with P&L tracking
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from app.db.session import get_db
from app.models.user import Portfolio, PortfolioHolding, User
from app.models.company import Company
from app.schemas.portfolio import (
    PortfolioCreate, PortfolioResponse, PortfolioWithPnL,
    PortfolioHoldingCreate, PortfolioHoldingResponse
)
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[PortfolioResponse])
def get_portfolios(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Get all portfolios for current user."""
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user.id).all()
    return portfolios


@router.post("/", response_model=PortfolioResponse)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Create new portfolio."""
    db_portfolio = Portfolio(**portfolio.dict(), user_id=user.id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.get("/{portfolio_id}", response_model=PortfolioWithPnL)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get portfolio with P&L calculation."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Calculate P&L
    total_invested = 0
    current_value = 0
    
    for holding in portfolio.holdings:
        stock = db.query(Company).filter(Company.symbol == holding.symbol).first()
        if stock and stock.current_price:
            total_invested += holding.total_invested
            current_value += stock.current_price * holding.quantity
    
    total_pnl = current_value - total_invested
    total_pnl_percent = (total_pnl / total_invested * 100) if total_invested > 0 else 0
    
    # Build response
    result = PortfolioWithPnL(
        id=portfolio.id,
        name=portfolio.name,
        description=portfolio.description,
        is_public=portfolio.is_public,
        user_id=portfolio.user_id,
        created_at=portfolio.created_at,
        updated_at=portfolio.updated_at,
        holdings=portfolio.holdings,
        total_invested=total_invested,
        current_value=current_value,
        total_pnl=total_pnl,
        total_pnl_percent=total_pnl_percent
    )
    
    return result


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Update portfolio."""
    db_portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user.id
    ).first()
    
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    update_data = portfolio_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_portfolio, field, value)
    
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Delete portfolio."""
    db_portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user.id
    ).first()
    
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    db.delete(db_portfolio)
    db.commit()
    return {"message": "Portfolio deleted successfully"}


@router.post("/{portfolio_id}/holdings", response_model=PortfolioHoldingResponse)
def add_holding(
    portfolio_id: int,
    holding: PortfolioHoldingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Add or update stock holding in portfolio."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Check if holding exists
    existing = db.query(PortfolioHolding).filter(
        PortfolioHolding.portfolio_id == portfolio_id,
        PortfolioHolding.symbol == holding.symbol
    ).first()
    
    if existing:
        # Update existing holding (average up/down)
        total_quantity = existing.quantity + holding.quantity
        total_cost = (existing.quantity * existing.avg_price) + (holding.quantity * holding.avg_price)
        existing.avg_price = total_cost / total_quantity if total_quantity > 0 else 0
        existing.quantity = total_quantity
        existing.total_invested = total_cost
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new holding
        db_holding = PortfolioHolding(
            portfolio_id=portfolio_id,
            symbol=holding.symbol,
            quantity=holding.quantity,
            avg_price=holding.avg_price,
            total_invested=holding.quantity * holding.avg_price,
            notes=holding.notes
        )
        db.add(db_holding)
        db.commit()
        db.refresh(db_holding)
        return db_holding


@router.delete("/{portfolio_id}/holdings/{symbol}")
def remove_holding(
    portfolio_id: int,
    symbol: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Remove stock from portfolio."""
    holding = db.query(PortfolioHolding).filter(
        PortfolioHolding.portfolio_id == portfolio_id,
        PortfolioHolding.symbol == symbol
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    db.delete(holding)
    db.commit()
    return {"message": f"Holding {symbol} removed successfully"}


@router.get("/{portfolio_id}/performance")
def get_portfolio_performance(
    portfolio_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get detailed portfolio performance metrics."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Calculate metrics
    holdings_data = []
    total_invested = 0
    current_value = 0
    
    for holding in portfolio.holdings:
        stock = db.query(Company).filter(Company.symbol == holding.symbol).first()
        if stock and stock.current_price:
            invested = holding.quantity * holding.avg_price
            current = holding.quantity * stock.current_price
            pnl = current - invested
            pnl_percent = (pnl / invested * 100) if invested > 0 else 0
            
            holdings_data.append({
                "symbol": holding.symbol,
                "name": stock.name,
                "quantity": holding.quantity,
                "avg_price": holding.avg_price,
                "current_price": stock.current_price,
                "invested": invested,
                "current_value": current,
                "pnl": pnl,
                "pnl_percent": pnl_percent,
                "sector": stock.sector
            })
            
            total_invested += invested
            current_value += current
    
    total_pnl = current_value - total_invested
    total_pnl_percent = (total_pnl / total_invested * 100) if total_invested > 0 else 0
    
    # Sector allocation
    sector_allocation = {}
    for h in holdings_data:
        sector = h.get("sector", "Other")
        if sector not in sector_allocation:
            sector_allocation[sector] = 0
        sector_allocation[sector] += h["current_value"]
    
    # Convert to percentages
    sector_allocation_pct = {
        k: round((v / current_value * 100) if current_value > 0 else 0, 2)
        for k, v in sector_allocation.items()
    }
    
    return {
        "portfolio_id": portfolio_id,
        "portfolio_name": portfolio.name,
        "total_invested": round(total_invested, 2),
        "current_value": round(current_value, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_percent": round(total_pnl_percent, 2),
        "holdings_count": len(holdings_data),
        "holdings": holdings_data,
        "sector_allocation": sector_allocation_pct
    }
