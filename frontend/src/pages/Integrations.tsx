import { useState } from 'react'

interface Integration {
  id: string
  name: string
  type: 'exchange' | 'notification' | 'data'
  icon: string
  status: 'active' | 'inactive' | 'error'
  description: string
}

const defaultIntegrations: Integration[] = [
  { id: 'binance', name: 'Binance', type: 'exchange', icon: '🟡', status: 'active', description: 'Crypto trading' },
  { id: 'kraken', name: 'Kraken', type: 'exchange', icon: '🟣', status: 'active', description: 'Crypto trading' },
  { id: 'interactive_brokers', name: 'Interactive Brokers', type: 'exchange', icon: '🔵', status: 'active', description: 'Stocks trading' },
  { id: 'telegram', name: 'Telegram', type: 'notification', icon: '📱', status: 'active', description: 'Alerts & commands' },
  { id: 'discord', name: 'Discord', type: 'notification', icon: '💬', status: 'active', description: 'Alerts & commands' },
  { id: 'news_api', name: 'News API', type: 'data', icon: '📰', status: 'active', description: 'Sentiment analysis' },
]

const availableIntegrations: Integration[] = [
  { id: 'coinbase', name: 'Coinbase', type: 'exchange', icon: '🔷', status: 'inactive', description: 'Crypto trading' },
  { id: 'alpaca', name: 'Alpaca', type: 'exchange', icon: '🦙', status: 'inactive', description: 'Stocks trading' },
  { id: 'slack', name: 'Slack', type: 'notification', icon: '💼', status: 'inactive', description: 'Alerts & commands' },
  { id: 'twitter', name: 'Twitter/X', type: 'data', icon: '🐦', status: 'inactive', description: 'Sentiment analysis' },
  { id: 'coingecko', name: 'CoinGecko', type: 'data', icon: '🦎', status: 'inactive', description: 'Price data' },
]

export default function Integrations() {
  const [integrations, setIntegrations] = useState<Integration[]>(defaultIntegrations)
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedType, setSelectedType] = useState<string>('all')
  
  const activeCount = integrations.filter(i => i.status === 'active').length
  const totalCount = 15
  
  const filteredIntegrations = selectedType === 'all' 
    ? integrations 
    : integrations.filter(i => i.type === selectedType)
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-700'
      case 'error': return 'bg-red-100 text-red-700'
      default: return 'bg-gray-100 text-gray-500'
    }
  }
  
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'exchange': return '💱'
      case 'notification': return '🔔'
      case 'data': return '📊'
      default: return '⚙️'
    }
  }
  
  const handleRemove = (id: string) => {
    setIntegrations(prev => prev.filter(i => i.id !== id))
  }
  
  const handleAdd = (integration: Integration) => {
    setIntegrations(prev => [...prev, { ...integration, status: 'active' }])
    setShowAddModal(false)
  }
  
  return (
    <div className="pl-64 min-h-screen bg-background">
      <main className="p-6">
        {/* Title */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Integrations</h1>
            <p className="text-gray-500">Connect your exchanges and data sources</p>
          </div>
          <button 
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium flex items-center gap-2 hover:from-purple-600 hover:to-pink-600 transition-all"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Integration
          </button>
        </div>
        
        {/* Stats */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-8">
          <div className="flex items-center gap-4">
            <div className="text-4xl font-bold text-gray-900">{activeCount} / {totalCount}</div>
            <div className="text-gray-500">connected</div>
          </div>
        </div>
        
        {/* Filters */}
        <div className="flex gap-2 mb-6">
          {['all', 'exchange', 'notification', 'data'].map(type => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedType === type
                  ? 'bg-purple-100 text-purple-700'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              {type === 'all' ? 'All' : type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
        
        {/* Integrations Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {filteredIntegrations.map(integration => (
            <div key={integration.id} className="bg-white rounded-2xl shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center">
                    <span className="text-2xl">{integration.icon}</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900">{integration.name}</h3>
                    <span className="text-sm text-gray-500 capitalize">{integration.type}</span>
                  </div>
                </div>
                <button 
                  onClick={() => handleRemove(integration.id)}
                  className="text-gray-400 hover:text-red-500 transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="flex items-center gap-2">
                <span className={`px-2 py-1 ${getStatusColor(integration.status)} rounded-full text-xs font-medium`}>
                  {integration.status.charAt(0).toUpperCase() + integration.status.slice(1)}
                </span>
                <span className="text-gray-500 text-sm">{integration.description}</span>
              </div>
            </div>
          ))}
          
          {/* Add New Card */}
          <div 
            onClick={() => setShowAddModal(true)}
            className="bg-gray-100 rounded-2xl p-6 flex items-center justify-center cursor-pointer hover:bg-gray-200 transition-colors"
          >
            <div className="text-center">
              <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center mx-auto mb-2 shadow-sm">
                <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              </div>
              <span className="text-gray-500 font-medium">Add Integration</span>
            </div>
          </div>
        </div>
        
        {/* Add Modal */}
        {showAddModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 m-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900">Add Integration</h2>
                <button 
                  onClick={() => setShowAddModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                {availableIntegrations.map(integration => (
                  <button
                    key={integration.id}
                    onClick={() => handleAdd(integration)}
                    className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors text-left"
                  >
                    <span className="text-2xl">{integration.icon}</span>
                    <div>
                      <div className="font-medium text-gray-900">{integration.name}</div>
                      <div className="text-sm text-gray-500">{integration.description}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}