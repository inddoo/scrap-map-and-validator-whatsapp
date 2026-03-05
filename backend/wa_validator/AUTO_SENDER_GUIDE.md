# WhatsApp Auto Sender Guide

## 📨 Fitur Auto Sender

Kirim pesan WhatsApp otomatis ke banyak nomor sekaligus dengan delay anti-spam.

## ⚠️ PENTING - Baca Sebelum Menggunakan

### Aturan Penggunaan
- ✅ Gunakan untuk komunikasi bisnis yang sah
- ✅ Kirim hanya ke nomor yang sudah opt-in
- ✅ Gunakan delay yang cukup (min 5 detik)
- ❌ JANGAN spam atau kirim pesan tidak diinginkan
- ❌ JANGAN kirim terlalu banyak pesan sekaligus
- ❌ JANGAN gunakan untuk penipuan atau scam

### Risiko
- WhatsApp bisa ban akun Anda jika terdeteksi spam
- Gunakan dengan bijak dan bertanggung jawab
- Kami tidak bertanggung jawab atas penyalahgunaan

## 🚀 Cara Menggunakan

### 1. Inisialisasi WhatsApp (Wajib)

Sebelum mengirim pesan, pastikan WhatsApp sudah diinisialisasi:

```bash
POST /wa/init
```

Scan QR code sekali saja, session akan tersimpan.

### 2. Kirim Pesan Tunggal

Kirim pesan ke satu nomor:

```bash
POST /wa/send
Content-Type: application/json

{
  "phone": "628123456789",
  "message": "Halo, ini pesan test!",
  "delay": 5
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "phone": "628123456789",
    "message_sent": true,
    "status": "✓ Pesan terkirim",
    "error": null
  }
}
```

### 3. Kirim Pesan Massal (Bulk)

Kirim pesan yang sama ke banyak nomor:

```bash
POST /wa/send-bulk
Content-Type: application/json

{
  "phone_numbers": [
    "628123456789",
    "628987654321",
    "628555666777"
  ],
  "message": "Halo! Ini pesan broadcast.",
  "min_delay": 5,
  "max_delay": 10,
  "stop_on_error": false
}
```

**Parameters:**
- `phone_numbers`: List nomor telepon (format: 628xxx)
- `message`: Pesan yang akan dikirim (sama untuk semua)
- `min_delay`: Delay minimum antar pesan (detik)
- `max_delay`: Delay maximum antar pesan (detik)
- `stop_on_error`: Stop jika ada error (default: false)

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "phone": "628123456789",
      "message_sent": true,
      "status": "✓ Pesan terkirim",
      "error": null
    },
    ...
  ],
  "summary": {
    "total": 3,
    "sent": 3,
    "failed": 0,
    "sent_percent": 100.0,
    "failed_percent": 0.0
  }
}
```

### 4. Kirim Pesan Personal (Template)

Kirim pesan dengan personalisasi menggunakan template:

```bash
POST /wa/send-personalized
Content-Type: application/json

{
  "contacts": [
    {
      "phone": "628123456789",
      "name": "John Doe",
      "company": "ABC Corp"
    },
    {
      "phone": "628987654321",
      "name": "Jane Smith",
      "company": "XYZ Ltd"
    }
  ],
  "message_template": "Halo {name} dari {company}!\n\nIni pesan khusus untuk Anda.",
  "min_delay": 5,
  "max_delay": 10
}
```

**Template Variables:**
- Gunakan `{field_name}` untuk placeholder
- Field harus ada di setiap contact object
- Contoh: `{name}`, `{company}`, `{phone}`, dll

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "phone": "628123456789",
      "message_sent": true,
      "status": "✓ Pesan terkirim",
      "error": null,
      "contact": {
        "phone": "628123456789",
        "name": "John Doe",
        "company": "ABC Corp"
      }
    },
    ...
  ],
  "summary": {
    "total": 2,
    "sent": 2,
    "failed": 0,
    "sent_percent": 100.0,
    "failed_percent": 0.0
  }
}
```

## 📋 Format Pesan

### Single Line
```
"message": "Halo, ini pesan singkat!"
```

### Multi Line
```
"message": "Halo!\n\nIni pesan multi-line.\n\nTerima kasih."
```

### Dengan Emoji
```
"message": "🎉 Promo Spesial! 🎉\n\nDiskon 50% hari ini!"
```

### Template Personal
```
"message_template": "Halo {name}! 👋\n\nKami dari {company} ingin menawarkan...\n\nHubungi: {phone}"
```

## ⏱️ Delay & Anti-Spam

### Rekomendasi Delay
- **Minimum**: 5 detik antar pesan
- **Maksimum**: 10-15 detik antar pesan
- **Random**: Gunakan min/max untuk variasi

### Kenapa Perlu Delay?
- Menghindari deteksi spam oleh WhatsApp
- Terlihat lebih natural (seperti manusia)
- Mengurangi risiko ban akun

### Best Practices
```json
{
  "min_delay": 5,    // Minimal 5 detik
  "max_delay": 10    // Random 5-10 detik
}
```

Untuk lebih aman:
```json
{
  "min_delay": 10,   // Minimal 10 detik
  "max_delay": 20    // Random 10-20 detik
}
```

## 🎯 Use Cases

### 1. Broadcast Promo
```json
{
  "phone_numbers": ["628xxx", "628yyy"],
  "message": "🎉 PROMO SPESIAL!\n\nDiskon 50% untuk semua produk!\nKunjungi: www.toko.com",
  "min_delay": 10,
  "max_delay": 15
}
```

### 2. Reminder Personal
```json
{
  "contacts": [
    {"phone": "628xxx", "name": "John", "date": "15 Maret"}
  ],
  "message_template": "Halo {name}!\n\nReminder: Meeting Anda pada {date}.\n\nTerima kasih.",
  "min_delay": 5,
  "max_delay": 10
}
```

### 3. Follow-up Leads
```json
{
  "contacts": [
    {"phone": "628xxx", "name": "Jane", "product": "Laptop"}
  ],
  "message_template": "Halo {name}!\n\nTerima kasih sudah tertarik dengan {product}.\n\nAda yang bisa kami bantu?",
  "min_delay": 8,
  "max_delay": 12
}
```

## 🛡️ Error Handling

### Nomor Tidak Valid
```json
{
  "phone": "628xxx",
  "message_sent": false,
  "status": "Nomor tidak valid atau tidak terdaftar",
  "error": "Input box not found"
}
```

### Timeout
```json
{
  "phone": "628xxx",
  "message_sent": false,
  "status": "Error: Timeout",
  "error": "Timeout waiting for input box"
}
```

### Stop on Error
Jika `stop_on_error: true`, proses akan berhenti saat ada error pertama.

## 📊 Monitoring

### Check Summary
Setiap response bulk/personalized memiliki summary:

```json
{
  "summary": {
    "total": 10,
    "sent": 8,
    "failed": 2,
    "sent_percent": 80.0,
    "failed_percent": 20.0
  }
}
```

### Check Individual Results
Cek status setiap nomor di array `results`:

```json
{
  "results": [
    {
      "phone": "628xxx",
      "message_sent": true,
      "status": "✓ Pesan terkirim"
    },
    {
      "phone": "628yyy",
      "message_sent": false,
      "status": "Nomor tidak valid"
    }
  ]
}
```

## ⚠️ Batasan & Limitasi

### WhatsApp Limits
- WhatsApp memiliki rate limit untuk mencegah spam
- Terlalu banyak pesan dalam waktu singkat = risiko ban
- Gunakan delay yang cukup!

### Rekomendasi
- **Per Batch**: Maksimal 50-100 nomor
- **Per Hari**: Maksimal 200-300 pesan
- **Delay**: Minimal 5 detik, ideal 10-15 detik

### Tanda-tanda Spam Detection
- Pesan tidak terkirim
- Akun di-suspend sementara
- Muncul captcha
- Akun di-ban permanent

## 🔒 Keamanan

### Session
- Session WhatsApp tersimpan lokal
- Jangan share session folder
- Logout jika tidak digunakan

### Data Privacy
- Jangan kirim data sensitif
- Patuhi GDPR/privacy laws
- Dapatkan consent sebelum kirim pesan

## 💡 Tips & Tricks

### 1. Test Dulu
Kirim ke nomor sendiri dulu untuk test:
```json
{
  "phone": "628_YOUR_NUMBER",
  "message": "Test message"
}
```

### 2. Gunakan Template
Lebih personal dan efektif:
```
"Halo {name}!" > "Halo!"
```

### 3. Timing
Kirim di jam kerja (09:00 - 17:00) untuk response lebih baik.

### 4. Follow-up
Jangan kirim berulang ke nomor yang sama dalam waktu dekat.

### 5. Monitor
Cek summary dan results untuk evaluasi.

## 🐛 Troubleshooting

### Pesan Tidak Terkirim
1. Cek nomor valid (sudah divalidasi?)
2. Cek koneksi internet
3. Cek WhatsApp Web masih login
4. Coba delay lebih lama

### Session Expired
1. Restart backend
2. Scan QR code lagi
3. Coba kirim ulang

### Terlalu Lambat
1. Kurangi delay (tapi hati-hati spam!)
2. Kirim dalam batch kecil
3. Gunakan multiple sessions (advanced)

## 📚 Contoh Lengkap

### Python Example
```python
import requests

# 1. Init WhatsApp
response = requests.post('http://localhost:8000/wa/init')
print(response.json())

# 2. Send bulk messages
data = {
    "phone_numbers": ["628123456789", "628987654321"],
    "message": "Halo! Ini pesan test.",
    "min_delay": 5,
    "max_delay": 10
}
response = requests.post('http://localhost:8000/wa/send-bulk', json=data)
print(response.json())
```

### JavaScript Example
```javascript
// 1. Init WhatsApp
const initResponse = await fetch('http://localhost:8000/wa/init', {
  method: 'POST'
});
console.log(await initResponse.json());

// 2. Send personalized messages
const data = {
  contacts: [
    { phone: '628123456789', name: 'John' },
    { phone: '628987654321', name: 'Jane' }
  ],
  message_template: 'Halo {name}! Ini pesan untuk Anda.',
  min_delay: 5,
  max_delay: 10
};

const sendResponse = await fetch('http://localhost:8000/wa/send-personalized', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});
console.log(await sendResponse.json());
```

---

**⚠️ DISCLAIMER:**
Gunakan fitur ini dengan bijak dan bertanggung jawab. Penyalahgunaan dapat mengakibatkan ban akun WhatsApp Anda. Kami tidak bertanggung jawab atas penyalahgunaan fitur ini.

**✅ BEST PRACTICE:**
- Dapatkan consent sebelum kirim pesan
- Gunakan delay yang cukup
- Jangan spam
- Patuhi hukum dan regulasi
- Gunakan untuk komunikasi bisnis yang sah
