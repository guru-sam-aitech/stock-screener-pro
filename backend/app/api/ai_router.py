"""FastAPI router for AI analytics endpoints."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ai_service import ai_service


router = APIRouter(prefix="/api/ai", tags=["ai-analytics"])


class StockInput(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    pe_ratio: Optional[float] = Field(None, ge=-1000, le=10000)
    pb_ratio: Optional[float] = Field(None, ge=-1000, le=10000)
    roe: Optional[float] = Field(None, ge=-1000, le=10000)
    debt_to_equity: Optional[float] = Field(None, ge=-1000, le=10000)
    revenue_growth: Optional[float] = Field(None, ge=-1000, le=10000)
    profit_growth: Optional[float] = Field(None, ge=-1000, le=10000)
    price_change_percent: Optional[float] = Field(None, ge=-100, le=1000)
    market_cap: Optional[float] = Field(None, ge=0)
    volume: Optional[float] = Field(None, ge=0)
    rsi: Optional[float] = Field(None, ge=0, le=100)


class SentimentInput(BaseModel):
    headlines: List[str] = Field(..., description="List of news headlines to analyze")


class PatternInput(BaseModel):
    prices: List[float] = Field(..., description="Historical prices for pattern detection")


class PortfolioHolding(BaseModel):
    symbol: str
    current_value: float = Field(ge=0)


class PortfolioInput(BaseModel):
    holdings: List[PortfolioHolding] = Field(..., description="Current portfolio holdings")
    risk_tolerance: str = Field("MODERATE", description="LOW, MODERATE, or HIGH")


@router.post("/score")
def score_stock(stock: StockInput) -> Dict[str, Any]:
    """Get AI-style quality score and research stance for a stock."""
    try:
        result = ai_service.score_stock(stock.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {e}")


@router.post("/risk")
def assess_risk(stock: StockInput) -> Dict[str, Any]:
    """Get explainable risk score and risk factors for a stock."""
    try:
        result = ai_service.assess_risk(stock.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {e}")


@router.post("/sentiment")
def analyze_sentiment(input_data: SentimentInput) -> Dict[str, Any]:
    """Analyze sentiment of news headlines using transparent keyword baseline."""
    try:
        result = ai_service.analyze_sentiment(input_data.headlines)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {e}")


@router.post("/patterns")
def detect_patterns(input_data: PatternInput) -> Dict[str, Any]:
    """Detect trend and support/resistance patterns from price history."""
    try:
        result = ai_service.detect_patterns(input_data.prices)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pattern detection failed: {e}")


@router.post("/alerts")
def generate_alerts(stock: StockInput, average_volume: Optional[float] = None) -> List[Dict[str, str]]:
    """Generate smart monitoring alerts for a stock."""
    try:
        result = ai_service.generate_smart_alerts(stock.model_dump(), average_volume)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert generation failed: {e}")


@router.post("/portfolio/optimize")
def optimize_portfolio(input_data: PortfolioInput) -> Dict[str, Any]:
    """Get diversification-oriented portfolio rebalance suggestions."""
    try:
        holdings = [h.model_dump() for h in input_data.holdings]
        result = ai_service.optimize_portfolio(holdings, input_data.risk_tolerance)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Portfolio optimization failed: {e}")


@router.get("/health")
def health_check() -> Dict[str, str]:
    """Health check for AI service."""
    return {"status": "ok", "service": "ai-analytics"}
