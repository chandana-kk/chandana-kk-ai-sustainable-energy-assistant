import { motion } from 'framer-motion';
import type { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  unit?: string;
  icon: LucideIcon;
  color?: string;
  delay?: number;
}

export function StatCard({ title, value, unit, icon: Icon, color = 'sky', delay = 0 }: StatCardProps) {
  const colors: Record<string, string> = {
    sky: 'from-sky-500/20 to-sky-600/5 text-sky-400',
    emerald: 'from-emerald-500/20 to-emerald-600/5 text-emerald-400',
    amber: 'from-amber-500/20 to-amber-600/5 text-amber-400',
    violet: 'from-violet-500/20 to-violet-600/5 text-violet-400',
  };
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className={`glass rounded-2xl p-5 bg-gradient-to-br ${colors[color] || colors.sky}`}
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm opacity-70 mb-1">{title}</p>
          <p className="text-2xl font-bold">
            {value}
            {unit && <span className="text-sm font-normal ml-1 opacity-70">{unit}</span>}
          </p>
        </div>
        <Icon className="w-8 h-8 opacity-80" />
      </div>
    </motion.div>
  );
}
