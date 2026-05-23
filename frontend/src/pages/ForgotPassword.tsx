import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { authApi } from '../services/api'

export default function ForgotPassword() {
  const { t } = useTranslation()
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await authApi.forgotPassword(email)
    setSent(true)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-slate-900 p-4">
      <motion.div className="glass w-full max-w-md p-8 rounded-3xl" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <h1 className="text-xl font-bold text-white mb-4">{t('forgotPassword')}</h1>
        {sent ? (
          <p className="text-emerald-400">Reset link sent if account exists.</p>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email"
              className="input-field"
              placeholder={t('email')}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <button type="submit" className="btn-primary w-full">
              {t('sendReset')}
            </button>
          </form>
        )}
        <Link to="/login" className="block text-center mt-4 text-brand-400 text-sm">
          {t('login')}
        </Link>
      </motion.div>
    </div>
  )
}
