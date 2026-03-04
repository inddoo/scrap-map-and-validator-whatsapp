# Troubleshooting WhatsApp Validator

## Error: "Not logged in!"

### Gejala:
```
Menunggu scan... (120 detik)
✓ Login berhasil!
✓ Session tersimpan!

# Tapi saat validasi:
Error: Not logged in!
```

### Penyebab:
1. WhatsApp Web belum fully loaded setelah scan QR
2. Session belum tersimpan dengan benar
3. Chat list belum muncul

### Solusi:

#### 1. Tunggu Lebih Lama Setelah Scan QR

Setelah scan QR berhasil, sistem sekarang otomatis menunggu 10 detik untuk memastikan WhatsApp Web fully loaded.

#### 2. Verifikasi Login Manual

Setelah scan QR, cek di Chrome:
- Apakah chat list sudah muncul?
- Apakah ada loading indicator?
- Apakah bisa klik chat?

Jika belum, tunggu sampai fully loaded baru coba validasi.

#### 3. Re-Initialize

Jika masih error, tutup dan initialize ulang:

```bash
POST /wa/close
POST /wa/init
```

#### 4. Hapus Session Lama

Jika masih bermasalah, hapus session dan scan ulang:

```bash
# Stop backend
# Hapus folder session
rm -rf backend/wa_session/

# Start backend lagi
python backend/run.py

# Initialize ulang
POST /wa/init
```

## Error: "Store not available"

### Gejala:
```
Error: Store not available
```

### Penyebab:
WhatsApp Web belum fully loaded atau Store object belum tersedia.

### Solusi:

#### 1. Tunggu Lebih Lama

Script akan otomatis inject Store exposure code. Tunggu 5-10 detik.

#### 2. Refresh WhatsApp Web

Jika masih error:
1. Tutup Chrome
2. Call `/wa/close`
3. Call `/wa/init` lagi

#### 3. Update Chrome

Pastikan Chrome versi terbaru:
```bash
chrome://settings/help
```

## Error: "Query failed"

### Gejala:
```
[1/3] 81234567890
  Querying: 6281234567890
  → ⚠️ Query failed
```

### Penyebab:
1. Rate limit dari WhatsApp
2. Koneksi internet bermasalah
3. WhatsApp Web error

### Solusi:

#### 1. Tambah Delay

Edit `wa_checker.py`:
```python
# Dari 1.5 detik jadi 3 detik
time.sleep(3)
```

#### 2. Batch Kecil

Jangan validasi terlalu banyak sekaligus:
- Max 20-30 nomor per batch
- Tunggu 1-2 menit antar batch

#### 3. Cek Koneksi

Pastikan koneksi internet stabil.

## Error: "Timeout"

### Gejala:
```
Menunggu scan... (120 detik)
✗ Timeout
```

### Penyebab:
QR code tidak di-scan dalam 120 detik.

### Solusi:

#### 1. Scan Lebih Cepat

Siapkan HP sebelum call `/wa/init`.

#### 2. Perpanjang Timeout

Edit `wa_checker.py`:
```python
# Dari 120 detik jadi 180 detik
WebDriverWait(self.driver, 180)
```

## Error: "Chrome not found"

### Gejala:
```
Error: Chrome not found
```

### Penyebab:
Chrome tidak terinstall atau tidak di PATH.

### Solusi:

#### 1. Install Chrome

Download dan install Chrome:
https://www.google.com/chrome/

#### 2. Install ChromeDriver

```bash
pip install webdriver-manager
```

Atau download manual:
https://chromedriver.chromium.org/

## Tips Umum

### 1. Restart Backend

Jika ada masalah, restart backend:
```bash
# Stop (Ctrl+C)
# Start lagi
python backend/run.py
```

### 2. Clear Session

Hapus session lama jika bermasalah:
```bash
rm -rf backend/wa_session/
```

### 3. Monitor Chrome

Jangan tutup Chrome window yang dibuka otomatis. Lihat apa yang terjadi di sana untuk debug.

### 4. Check Logs

Lihat console output untuk error detail:
```bash
python backend/run.py
```

### 5. Test dengan Nomor Sedikit

Test dulu dengan 1-2 nomor sebelum validasi banyak:
```json
{
  "phone_numbers": ["81234567890"]
}
```

## Best Practices

1. **Scan QR Sekali**: Setelah scan, session tersimpan. Tidak perlu scan lagi.

2. **Tunggu Fully Loaded**: Setelah scan, tunggu sampai chat list muncul.

3. **Batch Kecil**: Validasi 20-30 nomor per batch untuk avoid rate limit.

4. **Delay Cukup**: Gunakan delay 1.5-3 detik antar nomor.

5. **Monitor Chrome**: Jangan tutup Chrome, lihat untuk debug.

6. **Stable Connection**: Pastikan koneksi internet stabil.

7. **Update Chrome**: Gunakan Chrome versi terbaru.

## Kontak Support

Jika masih bermasalah, cek:
1. Console output backend
2. Chrome DevTools (F12)
3. Network tab untuk error
4. Screenshot error untuk debug
