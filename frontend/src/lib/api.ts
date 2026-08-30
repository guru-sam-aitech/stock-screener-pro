// API Client for Market Mind

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Stock {
  symbol: string
  name: string
  exchange: string
  sector: string
  industry: string
  country: string
  market_cap: number
  current_price: number
  pe_ratio: number
  pb_ratio: number
  roe: number
  roa: number
  debt_to_equity: number
  current_ratio: number
  dividend_yield: number
  revenue_growth: number
  profit_growth: number
}

export interface ScreenerResponse {
  total: number
  limit: number
  offset: number
  results: Stock[]
}

export interface ScreenerFilters {
  market_cap_min?: number
  market_cap_max?: number
  pe_min?: number
  pe_max?: number
  pb_min?: number
  pb_max?: number
  roe_min?: number
  roa_min?: number
  debt_to_equity_max?: number
  current_ratio_min?: number
  revenue_growth_min?: number
  profit_growth_min?: number
  dividend_yield_min?: number
  exchange?: string
  sector?: string
  country?: string
  limit?: number
  offset?: number
  sort_by?: string
  sort_order?: string
}

export async function screenStocks(filters: ScreenerFilters = {}): Promise<ScreenerResponse> {
  const params = new URLSearchParams()
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      params.append(key, value.toString())
    }
  })
  
  const response = await fetch(`${API_BASE_URL}/api/v1/screener?${params}`)
  
  if (!response.ok) {
    throw new Error('Failed to fetch stocks')
  }
  
  return response.json()
}

export async function getCompanyDetails(symbol: string): Promise<Stock> {
  const response = await fetch(`${API_BASE_URL}/api/v1/screener/${encodeURIComponent(symbol)}`)
  
  if (!response.ok) {
    throw new Error('Failed to fetch company details')
  }
  
  return response.json()
}

export async function getSectors(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/screener/sectors/list`)
  
  if (!response.ok) {
    throw new Error('Failed to fetch sectors')
  }
  
  return response.json()
}

export async function getExchanges(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/screener/exchanges/list`)
  
  if (!response.ok) {
    throw new Error('Failed to fetch exchanges')
  }
  
  return response.json()
}
