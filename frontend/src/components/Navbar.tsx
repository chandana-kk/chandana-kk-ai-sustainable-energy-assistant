import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Moon, Sun, Zap, LogOut, LayoutDashboard, Shield } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useTheme } from '../contexts/ThemeContext'

const LANGS = [
  { code: 'en', label: 'EN' },
  { code: 'kn', label: 'ಕನ್' },
  { code: 'hi', label: 'हि' },
  { code: 'ta', label: 'த' },
  { code: 'te', label: 'తె' },
]

export default function Navbar() {
  const { t, i18n } = useTranslation()
  const { user, logout } = useAuth()
  const { theme, toggle } = useTheme()

  const changeLang = (code: string) => {
    i18n.changeLanguage(code)
    localStorage.setItem('language', code)
  }

  return (
    <motion.nav
      className="glass sticky top-0 z-50 px-4 py-3 mb-6"
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
    >
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        <Link to="/dashboard" className="flex items-center gap-2 font-bold text-lg">
          <Zap className="w-7 h-7 text-brand-500" />
          <span className="bg-gradient-to-r from-brand-500 to-cyan-400 bg-clip-text text-transparent">
            {t('appName')}
          </span>
        </Link>

        <div className="flex items-center gap-2 flex-wrap">
          <div className="flex rounded-lg overflow-hidden border border-slate-600/50">
            {LANGS.map((l) => (
              <button
                key={l.code}
                type="button"
                onClick={() => changeLang(l.code)}
                className={`px-2 py-1 text-xs font-medium ${
                  i18n.language === l.code
                    ? 'bg-brand-500 text-white'
                    : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700'
                }`}
              >
                {l.label}
              </button>
            ))}
          </div>

          <button type="button" onClick={toggle} className="p-2 rounded-lg glass" aria-label="Toggle theme">
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>

          <Link to="/dashboard" className="p-2 rounded-lg glass hidden sm:block" title={t('dashboard')}>
            <LayoutDashboard className="w-5 h-5" />
          </Link>

          {user?.role === 'admin' && (
            <Link to="/admin" className="p-2 rounded-lg glass" title={t('admin')}>
              <Shield className="w-5 h-5" />
            </Link>
          )}

          <button type="button" onClick={logout} className="p-2 rounded-lg glass text-red-400" title={t('logout')}>
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>
    </motion.nav>
  )
}
