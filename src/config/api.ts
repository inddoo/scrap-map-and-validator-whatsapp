/**
 * API configuration
 */

export const API_BASE_URL = 'http://localhost:8000'

export const API_ENDPOINTS = {
    scrape: `${API_BASE_URL}/scrape`,
    progress: `${API_BASE_URL}/progress`,
    stop: `${API_BASE_URL}/stop-scraping`,
    exportCsv: `${API_BASE_URL}/export-csv`,
} as const

export const PROGRESS_POLL_INTERVAL = 1000 // milliseconds
