/**
 * Build search query for Google Maps
 */
export const buildSearchQuery = (category: string, province: string, city: string): string => {
    let location = ''
    const cat = category.trim()
    const prov = province.trim()
    const cty = city.trim()

    if (cty && prov) {
        location = `${cty}, ${prov}`
    } else if (cty) {
        location = cty
    } else if (prov) {
        location = prov
    }

    return `${cat} ${location}`
}

/**
 * Scroll element into view smoothly
 */
export const scrollToElement = (elementId: string, delay: number = 0) => {
    setTimeout(() => {
        const element = document.getElementById(elementId)
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
    }, delay)
}

/**
 * Parse phone numbers from text (one per line)
 */
export const parsePhoneNumbers = (text: string): string[] => {
    return text
        .split('\n')
        .map(n => n.trim())
        .filter(n => n.length > 0)
}
