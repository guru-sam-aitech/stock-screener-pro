from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Company(Base):
    """Company/Stock master data."""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    exchange = Column(String, index=True)  # NSE, BSE, NYSE, NASDAQ
    sector = Column(String, index=True)
    industry = Column(String, index=True)
    country = Column(String, default="IN")
    
    # Market Data
    market_cap = Column(Float)  # In crores for India, billions for US
    current_price = Column(Float)
    currency = Column(String, default="INR")
    
    # Fundamentals
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    dividend_yield = Column(Float)
    roe = Column(Float)  # Return on Equity
    roa = Column(Float)  # Return on Assets
    debt_to_equity = Column(Float)
    current_ratio = Column(Float)
    quick_ratio = Column(Float)
    
    # Growth Metrics
    revenue_growth = Column(Float)
    profit_growth = Column(Float)
    eps_growth = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    financials = relationship("FinancialData", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company {self.symbol}>"


class FinancialData(Base):
    """Annual/Quarterly financial statements."""
    
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Period Info
    period_type = Column(String)  # 'annual' or 'quarterly'
    fiscal_year = Column(Integer)
    period_end_date = Column(DateTime)
    
    # Income Statement
    revenue = Column(Float)
    operating_revenue = Column(Float)
    cost_of_revenue = Column(Float)
    gross_profit = Column(Float)
    operating_expenses = Column(Float)
    operating_income = Column(Float)
    net_income = Column(Float)
    ebitda = Column(Float)
    eps = Column(Float)  # Earnings per share
    
    # Balance Sheet
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    shareholders_equity = Column(Float)
    cash_and_equivalents = Column(Float)
    total_debt = Column(Float)
    
    # Cash Flow
    operating_cash_flow = Column(Float)
    free_cash_flow = Column(Float)
    capital_expenditure = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="financials")
    
    def __repr__(self):
        return f"<FinancialData {self.company_id} {self.fiscal_year}>"
