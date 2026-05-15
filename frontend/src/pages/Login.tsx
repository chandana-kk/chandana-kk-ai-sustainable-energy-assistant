import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Zap } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export function Login() {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass rounded-3xl p-8 w-full max-w-md"
      >
        <div className="flex items-center justify-center gap-2 mb-6 text-sky-400">
          <Zap className="w-10 h-10" />
          <h1 className="text-2xl font-bold">{t('appName')}</h1>
        </div>
        <p className="text-center text-sm opacity-70 mb-8">{t('tagline')}</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm opacity-80">{t('email')}</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full mt-1 px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10 focus:border-sky-500 outline-none"
            />
          </div>
          <div>
            <label className="text-sm opacity-80">{t('password')}</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full mt-1 px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10 focus:border-sky-500 outline-none"
            />
          </div>
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-sky-500 hover:bg-sky-600 font-semibold transition disabled:opacity-50"
          >
            {loading ? '...' : t('login')}
          </button>
        </form>
        <p className="mt-4 text-center text-sm">
          <Link to="/forgot-password" className="text-sky-400 hover:underline">
            {t('forgotPassword')}
          </Link>
        </p>
        <p className="mt-4 text-center text-sm opacity-70">
          {t('noAccount')}{' '}
          <Link to="/signup" className="text-sky-400 hover:underline">
            {t('signup')}
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
