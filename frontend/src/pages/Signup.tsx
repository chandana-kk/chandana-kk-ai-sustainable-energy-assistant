import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Zap } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'

export default function Signup() {
  const { t, i18n } = useTranslation()
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    email: '',
    password: '',
    full_name: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register({
        ...form,
        preferred_language: i18n.language,
      })
      navigate('/dashboard')
    } catch {
      setError('Registration failed. Email may already exist.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4">
      <motion.div
        className="glass w-full max-w-md p-8 rounded-3xl"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="text-center mb-8">
          <Zap className="w-12 h-12 text-brand-500 mx-auto mb-3" />
          <h1 className="text-2xl font-bold text-white">{t('createAccount')}</h1>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            className="input-field"
            placeholder={t('fullName')}
            value={form.full_name}
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            required
          />
          <input
            type="email"
            className="input-field"
            placeholder={t('email')}
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
          <input
            type="password"
            className="input-field"
            placeholder={t('password')}
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            minLength={6}
            required
          />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {t('signup')}
          </button>
        </form>
        <p className="text-center mt-4 text-sm text-slate-500">
          {t('alreadyHaveAccount')}{' '}
          <Link to="/login" className="text-brand-400 hover:underline">
            {t('login')}
          </Link>
        </p>
      </motion.div>
    </div>
  )
}
