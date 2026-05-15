import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, X, Send } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { settingsApi } from '../services/api';

export function Chatbot() {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<{ role: 'user' | 'bot'; text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    const msg = input.trim();
    setInput('');
    setMessages((m) => [...m, { role: 'user', text: msg }]);
    setLoading(true);
    try {
      const { data } = await settingsApi.chat(msg);
      setMessages((m) => [...m, { role: 'bot', text: data.reply }]);
    } catch {
      setMessages((m) => [...m, { role: 'bot', text: 'Unable to reach assistant. Check backend connection.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setOpen(!open)}
        className="fixed bottom-6 right-6 z-50 p-4 rounded-full bg-sky-500 text-white shadow-lg shadow-sky-500/30"
        aria-label={t('chatbot')}
      >
        {open ? <X className="w-6 h-6" /> : <MessageCircle className="w-6 h-6" />}
      </motion.button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-24 right-6 z-50 w-96 max-w-[calc(100vw-3rem)] glass rounded-2xl flex flex-col max-h-[420px] shadow-2xl"
          >
            <div className="p-4 border-b border-white/10 font-semibold">{t('chatbot')}</div>
            <div className="flex-1 overflow-y-auto p-4 space-y-3 min-h-[200px]">
              {messages.length === 0 && (
                <p className="text-sm opacity-60">Ask about bills, predictions, or savings tips.</p>
              )}
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`text-sm p-2 rounded-lg ${
                    m.role === 'user' ? 'bg-sky-500/20 ml-8' : 'bg-slate-700/50 mr-8'
                  }`}
                >
                  {m.text}
                </div>
              ))}
              {loading && <p className="text-xs opacity-50">Thinking...</p>}
            </div>
            <div className="p-3 flex gap-2 border-t border-white/10">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && send()}
                className="flex-1 bg-slate-800/50 rounded-lg px-3 py-2 text-sm border border-white/10"
                placeholder="Type a message..."
              />
              <button onClick={send} className="p-2 bg-sky-500 rounded-lg">
                <Send className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
