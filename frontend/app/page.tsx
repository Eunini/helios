'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      <nav className="flex items-center justify-between p-6 border-b border-gray-700">
        <h1 className="text-2xl font-bold text-white">
          <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Helios
          </span>
        </h1>
        <div className="flex space-x-4">
          <Link href="/dashboard">
            <Button className="bg-blue-600 hover:bg-blue-700">Dashboard</Button>
          </Link>
        </div>
      </nav>

      <main className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-4">
        <div className="max-w-2xl text-center">
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
            AI-Powered Operations
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Helios is an autonomous operations manager designed for small retail businesses in emerging markets. Manage inventory, finances, and customer relationships with AI agents that work 24/7.
          </p>

          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="p-6 rounded-lg bg-white/5 border border-white/10 hover:border-blue-500/50 transition">
              <div className="text-3xl mb-3">📦</div>
              <h3 className="font-semibold text-white mb-2">Inventory Management</h3>
              <p className="text-gray-400 text-sm">
                Real-time stock tracking, low stock alerts, and supplier management
              </p>
            </div>

            <div className="p-6 rounded-lg bg-white/5 border border-white/10 hover:border-blue-500/50 transition">
              <div className="text-3xl mb-3">💰</div>
              <h3 className="font-semibold text-white mb-2">Financial Tracking</h3>
              <p className="text-gray-400 text-sm">
                Automatic transaction recording, cash flow analysis, and financial reports
              </p>
            </div>

            <div className="p-6 rounded-lg bg-white/5 border border-white/10 hover:border-blue-500/50 transition">
              <div className="text-3xl mb-3">📊</div>
              <h3 className="font-semibold text-white mb-2">Business Intelligence</h3>
              <p className="text-gray-400 text-sm">
                Analytics, insights, and actionable recommendations for growth
              </p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard">
              <Button size="lg" className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700">
                Get Started
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              className="w-full sm:w-auto border-white text-white hover:bg-white/10"
              onClick={() => window.location.href = 'https://github.com'}
            >
              Learn More
            </Button>
          </div>

          <div className="mt-16 pt-8 border-t border-gray-700">
            <p className="text-gray-400 text-sm">
              Built with FastAPI, Next.js, and AI agents. Helios v1.0.0
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}
