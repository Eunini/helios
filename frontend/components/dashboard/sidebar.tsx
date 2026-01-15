'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { href: '/dashboard', label: 'Overview' },
  { href: '/dashboard/inventory', label: 'Inventory' },
  { href: '/dashboard/customers', label: 'Customers' },
  { href: '/dashboard/staff', label: 'Staff' },
  { href: '/dashboard/insights', label: 'Insights' },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-gray-900 text-white p-6 min-h-screen">
      <h1 className="text-2xl font-bold mb-8">
        <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
          Helios
        </span>
      </h1>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/')
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block px-4 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="mt-8 pt-8 border-t border-gray-700">
        <p className="text-xs text-gray-500">v1.0.0</p>
        <p className="text-xs text-gray-500 mt-2">AI Operations Manager</p>
      </div>
    </aside>
  )
}
