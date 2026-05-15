import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import {
  Zap,
  Activity,
  Gauge,
  IndianRupee,
  Leaf,
  TrendingUp,
  AlertTriangle,
  Download,
  Volume2,
} from 'lucide-react';
import { Navbar } from '../components/Navbar';
import { StatCard } from '../components/StatCard';
import { EnergyChart } from '../components/EnergyChart';
import { Chatbot } from '../components/Chatbot';
import { useAuth } from '../contexts/AuthContext';
import { useEnergyWebSocket } from '../hooks/useEnergyWebSocket';
import {
  energyApi,
  predictionsApi,
  recommendationsApi,
  alertsApi,
  settingsApi,
} from '../services/api';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

const COLORS = ['#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#64748b'];

export function Dashboard() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const { data: live, connected } = useEnergyWebSocket();
  const [chartTab, setChartTab] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  const [history, setHistory] = useState<{ daily: { label: string; value: number }[]; weekly: unknown[]; monthly: unknown[] } | null>(null);
  const [predictions, setPredictions] = useState<{ points: { label: string; actual?: number; predicted: number }[]; peak_load_kw: number; confidence: number } | null>(null);
  const [recommendations, setRecommendations] = useState<{ id: string; title: string; description: string; impact: string }[]>([]);
  const [alerts, setAlerts] = useState<{ id: string; message: string; severity: string }[]>([]);
  const [tips, setTips] = useState<string[]>([]);

  useEffect(() => {
    energyApi.history().then((r) => setHistory(r.data)).catch(() => {});
    predictionsApi.get('daily').then((r) => setPredictions(r.data)).catch(() => {});
    recommendationsApi.list().then((r) => setRecommendations(r.data)).catch(() => {});
    alertsApi.list().then((r) => setAlerts(r.data)).catch(() => {});
    alertsApi.tips().then((r) => setTips(r.data.tips)).catch(() => {});
  }, []);

  const downloadReport = async () => {
    const { data } = await settingsApi.reportPdf();
    const url = URL.createObjectURL(data);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'energy_report.pdf';
    a.click();
  };

  const chartData =
    chartTab === 'daily'
      ? history?.daily
      : chartTab === 'weekly'
        ? (history?.weekly as { label: string; value: number }[])
        : (history?.monthly as { label: string; value: number }[]);

  const applianceData =
    live?.appliances?.map((a) => ({ name: a.name, value: a.share_percent })) || [];

  return (
    <div className="min-h-screen gradient-bg">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <h1 className="text-2xl font-bold">
            {t('welcome')}, {user?.full_name}
          </h1>
          <p className="text-sm opacity-60 flex items-center gap-2 mt-1">
            <span className={`w-2 h-2 rounded-full ${connected ? 'bg-emerald-400' : 'bg-red-400'}`} />
            {t('liveData')} — {connected ? 'WebSocket' : 'Polling'}
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard title={t('voltage')} value={live?.live?.voltage ?? '—'} unit="V" icon={Zap} delay={0} />
          <StatCard title={t('current')} value={live?.live?.current ?? '—'} unit="A" icon={Activity} color="emerald" delay={0.05} />
          <StatCard title={t('power')} value={live?.live?.power_kw ?? '—'} unit="kW" icon={Gauge} color="amber" delay={0.1} />
          <StatCard title={t('energyUsage')} value={live?.daily_kwh ?? '—'} unit={t('kwh')} icon={TrendingUp} color="violet" delay={0.15} />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard title={t('estimatedBill')} value={`₹${live?.estimated_bill?.toFixed(0) ?? '—'}`} icon={IndianRupee} />
          <StatCard title={t('carbonFootprint')} value={live?.carbon_kg?.toFixed(1) ?? '—'} unit="kg CO₂" icon={Leaf} color="emerald" />
          <StatCard title={t('savings')} value={`₹${live?.savings_potential?.toFixed(0) ?? '—'}`} icon={TrendingUp} color="violet" />
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 glass rounded-2xl p-5">
            <div className="flex gap-2 mb-4">
              {(['daily', 'weekly', 'monthly'] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setChartTab(tab)}
                  className={`px-4 py-1.5 rounded-lg text-sm ${
                    chartTab === tab ? 'bg-sky-500 text-white' : 'bg-white/5'
                  }`}
                >
                  {t(tab)}
                </button>
              ))}
            </div>
            <h2 className="font-semibold mb-2">{t('history')}</h2>
            <EnergyChart data={chartData || []} />
          </div>
          <div className="glass rounded-2xl p-5">
            <h2 className="font-semibold mb-4">{t('appliances')}</h2>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie data={applianceData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                  {applianceData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <div className="glass rounded-2xl p-5">
            <h2 className="font-semibold mb-4">{t('predictions')}</h2>
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={predictions?.points || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" />
                <XAxis dataKey="label" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="actual" stroke="#94a3b8" dot={false} />
                <Line type="monotone" dataKey="predicted" stroke="#0ea5e9" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-xs opacity-60 mt-2">
              Peak: {predictions?.peak_load_kw} kW · Confidence: {((predictions?.confidence ?? 0) * 100).toFixed(0)}%
            </p>
          </div>
          <div className="glass rounded-2xl p-5">
            <h2 className="font-semibold mb-4">{t('recommendations')}</h2>
            <div className="space-y-3 max-h-72 overflow-y-auto">
              {recommendations.map((r, i) => (
                <motion.div
                  key={r.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="p-3 rounded-xl bg-sky-500/10 border border-sky-500/20"
                >
                  <p className="font-medium text-sm">{r.title}</p>
                  <p className="text-xs opacity-70 mt-1">{r.description}</p>
                  <span className="text-xs text-sky-400 capitalize">{r.impact} impact</span>
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        <motion.div className="grid lg:grid-cols-3 gap-6">
          <div className="glass rounded-2xl p-5">
            <h2 className="font-semibold mb-3 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              {t('alerts')}
            </h2>
            <ul className="space-y-2">
              {alerts.map((a) => (
                <li
                  key={a.id}
                  className={`text-sm p-2 rounded-lg ${
                    a.severity === 'critical'
                      ? 'bg-red-500/20'
                      : a.severity === 'warning'
                        ? 'bg-amber-500/20'
                        : 'bg-sky-500/10'
                  }`}
                >
                  {a.message}
                </li>
              ))}
            </ul>
          </div>
          <div className="glass rounded-2xl p-5">
            <h2 className="font-semibold mb-3">{t('tips')}</h2>
            <ul className="space-y-2 text-sm opacity-80">
              {tips.map((tip, i) => (
                <li key={i} className="flex gap-2">
                  <span className="text-sky-400">•</span>
                  {tip}
                </li>
              ))}
            </ul>
          </div>
          <div className="glass rounded-2xl p-5">
            <h2 className="font-semibold mb-3">{t('peakAnalysis')}</h2>
            <p className="text-sm opacity-80">{live?.peak_hour || '18:00 - 22:00'}</p>
            <p className="text-xs opacity-60 mt-4">Voice alerts placeholder — integrate Web Speech API for hardware events.</p>
            <button
              className="mt-3 flex items-center gap-2 text-sm text-sky-400"
              title="Voice alert placeholder"
            >
              <Volume2 className="w-4 h-4" /> Voice alerts (coming soon)
            </button>
            <button
              onClick={downloadReport}
              className="mt-4 flex items-center gap-2 px-4 py-2 rounded-lg bg-sky-500/20 text-sky-300 text-sm hover:bg-sky-500/30"
            >
              <Download className="w-4 h-4" />
              {t('downloadReport')}
            </button>
          </div>
        </motion.div>
      </main>
      <Chatbot />
    </div>
  );
}
