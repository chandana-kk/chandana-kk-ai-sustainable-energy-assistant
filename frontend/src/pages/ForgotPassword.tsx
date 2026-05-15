import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { authApi } from '../services/api';

export function ForgotPassword() {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await authApi.forgotPassword(email);
    setSent(true);
  };

  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center p-4">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-3xl p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold mb-2">{t('forgotPassword')}</h1>
        {sent ? (
          <p className="text-emerald-400">Reset instructions sent if the email exists.</p>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4 mt-4">
            <input
              type="email"
              required
              placeholder={t('email')}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-slate-800/50 border border-white/10"
            />
            <button type="submit" className="w-full py-3 rounded-xl bg-sky-500 font-semibold">
              {t('sendReset')}
            </button>
          </form>
        )}
        <Link to="/login" className="block mt-4 text-center text-sky-400 text-sm">
          {t('login')}
        </Link>
      </motion.div>
    </div>
  );
}
