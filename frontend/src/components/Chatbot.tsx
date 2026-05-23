import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageCircle, X, Send } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { settingsApi } from '../services/api'

export default function Chatbot() {
  const { t } = useTranslation()
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<{ role: 'user' | 'bot'; text: string }[]>([])
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!input.trim()) return
    const userMsg = input.trim()
    setInput('')
    setMessages((m) => [...m, { role: 'user', text: userMsg }])
    setLoading(true)
    try {
      const { data } = await settingsApi.chat(userMsg)
      setMessages((m) => [...m, { role: 'bot', text: data.reply }])
    } catch {
      setMessages((m) => [
        ...m,
        { role: 'bot', text: 'Unable to reach assistant. Check backend connection.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <motion.button
        type="button"
        className="fixed bottom-6 right-6 z-50 p-4 rounded-full bg-gradient-to-r from-brand-500 to-cyan-500 text-white shadow-2xl"
        onClick={() => setOpen(!open)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {open ? <X className="w-6 h-6" /> : <MessageCircle className="w-6 h-6" />}
      </motion.button>

      <AnimatePresence>
        {open && (
          <motion.div
            className="fixed bottom-24 right-6 z-50 w-80 sm:w-96 glass rounded-2xl overflow-hidden flex flex-col max-h-[420px]"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
          >
            <div className="p-3 border-b border-white/10 font-semibold">{t('chatbot')}</div>
            <div className="flex-1 overflow-y-auto p-3 space-y-2 min-h-[200px]">
              {messages.length === 0 && (
                <p className="text-sm text-slate-500">{t('askAssistant')}</p>
              )}
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`text-sm p-2 rounded-lg max-w-[90%] ${
                    msg.role === 'user'
                      ? 'ml-auto bg-brand-500/30'
                      : 'bg-slate-700/50'
                  }`}
                >
                  {msg.text}
                </div>
              ))}
              {loading && <p className="text-xs text-slate-500">...</p>}
            </div>
            <div className="p-2 flex gap-2 border-t border-white/10">
              <input
                className="flex-1 input-field text-sm py-2"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && send()}
                placeholder={t('askAssistant')}
              />
              <button type="button" onClick={send} className="btn-primary p-2">
                <Send className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
