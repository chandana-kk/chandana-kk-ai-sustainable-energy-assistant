import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Zap, Sun, Moon, LogOut, Shield } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { languages } from '../i18n';
import { settingsApi } from '../services/api';

export function Navbar() {
  const { t, i18n } = useTranslation();
  const { user, logout } = useAuth();
  const { theme, toggle } = useTheme();

  const changeLanguage = async (code: string) => {
    i18n.changeLanguage(code);
    localStorage.setItem('language', code);
    try {
      await settingsApi.update({ language: code });
    } catch {
      /* offline ok */
    }
  };

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass sticky top-0 z-50 px-4 py-3"
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        <Link to="/dashboard" className="flex items-center gap-2 text-sky-400 font-bold text-lg">
          <Zap className="w-7 h-7" />
          <span>{t('appName')}</span>
        </Link>
        <div className="flex items-center gap-2 flex-wrap justify-end">
          <select
            value={i18n.language}
            onChange={(e) => changeLanguage(e.target.value)}
            className="glass rounded-lg px-2 py-1.5 text-sm bg-transparent border border-white/10"
            aria-label={t('language')}
          >
            {languages.map((l) => (
              <option key={l.code} value={l.code} className="bg-slate-800">
                {l.label}
              </option>
            ))}
          </select>
          <button
            onClick={toggle}
            className="p-2 rounded-lg glass hover:bg-white/5 transition"
            aria-label={theme === 'dark' ? t('lightMode') : t('darkMode')}
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
          {user?.role === 'admin' && (
            <Link to="/admin" className="p-2 rounded-lg glass hover:bg-white/5" title={t('admin')}>
              <Shield className="w-5 h-5" />
            </Link>
          )}
          <button
            onClick={logout}
            className="flex items-center gap-1 px-3 py-2 rounded-lg bg-red-500/20 text-red-300 hover:bg-red-500/30 text-sm"
          >
            <LogOut className="w-4 h-4" />
            {t('logout')}
          </button>
        </div>
      </div>
    </motion.nav>
  );
}
