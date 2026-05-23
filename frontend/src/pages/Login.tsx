import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Zap } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'

export default function Login() {
  const { t } = useTranslation()
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('demo@smartenergy.ai')
  const [password, setPassword] = useState('demo123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch {
      setError('Invalid credentials. Run database/seed.py for demo user.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4">
      <motion.div
        className="glass w-full max-w-md p-8 rounded-3xl"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
      >
        <div className="text-center mb-8">
          <Zap className="w-12 h-12 text-brand-500 mx-auto mb-3" />
          <h1 className="text-2xl font-bold text-white">{t('appName')}</h1>
          <p className="text-slate-400 text-sm mt-1">{t('tagline')}</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm text-slate-400">{t('email')}</label>
            <input
              type="email"
              className="input-field mt-1"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="text-sm text-slate-400">{t('password')}</label>
            <input
              type="password"
              className="input-field mt-1"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {loading ? '...' : t('login')}
          </button>
        </form>
        <p className="text-center mt-4 text-sm text-slate-400">
          <Link to="/forgot-password" className="text-brand-400 hover:underline">
            {t('forgotPassword')}
          </Link>
        </p>
        <p className="text-center mt-2 text-sm text-slate-500">
          {t('dontHaveAccount')}{' '}
          <Link to="/signup" className="text-brand-400 hover:underline">
            {t('signup')}
          </Link>
        </p>
      </motion.div>
    </div>
  )
}
