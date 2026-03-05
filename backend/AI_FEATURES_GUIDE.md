# 🤖 AI Features Guide - Gemini Integration

## Overview
Fitur AI menggunakan Google Gemini untuk:
1. **Generate Pesan Personal** - Membuat pesan unik untuk setiap kontak berdasarkan data CSV
2. **Auto Responder** - Membalas pesan masuk secara otomatis dengan AI

---

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Get Gemini API Key
1. Kunjungi: https://makersuite.google.com/app/apikey
2. Login dengan Google Account
3. Klik "Create API Key"
4. Copy API key

### 3. Set Environment Variable
Buat file `.env` di folder `backend/`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## Features

### 🎯 Feature 1: AI Message Generation

Generate pesan personal untuk setiap kontak berdasarkan data CSV.

#### How It Works:
1. Upload CSV dengan kolom: `phone`, `name`, `company`, dll
2. Tulis template/instruksi untuk AI
3. AI akan generate pesan unik untuk setiap kontak

#### Example:

**CSV Data:**
```csv
phone,name,company,position
628123456789,John Doe,PT ABC,Manager
628987654321,Jane Smith,CV XYZ,Director
```

**Template/Instruksi:**
```
Buatkan pesan promosi untuk {name} dari perusahaan {company}. 
Tawarkan diskon khusus 20% untuk layanan IT kami.
Gunakan bahasa profesional tapi ramah.
```

**AI Generated Message untuk John:**
```
Halo Pak John Doe! 👋

Saya dari tim marketing ingin menawarkan kesempatan spesial untuk PT ABC.

Kami memberikan diskon 20% untuk semua layanan IT kami, termasuk:
✅ Pembuatan Website
✅ Aplikasi Mobile
✅ Sistem ERP

Sebagai Manager, Bapak pasti memahami pentingnya digitalisasi bisnis.

Tertarik untuk diskusi lebih lanjut? 😊
```

#### API Endpoint:
```http
POST http://localhost:8000/ai/generate-messages
Content-Type: application/json

{
  "template": "Buatkan pesan untuk {name}...",
  "csv_data": [
    {"phone": "628xxx", "name": "John", "company": "PT ABC"},
    ...
  ],
  "context": "Kami adalah perusahaan IT..."
}
```

---

### 🤖 Feature 2: Auto Responder

AI akan membalas pesan masuk secara otomatis berdasarkan prompt yang Anda berikan.

#### How It Works:
1. Aktifkan "Auto Responder AI"
2. Tulis prompt/instruksi untuk AI responder
3. AI akan monitor dan balas pesan masuk

#### Example Prompts:

**Customer Service:**
```
Anda adalah customer service yang ramah dan profesional.
Jawab pertanyaan pelanggan tentang produk dan layanan kami.
Jika ada pertanyaan teknis, arahkan ke tim support.
Gunakan emoji yang sesuai.
```

**Sales:**
```
Anda adalah sales yang persuasif namun tidak pushy.
Tawarkan produk yang sesuai dengan kebutuhan pelanggan.
Jika pelanggan tertarik, tawarkan untuk meeting atau demo.
Selalu follow up dengan sopan.
```

**Appointment Booking:**
```
Anda adalah asisten yang membantu booking appointment.
Tanyakan tanggal dan waktu yang diinginkan.
Konfirmasi detail appointment.
Kirim reminder H-1.
```

#### API Endpoint:
```http
POST http://localhost:8000/ai/auto-responder
Content-Type: application/json

{
  "incoming_message": "Halo, saya mau tanya harga website?",
  "sender_phone": "628123456789",
  "sender_data": {
    "name": "John Doe",
    "company": "PT ABC"
  },
  "response_prompt": "Anda adalah sales yang ramah...",
  "conversation_history": [
    {"role": "bot", "message": "Halo! Ada yang bisa dibantu?"},
    {"role": "user", "message": "Halo, saya mau tanya harga website?"}
  ]
}
```

---

### 📨 Feature 3: Send AI Personalized Messages

Kirim pesan AI-generated dengan auto responder dalam satu flow.

#### API Endpoint:
```http
POST http://localhost:8000/wa/send-ai-personalized
Content-Type: application/json

{
  "csv_data": [
    {"phone": "628xxx", "name": "John", "company": "PT ABC"},
    ...
  ],
  "message_template": "Buatkan pesan untuk {name}...",
  "use_ai": true,
  "context": "Kami adalah perusahaan IT...",
  "min_delay": 5,
  "max_delay": 10,
  "auto_responder_enabled": true,
  "auto_responder_prompt": "Anda adalah customer service..."
}
```

---

## Frontend Usage

### 1. Upload CSV
```typescript
// CSV harus punya kolom "phone"
// Kolom lain: name, company, position, dll (opsional)
```

### 2. Enable AI
```typescript
setUseAI(true)
```

### 3. Write Template/Instruction
```typescript
setSenderMessage("Buatkan pesan promosi untuk {name}...")
setAiContext("Kami adalah perusahaan IT...")
```

### 4. Generate Messages
```typescript
await handleGenerateAIMessages()
// AI akan generate pesan untuk setiap kontak
```

### 5. Review & Send
```typescript
// Review generated messages
// Click "Kirim Pesan AI"
await handleSendAIMessages()
```

---

## Best Practices

### ✅ DO:
- Gunakan template yang jelas dan spesifik
- Berikan konteks yang cukup untuk AI
- Review generated messages sebelum kirim
- Set delay yang cukup (min 5-10 detik)
- Test dengan 1-2 nomor dulu
- Monitor auto responder responses

### ❌ DON'T:
- Jangan kirim spam atau pesan tidak diinginkan
- Jangan gunakan untuk scam atau penipuan
- Jangan kirim terlalu banyak sekaligus (max 50-100)
- Jangan set delay terlalu pendek
- Jangan biarkan auto responder tanpa monitoring

---

## Troubleshooting

### Error: "GEMINI_API_KEY not found"
**Solution:** Set API key di `.env` file

### Error: "Rate limit exceeded"
**Solution:** 
- Tunggu beberapa menit
- Reduce jumlah requests
- Upgrade Gemini API plan

### AI Generated Messages Not Personal
**Solution:**
- Berikan template yang lebih spesifik
- Tambahkan konteks yang lebih detail
- Pastikan CSV data lengkap

### Auto Responder Not Working
**Solution:**
- Check WhatsApp Web masih login
- Check prompt auto responder jelas
- Monitor console logs untuk errors

---

## Pricing

### Gemini API (Free Tier):
- 60 requests per minute
- 1,500 requests per day
- Cukup untuk 1,500 pesan per hari

### Gemini API (Paid):
- Unlimited requests
- Faster response
- Priority support

**Link:** https://ai.google.dev/pricing

---

## Examples

### Example 1: Sales Outreach
```javascript
// CSV: phone, name, company, industry
// Template: "Buatkan pesan sales untuk {name} dari {company} di industri {industry}"
// Context: "Kami menawarkan solusi CRM untuk meningkatkan sales"
```

### Example 2: Event Invitation
```javascript
// CSV: phone, name, position, company
// Template: "Undang {name} ({position}) dari {company} ke webinar kami"
// Context: "Webinar tentang Digital Transformation, tanggal 15 Maret 2024"
```

### Example 3: Follow Up
```javascript
// CSV: phone, name, last_meeting_date, topic
// Template: "Follow up {name} tentang meeting terakhir tanggal {last_meeting_date} topik {topic}"
// Context: "Tanyakan progress dan tawarkan bantuan"
```

---

## Security & Privacy

⚠️ **IMPORTANT:**
- Jangan share API key dengan orang lain
- Jangan commit API key ke Git
- Jangan kirim data sensitif ke AI
- Comply dengan WhatsApp Terms of Service
- Respect privacy dan GDPR regulations

---

## Support

Jika ada pertanyaan atau issue:
1. Check dokumentasi ini
2. Check console logs untuk errors
3. Test dengan data sample dulu
4. Contact developer

---

**Happy Automating! 🚀**
