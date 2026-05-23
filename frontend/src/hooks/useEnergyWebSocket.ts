import { useEffect, useState } from 'react'
import { getWsUrl } from '../services/api'

export interface LiveReading {
  timestamp: string
  voltage: number
  current: number
  power_kw: number
  power_w: number
  frequency: number
  power_factor: number
  daily_kwh: number
  monthly_kwh: number
  estimated_bill: number
  carbon_kg: number
  appliances: Record<string, number>
}

export function useEnergyWebSocket(token: string | null) {
  const [reading, setReading] = useState<LiveReading | null>(null)
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    if (!token) return

    const ws = new WebSocket(getWsUrl(token))

    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onerror = () => setConnected(false)
    ws.onmessage = (ev) => {
      try {
        setReading(JSON.parse(ev.data))
      } catch {
        /* ignore */
      }
    }

    return () => ws.close()
  }, [token])

  return { reading, connected }
}
