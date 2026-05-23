import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (data: {
    email: string
    password: string
    full_name: string
    preferred_language?: string
  }) => api.post('/auth/register', data),
  forgotPassword: (email: string) => api.post('/auth/forgot-password', { email }),
  me: () => api.get('/auth/me'),
}

export const energyApi = {
  live: () => api.get('/energy/live'),
  history: (period: string) => api.get('/energy/history', { params: { period } }),
  peak: () => api.get('/energy/peak-analysis'),
  tips: () => api.get('/energy/savings-tips'),
}

export const predictionsApi = {
  get: (horizon: string) => api.get(`/predictions/${horizon}`),
  cost: () => api.get('/predictions/cost-estimate'),
}

export const recommendationsApi = {
  list: () => api.get('/recommendations'),
  nilm: () => api.get('/recommendations/nilm'),
}

export const alertsApi = {
  list: () => api.get('/alerts'),
}

export const settingsApi = {
  update: (data: Record<string, string>) => api.patch('/settings/profile', data),
  chat: (message: string) => api.post('/settings/chat', { message }),
  carbon: () => api.get('/settings/carbon-footprint'),
  reportUrl: () => `${API_BASE}/api/v1/settings/report/pdf`,
}

export const adminApi = {
  stats: () => api.get('/admin/stats'),
  users: () => api.get('/admin/users'),
}

export function getWsUrl(token: string): string {
  const wsBase = import.meta.env.VITE_WS_URL || API_BASE.replace(/^http/, 'ws')
  return `${wsBase}/ws/energy?token=${token}`
}
