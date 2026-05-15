import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Zap } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export function Signup() {
  const { t } = useTranslation();
  const { register } = useAuth();
  const navigate = useNavigate();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(email, password, fullName);
      navigate('/dashboard');
    } catch {
      setError('Registration failed. Email may already exist.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-3xl p-8 w-full max-w-md"
      >
        <div className="flex items-center justify-center gap-2 mb-6 text-sky-400">
          <Zap className="w-10 h-10" />
          <h1 className="text-2xl font-bold">{t('signup')}</h1>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm opacity-80">{t('fullName')}</label>
            <input
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full mt-1 px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10 focus:border-sky-500 outline-none"
            />
          </div>
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
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full mt-1 px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10 focus:border-sky-500 outline-none"
            />
          </div>
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-sky-500 hover:bg-sky-600 font-semibold"
          >
            {t('signup')}
          </button>
        </form>
        <p className="mt-4 text-center text-sm opacity-70">
          {t('hasAccount')}{' '}
          <Link to="/login" className="text-sky-400 hover:underline">
            {t('login')}
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
