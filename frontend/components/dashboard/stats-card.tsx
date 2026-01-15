'use client'

import React from 'react'
import { Card } from '@/components/ui/card'
import { formatCurrency } from '@/lib/utils'

interface StatsCardProps {
  title: string
  value: string | number
  subtext?: string
  icon?: React.ReactNode
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: number
}

export function StatsCard({
  title,
  value,
  subtext,
  icon,
  trend = 'neutral',
  trendValue,
}: StatsCardProps) {
  return (
    <Card className="p-6 bg-white hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <h3 className="text-2xl font-bold text-gray-900 mt-2">
            {typeof value === 'number' ? formatCurrency(value) : value}
          </h3>
          {subtext && <p className="text-gray-500 text-xs mt-1">{subtext}</p>}
          {trendValue !== undefined && (
            <div className={`text-xs mt-2 ${
              trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-gray-600'
            }`}>
              {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'} {trendValue}%
            </div>
          )}
        </div>
        {icon && <div className="text-3xl opacity-50">{icon}</div>}
      </div>
    </Card>
  )
}
