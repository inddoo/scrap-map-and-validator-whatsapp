# WhatsApp Validator - Query Method

## Metode Baru: Store.QueryExist.queryExist

Implementasi ini menggunakan fungsi internal WhatsApp Web untuk validasi nomor secara langsung, bukan dengan membuka chat satu per satu.

### Keunggulan Metode Ini

✅ **Lebih Cepat**: 1-2 detik per nomor (vs 10-15 detik metode lama)  
✅ **Lebih Reliable**: Langsung query ke server WhatsApp  
✅ **Deteksi Business**: Bisa detect Business vs Personal account  
✅ **Nama Bisnis**: Dapat nama bisnis jika tersedia  
✅ **Batch Processing**: Validasi banyak nomor sekaligus  

### Cara Kerja

1. **Aplikasi menerima nomor** yang Anda ketik
2. **Aplikasi menyuruh WhatsApp Web** di background untuk "bertanya" ke server WhatsApp: 
   > "Hei Server WhatsApp, tolong cek nomor ini ada tidak di database kamu?"
3. Ini dilakukan melalui perintah `Store.QueryExist.queryExist(number)`
4. **Server WhatsApp membalas** dengan data lengkap nomor tersebut:
   - Status: Terdaftar atau tidak
   - Tipe: Business (`biz: true`) atau Personal
   - Nama bisnis (jika ada)
5. **Aplikasi menampilkan** hasil kepada Anda

### Apakah Ini API Resmi?

**TIDAK.** Ini adalah eksploitasi fitur internal WhatsApp Web.

- Saat Anda menggunakan WhatsApp Web biasa dan ingin memulai obrolan dengan nomor baru (lewat link wa.me atau mengetik nomor), WhatsApp Web Anda juga diam-diam melakukan query ini ke server pusat untuk memastikan nomor itu valid
- Aplikasi ini hanya "meminjam" jalur browser WhatsApp Web Anda untuk mengirimkan query tersebut secara massal dan otomatis (bot)
- Itulah sebabnya aplikasi ini mengharuskan Anda untuk melakukan scan barcode terlebih dahulu agar bisa "menumpang" koneksi akun WhatsApp Anda

Kalau ini adalah fitur Meta API resmi berbayar, Anda tidak perlu men-scan barcode HP Anda ke aplikasinya, melainkan Anda cukup memasukkan Token/API Key bertipe teks (seperti sandi panjang) ke pengaturan aplikasi.

## Cara Pakai

### 1. Test Standalone

```bash
cd backend
python test_query_method.py
```

Masukkan nomor yang ingin ditest (pisahkan dengan koma):
```
081234567890, 082111222333, 085999888777
```

### 2. Integrasi dengan API

#### Initialize Checker

```bash
POST http://localhost:8000/wa/init
```

Response:
```json
{
  "success": true,
  "message": "WhatsApp checker ready! Session tersimpan."
}
```

#### Validate Numbers

```bash
POST http://localhost:8000/wa/validate
Content-Type: application/json

{
  "phone_numbers": [
    "081234567890",
    "082111222333",
    "085999888777"
  ]
}
```

Response:
```json
{
  "success": true,
  "results": [
    {
      "phone": "081234567890",
      "clean_phone": "6281234567890",
      "has_whatsapp": true,
      "is_business": true,
      "business_name": "Toko ABC",
      "status": "✓ WhatsApp Business - Toko ABC"
    },
    {
      "phone": "082111222333",
      "clean_phone": "6282111222333",
      "has_whatsapp": true,
      "is_business": false,
      "business_name": "",
      "status": "✓ WhatsApp Personal"
    },
    {
      "phone": "085999888777",
      "clean_phone": "6285999888777",
      "has_whatsapp": false,
      "is_business": false,
      "business_name": "",
      "status": "Nomor tidak terdaftar WhatsApp"
    }
  ],
  "summary": {
    "total": 3,
    "has_whatsapp": 2,
    "has_whatsapp_percent": 66.7,
    "is_business": 1,
    "is_business_percent": 33.3
  }
}
```

## Perbandingan Metode

| Aspek | Metode Lama (Open Chat) | Metode Baru (Query) |
|-------|------------------------|---------------------|
| Kecepatan | 10-15 detik/nomor | 1-2 detik/nomor |
| Reliability | Tergantung loading page | Langsung dari server |
| Deteksi Business | Ya (parsing HTML) | Ya (dari API internal) |
| Nama Bisnis | Ya (parsing HTML) | Ya (dari API internal) |
| Rate Limit | Ketat (perlu delay 5-10s) | Lebih longgar (1-2s) |
| Session | Tersimpan | Tersimpan |

## Kecepatan Estimasi

- **10 nomor**: ~20 detik (vs ~2 menit metode lama)
- **50 nomor**: ~1.5 menit (vs ~10 menit metode lama)
- **100 nomor**: ~3 menit (vs ~20 menit metode lama)
- **500 nomor**: ~15 menit (vs ~1.5 jam metode lama)

## Technical Details

### Store.QueryExist.queryExist

Fungsi ini adalah bagian dari WhatsApp Web internal API:

```javascript
window.Store.QueryExist.queryExist('6281234567890@c.us').then((result) => {
  console.log(result);
  // {
  //   wid: '6281234567890@c.us',
  //   status: 200,  // 200 = terdaftar, 404 = tidak terdaftar
  //   biz: true,    // true = business, false = personal
  //   vname: 'Toko ABC'  // nama bisnis (jika ada)
  // }
});
```

### Store Injection

Jika `window.Store` belum tersedia, script akan inject Store exposure code untuk mengakses internal API WhatsApp Web.

## Limitations

- Tetap butuh login WhatsApp Web (scan QR sekali)
- Rate limit: ~30-40 nomor/menit (lebih baik dari metode lama)
- Tidak bisa detect semua business account (tergantung setting pemilik)
- Butuh koneksi internet stabil
- Gunakan dengan bijak sesuai ToS WhatsApp

## Security & Privacy

- Session disimpan lokal di `wa_session/`
- Tidak ada data dikirim ke server lain
- Hanya akses WhatsApp Web resmi
- Menggunakan fungsi internal yang sudah ada di WhatsApp Web

## Troubleshooting

### Store not available

Jika muncul error "Store not available":
1. Tunggu beberapa detik sampai WhatsApp Web fully loaded
2. Script akan otomatis inject Store exposure code
3. Jika masih error, refresh browser dan coba lagi

### Query failed

Jika query gagal:
1. Cek koneksi internet
2. Pastikan sudah login WhatsApp Web
3. Coba logout dan login ulang
4. Hapus session: `rm -rf wa_session/`

### Rate limit

Jika terkena rate limit:
1. Kurangi kecepatan query (tambah delay)
2. Bagi nomor menjadi batch kecil
3. Tunggu beberapa menit sebelum lanjut

## License

Internal use only. Gunakan dengan bijak sesuai ToS WhatsApp.
