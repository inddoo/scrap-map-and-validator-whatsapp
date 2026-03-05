# 📝 Panduan Input Nama untuk Manual Entry

## Fitur Baru: Input Nama Pemilik Nomor

Sekarang Anda dapat memasukkan nama untuk setiap nomor telepon saat menggunakan mode manual input (tanpa CSV). Ini membuat pesan AI lebih personal dan tidak lagi menggunakan "Halo Contact 1", "Halo Contact 2", dll.

## Cara Menggunakan

### 1. Buka Tab "WA Sender"

### 2. Jangan Upload CSV (Mode Manual)
- Pastikan tidak ada CSV yang di-upload
- Form input nama hanya muncul di mode manual

### 3. Masukkan Nomor Telepon
```
628123456789
628987654321
628555666777
```

### 4. Masukkan Nama (Satu Per Baris)
```
John Doe
Jane Smith
Bob Johnson
```

**PENTING:** Urutan nama harus sesuai dengan urutan nomor telepon!

### 5. Aktifkan AI dan Generate Pesan
- Toggle "Gunakan AI untuk Generate Pesan"
- Masukkan instruksi/template untuk AI
- Klik "🤖 Generate Pesan dengan AI"

## Contoh Hasil

Dengan nama yang diinput:
```
Halo John Doe! 👋

Kami dari PT Digital Solutions ingin menawarkan...
```

Tanpa nama (akan fallback ke Contact 1, 2, dst):
```
Halo Contact 1! 👋

Kami dari PT Digital Solutions ingin menawarkan...
```

## Tips

1. **Jumlah Nama vs Nomor:**
   - Jika nama lebih sedikit dari nomor, sisanya akan menggunakan "Contact X"
   - Contoh: 5 nomor, 3 nama → 3 pertama pakai nama, 2 sisanya "Contact 4", "Contact 5"

2. **Nama Kosong:**
   - Jika field nama dibiarkan kosong, semua akan menggunakan "Contact 1", "Contact 2", dst

3. **Format Nama:**
   - Bisa nama lengkap: "John Doe"
   - Bisa nama panggilan: "John"
   - Bisa nama perusahaan: "PT ABC"

4. **CSV Mode:**
   - Jika menggunakan CSV, nama diambil dari kolom CSV (biasanya kolom "name")
   - Field input nama manual tidak akan muncul

## Troubleshooting

**Q: Field nama tidak muncul?**
A: Pastikan tidak ada CSV yang di-upload. Hapus CSV terlebih dahulu.

**Q: Nama tidak sesuai dengan nomor?**
A: Periksa urutan! Nama baris ke-1 akan dipasangkan dengan nomor baris ke-1, dst.

**Q: Bisa pakai emoji di nama?**
A: Tidak disarankan karena ChromeDriver memiliki keterbatasan dengan karakter Unicode.

## File Terkait

- `src/App.tsx` - UI dan logic untuk input nama
- `backend/ai/gemini_service.py` - AI service yang menggunakan nama untuk personalisasi
- `backend/api/routes.py` - API endpoint untuk generate pesan

---

✅ Fitur ini sudah terintegrasi penuh dengan sistem AI dan WA Sender!
