import { useState, useCallback } from 'react'
import { api } from '../hooks/useApi'

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

interface AgentCardProps {
  agent: Agent
  onUpdate?: () => void
}

const agentEmojis: Record<string, string> = {
  heliox: '🌟',
  syntax: '🔧',
  prisme: '🎨'
}

const agentColors: Record<string, string> = {
  heliox: 'from-yellow-400 to-yellow-500',
  syntax: 'from-blue-400 to-blue-500',
  prisme: 'from-purple-400 to-purple-500'
}

const strategyLabels: Record<string, string> = {
  momentum: 'Momentum',
  mean_reversion: 'Mean Reversion',
  sentiment: 'Sentiment'
}

export default function AgentCard({ agent, onUpdate }: AgentCardProps) {
  const [sliderValue, setSliderValue] = useState(agent.risk_slider_value * 10)
  const [saving, setSaving] = useState(false)
  
  const getRiskColor = (value: number) => {
    if (value <= 3) return 'text-green-500'
    if (value <= 6) return 'text-yellow-500'
    return 'text-red-500'
  }
  
  const getRiskLabel = (value: number) => {
    if (value <= 3) return 'Conservative'
    if (value <= 6) return 'Moderate'
    return 'Aggressive'
  }
  
  const handleSliderChange = useCallback(async (value: number) => {
    setSliderValue(value)
    setSaving(true)
    
    try {
      await api.configureAgent(agent.name, value / 10)
      onUpdate?.()
    } catch (error) {
      console.error('Failed to update risk:', error)
    } finally {
      setSaving(false)
    }
  }, [agent.name, onUpdate])
  
  const emoji = agentEmojis[agent.name] || '🤖'
  const color = agentColors[agent.name] || 'from-gray-400 to-gray-500'
  const riskColor = getRiskColor(sliderValue)
  const riskLabel = getRiskLabel(sliderValue)
  
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 bg-gradient-to-br ${color} rounded-xl flex items-center justify-center`}>
            <span className="text-2xl">{emoji}</span>
          </div>
          <div>
            <h3 className="font-bold text-gray-900 capitalize">{agent.name}</h3>
            <span className="text-sm text-gray-500">{strategyLabels[agent.strategy] || agent.strategy}</span>
          </div>
        </div>
        <span className={`px-2 py-1 ${agent.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'} rounded-full text-xs font-medium`}>
          {agent.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>
      
      <div className="space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">Win Rate</span>
          <span className="font-medium text-gray-900">{agent.accuracy ? `${(agent.accuracy * 100).toFixed(0)}%` : 'N/A'}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">Predictions</span>
          <span className="font-medium text-gray-900">{agent.total_predictions || 0}</span>
        </div>
        
        {/* Risk Slider */}
        <div className="pt-2">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-gray-500">Risk Level</span>
            <span className={`font-medium ${riskColor}`}>
              {sliderValue.toFixed(0)}/10 ({riskLabel})
              {saving && <span className="ml-2 text-gray-400">saving...</span>}
            </span>
          </div>
          
          <div className="relative">
            <input
              type="range"
              min="1"
              max="10"
              step="1"
              value={sliderValue}
              onChange={(e) => handleSliderChange(Number(e.target.value))}
              className="w-full h-2 rounded-full appearance-none cursor-pointer"
              style={{
                background: `linear-gradient(to right, #22C55E 0%, #F59E0B ${(sliderValue / 10) * 60}%, #EF4444 100%)`
              }}
            />
          </div>
          
          <div className="flex justify-between text-xs mt-1">
            <span className="text-green-500">Conservative</span>
            <span className="text-red-500">Aggressive</span>
          </div>
        </div>
        
        {agent.total_profit !== undefined && (
          <div className="pt-2 border-t border-gray-100">
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Total Profit</span>
              <span className={`font-medium ${agent.total_profit >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                {agent.total_profit >= 0 ? '+' : ''}{agent.total_profit.toFixed(2)}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}