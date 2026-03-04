// Map Scraper Types
export interface MapResult {
    name: string
    phone: string
    website: string
    rating: string
    reviews_count: string
    category: string
    address: string
    plus_code: string
    hours: string
    price_level: string
    price_range: string
    latitude: string
    longitude: string
    link: string
}

// WhatsApp Validator Types
export interface WAResult {
    phone: string
    clean_phone: string
    has_whatsapp: boolean
    is_business: boolean
    business_name: string
    status: string
}

export interface WASummary {
    total: number
    has_whatsapp: number
    has_whatsapp_percent: number
    is_business: number
    is_business_percent: number
}

// Progress Types
export interface Progress {
    current: number
    total: number
    message: string
    current_place: string
}

// Modal Types
export type ModalType = 'success' | 'error' | 'info' | 'warning'

export interface ModalState {
    isOpen: boolean
    title: string
    message: string
    type: ModalType
}

// CSV Preview Types
export interface CSVPreview {
    headers: string[]
    rows: string[][]
}

// Tab Types
export type TabType = 'scraper' | 'wa-validator'
