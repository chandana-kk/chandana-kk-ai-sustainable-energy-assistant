import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  language: string;
  theme: string;
}

export const authApi = {
  register: (data: { email: string; password: string; full_name: string }) =>
    api.post<TokenResponse>('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post<TokenResponse>('/auth/login', data),
  forgotPassword: (email: string) => api.post('/auth/forgot-password', { email }),
  me: () => api.get<User>('/auth/me'),
};

export const energyApi = {
  live: () => api.get('/energy/live'),
  history: () => api.get('/energy/history'),
};

export const predictionsApi = {
  get: (horizon: string) => api.get(`/predictions/${horizon}`),
};

export const recommendationsApi = {
  list: () => api.get('/recommendations'),
};

export const alertsApi = {
  list: () => api.get('/alerts'),
  tips: () => api.get('/alerts/tips'),
};

export const settingsApi = {
  update: (data: Record<string, unknown>) => api.patch('/settings', data),
  chat: (message: string) => api.post('/settings/chat', { message }),
  reportPdf: () =>
    api.get('/settings/report/pdf', { responseType: 'blob' }),
};

export const adminApi = {
  stats: () => api.get('/admin/stats'),
};

export function getWsUrl(): string {
  return import.meta.env.VITE_WS_URL || `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.hostname}:8000/ws/energy`;
}

export default api;
