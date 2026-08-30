import React, { useState } from 'react';

interface StockData {
  symbol: string;
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

interface AIScore {
  ai_score: number;
  stance: string;
  strengths: string[];
  risk_flags: string[];
}

interface RiskAssessment {
  risk_score: number;
  risk_level: string;
  risk_factors: string[];
}

interface SentimentResult {
  sentiment: string;
  sentiment_score: number;
  positive: number;
  negative: number;
  neutral: number;
}

interface PatternResult {
  signal: string;
  trend: string;
  support: number;
  resistance: number;
  patterns: string[];
}

interface Alert {
  type: string;
  severity: string;
  message: string;
}

const AIAnalytics: React.FC = () => {
  const [stockData, setStockData] = useState<StockData>({
    symbol: '',
    pe_ratio: undefined,
    pb_ratio: undefined,
    roe: undefined,
    debt_to_equity: undefined,
    revenue_growth: undefined,
    profit_growth: undefined,
    price_change_percent: undefined,
    market_cap: undefined,
    volume: undefined,
    rsi: undefined,
  });

  const [aiScore, setAiScore] = useState<AIScore | null>(null);
  const [risk, setRisk] = useState<RiskAssessment | null>(null);
  const [sentiment, setSentiment] = useState<SentimentResult | null>(null);
  const [patterns, setPatterns] = useState<PatternResult | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setStockData(prev => ({
      ...prev,
      [name]: value === '' ? undefined : parseFloat(value),
    }));
  };

  const analyzeStock = async () => {
    if (!stockData.symbol) {
      setError('Please enter a stock symbol');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

      const [scoreRes, riskRes, alertsRes] = await Promise.all([
        fetch(`${baseUrl}/api/ai/score`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(stockData),
        }),
        fetch(`${baseUrl}/api/ai/risk`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(stockData),
        }),
        fetch(`${baseUrl}/api/ai/alerts`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(stockData),
        }),
      ]);

      const scoreData = await scoreRes.json();
      const riskData = await riskRes.json();
      const alertsData = await alertsRes.json();

      setAiScore(scoreData);
      setRisk(riskData);
      setAlerts(alertsData);
    } catch (err) {
      setError('Failed to analyze stock. Please try again.');
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

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'LOW': return 'text-green-600';
      case 'MODERATE': return 'text-yellow-600';
      case 'HIGH': return 'text-orange-600';
      case 'VERY HIGH': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">AI Analytics Dashboard</h1>

      {/* Input Form */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Stock Analysis Input</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            name="symbol"
            placeholder="Symbol (e.g., AAPL)"
            value={stockData.symbol}
            onChange={(e) => setStockData(prev => ({ ...prev, symbol: e.target.value }))}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="pe_ratio"
            placeholder="P/E Ratio"
            value={stockData.pe_ratio || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="pb_ratio"
            placeholder="P/B Ratio"
            value={stockData.pb_ratio || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="roe"
            placeholder="ROE (%)"
            value={stockData.roe || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="debt_to_equity"
            placeholder="Debt to Equity"
            value={stockData.debt_to_equity || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="revenue_growth"
            placeholder="Revenue Growth (%)"
            value={stockData.revenue_growth || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="profit_growth"
            placeholder="Profit Growth (%)"
            value={stockData.profit_growth || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="price_change_percent"
            placeholder="Price Change (%)"
            value={stockData.price_change_percent || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="rsi"
            placeholder="RSI"
            value={stockData.rsi || ''}
            onChange={handleInputChange}
            className="border rounded px-3 py-2"
          />
        </div>
        <button
          onClick={analyzeStock}
          disabled={loading}
          className="mt-4 bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Analyzing...' : 'Analyze Stock'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {/* Results Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* AI Score */}
        {aiScore && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3">AI Quality Score</h3>
            <div className={`text-4xl font-bold ${getScoreColor(aiScore.ai_score)} mb-2`}>
              {aiScore.ai_score}/100
            </div>
            <div className="text-sm text-gray-600 mb-3">{aiScore.stance}</div>
            <div className="space-y-2">
              <div>
                <h4 className="font-medium text-green-700 text-sm">Strengths</h4>
                <ul className="text-sm text-gray-700 list-disc list-inside">
                  {aiScore.strengths.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-red-700 text-sm">Risk Flags</h4>
                <ul className="text-sm text-gray-700 list-disc list-inside">
                  {aiScore.risk_flags.map((f, i) => <li key={i}>{f}</li>)}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Risk Assessment */}
        {risk && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3">Risk Assessment</h3>
            <div className={`text-3xl font-bold ${getRiskColor(risk.risk_level)} mb-2`}>
              {risk.risk_level}
            </div>
            <div className="text-sm text-gray-600 mb-3">Score: {risk.risk_score}/100</div>
            <ul className="text-sm text-gray-700 list-disc list-inside">
              {risk.risk_factors.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
          </div>
        )}

        {/* Smart Alerts */}
        {alerts.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3">Smart Alerts</h3>
            <div className="space-y-2">
              {alerts.map((alert, i) => (
                <div
                  key={i}
                  className={`p-2 rounded text-sm ${
                    alert.severity === 'HIGH'
                      ? 'bg-red-100 text-red-800'
                      : alert.severity === 'MEDIUM'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-blue-100 text-blue-800'
                  }`}
                >
                  <div className="font-medium">{alert.type}</div>
                  <div>{alert.message}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="mt-6 p-4 bg-gray-100 rounded text-sm text-gray-700">
        <strong>Disclaimer:</strong> AI analytics are for educational and research purposes only. They do not constitute investment advice, recommendations, or predictions of future performance. Always do your own research and consult with a qualified financial advisor before making investment decisions.
      </div>
    </div>
  );
};

export default AIAnalytics;
