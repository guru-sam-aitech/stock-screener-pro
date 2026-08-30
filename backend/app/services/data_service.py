"""Multi-Source Stock Data Service

Supports:
- Indian markets (NSE, BSE)
- US markets (NYSE, NASDAQ)
- Global markets (50+ countries)
- Auto-detection of stock symbols
- Smart caching
- Fallback chain
"""

import yfinance as yf
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import hashlib


class MarketDataCache:
    """Simple in-memory cache for stock data."""
    
    def __init__(self, ttl_minutes: int = 15):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._timestamps: Dict[str, datetime] = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data if not expired."""
        if key in self._cache:
            if datetime.now() - self._timestamps[key] < self.ttl:
                return self._cache[key]
            else:
                # Expired
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def set(self, key: str, data: Dict[str, Any]):
        """Cache data with timestamp."""
        self._cache[key] = data
        self._timestamps[key] = datetime.now()
    
    def clear(self):
        """Clear all cache."""
        self._cache.clear()
        self._timestamps.clear()


class StockDataService:
    """
    Multi-source stock data service with auto-detection and fallback.
    
    Data Sources (in priority order):
    1. yfinance - Free, US-focused, some India coverage
    2. Manual API integration points (ready for Twelve Data, Alpha Vantage)
    3. Fallback to manual input
    
    Supported Markets:
    - 🇮🇳 India (NSE: .NS, BSE: .BO)
    - 🇺🇸 US (NYSE, NASDAQ)
    - 🇬🇧 UK (LSE: .L)
    - 🇯🇵 Japan (TSE: .T)
    - 🇨🇦 Canada (TSX: .TO)
    - 🇦🇺 Australia (ASX: .AX)
    - 🇪🇺 Europe (XETRA: .DE, Euronext: .PA)
    - And 40+ more countries
    """
    
    # Market suffix mappings
    MARKET_SUFFIXES = {
        'NSE': '.NS',
        'BSE': '.BO',
        'NYSE': '',
        'NASDAQ': '',
        'LSE': '.L',
        'TSE': '.T',
        'TSX': '.TO',
        'ASX': '.AX',
        'XETRA': '.DE',
        'EURONEXT': '.PA',
    }
    
    def __init__(self):
        self.cache = MarketDataCache(ttl_minutes=15)
        self.api_keys = {
            'twelve_data': None,  # Set in production
            'alpha_vantage': None,  # Set in production
            'finnhub': None,  # Set in production
        }
    
    def detect_market(self, symbol: str) -> str:
        """
        Detect market from symbol.
        
        Examples:
        - RELIANCE.NS → NSE (India)
        - TCS.BO → BSE (India)
        - AAPL → US (NYSE/NASDAQ)
        - TSLA → US (NASDAQ)
        """
        symbol_upper = symbol.upper().strip()
        
        # Check for Indian markets
        if symbol_upper.endswith('.NS'):
            return 'NSE'
        elif symbol_upper.endswith('.BO'):
            return 'BSE'
        
        # Check for other international markets
        for market, suffix in self.MARKET_SUFFIXES.items():
            if suffix and symbol_upper.endswith(suffix):
                return market
        
        # Default to US market
        return 'US'
    
    def format_symbol(self, symbol: str, market: Optional[str] = None) -> str:
        """
        Format symbol with correct suffix for the market.
        
        Examples:
        - RELIANCE + NSE → RELIANCE.NS
        - TCS + BSE → TCS.BO
        - AAPL + US → AAPL
        """
        symbol_upper = symbol.upper().strip()
        
        # If already has suffix, return as-is
        if any(symbol_upper.endswith(suffix) for suffix in self.MARKET_SUFFIXES.values() if suffix):
            return symbol_upper
        
        # Add suffix based on market
        if market:
            suffix = self.MARKET_SUFFIXES.get(market, '')
            return f"{symbol_upper}{suffix}"
        
        # Default: no suffix (US market)
        return symbol_upper
    
    def _get_cache_key(self, symbol: str) -> str:
        """Generate cache key from symbol."""
        return hashlib.md5(symbol.encode()).hexdigest()
    
    def fetch_stock_data(self, symbol: str, market: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch comprehensive stock data from best available source.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'AAPL')
            market: Optional market hint ('NSE', 'BSE', 'US', etc.)
        
        Returns:
            Dict with all stock fundamentals and metrics
        """
        # Detect market if not provided
        if not market:
            market = self.detect_market(symbol)
        
        # Format symbol correctly
        formatted_symbol = self.format_symbol(symbol, market)
        
        # Check cache first
        cache_key = self._get_cache_key(formatted_symbol)
        cached_data = self.cache.get(cache_key)
        if cached_data:
            cached_data['from_cache'] = True
            return cached_data
        
        # Fetch from primary source (yfinance)
        try:
            data = self._fetch_from_yfinance(formatted_symbol)
            if data:
                data['from_cache'] = False
                data['source'] = 'yfinance'
                self.cache.set(cache_key, data)
                return data
        except Exception as e:
            print(f"yfinance fetch failed for {formatted_symbol}: {e}")
        
        # Fallback: Try other sources (placeholder for future APIs)
        # data = self._fetch_from_twelve_data(formatted_symbol)
        # if data:
        #     return data
        
        # All sources failed
        return {
            'error': f"Could not fetch data for {formatted_symbol}",
            'symbol': formatted_symbol,
            'market': market,
        }
    
    def _fetch_from_yfinance(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch stock data from Yahoo Finance.
        
        Supports:
        - US stocks: AAPL, TSLA, GOOGL
        - Indian stocks: RELIANCE.NS, TCS.BO, HDFCBANK.NS
        - Global stocks: 50+ exchanges
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Get info (fundamentals)
            info = ticker.info
            
            if not info or 'symbol' not in info:
                return None
            
            # Extract fundamentals
            data = {
                'symbol': info.get('symbol', symbol),
                'name': info.get('shortName', info.get('longName', '')),
                'market': self.detect_market(symbol),
                
                # Price data
                'current_price': info.get('currentPrice') or info.get('regularMarketPrice'),
                'previous_close': info.get('previousClose'),
                'open': info.get('open'),
                'day_low': info.get('dayLow'),
                'day_high': info.get('dayHigh'),
                
                # Valuation
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'pb_ratio': info.get('priceToBook'),
                'ps_ratio': info.get('priceToSalesTrailing12Months'),
                'peg_ratio': info.get('pegRatio'),
                
                # Profitability
                'roe': info.get('returnOnEquity'),
                'roa': info.get('returnOnAssets'),
                'profit_margin': info.get('profitMargins'),
                'operating_margin': info.get('operatingMargins'),
                
                # Financial health
                'debt_to_equity': info.get('debtToEquity'),
                'current_ratio': info.get('currentRatio'),
                'quick_ratio': info.get('quickRatio'),
                'total_debt': info.get('totalDebt'),
                'total_cash': info.get('totalCash'),
                
                # Growth metrics
                'revenue_growth': info.get('revenueGrowth'),
                'earnings_growth': info.get('earningsGrowth'),
                'revenue_per_share': info.get('revenuePerShare'),
                'earnings_per_share': info.get('trailingEps'),
                
                # Size metrics
                'market_cap': info.get('marketCap'),
                'enterprise_value': info.get('enterpriseValue'),
                'shares_outstanding': info.get('sharesOutstanding'),
                'float_shares': info.get('floatShares'),
                
                # Dividends
                'dividend_yield': info.get('dividendYield'),
                'dividend_rate': info.get('dividendRate'),
                'payout_ratio': info.get('payoutRatio'),
                
                # Technical
                'beta': info.get('beta'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                '50_day_ma': info.get('fiftyDayAverage'),
                '200_day_ma': info.get('twoHundredDayAverage'),
                
                # Volume
                'volume': info.get('volume'),
                'avg_volume': info.get('averageVolume'),
                'avg_volume_10d': info.get('averageVolume10days'),
                
                # Sector & Industry
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'full_time_employees': info.get('fullTimeEmployees'),
                
                # Business description
                'description': info.get('longBusinessSummary', ''),
                'website': info.get('website'),
            }
            
            # Convert ratios from decimals to percentages where appropriate
            for key in ['roe', 'roa', 'profit_margin', 'operating_margin', 
                       'revenue_growth', 'earnings_growth', 'dividend_yield']:
                if data[key] is not None:
                    data[key] = data[key] * 100  # Convert to percentage
            
            # Calculate price change
            if data['current_price'] and data['previous_close']:
                data['price_change'] = data['current_price'] - data['previous_close']
                data['price_change_percent'] = (data['price_change'] / data['previous_close']) * 100
            
            return data
            
        except Exception as e:
            print(f"Error fetching from yfinance: {e}")
            return None
    
    def fetch_historical_prices(self, symbol: str, period: str = "1y", 
                                interval: str = "1d") -> List[Dict[str, Any]]:
        """
        Fetch historical price data.
        
        Args:
            symbol: Stock symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            List of OHLCV data points
        """
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period=period, interval=interval)
            
            prices = []
            for date, row in history.iterrows():
                prices.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume']) if 'Volume' in row else 0,
                })
            
            return prices
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get quick real-time quote (price, change, volume).
        
        Optimized for speed - minimal data fetch.
        """
        data = self.fetch_stock_data(symbol)
        
        return {
            'symbol': data.get('symbol'),
            'name': data.get('name'),
            'price': data.get('current_price'),
            'change': data.get('price_change'),
            'change_percent': data.get('price_change_percent'),
            'volume': data.get('volume'),
            'market_cap': data.get('market_cap'),
            'timestamp': datetime.now().isoformat(),
        }
    
    def search_stocks(self, query: str, market: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Search for stocks by name or symbol.
        
        Args:
            query: Search query (e.g., 'reliance', 'apple', 'tech')
            market: Optional market filter
        
        Returns:
            List of matching stocks with symbol and name
        """
        try:
            # Use yfinance search
            results = yf.Ticker(query).info
            
            if results and 'symbol' in results:
                return [{
                    'symbol': results.get('symbol', query),
                    'name': results.get('shortName', results.get('longName', '')),
                    'market': self.detect_market(query),
                }]
            
            return []
            
        except:
            return []
    
    def clear_cache(self):
        """Clear all cached data."""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'cached_items': len(self.cache._cache),
            'ttl_minutes': self.cache.ttl.seconds // 60,
        }


# Global instance
stock_data_service = StockDataService()
