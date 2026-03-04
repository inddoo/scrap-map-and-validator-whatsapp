import type { MapResult, CSVPreview } from '../types'

/**
 * Parse CSV file and extract phone numbers
 */
export const parseCSVFile = async (file: File): Promise<{ phones: string[], preview: CSVPreview }> => {
    const text = await file.text()
    const lines = text.split('\n').filter(line => line.trim())

    if (lines.length === 0) {
        throw new Error('File CSV tidak berisi data!')
    }

    // Parse CSV header
    const headers = lines[0].split(',').map(h => h.trim())
    const headersLower = headers.map(h => h.toLowerCase())
    const phoneIndex = headersLower.findIndex(h => h === 'phone' || h === 'nomor' || h === 'telepon')

    if (phoneIndex === -1) {
        throw new Error('CSV harus memiliki kolom "phone"!')
    }

    // Extract phone numbers and full rows
    const phones: string[] = []
    const rows: string[][] = []

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim())
        if (values[phoneIndex]) {
            const phone = values[phoneIndex].replace(/[^0-9]/g, '')
            if (phone) {
                phones.push(phone)
                rows.push(values)
            }
        }
    }

    if (phones.length === 0) {
        throw new Error('Tidak ada nomor telepon valid di CSV!')
    }

    return {
        phones,
        preview: { headers, rows }
    }
}

/**
 * Export map results to CSV
 */
export const exportMapResultsToCSV = (results: MapResult[], category: string, location: string) => {
    const headers = [
        'name', 'phone', 'website', 'rating', 'reviews_count', 'category',
        'address', 'plus_code', 'hours', 'price_level', 'price_range',
        'latitude', 'longitude', 'link'
    ]

    const csvRows = []

    // Add header row
    csvRows.push(headers.join(','))

    // Add data rows
    for (const row of results) {
        const values = headers.map(header => {
            const value = row[header as keyof MapResult] || ''
            const escaped = String(value).replace(/"/g, '""')
            return `"${escaped}"`
        })
        csvRows.push(values.join(','))
    }

    // Create CSV string
    const csvContent = csvRows.join('\n')

    // Create blob with UTF-8 BOM for Excel
    const BOM = '\uFEFF'
    const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })

    // Create download link
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url

    const locationStr = location || 'data'
    const filename = `google_maps_${category}_${locationStr.replace(/\s+/g, '_')}.csv`
    a.download = filename

    document.body.appendChild(a)
    a.click()

    // Cleanup
    setTimeout(() => {
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
    }, 100)

    return filename
}

/**
 * Download blob as file
 */
export const downloadBlob = (blob: Blob, filename: string) => {
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()

    setTimeout(() => {
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
    }, 100)
}
