import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Users, Activity, Zap, Server } from 'lucide-react';
import { Navbar } from '../components/Navbar';
import { StatCard } from '../components/StatCard';
import { adminApi } from '../services/api';

export function Admin() {
  const { t } = useTranslation();
  const [stats, setStats] = useState({
    total_users: 0,
    active_sessions: 0,
    total_energy_kwh: 0,
    avg_daily_kwh: 0,
    system_status: 'unknown',
  });

  useEffect(() => {
    adminApi.stats().then((r) => setStats(r.data)).catch(() => {});
  }, []);

  return (
    <div className="min-h-screen gradient-bg">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-2xl font-bold mb-6">{t('adminStats')}</h1>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard title="Total Users" value={stats.total_users} icon={Users} />
          <StatCard title="Active Sessions" value={stats.active_sessions} icon={Activity} color="emerald" />
          <StatCard title="Total Energy" value={stats.total_energy_kwh} unit="kWh" icon={Zap} color="amber" />
          <StatCard title="System" value={stats.system_status} icon={Server} color="violet" />
        </div>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass rounded-2xl p-6 mt-6"
        >
          <p className="opacity-70 text-sm">
            Admin panel for user analytics and system monitoring. Seed admin via POST /api/v1/admin/seed-admin
          </p>
        </motion.div>
      </main>
    </div>
  );
}
