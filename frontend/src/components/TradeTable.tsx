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

interface TradeTableProps {
  trades: Trade[]
  loading?: boolean
}

export default function TradeTable({ trades, loading }: TradeTableProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-sm p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Trades</h2>
        <div className="text-center py-8 text-gray-500">Loading...</div>
      </div>
    )
  }
  
  if (!trades || trades.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-sm p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Trades</h2>
        <div className="text-center py-8 text-gray-500">No trades yet</div>
      </div>
    )
  }
  
  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  }
  
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price)
  }
  
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Trades</h2>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left text-gray-500 text-sm">
              <th className="pb-3">Time</th>
              <th className="pb-3">Asset</th>
              <th className="pb-3">Type</th>
              <th className="pb-3">Price</th>
              <th className="pb-3">Amount</th>
              <th className="pb-3">AI Agent</th>
              <th className="pb-3">P&L</th>
            </tr>
          </thead>
          <tbody className="text-sm">
            {trades.map((trade) => (
              <tr key={trade.id} className="border-t border-gray-100">
                <td className="py-3">{formatTime(trade.created_at)}</td>
                <td className="py-3 font-medium">{trade.symbol}</td>
                <td className="py-3">
                  <span className={`px-2 py-1 rounded text-xs ${
                    trade.side === 'buy' 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-red-100 text-red-700'
                  }`}>
                    {trade.side.toUpperCase()}
                  </span>
                </td>
                <td className="py-3">{formatPrice(trade.price)}</td>
                <td className="py-3">{trade.amount}</td>
                <td className="py-3 capitalize">{trade.agent_name}</td>
                <td className={`py-3 ${trade.pnl && trade.pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  {trade.pnl !== undefined ? `${trade.pnl >= 0 ? '+' : ''}${formatPrice(trade.pnl)}` : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}