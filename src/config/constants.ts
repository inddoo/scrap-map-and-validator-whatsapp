// API Configuration
export const API_BASE_URL = 'http://localhost:8000'

// API Endpoints
export const API_ENDPOINTS = {
    SCRAPE: '/scrape',
    PROGRESS: '/progress',
    STOP_SCRAPING: '/stop-scraping',
    WA_INIT: '/wa/init',
    WA_VALIDATE: '/wa/validate',
    WA_VALIDATE_CSV: '/wa/validate-csv',
    WA_EXPORT: '/wa/export',
    WA_CLOSE: '/wa/close'
} as const

// Modal Configuration
export const MODAL_COLORS = {
    success: 'from-green-500 to-emerald-500',
    error: 'from-red-500 to-pink-500',
    info: 'from-blue-500 to-indigo-500',
    warning: 'from-yellow-500 to-orange-500'
} as const

export const MODAL_ICONS = {
    success: '✅',
    error: '❌',
    info: 'ℹ️',
    warning: '⚠️'
} as const

// Timing Configuration
export const TIMING = {
    PROGRESS_INTERVAL: 1000,
    SCROLL_DELAY: 500
} as const
