import { useEffect, useState } from 'react'
import { api } from '../hooks/useApi'

interface AgentStats {
  name: string
  win_rate: number
  risk_level: number
  total_profit: number
  total_trades: number
}

interface Feedback {
  agent: string
  message: string
  timestamp: string
}

const agentEmojis: Record<string, string> = {
  heliox: '🌟',
  syntax: '🔧',
  prisme: '🎨'
}

const agentColors: Record<string, string> = {
  heliox: 'border-yellow-500',
  syntax: 'border-blue-500',
  prisme: 'border-purple-500'
}

// Demo data for initial display
const demoAgentStats: AgentStats[] = [
  { name: 'heliox', win_rate: 72, risk_level: 8, total_profit: 1250, total_trades: 45 },
  { name: 'syntax', win_rate: 65, risk_level: 5, total_profit: 847, total_trades: 38 },
  { name: 'prisme', win_rate: 58, risk_level: 3, total_profit: 520, total_trades: 27 }
]

const demoFeedback: Feedback[] = [
  { agent: 'heliox', message: 'BTC showed strong momentum signals. Entered long position with tight stop-loss. Risk level 8/10 suitable for this aggressive trade.', timestamp: new Date(Date.now() - 2 * 60000).toISOString() },
  { agent: 'syntax', message: 'ETH price deviated from mean by 2.5 standard deviations. Mean reversion strategy suggests selling. Risk level 5/10 maintained.', timestamp: new Date(Date.now() - 15 * 60000).toISOString() },
  { agent: 'prisme', message: 'News sentiment for AAPL turned positive after earnings beat. Conservative entry with small position size. Risk level 3/10 appropriate.', timestamp: new Date(Date.now() - 60 * 60000).toISOString() }
]

const monthlyPerformance = [60, 75, 45, 80, 55, 90, 70, 85]

export default function Stats() {
  const [agentStats, setAgentStats] = useState<AgentStats[]>(demoAgentStats)
  const [feedback, setFeedback] = useState<Feedback[]>(demoFeedback)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    loadStats()
  }, [])
  
  const loadStats = async () => {
    setLoading(true)
    try {
      const stats = await api.getStats().catch(() => null)
      if (stats?.agents) {
        setAgentStats(stats.agents)
      }
      if (stats?.feedback) {
        setFeedback(stats.feedback)
      }
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }
  
  const formatTimeAgo = (timestamp: string) => {
    const diff = Date.now() - new Date(timestamp).getTime()
    const minutes = Math.floor(diff / 60000)
    if (minutes < 60) return `${minutes} minutes ago`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours} hours ago`
    return `${Math.floor(hours / 24)} days ago`
  }
  
  const getRiskColor = (level: number) => {
    if (level <= 3) return 'text-green-500'
    if (level <= 6) return 'text-yellow-500'
    return 'text-red-500'
  }
  
  const getRiskLabel = (level: number) => {
    if (level <= 3) return 'Conservative'
    if (level <= 6) return 'Moderate'
    return 'Aggressive'
  }
  
  return (
    <div className="pl-64 min-h-screen bg-background">
      <main className="p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-8">Statistics</h1>
        
        {/* Performance Chart */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-8">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Performance Over Time</h2>
          <div className="h-64 flex items-end gap-2">
            {monthlyPerformance.map((height, index) => {
              const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
              return (
                <div key={index} className="flex-1 flex flex-col items-center">
                  <div 
                    className="w-full bg-green-500 rounded-t transition-all"
                    style={{ height: `${height}%` }}
                  ></div>
                  <span className="text-xs mt-2 text-gray-500">{months[index]}</span>
                </div>
              )
            })}
          </div>
          <div className="mt-4 flex justify-between text-sm">
            <div>
              <span className="text-gray-500">Total Return:</span>
              <span className="text-green-500 font-bold ml-2">+28.5%</span>
            </div>
            <div>
              <span className="text-gray-500">Sharpe Ratio:</span>
              <span className="text-gray-900 font-bold ml-2">1.45</span>
            </div>
          </div>
        </div>
        
        {/* Risk by AI */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-8">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Risk Level by AI Agent</h2>
          <div className="space-y-4">
            {agentStats.map(agent => (
              <div key={agent.name} className="flex items-center gap-4">
                <div className="w-24 flex items-center gap-2">
                  <span className="text-2xl">{agentEmojis[agent.name] || '🤖'}</span>
                  <span className="font-medium text-gray-900 capitalize">{agent.name}</span>
                </div>
                <div className="flex-1">
                  <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      className="h-full rounded-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500"
                      style={{ width: `${agent.risk_level * 10}%` }}
                    ></div>
                  </div>
                </div>
                <div className="w-16 text-right">
                  <span className={`font-bold ${getRiskColor(agent.risk_level)}`}>
                    {agent.risk_level}/10
                  </span>
                </div>
                <div className="w-24 text-right">
                  <span className={`text-sm ${getRiskColor(agent.risk_level)}`}>
                    {getRiskLabel(agent.risk_level)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Win Rate by AI */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h3 className="text-sm text-gray-500 mb-4">Win Rate by AI</h3>
            <div className="space-y-3">
              {agentStats.map(agent => (
                <div key={agent.name} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{agentEmojis[agent.name] || '🤖'}</span>
                    <span className="font-medium capitalize">{agent.name}</span>
                  </div>
                  <span className={`font-bold ${agent.win_rate >= 60 ? 'text-green-500' : 'text-yellow-500'}`}>
                    {agent.win_rate}%
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Best Trade */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h3 className="text-sm text-gray-500 mb-4">Best Trade</h3>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-500">+$1,250.00</div>
                <div className="text-sm text-gray-500">BTC/USDT • Heliox</div>
              </div>
            </div>
          </div>
          
          {/* Worst Trade */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h3 className="text-sm text-gray-500 mb-4">Worst Trade</h3>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                </svg>
              </div>
              <div>
                <div className="text-2xl font-bold text-red-500">-$890.00</div>
                <div className="text-sm text-gray-500">ETH/USDT • Prisme</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* AI Feedback Section */}
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Recent AI Feedback</h2>
          <div className="space-y-4">
            {feedback.map((item, index) => (
              <div key={index} className={`border-l-4 ${agentColors[item.agent] || 'border-gray-300'} pl-4 py-2`}>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{agentEmojis[item.agent] || '🤖'}</span>
                  <span className="font-medium text-gray-900 capitalize">{item.agent}</span>
                  <span className="text-gray-400 text-sm">• {formatTimeAgo(item.timestamp)}</span>
                </div>
                <p className="text-gray-600">"{item.message}"</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}