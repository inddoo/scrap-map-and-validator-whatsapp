# Format Input Nomor Telepon

## Cara Input yang Benar

User hanya perlu input **angka setelah +62** saja.

### ✅ Format yang Benar

```
81234567890
85999888777
274123456
```

Sistem akan otomatis menambahkan `62` di depan:
- `81234567890` → `6281234567890`
- `85999888777` → `6285999888777`
- `274123456` → `62274123456`

### ⚠️ Format yang Juga Diterima (Tapi Tidak Perlu)

Jika user input dengan format lain, sistem akan otomatis clean:

```
081234567890    → 6281234567890 (0 dihapus otomatis)
+62 812-345-678 → 6281234567890 (karakter non-digit dihapus)
62812345678     → 6281234567890 (sudah ada 62, tidak ditambah lagi)
```

## Contoh Penggunaan

### API Request

```json
{
  "phone_numbers": [
    "81234567890",
    "85999888777",
    "274123456"
  ]
}
```

### CSV File

```csv
name,phone,address
Restoran A,81234567890,Jl. Sudirman
Cafe B,85999888777,Jl. Merdeka
Hotel C,274123456,Jl. Malioboro
```

### Test Script

```bash
python test_wa_validator.py
```

Input:
```
81234567890, 85999888777, 274123456
```

## Jenis Nomor yang Didukung

### Nomor HP (Mobile)

Format: `8xxxxxxxxxx` (dimulai dengan 8)

Contoh:
- `81234567890` → Telkomsel, XL, Indosat
- `85999888777` → Smartfren, Three
- `89876543210` → Operator lain

### Nomor Telepon Rumah (Landline)

Format: `[kode area]xxxxxxx`

Contoh:
- `274123456` → Yogyakarta (0274)
- `21123456` → Jakarta (021)
- `31123456` → Surabaya (031)

## Validasi Format

Sistem akan validasi:
1. Hapus semua karakter non-digit
2. Hapus leading 0 jika ada
3. Tambah 62 di depan jika belum ada
4. Cek panjang nomor (minimal 9 digit, maksimal 15 digit)

## Tips

1. **Jangan pakai 0 di depan** - Langsung mulai dari 8 untuk HP
2. **Jangan pakai +62** - Sistem sudah otomatis tambahkan
3. **Format bebas** - Bisa pakai spasi, dash, atau tanpa apa-apa
4. **Batch input** - Pisahkan dengan koma untuk multiple nomor

## Error Handling

Jika nomor tidak valid:
- Terlalu pendek: `Error: Nomor terlalu pendek`
- Terlalu panjang: `Error: Nomor terlalu panjang`
- Format salah: `Error: Format nomor tidak valid`
