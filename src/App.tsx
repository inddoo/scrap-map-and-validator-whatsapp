import { useState } from 'react'

interface MapResult {
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

interface WAResult {
    phone: string
    clean_phone: string
    has_whatsapp: boolean
    is_business: boolean
    business_name: string
    status: string
}

interface WASummary {
    total: number
    has_whatsapp: number
    has_whatsapp_percent: number
    is_business: number
    is_business_percent: number
}

interface ModalProps {
    isOpen: boolean
    onClose: () => void
    title: string
    message: string
    type: 'success' | 'error' | 'info' | 'warning'
}

function Modal({ isOpen, onClose, title, message, type }: ModalProps) {
    if (!isOpen) return null

    const colors = {
        success: 'from-green-500 to-emerald-500',
        error: 'from-red-500 to-pink-500',
        info: 'from-blue-500 to-indigo-500',
        warning: 'from-yellow-500 to-orange-500'
    }

    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    }

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
            onClick={onClose}
        >
            <div
                className="bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 overflow-hidden transform transition-all duration-300 scale-100"
                onClick={(e) => e.stopPropagation()}
            >
                <div className={`bg-gradient-to-r ${colors[type]} p-6 text-white`}>
                    <div className="flex items-center gap-3">
                        <span className="text-4xl">{icons[type]}</span>
                        <h3 className="text-2xl font-bold">{title}</h3>
                    </div>
                </div>
                <div className="p-6">
                    <p className="text-gray-700 text-lg whitespace-pre-line leading-relaxed">{message}</p>
                </div>
                <div className="p-6 pt-0 flex justify-end">
                    <button
                        onClick={onClose}
                        className="px-8 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-xl hover:from-purple-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
                    >
                        OK
                    </button>
                </div>
            </div>
        </div>
    )
}

function App() {
    const [category, setCategory] = useState('')
    const [province, setProvince] = useState('')
    const [city, setCity] = useState('')
    const [results, setResults] = useState<MapResult[]>([])
    const [loading, setLoading] = useState(false)
    const [exporting, setExporting] = useState(false)
    const [canStop, setCanStop] = useState(false)
    const [progress, setProgress] = useState({ current: 0, total: 0, message: '', current_place: '' })

    // WA Validation state
    const [activeTab, setActiveTab] = useState<'scraper' | 'wa-validator'>('scraper')
    const [waInitialized, setWaInitialized] = useState(false)
    const [waInitializing, setWaInitializing] = useState(false)
    const [waValidating, setWaValidating] = useState(false)
    const [waResults, setWaResults] = useState<WAResult[]>([])
    const [waSummary, setWaSummary] = useState<WASummary | null>(null)
    const [phoneNumbers, setPhoneNumbers] = useState('')
    const [csvData, setCsvData] = useState<string[]>([])  // Store CSV phone numbers
    const [csvFileName, setCsvFileName] = useState('')
    const [csvPreview, setCsvPreview] = useState<{ headers: string[], rows: string[][] }>({ headers: [], rows: [] })  // Store full CSV preview

    // Modal state
    const [modal, setModal] = useState<{
        isOpen: boolean
        title: string
        message: string
        type: 'success' | 'error' | 'info' | 'warning'
    }>({
        isOpen: false,
        title: '',
        message: '',
        type: 'info'
    })

    const showModal = (title: string, message: string, type: 'success' | 'error' | 'info' | 'warning') => {
        setModal({ isOpen: true, title, message, type })
    }

    const closeModal = () => {
        setModal({ ...modal, isOpen: false })
    }

    const handleScrape = async () => {
        // Validasi kategori
        if (!category.trim()) {
            showModal('Kategori Kosong', 'Masukkan kategori!\n\nContoh: Cafe, Restoran, Hotel', 'warning')
            return
        }

        // Build location
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

        // Validasi location
        if (!location) {
            showModal('Lokasi Kosong', 'Masukkan minimal provinsi atau kota!\n\nContoh:\n• Provinsi: Jawa Timur\n• Kota: Malang', 'warning')
            return
        }

        // Build query
        const queries = [
            `${cat} ${location}`,
            `${cat} di ${location}`,
            `${cat} ${cty || prov}`,
        ]

        const query = queries[0]

        console.log('=== SCRAPING INFO ===')
        console.log('Kategori:', cat)
        console.log('Provinsi:', prov || '(kosong)')
        console.log('Kota:', cty || '(kosong)')
        console.log('Location:', location)
        console.log('Query final:', query)
        console.log('Query alternatif:', queries)
        console.log('====================')

        setLoading(true)
        setCanStop(true)
        setProgress({ current: 0, total: 0, message: 'Memulai...', current_place: '' })

        const progressInterval = setInterval(async () => {
            try {
                const res = await fetch('http://localhost:8000/progress')
                const data = await res.json()
                setProgress(data)
            } catch (err) {
                console.error('Error fetching progress:', err)
            }
        }, 1000)

        try {
            const response = await fetch('http://localhost:8000/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            })

            if (!response.ok) {
                const errorData = await response.json()
                console.error('Server error:', errorData)
                showModal('Error Server', errorData.detail || 'Terjadi kesalahan pada server', 'error')
                return
            }

            const data = await response.json()
            console.log('Scraping result:', data)
            setResults(data.data || [])

            if (data.count === 0) {
                showModal(
                    'Tidak Ada Hasil',
                    'Tidak ada hasil ditemukan!\n\nKemungkinan:\n• Query terlalu spesifik\n• Tidak ada tempat dengan kategori tersebut\n• Coba ubah kata kunci\n  (contoh: "Cafe" → "Kafe")',
                    'warning'
                )
            } else {
                showModal('Berhasil!', `Berhasil scrape ${data.count} tempat!`, 'success')
            }
        } catch (error) {
            console.error('Error:', error)
            showModal('Gagal Scraping', 'Gagal scraping data.\n\nPastikan backend berjalan di:\nhttp://localhost:8000', 'error')
        } finally {
            clearInterval(progressInterval)
            setLoading(false)
            setCanStop(false)
        }
    }

    const handleStopScraping = async () => {
        try {
            await fetch('http://localhost:8000/stop-scraping', {
                method: 'POST'
            })
            showModal('Dihentikan', 'Scraping berhasil dihentikan!', 'info')
        } catch (error) {
            console.error('Error stopping:', error)
        }
    }

    const handleExportCSV = async () => {
        console.log('=== EXPORT CSV ===')
        console.log('Results count:', results.length)

        if (results.length === 0) {
            showModal('Tidak Ada Data', 'Tidak ada data untuk di-export!\n\nSilakan scrape data terlebih dahulu.', 'warning')
            return
        }

        setExporting(true)
        try {
            // Create CSV content directly from results
            const headers = ['name', 'phone', 'website', 'rating', 'reviews_count', 'category', 'address', 'plus_code', 'hours', 'price_level', 'price_range', 'latitude', 'longitude', 'link']
            const csvRows = []

            // Add header row
            csvRows.push(headers.join(','))

            // Add data rows
            for (const row of results) {
                const values = headers.map(header => {
                    const value = row[header as keyof MapResult] || ''
                    // Escape quotes and wrap in quotes if contains comma
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

            const locationStr = city || province || 'data'
            const filename = `google_maps_${category}_${locationStr.replace(/\s+/g, '_')}.csv`
            a.download = filename

            document.body.appendChild(a)
            a.click()

            // Cleanup
            setTimeout(() => {
                window.URL.revokeObjectURL(url)
                document.body.removeChild(a)
            }, 100)

            console.log('Download triggered!')
            showModal('Berhasil Export!', `Berhasil export ${results.length} data ke CSV!\n\nFile: ${filename}`, 'success')
        } catch (error) {
            console.error('Export error:', error)
            showModal('Gagal Export', `Terjadi kesalahan:\n${error}`, 'error')
        } finally {
            setExporting(false)
            console.log('=== EXPORT COMPLETE ===')
        }
    }

    const handleReset = () => {
        setCategory('')
        setProvince('')
        setCity('')
        setResults([])
        setProgress({ current: 0, total: 0, message: '', current_place: '' })
    }

    // WhatsApp Validation Functions

    const handleInitWA = async () => {
        setWaInitializing(true)
        try {
            const response = await fetch('http://localhost:8000/wa/init', {
                method: 'POST'
            })

            if (!response.ok) {
                const errorData = await response.json()
                const errorMsg = errorData.detail || 'Gagal inisialisasi WhatsApp checker'

                // Show detailed error
                showModal(
                    'Error Inisialisasi',
                    errorMsg + '\n\n💡 Tips:\n• Tutup semua Chrome yang sedang berjalan\n• Restart backend (python run.py)\n• Pastikan Chrome terinstall\n• Coba lagi',
                    'error'
                )
                return
            }

            const data = await response.json()
            setWaInitialized(true)
            showModal('Berhasil!', data.message || 'WhatsApp checker berhasil diinisialisasi!\n\nAnda sudah login ke WhatsApp Web.', 'success')
        } catch (error) {
            console.error('Error initializing WA:', error)
            showModal(
                'Error Koneksi',
                'Gagal terhubung ke backend.\n\n💡 Pastikan:\n• Backend berjalan (python run.py)\n• Port 8000 tidak dipakai aplikasi lain\n• Tidak ada firewall yang memblokir',
                'error'
            )
        } finally {
            setWaInitializing(false)
        }
    }

    const handleUploadCSV = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (!file) return

        try {
            const text = await file.text()
            const lines = text.split('\n').filter(line => line.trim())

            if (lines.length === 0) {
                showModal('CSV Kosong', 'File CSV tidak berisi data!', 'warning')
                return
            }

            // Parse CSV header
            const headers = lines[0].split(',').map(h => h.trim())
            const headersLower = headers.map(h => h.toLowerCase())
            const phoneIndex = headersLower.findIndex(h => h === 'phone' || h === 'nomor' || h === 'telepon')

            if (phoneIndex === -1) {
                showModal('Format CSV Salah', 'CSV harus memiliki kolom "phone"!', 'error')
                return
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
                showModal('Tidak Ada Nomor', 'Tidak ada nomor telepon valid di CSV!', 'warning')
                return
            }

            setCsvData(phones)
            setCsvFileName(file.name)
            setCsvPreview({ headers, rows })
            showModal('CSV Berhasil Dimuat!', `Berhasil memuat ${phones.length} nomor dari ${file.name}\n\nSilakan klik "Validasi CSV" untuk memulai validasi.`, 'success')
        } catch (error) {
            console.error('Error reading CSV:', error)
            showModal('Error', 'Gagal membaca file CSV!', 'error')
        } finally {
            // Reset file input
            event.target.value = ''
        }
    }

    const handleValidateCSV = async () => {
        if (!waInitialized) {
            showModal('WhatsApp Belum Siap', 'Silakan inisialisasi WhatsApp checker terlebih dahulu!', 'warning')
            return
        }

        if (csvData.length === 0) {
            showModal('Tidak Ada Data CSV', 'Silakan upload file CSV terlebih dahulu!', 'warning')
            return
        }

        setWaValidating(true)
        try {
            const response = await fetch('http://localhost:8000/wa/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone_numbers: csvData })
            })

            if (!response.ok) {
                const errorData = await response.json()
                showModal('Error', errorData.detail || 'Gagal validasi nomor', 'error')
                return
            }

            const data = await response.json()
            setWaResults(data.results)
            setWaSummary(data.summary)

            showModal(
                'Validasi Selesai!',
                `Berhasil validasi ${data.summary.total} nomor dari CSV!\n\n` +
                `✅ Punya WhatsApp: ${data.summary.has_whatsapp} (${data.summary.has_whatsapp_percent}%)\n` +
                `💼 WhatsApp Business: ${data.summary.is_business} (${data.summary.is_business_percent}%)`,
                'success'
            )

            // Clear CSV data after validation
            setCsvData([])
            setCsvFileName('')

            // Auto scroll to results table after modal closes
            setTimeout(() => {
                const resultsSection = document.getElementById('wa-results-section')
                if (resultsSection) {
                    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
                }
            }, 500)
        } catch (error) {
            console.error('Error validating CSV:', error)
            showModal('Error', 'Gagal validasi nomor dari CSV.', 'error')
        } finally {
            setWaValidating(false)
        }
    }

    const handleClearCSV = () => {
        setCsvData([])
        setCsvFileName('')
        setCsvPreview({ headers: [], rows: [] })
    }

    const handleDeleteCSVColumn = (columnIndex: number) => {
        // Remove column from headers
        const newHeaders = csvPreview.headers.filter((_, i) => i !== columnIndex)

        // Remove column from all rows
        const newRows = csvPreview.rows.map(row =>
            row.filter((_, i) => i !== columnIndex)
        )

        setCsvPreview({ headers: newHeaders, rows: newRows })

        // If the deleted column was the phone column, we need to update csvData
        const headersLower = csvPreview.headers.map(h => h.toLowerCase())
        const phoneIndex = headersLower.findIndex(h => h === 'phone' || h === 'nomor' || h === 'telepon')

        if (columnIndex === phoneIndex) {
            // Phone column was deleted, clear csvData
            setCsvData([])
            showModal('Kolom Phone Dihapus', 'Kolom phone telah dihapus. Data validasi direset.', 'warning')
        }
    }

    const handleValidateNumbers = async () => {
        if (!waInitialized) {
            showModal('WhatsApp Belum Siap', 'Silakan inisialisasi WhatsApp checker terlebih dahulu!', 'warning')
            return
        }

        if (!phoneNumbers.trim()) {
            showModal('Nomor Kosong', 'Masukkan nomor telepon terlebih dahulu!', 'warning')
            return
        }

        // Parse phone numbers (one per line)
        const numbers = phoneNumbers
            .split('\n')
            .map(n => n.trim())
            .filter(n => n.length > 0)

        if (numbers.length === 0) {
            showModal('Nomor Kosong', 'Tidak ada nomor valid untuk divalidasi!', 'warning')
            return
        }

        setWaValidating(true)
        try {
            const response = await fetch('http://localhost:8000/wa/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone_numbers: numbers })
            })

            if (!response.ok) {
                const errorData = await response.json()
                showModal('Error', errorData.detail || 'Gagal validasi nomor', 'error')
                return
            }

            const data = await response.json()
            setWaResults(data.results)
            setWaSummary(data.summary)

            showModal(
                'Validasi Selesai!',
                `Berhasil validasi ${data.summary.total} nomor!\n\n` +
                `✅ Punya WhatsApp: ${data.summary.has_whatsapp} (${data.summary.has_whatsapp_percent}%)\n` +
                `💼 WhatsApp Business: ${data.summary.is_business} (${data.summary.is_business_percent}%)`,
                'success'
            )
        } catch (error) {
            console.error('Error validating numbers:', error)
            showModal('Error', 'Gagal validasi nomor.\n\nPastikan backend berjalan.', 'error')
        } finally {
            setWaValidating(false)
        }
    }

    const handleExportWAResults = async () => {
        if (waResults.length === 0) {
            showModal('Tidak Ada Data', 'Tidak ada hasil validasi untuk di-export!', 'warning')
            return
        }

        try {
            const response = await fetch('http://localhost:8000/wa/export')

            if (!response.ok) {
                const errorData = await response.json()
                showModal('Error', errorData.detail || 'Gagal export hasil', 'error')
                return
            }

            const blob = await response.blob()
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = 'wa_validation_results.csv'
            document.body.appendChild(a)
            a.click()

            setTimeout(() => {
                window.URL.revokeObjectURL(url)
                document.body.removeChild(a)
            }, 100)

            showModal('Berhasil!', `Berhasil export ${waResults.length} hasil validasi!`, 'success')
        } catch (error) {
            console.error('Error exporting WA results:', error)
            showModal('Error', 'Gagal export hasil validasi.', 'error')
        }
    }

    const handleCloseWA = async () => {
        try {
            await fetch('http://localhost:8000/wa/close', {
                method: 'POST'
            })
            setWaInitialized(false)
            setWaResults([])
            setWaSummary(null)
            showModal('Ditutup', 'WhatsApp checker berhasil ditutup.', 'info')
        } catch (error) {
            console.error('Error closing WA:', error)
        }
    }

    return (
        <>
            <Modal {...modal} onClose={closeModal} />

            <div className="min-h-screen w-full bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 py-8 px-4">
                <div className="w-full max-w-7xl mx-auto">
                    {/* Header */}
                    <div className="text-center mb-8">
                        <h1 className="text-5xl font-bold text-white mb-2 drop-shadow-lg">
                            🗺️ Google Maps Scraper
                        </h1>
                        <p className="text-purple-200 text-lg">Scrape data tempat dari Google Maps & validasi WhatsApp Business</p>
                    </div>

                    {/* Tabs */}
                    <div className="flex gap-4 mb-6 justify-center">
                        <button
                            onClick={() => setActiveTab('scraper')}
                            className={`px-8 py-4 font-bold rounded-xl transition-all duration-200 ${activeTab === 'scraper'
                                ? 'bg-white text-purple-700 shadow-xl scale-105'
                                : 'bg-white/20 text-white hover:bg-white/30'
                                }`}
                        >
                            🗺️ Maps Scraper
                        </button>
                        <button
                            onClick={() => setActiveTab('wa-validator')}
                            className={`px-8 py-4 font-bold rounded-xl transition-all duration-200 ${activeTab === 'wa-validator'
                                ? 'bg-white text-purple-700 shadow-xl scale-105'
                                : 'bg-white/20 text-white hover:bg-white/30'
                                }`}
                        >
                            💼 WA Business Validator
                        </button>
                    </div>

                    {/* Maps Scraper Tab */}
                    {activeTab === 'scraper' && (
                        <div className="animate-fade-in">
                            {/* Search Form */}
                            <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-6 mb-6">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                                    <div>
                                        <label className="block text-sm font-semibold text-purple-700 mb-2">
                                            🏪 Kategori
                                        </label>
                                        <input
                                            type="text"
                                            value={category}
                                            onChange={(e) => setCategory(e.target.value)}
                                            placeholder="Contoh: Restoran, Cafe, Hotel"
                                            className="w-full px-4 py-3 bg-white border-2 border-purple-300 rounded-xl focus:border-purple-600 focus:ring-4 focus:ring-purple-200 outline-none transition-all duration-200 text-gray-800 font-medium placeholder-gray-400"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-semibold text-purple-700 mb-2">
                                            🌏 Provinsi
                                        </label>
                                        <input
                                            type="text"
                                            value={province}
                                            onChange={(e) => setProvince(e.target.value)}
                                            placeholder="Contoh: Jawa Tengah, DKI Jakarta"
                                            className="w-full px-4 py-3 bg-white border-2 border-purple-300 rounded-xl focus:border-purple-600 focus:ring-4 focus:ring-purple-200 outline-none transition-all duration-200 text-gray-800 font-medium placeholder-gray-400"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-semibold text-purple-700 mb-2">
                                            🏙️ Kabupaten/Kota
                                        </label>
                                        <input
                                            type="text"
                                            value={city}
                                            onChange={(e) => setCity(e.target.value)}
                                            placeholder="Contoh: Semarang"
                                            onKeyPress={(e) => e.key === 'Enter' && handleScrape()}
                                            className="w-full px-4 py-3 bg-white border-2 border-purple-300 rounded-xl focus:border-purple-600 focus:ring-4 focus:ring-purple-200 outline-none transition-all duration-200 text-gray-800 font-medium placeholder-gray-400"
                                        />
                                    </div>
                                </div>

                                <div className="flex flex-wrap gap-3 justify-center">
                                    <button
                                        onClick={handleScrape}
                                        disabled={loading}
                                        className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-xl hover:from-purple-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                                    >
                                        {loading ? '⏳ Scraping...' : '🚀 Scrape Semua'}
                                    </button>

                                    {canStop && (
                                        <button
                                            onClick={handleStopScraping}
                                            className="px-6 py-3 bg-gradient-to-r from-red-500 to-pink-500 text-white font-bold rounded-xl hover:from-red-600 hover:to-pink-600 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                                        >
                                            ⛔ Stop
                                        </button>
                                    )}

                                    <button
                                        onClick={handleExportCSV}
                                        disabled={exporting || results.length === 0}
                                        className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold rounded-xl hover:from-green-600 hover:to-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                                    >
                                        {exporting ? '📤 Exporting...' : '📥 Download CSV'}
                                    </button>

                                    <button
                                        onClick={handleReset}
                                        disabled={loading}
                                        className="px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white font-bold rounded-xl hover:from-gray-600 hover:to-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                                    >
                                        🔄 Reset
                                    </button>
                                </div>
                            </div>

                            {/* Progress Section */}
                            {loading && (
                                <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-6 mb-6 animate-fade-in">
                                    <div className="flex items-center justify-center gap-3 mb-4">
                                        <span className="text-4xl animate-spin">⏳</span>
                                        <h2 className="text-2xl font-bold text-purple-700">
                                            {progress.message || 'Memulai scraping...'}
                                        </h2>
                                    </div>

                                    {progress.total > 0 && (
                                        <>
                                            {/* Progress Bar */}
                                            <div className="relative bg-purple-100 rounded-full h-8 overflow-hidden mb-6">
                                                <div
                                                    className="absolute top-0 left-0 h-full bg-gradient-to-r from-purple-600 to-indigo-600 transition-all duration-500 ease-out flex items-center justify-end pr-4"
                                                    style={{ width: `${(progress.current / progress.total) * 100}%` }}
                                                >
                                                    <span className="text-white font-bold text-sm">
                                                        {Math.round((progress.current / progress.total) * 100)}%
                                                    </span>
                                                </div>
                                            </div>

                                            {/* Stats Cards */}
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                                                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4 border-2 border-purple-200">
                                                    <div className="text-purple-600 text-sm font-semibold mb-1">PROGRESS</div>
                                                    <div className="text-3xl font-bold text-purple-700">
                                                        {progress.current} / {progress.total}
                                                    </div>
                                                </div>
                                                <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-xl p-4 border-2 border-indigo-200">
                                                    <div className="text-indigo-600 text-sm font-semibold mb-1">PERSENTASE</div>
                                                    <div className="text-3xl font-bold text-indigo-700">
                                                        {Math.round((progress.current / progress.total) * 100)}%
                                                    </div>
                                                </div>
                                                <div className="bg-gradient-to-br from-pink-50 to-pink-100 rounded-xl p-4 border-2 border-pink-200">
                                                    <div className="text-pink-600 text-sm font-semibold mb-1">TERSISA</div>
                                                    <div className="text-3xl font-bold text-pink-700">
                                                        {progress.total - progress.current}
                                                    </div>
                                                </div>
                                            </div>

                                            {/* Current Place */}
                                            {progress.current_place && (
                                                <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 rounded-lg p-4 animate-pulse">
                                                    <p className="text-green-700 font-semibold">
                                                        📍 Sedang scraping: <span className="font-bold">{progress.current_place}</span>
                                                    </p>
                                                </div>
                                            )}
                                        </>
                                    )}

                                    <p className="text-center text-gray-500 text-sm mt-4">
                                        ⚠️ Jangan tutup browser atau refresh halaman
                                    </p>
                                </div>
                            )}

                            {/* Success Message */}
                            {results.length > 0 && !loading && (
                                <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-2xl shadow-2xl p-6 mb-6 animate-fade-in">
                                    <p className="text-center text-2xl font-bold">
                                        ✅ Berhasil scrape {results.length} tempat!
                                    </p>
                                </div>
                            )}

                            {/* Results Grid */}
                            {results.length > 0 && (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {results.map((item, index) => (
                                        <div
                                            key={index}
                                            className="bg-white rounded-2xl shadow-xl p-6 hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 border-2 border-purple-100 hover:border-purple-300"
                                        >
                                            <h3 className="text-xl font-bold text-purple-700 mb-3 line-clamp-2">
                                                {item.name}
                                            </h3>
                                            <div className="space-y-2 text-gray-600">
                                                <p className="flex items-center gap-2">
                                                    <span className="text-yellow-500">⭐</span>
                                                    <span className="font-medium">{item.rating}</span>
                                                    {item.reviews_count && item.reviews_count !== '0' && (
                                                        <span className="text-xs text-gray-500">({item.reviews_count} ulasan)</span>
                                                    )}
                                                </p>
                                                {item.category && item.category !== 'Tidak tersedia' && (
                                                    <p className="flex items-center gap-2">
                                                        <span>🏷️</span>
                                                        <span className="text-sm font-medium text-purple-600">{item.category}</span>
                                                    </p>
                                                )}
                                                <p className="flex items-center gap-2">
                                                    <span>📞</span>
                                                    <span className="text-sm">{item.phone}</span>
                                                </p>
                                                <p className="flex items-center gap-2">
                                                    <span>🌐</span>
                                                    <span className="text-sm truncate">{item.website}</span>
                                                </p>
                                                {item.hours && item.hours !== 'Tidak tersedia' && (
                                                    <p className="flex items-center gap-2">
                                                        <span>🕐</span>
                                                        <span className="text-sm">{item.hours}</span>
                                                    </p>
                                                )}
                                                {item.price_level && item.price_level !== 'Tidak tersedia' && (
                                                    <p className="flex items-center gap-2">
                                                        <span>💰</span>
                                                        <span className="text-sm font-medium">{item.price_level}</span>
                                                    </p>
                                                )}
                                                {item.price_range && item.price_range !== 'Tidak tersedia' && (
                                                    <p className="flex items-center gap-2">
                                                        <span>💵</span>
                                                        <span className="text-sm text-green-600 font-medium">{item.price_range}</span>
                                                    </p>
                                                )}
                                                <p className="flex items-start gap-2">
                                                    <span className="mt-1">📍</span>
                                                    <span className="text-sm line-clamp-2">{item.address}</span>
                                                </p>
                                                {item.latitude && item.longitude && item.latitude !== 'Tidak tersedia' && (
                                                    <p className="flex items-center gap-2">
                                                        <span>🗺️</span>
                                                        <span className="text-xs text-gray-500">{item.latitude}, {item.longitude}</span>
                                                    </p>
                                                )}
                                            </div>
                                            <a
                                                href={item.link}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="mt-4 block text-center px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200"
                                            >
                                                Lihat di Maps →
                                            </a>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {/* WA Validator Tab */}
                    {activeTab === 'wa-validator' && (
                        <div className="animate-fade-in">
                            {/* WA Validator Panel */}
                            <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-8 mb-6">
                                <div className="text-center mb-6">
                                    <h2 className="text-3xl font-bold text-purple-700 mb-2">💼 WhatsApp Validator</h2>
                                    <p className="text-gray-600">
                                        Validasi nomor WhatsApp & deteksi Business account
                                    </p>
                                </div>

                                {!waInitialized ? (
                                    <div className="max-w-2xl mx-auto">
                                        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6 mb-6">
                                            <div className="flex items-start gap-4">
                                                <span className="text-4xl">ℹ️</span>
                                                <div>
                                                    <h3 className="font-bold text-blue-900 mb-2">Cara Kerja:</h3>
                                                    <ul className="text-blue-800 text-sm space-y-1">
                                                        <li>✅ Scan QR code SEKALI saja di awal</li>
                                                        <li>✅ Session tersimpan - tidak perlu scan lagi</li>
                                                        <li>✅ Validasi ratusan nomor tanpa scan ulang</li>
                                                        <li>✅ Deteksi WhatsApp Personal vs Business</li>
                                                        <li>✅ Dapatkan nama bisnis (jika ada)</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="text-center">
                                            <button
                                                onClick={handleInitWA}
                                                disabled={waInitializing}
                                                className="px-12 py-4 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-lg font-bold rounded-xl hover:from-green-600 hover:to-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-xl"
                                            >
                                                {waInitializing ? '⏳ Membuka WhatsApp Web...' : '🚀 Mulai - Scan QR Code'}
                                            </button>
                                            <p className="text-gray-500 text-sm mt-4">
                                                Chrome akan terbuka otomatis dengan WhatsApp Web
                                            </p>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="max-w-4xl mx-auto">
                                        {/* Status Badge */}
                                        <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300 rounded-xl p-4 mb-6 text-center">
                                            <p className="text-green-700 font-bold text-lg">
                                                ✅ WhatsApp Siap! Session tersimpan - tidak perlu scan QR lagi
                                            </p>
                                        </div>

                                        {/* Input Form */}
                                        <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl p-6 mb-6 border-2 border-purple-200">
                                            <h3 className="text-xl font-bold text-purple-700 mb-4 text-center">
                                                📝 Input Nomor Telepon
                                            </h3>

                                            <div className="bg-white rounded-lg p-4 mb-4 border border-purple-200">
                                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                                    Format: Angka setelah +62 (satu nomor per baris)
                                                </label>
                                                <textarea
                                                    value={phoneNumbers}
                                                    onChange={(e) => setPhoneNumbers(e.target.value)}
                                                    placeholder="Contoh:&#10;81234567890&#10;85999888777&#10;274123456"
                                                    rows={8}
                                                    className="w-full px-4 py-3 bg-gray-50 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 outline-none transition-all duration-200 text-gray-800 font-mono text-sm resize-none"
                                                />
                                                <div className="mt-2 text-xs text-gray-500">
                                                    💡 Tips: Input angka setelah +62 saja. Contoh: 81234567890 (bukan 081234567890)
                                                </div>
                                            </div>

                                            <div className="flex gap-3">
                                                <button
                                                    onClick={handleValidateNumbers}
                                                    disabled={waValidating || !phoneNumbers.trim()}
                                                    className="flex-1 px-6 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white text-lg font-bold rounded-xl hover:from-purple-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg"
                                                >
                                                    {waValidating ? '⏳ Memvalidasi...' : '🚀 Validasi Sekarang'}
                                                </button>

                                                <label className="px-6 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-lg font-bold rounded-xl hover:from-blue-700 hover:to-cyan-700 transform hover:scale-105 transition-all duration-200 shadow-lg cursor-pointer text-center flex items-center justify-center">
                                                    📤 Upload CSV
                                                    <input
                                                        type="file"
                                                        accept=".csv"
                                                        onChange={handleUploadCSV}
                                                        disabled={waValidating}
                                                        className="hidden"
                                                    />
                                                </label>
                                            </div>

                                            <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-3">
                                                <p className="text-xs text-blue-700 font-semibold mb-1">📄 Format CSV:</p>
                                                <code className="text-xs text-blue-900 block">
                                                    name,phone,address<br />
                                                    Toko A,81234567890,Jl. Sudirman<br />
                                                    Cafe B,85999888777,Jl. Merdeka
                                                </code>
                                            </div>
                                        </div>

                                        {/* CSV Preview */}
                                        {csvData.length > 0 && (
                                            <div className="bg-white rounded-2xl shadow-2xl p-6 mb-6 border-2 border-purple-200">
                                                {/* Header Section */}
                                                <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-purple-100">
                                                    <div className="flex items-center gap-4">
                                                        <div className="bg-gradient-to-br from-purple-500 to-indigo-500 text-white rounded-xl p-3 shadow-lg">
                                                            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                            </svg>
                                                        </div>
                                                        <div>
                                                            <h3 className="text-2xl font-bold text-purple-700 mb-1">
                                                                📄 {csvFileName}
                                                            </h3>
                                                            <div className="flex items-center gap-4 text-sm">
                                                                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full font-semibold">
                                                                    📊 {csvData.length} baris
                                                                </span>
                                                                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full font-semibold">
                                                                    📋 {csvPreview.headers.length} kolom
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <button
                                                        onClick={handleClearCSV}
                                                        className="px-6 py-3 bg-gradient-to-r from-red-500 to-pink-500 text-white font-bold rounded-xl hover:from-red-600 hover:to-pink-600 transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center gap-2"
                                                    >
                                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                                        </svg>
                                                        Hapus Semua
                                                    </button>
                                                </div>

                                                {/* Table Container */}
                                                <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-2 mb-6 shadow-inner">
                                                    <div className="bg-white rounded-lg overflow-hidden shadow-lg" style={{ height: '60vh' }}>
                                                        <div className="overflow-auto h-full">
                                                            <table className="w-full border-collapse">
                                                                <thead>
                                                                    <tr className="sticky top-0 z-10">
                                                                        <th className="px-4 py-4 text-center text-white font-bold bg-gradient-to-r from-purple-600 to-indigo-600 border-r border-purple-400 w-20 shadow-md">
                                                                            #
                                                                        </th>
                                                                        {csvPreview.headers.map((header, index) => (
                                                                            <th key={index} className="px-6 py-4 text-left text-white font-bold bg-gradient-to-r from-purple-600 to-indigo-600 border-r border-purple-400 shadow-md">
                                                                                <div className="flex items-center justify-between gap-3">
                                                                                    <div className="flex items-center gap-2">
                                                                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                                                                        </svg>
                                                                                        {header}
                                                                                    </div>
                                                                                    <button
                                                                                        onClick={() => handleDeleteCSVColumn(index)}
                                                                                        className="px-2 py-1 bg-red-500 hover:bg-red-600 rounded-lg transition-colors flex items-center gap-1 text-xs"
                                                                                        title={`Hapus kolom ${header}`}
                                                                                    >
                                                                                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                                                                        </svg>
                                                                                        Hapus
                                                                                    </button>
                                                                                </div>
                                                                            </th>
                                                                        ))}
                                                                    </tr>
                                                                </thead>
                                                                <tbody>
                                                                    {csvPreview.rows.map((row, rowIndex) => (
                                                                        <tr key={rowIndex} className="hover:bg-purple-50 transition-colors border-b border-gray-200">
                                                                            <td className="px-4 py-3 text-center font-bold text-purple-600 bg-purple-50 border-r border-gray-200">
                                                                                {rowIndex + 1}
                                                                            </td>
                                                                            {row.map((cell, cellIndex) => (
                                                                                <td key={cellIndex} className="px-6 py-3 text-gray-700 border-r border-gray-200">
                                                                                    <div className="max-w-xs truncate" title={cell}>
                                                                                        {cell || <span className="text-gray-400 italic">kosong</span>}
                                                                                    </div>
                                                                                </td>
                                                                            ))}
                                                                        </tr>
                                                                    ))}
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* Action Button */}
                                                <button
                                                    onClick={handleValidateCSV}
                                                    disabled={waValidating}
                                                    className="w-full px-8 py-5 bg-gradient-to-r from-green-600 to-emerald-600 text-white text-xl font-bold rounded-xl hover:from-green-700 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-2xl flex items-center justify-center gap-3"
                                                >
                                                    {waValidating ? (
                                                        <>
                                                            <svg className="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                                                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                            </svg>
                                                            Memvalidasi {csvData.length} Nomor...
                                                        </>
                                                    ) : (
                                                        <>
                                                            <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                            </svg>
                                                            Validasi {csvData.length} Nomor Sekarang
                                                        </>
                                                    )}
                                                </button>
                                            </div>
                                        )}

                                        {/* Action Buttons */}
                                        <div className="flex gap-4 justify-center">
                                            <button
                                                onClick={handleExportWAResults}
                                                disabled={waResults.length === 0}
                                                className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold rounded-xl hover:from-green-600 hover:to-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg"
                                            >
                                                📥 Download Hasil CSV
                                            </button>

                                            <button
                                                onClick={handleCloseWA}
                                                className="px-8 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white font-bold rounded-xl hover:from-gray-600 hover:to-gray-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
                                            >
                                                ❌ Tutup WhatsApp
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Summary */}
                            {waSummary && (
                                <div id="wa-results-section" className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-6 mb-6">
                                    <h3 className="text-2xl font-bold text-purple-700 mb-4 text-center">📊 Ringkasan Hasil</h3>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
                                        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border-2 border-blue-200 text-center">
                                            <div className="text-blue-600 text-sm font-semibold mb-2">TOTAL NOMOR</div>
                                            <div className="text-4xl font-bold text-blue-700">{waSummary.total}</div>
                                        </div>
                                        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border-2 border-green-200 text-center">
                                            <div className="text-green-600 text-sm font-semibold mb-2">PUNYA WHATSAPP</div>
                                            <div className="text-4xl font-bold text-green-700">
                                                {waSummary.has_whatsapp}
                                            </div>
                                            <div className="text-sm text-green-600 mt-1">
                                                {waSummary.has_whatsapp_percent}%
                                            </div>
                                        </div>
                                        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border-2 border-purple-200 text-center">
                                            <div className="text-purple-600 text-sm font-semibold mb-2">WA BUSINESS</div>
                                            <div className="text-4xl font-bold text-purple-700">
                                                {waSummary.is_business}
                                            </div>
                                            <div className="text-sm text-purple-600 mt-1">
                                                {waSummary.is_business_percent}%
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Results Table */}
                            {waResults.length > 0 && (
                                <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-6 overflow-x-auto">
                                    <h3 className="text-2xl font-bold text-purple-700 mb-4 text-center">📋 Detail Hasil Validasi</h3>
                                    <div className="overflow-x-auto">
                                        <table className="w-full min-w-[600px]">
                                            <thead>
                                                <tr className="bg-gradient-to-r from-purple-100 to-indigo-100 text-purple-700">
                                                    <th className="px-4 py-3 text-center font-bold rounded-tl-lg">No</th>
                                                    <th className="px-4 py-3 text-left font-bold">Nomor Input</th>
                                                    <th className="px-4 py-3 text-center font-bold">WhatsApp</th>
                                                    <th className="px-4 py-3 text-center font-bold">Tipe</th>
                                                    <th className="px-4 py-3 text-left font-bold">Nama Bisnis</th>
                                                    <th className="px-4 py-3 text-left font-bold rounded-tr-lg">Status</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {waResults.map((result, index) => (
                                                    <tr key={index} className="border-b border-gray-200 hover:bg-purple-50 transition-colors">
                                                        <td className="px-4 py-3 text-center font-semibold text-gray-600">{index + 1}</td>
                                                        <td className="px-4 py-3 font-mono text-sm text-gray-800">{result.phone}</td>
                                                        <td className="px-4 py-3 text-center">
                                                            {result.has_whatsapp ? (
                                                                <span className="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-bold">
                                                                    ✅ Ya
                                                                </span>
                                                            ) : (
                                                                <span className="inline-block px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-bold">
                                                                    ❌ Tidak
                                                                </span>
                                                            )}
                                                        </td>
                                                        <td className="px-4 py-3 text-center">
                                                            {result.is_business ? (
                                                                <span className="inline-block px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-bold">
                                                                    💼 Business
                                                                </span>
                                                            ) : result.has_whatsapp ? (
                                                                <span className="inline-block px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-bold">
                                                                    👤 Personal
                                                                </span>
                                                            ) : (
                                                                <span className="text-gray-400">-</span>
                                                            )}
                                                        </td>
                                                        <td className="px-4 py-3 text-gray-700 font-medium">
                                                            {result.business_name || '-'}
                                                        </td>
                                                        <td className="px-4 py-3 text-sm text-gray-600">
                                                            {result.status}
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div >
        </>
    )
}

export default App
