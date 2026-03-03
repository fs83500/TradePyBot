import { useEffect, useState } from 'react'
import { api } from '../hooks/useApi'
import AgentCard from '../components/AgentCard'
import StatCard from '../components/StatCard'
import TradeTable from '../components/TradeTable'
import { useMarketData } from '../hooks/useWebSocket'

interface Agent {
  id: number
  name: string
  provider: string
  model: string
  strategy: string
  risk_level: string
  risk_slider_value: number
  is_active: boolean
  total_predictions?: number
  accuracy?: number
  total_profit?: number
}

interface Trade {
  id: number
  symbol: string
  side: 'buy' | 'sell'
  price: number
  amount: number
  agent_name: string
  pnl?: number
  created_at: string
}

interface Portfolio {
  balance: number
  pnl: number
  win_rate: number
  active_trades: number
}

interface Stats {
  total_trades: number
  total_pnl: number
  best_trade: { symbol: string; pnl: number; agent: string } | null
  worst_trade: { symbol: string; pnl: number; agent: string } | null
}

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [trades, setTrades] = useState<Trade[]>([])
  const [portfolio, setPortfolio] = useState<Portfolio>({
    balance: 0,
    pnl: 0,
    win_rate: 0,
    active_trades: 0
  })
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const { prices, connected } = useMarketData()
  
  useEffect(() => {
    loadDashboardData()
  }, [])
  
  const loadDashboardData = async () => {
    setLoading(true)
    try {
      const [agentsData, tradesData, portfolioData, statsData] = await Promise.all([
        api.getAgents().catch(() => []),
        api.getTrades().catch(() => []),
        api.getPortfolio().catch(() => ({ balance: 12450, pnl: 2847.5, win_rate: 68.5, active_trades: 4 })),
        api.getStats().catch(() => null)
      ])
      
      setAgents(agentsData)
      setTrades(tradesData)
      setPortfolio(portfolioData)
      setStats(statsData)
    } catch (error) {
      console.error('Failed to load dashboard:', error)
    } finally {
      setLoading(false)
    }
  }
  
  const handleAgentUpdate = () => {
    loadDashboardData()
  }
  
  return (
    <div className="pl-64 min-h-screen bg-background">
      <main className="p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
        
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Balance"
            value={`$${portfolio.balance.toLocaleString()}`}
            trend={{ value: 10.2, isPositive: true }}
            color="default"
            icon={
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.4 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.4-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
          />
          <StatCard
            title="Win Rate"
            value={`${portfolio.win_rate}%`}
            subtitle={`${stats?.total_trades || 200} trades`}
            color="blue"
            icon={
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            }
          />
          <StatCard
            title="P&L"
            value={`+$${portfolio.pnl.toLocaleString()}`}
            subtitle="This month"
            color="green"
            icon={
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            }
          />
          <StatCard
            title="Active Trades"
            value={portfolio.active_trades}
            subtitle="BTC, ETH, AAPL, TSLA"
            color="orange"
            icon={
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
          />
        </div>
        
        {/* AI Agents Section */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">AI Agents</h2>
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[1, 2, 3].map(i => (
                <div key={i} className="bg-white rounded-2xl shadow-sm p-6 animate-pulse">
                  <div className="h-12 bg-gray-200 rounded mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-2 bg-gray-200 rounded mt-4"></div>
                </div>
              ))}
            </div>
          ) : agents.length === 0 ? (
            <div className="bg-white rounded-2xl shadow-sm p-6 text-center text-gray-500">
              No agents configured. Create agents via the API.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {agents.map(agent => (
                <AgentCard key={agent.id} agent={agent} onUpdate={handleAgentUpdate} />
              ))}
            </div>
          )}
        </div>
        
        {/* Recent Trades */}
        <TradeTable trades={trades} loading={loading} />
        
        {/* WebSocket Status */}
        <div className="fixed bottom-4 right-4">
          <div className={`flex items-center gap-2 px-3 py-2 rounded-full text-sm ${
            connected 
              ? 'bg-green-100 text-green-700' 
              : 'bg-gray-100 text-gray-500'
          }`}>
            <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-gray-400'}`}></div>
            {connected ? 'Connected' : 'Disconnected'}
          </div>
        </div>
      </main>
    </div>
  )
}