import React, { useState } from 'react';

interface StockData {
  symbol: string;
  name?: string;
  market?: string;
  current_price?: number;
  pe_ratio?: number;
  pb_ratio?: number;
  roe?: number;
  debt_to_equity?: number;
  revenue_growth?: number;
  profit_growth?: number;
  price_change_percent?: number;
  market_cap?: number;
  volume?: number;
  rsi?: number;
}

interface AIResult {
  symbol: string;
  ai_score: number;
  stance: string;
  strengths: string[];
  risk_flags: string[];
  fundamentals?: StockData;
  data_source?: string;
  from_cache?: boolean;
}

const AIAnalyticsAuto: React.FC = () => {
  const [symbol, setSymbol] = useState('');
  const [market, setMarket] = useState('');
  const [result, setResult] = useState<AIResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [autoFetched, setAutoFetched] = useState(false);

  const handleAutoAnalyze = async () => {
    if (!symbol.trim()) {
      setError('Please enter a stock symbol');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      
      const response = await fetch(`${baseUrl}/api/ai/auto-analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, market: market || undefined }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      setResult(data);
      setAutoFetched(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze stock');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 75) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStanceBadge = (stance: string) => {
    const colors = {
      'STRONG RESEARCH': 'bg-green-100 text-green-800',
      'POSITIVE RESEARCH': 'bg-blue-100 text-blue-800',
      'RESEARCH': 'bg-gray-100 text-gray-800',
      'CAUTION': 'bg-red-100 text-red-800',
    };
    return colors[stance as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const formatNumber = (num: number | undefined, decimals: number = 2) => {
    if (num === undefined || num === null) return 'N/A';
    return num.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: decimals });
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg shadow-lg p-6 mb-6">
        <h1 className="text-3xl font-bold text-white mb-2">🤖 AI Analytics with Auto-Fetch</h1>
        <p className="text-blue-100">
          Enter a symbol - AI will automatically fetch fundamentals and analyze the stock
        </p>
      </div>

      {/* Search Box */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Stock Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Stock Symbol
            </label>
            <input
              type="text"
              placeholder="e.g., RELIANCE.NS, AAPL, TCS.BO"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              onKeyPress={(e) => e.key === 'Enter' && handleAutoAnalyze()}
              className="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <p className="text-xs text-gray-500 mt-1">
              Supports: NSE (.NS), BSE (.BO), US, UK (.L), Japan (.T), and 50+ countries
            </p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Market (Optional)
            </label>
            <select
              value={market}
              onChange={(e) => setMarket(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Auto-Detect</option>
              <option value="NSE">NSE (India)</option>
              <option value="BSE">BSE (India)</option>
              <option value="US">US (NYSE/NASDAQ)</option>
              <option value="LSE">LSE (UK)</option>
              <option value="TSE">TSE (Japan)</option>
            </select>
          </div>
        </div>
        <button
          onClick={handleAutoAnalyze}
          disabled={loading}
          className="mt-4 w-full md:w-auto bg-blue-600 text-white px-8 py-3 rounded-md hover:bg-blue-700 disabled:bg-gray-400 font-semibold transition-colors"
        >
          {loading ? '🔄 Fetching & Analyzing...' : '🚀 Auto-Analyze Stock'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          {/* AI Score Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">
                  {result.symbol} {result.fundamentals?.name && (
                    <span className="text-lg font-normal text-gray-600 ml-2">
                      {result.fundamentals.name}
                    </span>
                  )}
                </h3>
                <div className="flex items-center gap-2 mt-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStanceBadge(result.stance)}`}>
                    {result.stance}
                  </span>
                  {result.data_source && (
                    <span className="text-xs text-gray-500">
                      Data: {result.data_source} {result.from_cache && '(cached)'}
                    </span>
                  )}
                </div>
              </div>
              <div className={`text-5xl font-bold ${getScoreColor(result.ai_score)}`}>
                {result.ai_score}
                <span className="text-2xl text-gray-400">/100</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-green-700 mb-2">✓ Strengths</h4>
                <ul className="space-y-1">
                  {result.strengths.map((s, i) => (
                    <li key={i} className="text-gray-700 text-sm">• {s}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-red-700 mb-2">⚠ Risk Flags</h4>
                <ul className="space-y-1">
                  {result.risk_flags.map((f, i) => (
                    <li key={i} className="text-gray-700 text-sm">• {f}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Fundamentals */}
          {result.fundamentals && (
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-semibold mb-4">📊 Fundamentals</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">Price</div>
                  <div className="text-lg font-semibold">
                    {result.fundamentals.current_price ? `₹${formatNumber(result.fundamentals.current_price, 2)}` : 'N/A'}
                  </div>
                </div>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">P/E Ratio</div>
                  <div className="text-lg font-semibold">{formatNumber(result.fundamentals.pe_ratio)}</div>
                </div>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">P/B Ratio</div>
                  <div className="text-lg font-semibold">{formatNumber(result.fundamentals.pb_ratio)}</div>
                </div>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">ROE</div>
                  <div className="text-lg font-semibold">{formatNumber(result.fundamentals.roe)}%</div>
                </div>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">Debt/Equity</div>
                  <div className="text-lg font-semibold">{formatNumber(result.fundamentals.debt_to_equity)}</div>
                </div>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">Revenue Growth</div>
                  <div className="text-lg font-semibold">{formatNumber(result.fundamentals.revenue_growth)}%</div>
                </div>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">Market Cap</div>
                  <div className="text-lg font-semibold">{formatNumber(result.fundamentals.market_cap / 100000, 1)} Cr</div>
                </div>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="text-xs text-gray-500">Sector</div>
                  <div className="text-lg font-semibold text-sm">{result.fundamentals.sector || 'N/A'}</div>
                </div>
              </div>
            </div>
          )}

          {/* Disclaimer */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-yellow-800">
              <strong>⚠️ Disclaimer:</strong> AI analytics are for educational and research purposes only. 
              They do not constitute investment advice, recommendations, or predictions of future performance. 
              Always do your own research and consult with a qualified financial advisor before making investment decisions.
            </p>
          </div>
        </div>
      )}

      {/* Example Stocks */}
      <div className="mt-8 bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-3">📝 Try These Examples</h3>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => { setSymbol('RELIANCE.NS'); setMarket('NSE'); }}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm transition-colors"
          >
            RELIANCE.NS (NSE)
          </button>
          <button
            onClick={() => { setSymbol('TCS.NS'); setMarket('NSE'); }}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm transition-colors"
          >
            TCS.NS (NSE)
          </button>
          <button
            onClick={() => { setSymbol('HDFCBANK.NS'); setMarket('NSE'); }}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm transition-colors"
          >
            HDFCBANK.NS (NSE)
          </button>
          <button
            onClick={() => { setSymbol('AAPL'); setMarket('US'); }}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm transition-colors"
          >
            AAPL (US)
          </button>
          <button
            onClick={() => { setSymbol('TSLA'); setMarket('US'); }}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm transition-colors"
          >
            TSLA (US)
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAnalyticsAuto;
