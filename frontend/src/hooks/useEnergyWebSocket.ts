import { useEffect, useRef, useState, useCallback } from 'react';
import { getWsUrl } from '../services/api';

export interface EnergyData {
  live: {
    voltage: number;
    current: number;
    power_kw: number;
    power_factor: number;
    frequency: number;
    timestamp: string;
  };
  daily_kwh: number;
  weekly_kwh: number;
  monthly_kwh: number;
  estimated_bill: number;
  carbon_kg: number;
  appliances: { name: string; power_w: number; share_percent: number; category: string }[];
  peak_hour: string;
  savings_potential: number;
}

export function useEnergyWebSocket(enabled = true) {
  const [data, setData] = useState<EnergyData | null>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (!enabled) return;
    const ws = new WebSocket(getWsUrl());
    wsRef.current = ws;
    ws.onopen = () => setConnected(true);
    ws.onmessage = (e) => {
      try {
        setData(JSON.parse(e.data));
      } catch {
        /* ignore parse errors */
      }
    };
    ws.onclose = () => {
      setConnected(false);
      setTimeout(connect, 3000);
    };
    ws.onerror = () => ws.close();
  }, [enabled]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  return { data, connected };
}
