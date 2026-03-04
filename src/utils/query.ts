/**
 * Query building utilities
 */

export interface QueryParams {
    category: string
    province: string
    city: string
}

/**
 * Build search query from form inputs
 */
export function buildQuery(params: QueryParams): string {
    const { category, province, city } = params

    let location = ''
    if (province.trim() && city.trim()) {
        location = `${city.trim()}, ${province.trim()}`
    } else if (city.trim()) {
        location = city.trim()
    } else if (province.trim()) {
        location = province.trim()
    }

    return category.trim() ? `${category.trim()} ${location}` : location
}

/**
 * Validate query parameters
 */
export function validateQuery(params: QueryParams): string | null {
    const { category, province, city } = params

    if (!category.trim()) {
        return 'Masukkan kategori!'
    }

    if (!province.trim() && !city.trim()) {
        return 'Masukkan minimal provinsi atau kota!'
    }

    return null
}

/**
 * Build CSV filename from query params
 */
export function buildCsvFilename(params: QueryParams): string {
    const { category, province, city } = params
    const locationStr = city || province || 'data'
    return `google_maps_${category}_${locationStr.replace(/\s+/g, '_')}.csv`
}
