'use client'

import { useState, useEffect } from 'react'
import { Search, Filter, ArrowUpDown } from 'lucide-react'

interface Stock {
  symbol: string
  name: string
  exchange: string
  sector: string
  market_cap: number
  current_price: number
  pe_ratio: number
  pb_ratio: number
  roe: number
  debt_to_equity: number
  dividend_yield: number
  revenue_growth: number
  profit_growth: number
}

interface ScreenerResponse {
  total: number
  limit: number
  offset: number
  results: Stock[]
}

export default function Screener() {
  const [stocks, setStocks] = useState<Stock[]>([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  
  // Filters
  const [marketCapMin, setMarketCapMin] = useState('')
  const [peMax, setPeMax] = useState('')
  const [roeMin, setRoeMin] = useState('')
  const [sector, setSector] = useState('')
  const [exchange, setExchange] = useState('')

  const fetchStocks = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (marketCapMin) params.append('market_cap_min', marketCapMin)
      if (peMax) params.append('pe_max', peMax)
      if (roeMin) params.append('roe_min', roeMin)
      if (sector) params.append('sector', sector)
      if (exchange) params.append('exchange', exchange)
      
      const response = await fetch(`http://localhost:8000/api/v1/screener?${params}`)
      const data: ScreenerResponse = await response.json()
      
      setStocks(data.results)
      setTotal(data.total)
    } catch (error) {
      console.error('Error fetching stocks:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStocks()
  }, [marketCapMin, peMax, roeMin, sector, exchange])

  const handleApplyFilters = () => {
    fetchStocks()
  }

  const handleClearFilters = () => {
    setMarketCapMin('')
    setPeMax('')
    setRoeMin('')
    setSector('')
    setExchange('')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Stock Screener</h1>
          <p className="text-gray-600 mt-2">Screen stocks across India & US markets</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Filter className="w-5 h-5 text-gray-600" />
            <h2 className="text-lg font-semibold">Filters</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Market Cap */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Market Cap Min (Cr)
              </label>
              <input
                type="number"
                value={marketCapMin}
                onChange={(e) => setMarketCapMin(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="50000"
              />
            </div>

            {/* P/E Ratio */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                P/E Max
              </label>
              <input
                type="number"
                value={peMax}
                onChange={(e) => setPeMax(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="25"
              />
            </div>

            {/* ROE */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                ROE Min (%)
              </label>
              <input
                type="number"
                value={roeMin}
                onChange={(e) => setRoeMin(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="15"
              />
            </div>

            {/* Sector */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Sector
              </label>
              <select
                value={sector}
                onChange={(e) => setSector(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Sectors</option>
                <option value="Technology">Technology</option>
                <option value="Financial Services">Financial Services</option>
                <option value="Healthcare">Healthcare</option>
                <option value="Energy">Energy</option>
                <option value="Consumer Goods">Consumer Goods</option>
              </select>
            </div>

            {/* Exchange */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Exchange
              </label>
              <select
                value={exchange}
                onChange={(e) => setExchange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Exchanges</option>
                <option value="NSE">NSE</option>
                <option value="BSE">BSE</option>
                <option value="NYSE">NYSE</option>
                <option value="NASDAQ">NASDAQ</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 mt-6">
            <button
              onClick={handleApplyFilters}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition flex items-center gap-2"
            >
              <Search className="w-4 h-4" />
              Apply Filters
            </button>
            <button
              onClick={handleClearFilters}
              className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
            >
              Clear All
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b flex justify-between items-center">
            <h2 className="text-lg font-semibold">
              Results {total > 0 && `(${total} stocks)`}
            </h2>
          </div>

          {loading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading stocks...</p>
            </div>
          ) : stocks.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              No stocks found. Try adjusting your filters.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exchange</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Market Cap (Cr)</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">P/E</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">ROE %</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">D/E</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {stocks.map((stock) => (
                    <tr key={stock.symbol} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm font-semibold text-blue-600">{stock.symbol}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm text-gray-900">{stock.name}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm text-gray-600">{stock.exchange}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <span className="text-sm font-medium">₹{stock.current_price?.toFixed(2)}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <span className="text-sm">₹{(stock.market_cap / 100000).toFixed(2)}L</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <span className={`text-sm ${stock.pe_ratio < 20 ? 'text-green-600' : stock.pe_ratio < 30 ? 'text-yellow-600' : 'text-red-600'}`}>
                          {stock.pe_ratio?.toFixed(2)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <span className={`text-sm ${stock.roe > 20 ? 'text-green-600' : stock.roe > 15 ? 'text-yellow-600' : 'text-gray-600'}`}>
                          {stock.roe?.toFixed(2)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <span className={`text-sm ${stock.debt_to_equity < 0.5 ? 'text-green-600' : stock.debt_to_equity < 1 ? 'text-yellow-600' : 'text-red-600'}`}>
                          {stock.debt_to_equity?.toFixed(2)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
