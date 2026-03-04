import { API_BASE_URL, API_ENDPOINTS } from '../config/constants'
import type { MapResult, WAResult, WASummary, Progress } from '../types'

// Scraper API
export const scraperAPI = {
    scrape: async (query: string) => {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.SCRAPE}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.detail || 'Terjadi kesalahan pada server')
        }

        return response.json() as Promise<{ data: MapResult[], count: number }>
    },

    getProgress: async () => {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.PROGRESS}`)
        return response.json() as Promise<Progress>
    },

    stopScraping: async () => {
        await fetch(`${API_BASE_URL}${API_ENDPOINTS.STOP_SCRAPING}`, {
            method: 'POST'
        })
    }
}

// WhatsApp Validator API
export const waValidatorAPI = {
    init: async () => {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.WA_INIT}`, {
            method: 'POST'
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.detail || 'Gagal inisialisasi WhatsApp checker')
        }

        return response.json() as Promise<{ message: string }>
    },

    validate: async (phoneNumbers: string[]) => {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.WA_VALIDATE}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone_numbers: phoneNumbers })
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.detail || 'Gagal validasi nomor')
        }

        return response.json() as Promise<{ results: WAResult[], summary: WASummary }>
    },

    validateCSV: async (file: File) => {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.WA_VALIDATE_CSV}`, {
            method: 'POST',
            body: formData
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.detail || 'Gagal validasi nomor')
        }

        return response.json() as Promise<{ results: WAResult[], summary: WASummary }>
    },

    export: async () => {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.WA_EXPORT}`)

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.detail || 'Gagal export hasil')
        }

        return response.blob()
    },

    close: async () => {
        await fetch(`${API_BASE_URL}${API_ENDPOINTS.WA_CLOSE}`, {
            method: 'POST'
        })
    }
}
