import { motion } from 'framer-motion'
import type { LucideIcon } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string
  unit?: string
  icon: LucideIcon
  trend?: string
  color?: string
}

export default function StatCard({
  title,
  value,
  unit,
  icon: Icon,
  trend,
  color = 'from-brand-500 to-cyan-500',
}: StatCardProps) {
  return (
    <motion.div
      className="glass-card"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500 dark:text-slate-400">{title}</p>
          <p className="text-2xl font-bold mt-1 text-slate-900 dark:text-white">
            {value}
            {unit && <span className="text-base font-normal text-slate-500 ml-1">{unit}</span>}
          </p>
          {trend && <p className="text-xs text-emerald-500 mt-1">{trend}</p>}
        </div>
        <div className={`p-3 rounded-xl bg-gradient-to-br ${color} shadow-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </motion.div>
  )
}
