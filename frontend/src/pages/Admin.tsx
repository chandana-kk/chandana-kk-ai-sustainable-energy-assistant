import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import Navbar from '../components/Navbar'
import { adminApi } from '../services/api'

export default function Admin() {
  const { t } = useTranslation()
  const [stats, setStats] = useState<Record<string, unknown> | null>(null)
  const [users, setUsers] = useState<unknown[]>([])

  useEffect(() => {
    adminApi.stats().then(({ data }) => setStats(data)).catch(() => {})
    adminApi.users().then(({ data }) => setUsers(data.users || [])).catch(() => {})
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 text-white">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 pb-12">
        <h1 className="text-2xl font-bold mb-6">{t('admin')} Panel</h1>
        <div className="grid md:grid-cols-3 gap-4 mb-8">
          {['users', 'energy_readings', 'alerts'].map((key) => (
            <motion.div key={key} className="glass-card" whileHover={{ scale: 1.02 }}>
              <p className="text-slate-400 text-sm capitalize">{key.replace('_', ' ')}</p>
              <p className="text-3xl font-bold">{String(stats?.[key] ?? '—')}</p>
            </motion.div>
          ))}
        </div>
        <div className="glass-card">
          <h2 className="font-semibold mb-4">Users</h2>
          <ul className="space-y-2 text-sm">
            {(users as { email: string; full_name: string; role: string }[]).map((u) => (
              <li key={u.email} className="flex justify-between border-b border-white/5 py-2">
                <span>{u.full_name}</span>
                <span className="text-slate-400">{u.email} · {u.role}</span>
              </li>
            ))}
          </ul>
        </div>
      </main>
    </div>
  )
}
