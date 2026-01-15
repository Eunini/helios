'use client'

import { useState, useEffect } from 'react'
import { StatsCard } from '@/components/dashboard/stats-card'
import { Card } from '@/components/ui/card'
import { ChatInterface } from '@/components/chat/chat-interface'
import api from '@/lib/api'
import { formatCurrency, formatDate } from '@/lib/utils'

export default function DashboardPage() {
  const [businessState, setBusinessState] = useState<any>(null)
  const [recentTransactions, setRecentTransactions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true)
        const [stateRes, transRes] = await Promise.all([
          api.getBusinessState(),
          api.listTransactions(5),
        ])
        setBusinessState(stateRes)
        setRecentTransactions(Array.isArray(transRes) ? transRes : [])
      } catch (err) {
        setError('Failed to load dashboard data. Make sure the backend is running.')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    loadData()
    const interval = setInterval(loadData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {businessState && (
          <>
            <StatsCard
              title="Total Cash"
              value={businessState.total_cash || 0}
              subtext="All time sales"
              icon="💰"
            />
            <StatsCard
              title="Inventory Value"
              value={businessState.total_inventory_value || 0}
              subtext="Current stock value"
              icon="📦"
            />
            <StatsCard
              title="Daily Sales"
              value={businessState.daily_sales || 0}
              subtext="Today's revenue"
              icon="📈"
            />
            <StatsCard
              title="Customers"
              value={businessState.total_customers || 0}
              subtext={`${businessState.low_stock_count || 0} items low`}
              icon="👥"
            />
          </>
        )}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Interface */}
        <div className="lg:col-span-2">
          <ChatInterface />
        </div>

        {/* Quick Stats */}
        <Card className="p-6 bg-white">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
          <div className="space-y-4">
            <div className="pb-4 border-b border-gray-200">
              <p className="text-sm text-gray-600">Total Products</p>
              <p className="text-2xl font-bold text-gray-900">
                {businessState?.total_products || 0}
              </p>
            </div>
            <div className="pb-4 border-b border-gray-200">
              <p className="text-sm text-gray-600">Staff Members</p>
              <p className="text-2xl font-bold text-gray-900">
                {businessState?.total_staff || 0}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Low Stock Items</p>
              <p className="text-2xl font-bold text-orange-600">
                {businessState?.low_stock_count || 0}
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Recent Transactions */}
      <Card className="p-6 bg-white">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Transactions</h3>
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {error}
          </div>
        )}
        {recentTransactions.length === 0 && !loading ? (
          <p className="text-gray-500 text-sm">No transactions yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Customer</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Amount</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Items</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
                </tr>
              </thead>
              <tbody>
                {recentTransactions.map((tx) => (
                  <tr key={tx.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-gray-900">
                      {tx.customer_name || 'Walk-in'}
                    </td>
                    <td className="py-3 px-4 font-semibold text-gray-900">
                      {formatCurrency(tx.total || 0)}
                    </td>
                    <td className="py-3 px-4 text-gray-600">
                      {Array.isArray(tx.items) ? tx.items.length : 0} items
                    </td>
                    <td className="py-3 px-4 text-gray-600">
                      {formatDate(tx.created_at || new Date())}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}
