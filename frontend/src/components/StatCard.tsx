interface StatCardProps {
  title: string
  value: string | number
  subtitle?: string
  icon: React.ReactNode
  trend?: {
    value: number
    isPositive: boolean
  }
  color?: 'default' | 'green' | 'blue' | 'orange'
}

const colorClasses = {
  default: 'text-gray-900',
  green: 'text-green-500',
  blue: 'text-blue-500',
  orange: 'text-orange-500'
}

const iconColorClasses = {
  default: 'text-gray-500',
  green: 'text-green-500',
  blue: 'text-blue-500',
  orange: 'text-orange-500'
}

export default function StatCard({ title, value, subtitle, icon, trend, color = 'default' }: StatCardProps) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-500 text-sm">{title}</span>
        <span className={iconColorClasses[color]}>
          {icon}
        </span>
      </div>
      <div className={`text-3xl font-bold ${colorClasses[color]}`}>
        {value}
      </div>
      {(subtitle || trend) && (
        <div className="mt-1">
          {trend ? (
            <span className={trend.isPositive ? 'text-green-500 text-sm' : 'text-red-500 text-sm'}>
              {trend.isPositive ? '+' : ''}{trend.value}%
            </span>
          ) : (
            <span className="text-gray-500 text-sm">{subtitle}</span>
          )}
        </div>
      )}
    </div>
  )
}