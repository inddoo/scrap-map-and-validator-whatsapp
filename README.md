# 🗺️ Google Maps Scraper & WhatsApp Business Validator

> Automated tool for extracting business data from Google Maps and validating WhatsApp Business accounts

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

### 📍 Google Maps Scraper
- **Automated Data Extraction** - Scrape business information from Google Maps
- **Comprehensive Data** - Name, phone, website, rating, reviews, address, coordinates, and more
- **Real-time Progress** - Live progress tracking with current place indicator
- **Flexible Search** - Search by category, province, and city
- **CSV Export** - Export results to CSV with UTF-8 BOM for Excel compatibility
- **Stop Anytime** - Pause scraping process at any moment

### 💼 WhatsApp Business Validator
- **Number Validation** - Check if phone numbers are registered on WhatsApp
- **Business Detection** - Automatically detect WhatsApp Business vs Personal accounts
- **Business Name Extraction** - Get business names from WhatsApp Business profiles
- **Session Persistence** - Scan QR code once, session saved for future use
- **Bulk Validation** - Upload CSV files for mass validation
- **CSV Preview & Edit** - Preview uploaded CSV and remove unnecessary columns
- **Export Results** - Download validation results as CSV

### 📨 WhatsApp Auto Sender (NEW!)
- **Single Message** - Send message to one number
- **Bulk Messages** - Send same message to multiple numbers
- **Personalized Messages** - Send customized messages using templates
- **Anti-Spam Delay** - Random delay between messages to avoid detection
- **Delivery Status** - Track which messages were sent successfully
- **Smart Retry** - Option to stop or continue on errors

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Chrome/Chromium browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/google-maps-scraper-wa-validator.git
cd google-maps-scraper-wa-validator
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

3. **Install frontend dependencies**
```bash
cd ..
npm install
```

### Running the Application

1. **Start the backend**
```bash
cd backend
python run.py
```
Backend runs at `http://localhost:8000`

2. **Start the frontend**
```bash
npm run dev
```
Frontend runs at `http://localhost:5173`

3. **Build for production**
```bash
npm run build
```

## 📖 Usage

### Google Maps Scraper

1. Navigate to the "Maps Scraper" tab
2. Enter search criteria:
   - **Category**: e.g., "Restaurant", "Cafe", "Hotel"
   - **Province**: e.g., "Central Java"
   - **City**: e.g., "Semarang"
3. Click "Scrape All"
4. Monitor progress in real-time
5. Download results as CSV

### WhatsApp Validator

#### First Time Setup
1. Navigate to "WA Business Validator" tab
2. Click "Start - Scan QR Code"
3. Scan QR code with your WhatsApp mobile app
4. Session is saved - no need to scan again!

#### Manual Validation
1. Enter phone numbers (one per line)
   - Format: digits after +62
   - Example: `81234567890` (not `081234567890`)
2. Click "Validate Now"
3. View results in the table below

#### CSV Validation
1. Click "Upload CSV"
2. Select CSV file (must have "phone" column)
3. Preview appears - review all data
4. Remove unnecessary columns (click "Delete" in header)
5. Click "Validate CSV Now"
6. Download results

## 📊 Data Format

### Input CSV for WhatsApp Validator
```csv
name,phone,address
Store A,81234567890,Jl. Sudirman No. 1
Cafe B,85999888777,Jl. Merdeka No. 2
```

**Note:** Phone format is digits after +62 (without leading 0)

### Output CSV from Maps Scraper
Contains: `name`, `phone`, `website`, `rating`, `reviews_count`, `category`, `address`, `plus_code`, `hours`, `price_level`, `price_range`, `latitude`, `longitude`, `link`

### Output CSV from WA Validator
Contains: `phone`, `clean_phone`, `has_whatsapp`, `is_business`, `business_name`, `status`

## 🏗️ Project Structure

```
.
├── backend/                    # Backend Python
│   ├── api/                   # API routes & schemas
│   ├── config/                # Configuration
│   ├── core/                  # Core functionality
│   ├── scrapers/              # Maps scraper modules
│   ├── wa_validator/          # WhatsApp validator
│   ├── main.py               # FastAPI app
│   └── run.py                # Run script
│
├── src/                       # Frontend React
│   ├── components/           # React components
│   ├── config/              # Configuration
│   ├── services/            # API services
│   ├── types/               # TypeScript types
│   ├── utils/               # Utility functions
│   └── App.tsx             # Main app
│
└── README.md               # This file
```

## 🔧 Configuration

### Backend Configuration
```python
# backend/config/settings.py
API_HOST = "0.0.0.0"
API_PORT = 8000
```

### Frontend Configuration
```typescript
// src/config/constants.ts
export const API_BASE_URL = 'http://localhost:8000'
```

## 📡 API Endpoints

### Maps Scraper
- `POST /scrape` - Start scraping
- `GET /progress` - Get scraping progress
- `POST /stop-scraping` - Stop scraping
- `POST /export-csv` - Export to CSV

### WhatsApp Validator
- `POST /wa/init` - Initialize WhatsApp Web (scan QR)
- `POST /wa/validate` - Validate phone numbers
- `POST /wa/validate-csv` - Validate from CSV file
- `GET /wa/export` - Export results to CSV
- `POST /wa/close` - Close WhatsApp session

### WhatsApp Auto Sender
- `POST /wa/send` - Send single message
- `POST /wa/send-bulk` - Send bulk messages (same message to all)
- `POST /wa/send-personalized` - Send personalized messages (template)

## 🛡️ How WhatsApp Validation Works

### Primary Method: Store.QueryExist
- Uses WhatsApp Web's internal API
- Direct query to WhatsApp servers
- Fast and accurate
- Returns Business/Personal status

### Fallback Method: URL Detection
When Store is unavailable, uses priority-based detection:

1. **Priority 1**: Explicit error messages (popup/dialog)
2. **Priority 2**: Message input box presence
3. **Priority 3**: Chat header detection
4. **Priority 4**: URL change validation (strict)

### Business Detection
- Checks for catalog/storefront icon (`span[data-icon="storefront"]`)
- Verifies business badge
- Extracts business name from chat header

## 🔒 Security & Privacy

- ✅ All processing happens locally on your machine
- ✅ No data sent to external servers
- ✅ WhatsApp session stored locally in `backend/wa_session`
- ✅ No paid API or third-party services required
- ✅ Open source and transparent code

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Windows
taskkill /F /IM chrome.exe /T

# Or use the provided script
kill_chrome.bat
```

### WhatsApp Not Logging In
1. Close all Chrome instances
2. Delete `backend/wa_session` folder
3. Restart backend (`python run.py`)
4. Scan QR code again

### Invalid Numbers Detected as Valid
- Ensure stable internet connection
- Wait for full page load (12 seconds)
- Verify number format: digits after +62
- Check if number is actually registered on WhatsApp

### CSV Upload Error
- Ensure CSV has "phone" column
- Use UTF-8 encoding
- Phone format: digits after +62 (e.g., `81234567890`)

## 📈 Use Cases

- 🎯 **Lead Generation** - Extract business contacts from Google Maps
- 📞 **Contact Validation** - Verify WhatsApp numbers before outreach
- 💼 **Business Intelligence** - Identify WhatsApp Business accounts
- 📊 **Market Research** - Collect business data by category and location
- 🤖 **Automation** - Automate repetitive data collection tasks
- 📨 **Bulk Messaging** - Send promotional messages to validated contacts
- 🎯 **Personalized Outreach** - Send customized messages to leads
- 📢 **Broadcast Campaigns** - Announce promotions or updates to customers

## 🎯 Best Practices

### For Scraping
- Don't scrape too many places at once
- Use specific categories
- Add delays between scraping sessions
- Respect rate limits

### For WhatsApp Validation
- Validate maximum 100 numbers per batch
- Use 1-2 second delay between numbers
- Don't logout from WhatsApp Web during validation
- Session persists - no need to scan QR repeatedly

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Please:
- Respect Google Maps Terms of Service
- Respect WhatsApp Terms of Service
- Use responsibly and ethically
- Don't spam or harass users
- Comply with local data protection laws (GDPR, CCPA, etc.)

The authors are not responsible for misuse of this tool.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Playwright](https://playwright.dev/) - Browser automation library
- [Selenium](https://www.selenium.dev/) - Web automation framework
- [TailwindCSS](https://tailwindcss.com/) - Utility-first CSS framework

## 📧 Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

**⭐ If you find this project useful, please consider giving it a star!**

**Made with ❤️ for automating business data collection and validation**

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-04
