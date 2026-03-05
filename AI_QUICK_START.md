# 🤖 AI Quick Start Guide

## Setup dalam 5 Menit

### 1. Get Gemini API Key (2 menit)
1. Buka: https://makersuite.google.com/app/apikey
2. Login dengan Google Account
3. Klik "Create API Key"
4. Copy API key yang muncul

### 2. Set API Key (1 menit)
Buat file `backend/.env`:
```env
GEMINI_API_KEY=paste_your_api_key_here
```

### 3. Install Dependencies (2 menit)
```bash
cd backend
pip install google-generativeai
```

### 4. Restart Backend
```bash
python run.py
```

---

## Test AI Features

### Test 1: Generate AI Messages

1. **Upload CSV** (`test_ai_sender.csv`)
   ```csv
   phone,name,company,position
   628123456789,John Doe,PT ABC,CEO
   ```

2. **Enable AI** ✅ Gunakan AI untuk Generate Pesan Personal

3. **Write Template:**
   ```
   Buatkan pesan promosi untuk {name} yang bekerja sebagai {position} di {company}.
   Tawarkan layanan IT kami dengan diskon 20%.
   Gunakan bahasa profesional tapi ramah.
   ```

4. **Click** 🤖 Generate Pesan AI

5. **Review** generated messages

6. **Send** 🤖 Kirim Pesan AI

---

### Test 2: Auto Responder

1. **Enable** ✅ Aktifkan Auto Responder AI

2. **Write Prompt:**
   ```
   Anda adalah customer service yang ramah.
   Jawab pertanyaan tentang produk dan harga.
   Jika ada pertanyaan teknis, arahkan ke tim support.
   ```

3. **Send messages** dengan auto responder enabled

4. **AI will monitor** dan balas pesan masuk otomatis

---

## Example Templates

### Sales Outreach
```
Buatkan pesan sales untuk {name} dari {company}.
Perkenalkan produk CRM kami yang bisa meningkatkan sales 30%.
Tawarkan free trial 14 hari.
Gunakan emoji yang sesuai.
```

### Event Invitation
```
Undang {name} ({position}) dari {company} ke webinar kami.
Topik: Digital Transformation untuk {industry}
Tanggal: 15 Maret 2024, 14:00 WIB
Gratis dan ada sertifikat.
```

### Follow Up
```
Follow up {name} tentang meeting terakhir.
Tanyakan apakah ada pertanyaan lebih lanjut.
Tawarkan bantuan untuk implementasi.
Profesional tapi tidak pushy.
```

---

## Tips

✅ **DO:**
- Test dengan 1-2 nomor dulu
- Review AI messages sebelum kirim
- Gunakan template yang spesifik
- Set delay 5-10 detik

❌ **DON'T:**
- Kirim spam
- Kirim terlalu banyak sekaligus
- Gunakan untuk scam
- Set delay terlalu pendek

---

## Troubleshooting

**Q: Error "GEMINI_API_KEY not found"**
A: Check file `.env` sudah dibuat dan API key sudah diset

**Q: AI messages tidak personal**
A: Berikan template yang lebih spesifik dan detail

**Q: Rate limit exceeded**
A: Tunggu beberapa menit, free tier ada limit 60 req/min

---

## Need Help?

📖 Full documentation: [AI_FEATURES_GUIDE.md](backend/AI_FEATURES_GUIDE.md)

🚀 Happy Automating!
