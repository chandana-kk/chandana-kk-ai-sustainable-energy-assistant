import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en.json'
import kn from './locales/kn.json'
import hi from './locales/hi.json'
import ta from './locales/ta.json'
import te from './locales/te.json'

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    kn: { translation: kn },
    hi: { translation: hi },
    ta: { translation: ta },
    te: { translation: te },
  },
  lng: localStorage.getItem('language') || 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
})

export default i18n
