import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

interface Point {
  label: string
  kwh: number
  cost?: number
}

interface EnergyChartProps {
  data: Point[]
  type?: 'area' | 'bar'
}

export default function EnergyChart({ data, type = 'area' }: EnergyChartProps) {
  if (!data.length) return null

  const Chart = type === 'bar' ? BarChart : AreaChart

  return (
    <ResponsiveContainer width="100%" height={280}>
      <Chart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="energyGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#0ea5e9" stopOpacity={0.4} />
            <stop offset="100%" stopColor="#0ea5e9" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
        <XAxis dataKey="label" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip
          contentStyle={{
            background: 'rgba(15,23,42,0.9)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 12,
          }}
        />
        {type === 'bar' ? (
          <Bar dataKey="kwh" fill="#0ea5e9" radius={[6, 6, 0, 0]} />
        ) : (
          <Area
            type="monotone"
            dataKey="kwh"
            stroke="#0ea5e9"
            fill="url(#energyGrad)"
            strokeWidth={2}
          />
        )}
      </Chart>
    </ResponsiveContainer>
  )
}
