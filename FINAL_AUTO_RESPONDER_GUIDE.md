# Auto Responder - Panduan Lengkap

## Fitur yang Sudah Diperbaiki ✅

### 1. Deteksi Chat Baru
Bot sekarang bisa mendeteksi chat baru dengan 3 strategi:
- **Strategy 1**: Lingkaran hijau dengan angka (unread count badge)
- **Strategy 2**: Waktu hijau (green timestamp) + teks bold
- **Strategy 3**: Visual check semua chat untuk elemen hijau

### 2. Filter Grup Chat
Bot HANYA balas chat personal (1-on-1), TIDAK balas grup:
- Deteksi keyword grup (GRUP, KOMUNITAS, SOLUSI, dll)
- Deteksi icon grup
- Deteksi aria-label grup

### 3. AI Response Dinamis
AI sekarang memberikan jawaban yang:
- Relevan dengan pertanyaan
- Natural dan tidak template
- Kontekstual dan personal
- Menggunakan nama pelanggan

### 4. Input Box Detection
Bot kirim ke chat box yang benar (bukan search box):
- 3 strategi pencarian input box
- Validasi aria-label "ketik pesan"
- Tutup popup otomatis sebelum kirim

## Cara Menggunakan

### 1. Setup

```bash
# Backend
cd backend
python run.py

# Frontend (terminal baru)
cd ..
npm run dev
```

### 2. Login WhatsApp Web

1. Buka browser yang digunakan backend
2. Scan QR code WhatsApp Web
3. Tunggu sampai chat list muncul

### 3. Start Auto Responder

1. Buka frontend di browser
2. Klik tab "Auto Responder"
3. Isi "Response Prompt" dengan instruksi untuk AI:

**Contoh Prompt yang Baik:**
```
Kamu adalah customer service toko elektronik "ElektroKu".

Informasi Bisnis:
- Jam operasional: Senin-Jumat 09.00-17.00 WIB
- Produk: Laptop, HP, Aksesoris
- Harga laptop mulai 3 juta
- Harga HP mulai 1.5 juta
- Lokasi: Jakarta Selatan
- Pengiriman: JNE, J&T, Grab

Cara Merespons:
- Jika tanya harga: Tanyakan dulu kebutuhan mereka (merk, spesifikasi)
- Jika tanya stok: Konfirmasi produk yang dimaksud
- Jika komplain: Minta maaf dan tawarkan solusi
- Jika mau pesan: Tanyakan detail (warna, jumlah, alamat)
- Selalu ramah, profesional, dan helpful
- Gunakan nama pelanggan untuk personalisasi
```

4. Klik "Start Auto Responder"
5. Status berubah jadi "Running"

### 4. Testing

Kirim pesan dari HP lain ke nomor yang login:

**Test 1: Sapaan**
```
User: "Halo"
Bot: "Halo! Selamat datang di ElektroKu. Ada yang bisa saya bantu?"
```

**Test 2: Pertanyaan**
```
User: "Berapa harga laptop?"
Bot: "Untuk laptop, kami punya berbagai pilihan mulai dari 3 juta. Boleh saya tahu kebutuhan Anda? Untuk gaming, kerja, atau kuliah?"
```

**Test 3: Request**
```
User: "Mau pesan HP"
Bot: "Baik, untuk pemesanan HP. Boleh saya tahu merk dan tipe yang Anda inginkan? Kami punya berbagai pilihan mulai dari 1.5 juta."
```

## Log Output

### Chat Terdeteksi dengan Baik:
```
[Loop #1] Checking for unread personal chats...
  Searching for chats...
    Strategy 1: Looking for green unread count badges...
      Found 1 badge(s) with span[data-icon="unread-count"]
      ✓ Found unread personal chat: Saya
    ✓ Strategy 1 found 1 unread chat(s)

📱 Processing personal chat: Saya (628xxx)
  ✓ Found 1 new incoming message(s)
  
📨 New message from Saya (628xxx)
   Message: jusl apa?
   🤖 Generating response with llama-3.1-70b-versatile...
   📩 Incoming: jusl apa?
   💬 Generated: Halo! Maaf, saya kurang mengerti...
   🔍 Looking for chat input box...
   ✓ Found chat input: Ketik pesan ke Saya
   ✅ Response sent successfully
```

### Grup Chat Di-Skip:
```
Strategy 2: Looking for green timestamps...
  Scanning 5 chat items...
  Skipping group chat: SOLUSI SEHAT KELUARGA HARMONI
  ✓ Found unread personal chat: John Doe
```

## Troubleshooting

### Bot tidak detect chat baru

**Cek 1: WhatsApp Web Login**
- Pastikan sudah login
- Refresh halaman jika perlu
- Cek apakah chat list terlihat

**Cek 2: Log Backend**
```
Strategy 1: Looking for green unread count badges...
  Found 0 badge(s)
Strategy 2: Looking for green timestamps...
  Scanning 0 chat items...
```
Jika "0 chat items", berarti WhatsApp belum load atau tidak login.

**Cek 3: Test Manual**
- Kirim pesan dari HP lain
- Cek apakah muncul lingkaran hijau di chat
- Cek apakah waktu berwarna hijau

### Bot balas di grup (BUG!)

Seharusnya tidak terjadi. Jika terjadi:
1. Cek nama grup di log
2. Tambahkan keyword grup ke `_is_group_chat()`
3. Report bug dengan nama grup

### AI jawaban tidak relevan

**Perbaiki Response Prompt:**
- Tambahkan lebih banyak context tentang bisnis
- Berikan contoh FAQ dan jawaban
- Berikan instruksi lebih spesifik

**Contoh:**
```
JANGAN:
"Jawab dengan sopan"

LAKUKAN:
"Jika user tanya harga, tanyakan dulu kebutuhan mereka.
Jika user komplain, minta maaf dan tawarkan solusi.
Jika user mau pesan, tanyakan detail produk."
```

### Element click intercepted

Sudah diperbaiki dengan:
- Tutup popup 3x sebelum kirim
- Gunakan ESC key
- Gunakan JavaScript click

Jika masih terjadi, cek apakah ada popup/dialog yang menghalangi.

### Groq API Error

```
⚠️ All Groq models failed for auto-responder!
Last error: HTTP 429
```

**Solusi:**
1. Cek GROQ_API_KEY di `.env`
2. Cek quota di https://console.groq.com
3. Tunggu beberapa menit (rate limit)
4. Bot akan fallback ke template response

## Tips & Best Practices

### 1. Response Prompt yang Efektif

✅ **BAIK:**
- Spesifik tentang bisnis Anda
- Berikan context lengkap
- Instruksi jelas untuk berbagai skenario
- Contoh FAQ dan jawaban

❌ **KURANG BAIK:**
- Generic: "Jawab dengan sopan"
- Tidak ada context bisnis
- Tidak ada instruksi spesifik

### 2. Monitoring

Selalu monitor log backend untuk:
- Chat yang terdeteksi
- AI response yang digenerate
- Error yang terjadi

### 3. Testing Berkala

Test dengan berbagai jenis pesan:
- Sapaan
- Pertanyaan
- Request
- Komplain
- Spam

### 4. Update Prompt

Update response prompt berdasarkan:
- Pertanyaan yang sering muncul
- Feedback pelanggan
- Perubahan produk/layanan

## Fitur Mendatang (Roadmap)

- [ ] Conversation history (ingat percakapan sebelumnya)
- [ ] Multi-language support
- [ ] Custom response per contact
- [ ] Schedule (jam operasional)
- [ ] Analytics dashboard
- [ ] Webhook integration

## Support

Jika ada masalah:
1. Cek log backend untuk error
2. Cek dokumentasi ini
3. Restart backend dan frontend
4. Clear browser cache
5. Re-login WhatsApp Web
