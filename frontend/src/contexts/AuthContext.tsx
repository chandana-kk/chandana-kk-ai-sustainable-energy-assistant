import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { authApi } from '../services/api'

export interface User {
  id: string
  email: string
  full_name: string
  role: string
  preferred_language: string
  theme: string
}

interface AuthContextValue {
  user: User | null
  token: string | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (data: {
    email: string
    password: string
    full_name: string
    preferred_language?: string
  }) => Promise<void>
  logout: () => void
  setUser: (u: User | null) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  const persist = useCallback((accessToken: string, u: User) => {
    localStorage.setItem('token', accessToken)
    setToken(accessToken)
    setUser(u)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }, [])

  const login = useCallback(
    async (email: string, password: string) => {
      const { data } = await authApi.login(email, password)
      persist(data.access_token, data.user)
    },
    [persist],
  )

  const register = useCallback(
    async (payload: {
      email: string
      password: string
      full_name: string
      preferred_language?: string
    }) => {
      const { data } = await authApi.register(payload)
      persist(data.access_token, data.user)
    },
    [persist],
  )

  useEffect(() => {
    if (!token) {
      setLoading(false)
      return
    }
    authApi
      .me()
      .then(({ data }) => setUser(data))
      .catch(() => logout())
      .finally(() => setLoading(false))
  }, [token, logout])

  const value = useMemo(
    () => ({ user, token, loading, login, register, logout, setUser }),
    [user, token, loading, login, register, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
