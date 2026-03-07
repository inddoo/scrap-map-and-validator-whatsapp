# Cara Test Auto Responder

## Persiapan

1. Pastikan backend sudah running:
```bash
cd backend
python run.py
```

2. Buka browser dan login WhatsApp Web
3. Buka frontend di browser lain

## Test Steps

### Test 1: Chat Personal (Harus Berhasil)

1. Buka tab "Auto Responder" di frontend
2. Isi prompt response (contoh: "Saya asisten virtual, ada yang bisa saya bantu?")
3. Klik "Start Auto Responder"
4. Status harus berubah jadi "Running"

5. Dari HP lain, kirim pesan WhatsApp ke nomor yang login
   - Contoh: "Halo, apa kabar?"

6. Tunggu 3-6 detik
7. Bot harus otomatis balas dengan AI response

8. Cek console log backend:
```
[Loop #1] Checking for unread personal chats...
  ✓ Found 1 unread personal chat(s)
  
  📱 Processing personal chat: [Nama] (628xxx)
    ✓ Found 1 new incoming message(s)
    
📨 New message from [Nama] (628xxx)
   Message: Halo, apa kabar?
   🤖 AI Response: Halo! Saya baik...
   ✅ Response sent successfully
```

### Test 2: Grup Chat (Harus Di-Skip)

1. Auto responder masih running
2. Kirim pesan di grup WhatsApp
3. Bot TIDAK boleh balas
4. Cek console log:
```
Skipping group chat: NAMA GRUP
```

### Test 3: Pesan Sudah Dibalas (Tidak Balas Lagi)

1. Auto responder masih running
2. Pesan yang sudah dibalas sebelumnya tidak akan dibalas lagi
3. Cek console log:
```
No new messages (already processed or no incoming messages)
```

### Test 4: Stop Auto Responder

1. Klik "Stop Auto Responder"
2. Status berubah jadi "Stopped"
3. Kirim pesan baru
4. Bot tidak akan balas

## Expected Results

✅ Bot balas chat personal (1-on-1)
✅ Bot TIDAK balas grup chat
✅ Bot TIDAK balas pesan yang sudah dibalas
✅ Bot TIDAK balas pesan sendiri
✅ Bot TIDAK balas pesan sistem
✅ Response menggunakan Groq AI
✅ Popup/dialog ditutup otomatis

## Troubleshooting

### Bot tidak balas sama sekali
- Cek apakah WhatsApp Web masih login
- Cek console log untuk error
- Restart auto responder

### Bot balas di grup (BUG!)
- Cek nama grup, mungkin tidak terdeteksi
- Tambahkan keyword grup di `_is_group_chat()`

### Element click intercepted
- Sudah diperbaiki dengan popup handler
- Bot akan coba tutup popup 3x sebelum kirim

### Groq API error
- Cek GROQ_API_KEY di .env
- Cek quota Groq API
- Bot akan fallback ke template response
