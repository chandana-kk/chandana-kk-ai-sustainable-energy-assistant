import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import {
  Zap,
  Gauge,
  Activity,
  IndianRupee,
  Leaf,
  Bell,
  Download,
  TrendingUp,
  Lightbulb,
} from 'lucide-react'
import {
  Line,
  LineChart,
  Pie,
  PieChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import Navbar from '../components/Navbar'
import StatCard from '../components/StatCard'
import EnergyChart from '../components/EnergyChart'
import Chatbot from '../components/Chatbot'
import { useAuth } from '../contexts/AuthContext'
import { useEnergyWebSocket } from '../hooks/useEnergyWebSocket'
import {
  energyApi,
  predictionsApi,
  recommendationsApi,
  alertsApi,
  settingsApi,
} from '../services/api'

const COLORS = ['#0ea5e9', '#22d3ee', '#a78bfa', '#f472b6', '#fbbf24', '#34d399']

export default function Dashboard() {
  const { t } = useTranslation()
  const { user, token } = useAuth()
  const { reading, connected } = useEnergyWebSocket(token)
  const [period, setPeriod] = useState('daily')
  const [history, setHistory] = useState<{ label: string; kwh: number }[]>([])
  const [predictions, setPredictions] = useState<{ hour: string; predicted_kwh: number }[]>([])
  const [recs, setRecs] = useState<
    { id: string; title: string; description: string; priority: string; potential_savings_inr: number }[]
  >([])
  const [alerts, setAlerts] = useState<{ message: string; severity: string }[]>([])
  const [appliances, setAppliances] = useState<{ name: string; power_kw: number; percentage: number }[]>([])
  const [tips, setTips] = useState<{ tip: string; savings_percent: number }[]>([])
  const [carbon, setCarbon] = useState<{ carbon_kg_monthly: number; equivalent_trees: number } | null>(null)
  const [peak, setPeak] = useState<Record<string, unknown> | null>(null)

  useEffect(() => {
    energyApi.history(period).then(({ data }) => setHistory(data))
  }, [period])

  useEffect(() => {
    predictionsApi.get('24h').then(({ data }) => setPredictions(data.predictions?.slice(0, 12) || []))
    recommendationsApi.list().then(({ data }) => setRecs(data.recommendations || []))
    recommendationsApi.nilm().then(({ data }) => setAppliances(data.appliances || []))
    alertsApi.list().then(({ data }) => setAlerts(data.alerts || []))
    energyApi.tips().then(({ data }) => setTips(data))
    energyApi.peak().then(({ data }) => setPeak(data))
    settingsApi.carbon().then(({ data }) => setCarbon(data))
  }, [])

  const r = reading

  const downloadReport = () => {
    const url = settingsApi.reportUrl()
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'energy_report.pdf')
    const tok = localStorage.getItem('token')
    fetch(url, { headers: { Authorization: `Bearer ${tok}` } })
      .then((res) => res.blob())
      .then((blob) => {
        link.href = URL.createObjectURL(blob)
        link.click()
      })
  }

  const applianceChart = appliances.length
    ? appliances
    : Object.entries(r?.appliances || {}).map(([name, power_kw]) => ({
        name,
        power_kw,
        percentage: r ? (100 * power_kw) / (r.power_kw || 1) : 0,
      }))

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-100 to-slate-200 dark:from-slate-950 dark:to-slate-900 text-slate-900 dark:text-white">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 pb-24">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mb-6">
          <h1 className="text-2xl md:text-3xl font-bold">
            {t('welcome')}, {user?.full_name}
          </h1>
          <p className="text-slate-500 dark:text-slate-400 flex items-center gap-2 mt-1">
            <span
              className={`w-2 h-2 rounded-full ${connected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}
            />
            {connected ? t('connected') : t('disconnected')} · {t('energyUsage')}
          </p>
        </motion.div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard
            title={t('livePower')}
            value={r ? `${r.power_kw}` : '—'}
            unit="kW"
            icon={Zap}
            color="from-amber-500 to-orange-500"
          />
          <StatCard
            title={t('voltage')}
            value={r ? `${r.voltage}` : '—'}
            unit="V"
            icon={Gauge}
            color="from-brand-500 to-cyan-500"
          />
          <StatCard
            title={t('current')}
            value={r ? `${r.current}` : '—'}
            unit="A"
            icon={Activity}
            color="from-violet-500 to-purple-500"
          />
          <StatCard
            title={t('estimatedBill')}
            value={r ? `₹${r.estimated_bill}` : '—'}
            icon={IndianRupee}
            color="from-emerald-500 to-teal-500"
          />
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2 glass-card">
            <div className="flex justify-between items-center mb-4">
              <h2 className="font-semibold">{t('historicalTrends')}</h2>
              <div className="flex gap-2">
                {(['daily', 'weekly', 'monthly'] as const).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPeriod(p)}
                    className={`px-3 py-1 rounded-lg text-xs ${
                      period === p ? 'bg-brand-500 text-white' : 'bg-slate-700/30'
                    }`}
                  >
                    {t(p)}
                  </button>
                ))}
              </div>
            </div>
            <EnergyChart data={history} />
          </div>

          <div className="glass-card">
            <h2 className="font-semibold mb-4">{t('appliances')} (NILM)</h2>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={applianceChart}
                  dataKey="power_kw"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ name }) => name}
                >
                  {applianceChart.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6 mb-6">
          <div className="glass-card">
            <h2 className="font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-brand-500" />
              {t('predictions')}
            </h2>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={predictions}>
                <XAxis dataKey="hour" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Line type="monotone" dataKey="predicted_kwh" stroke="#0ea5e9" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="glass-card">
            <h2 className="font-semibold mb-4">{t('recommendations')}</h2>
            <ul className="space-y-3 max-h-[220px] overflow-y-auto">
              {recs.map((rec) => (
                <li key={rec.id} className="p-3 rounded-xl bg-slate-800/30 border border-white/5">
                  <div className="flex justify-between">
                    <span className="font-medium text-sm">{rec.title}</span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded ${
                        rec.priority === 'high' ? 'bg-red-500/30' : 'bg-brand-500/30'
                      }`}
                    >
                      {rec.priority}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">{rec.description}</p>
                  <p className="text-xs text-emerald-400 mt-1">Save ~₹{rec.potential_savings_inr}</p>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-6">
          <div className="glass-card">
            <h2 className="font-semibold mb-3 flex items-center gap-2">
              <Bell className="w-5 h-5" /> {t('alerts')}
            </h2>
            {alerts.length === 0 ? (
              <p className="text-sm text-slate-500">{t('noAlerts')}</p>
            ) : (
              <ul className="space-y-2 text-sm">
                {alerts.slice(0, 5).map((a, i) => (
                  <li
                    key={i}
                    className={`p-2 rounded-lg ${
                      a.severity === 'critical' ? 'bg-red-500/20' : 'bg-amber-500/20'
                    }`}
                  >
                    {a.message}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="glass-card">
            <h2 className="font-semibold mb-3 flex items-center gap-2">
              <Leaf className="w-5 h-5 text-emerald-500" /> {t('carbonFootprint')}
            </h2>
            {carbon && (
              <>
                <p className="text-2xl font-bold">{carbon.carbon_kg_monthly} kg CO₂</p>
                <p className="text-sm text-slate-400 mt-1">
                  ≈ {carbon.equivalent_trees} trees to offset (annual est.)
                </p>
              </>
            )}
            <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
              <div>
                <p className="text-slate-500">{t('dailyUsage')}</p>
                <p className="font-semibold">{r?.daily_kwh ?? '—'} kWh</p>
              </div>
              <div>
                <p className="text-slate-500">{t('monthlyUsage')}</p>
                <p className="font-semibold">{r?.monthly_kwh ?? '—'} kWh</p>
              </div>
            </div>
          </div>

          <div className="glass-card">
            <h2 className="font-semibold mb-3 flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-yellow-400" /> {t('savingsTips')}
            </h2>
            <ul className="text-sm space-y-2">
              {tips.slice(0, 4).map((tip, i) => (
                <li key={i}>
                  {tip.tip} — <span className="text-emerald-400">~{tip.savings_percent}%</span>
                </li>
              ))}
            </ul>
            {peak && (
              <p className="text-xs text-slate-500 mt-3">
                {t('peakAnalysis')}: {String(peak.peak_label)} ({String(peak.peak_kwh)} kWh)
              </p>
            )}
          </div>
        </div>

        <button type="button" onClick={downloadReport} className="btn-primary flex items-center gap-2">
          <Download className="w-4 h-4" />
          {t('downloadReport')}
        </button>
      </main>
      <Chatbot />
    </div>
  )
}
