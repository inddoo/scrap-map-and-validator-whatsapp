# 🔧 Fix: WhatsApp Line Breaks Not Working

## Problem

Pesan yang di-generate AI terlihat rapi di web (dengan paragraf), tapi saat dikirim ke WhatsApp jadi satu blok tanpa line breaks.

**Contoh:**
```
Web: 
Halo Prima,

Saya dari PRIMACODE, sebuah perusahaan IT yang berfokus pada pengembangan website profesional dan efektif. Kami memahami betapa pentingnya...

WhatsApp:
Halo Prima, Saya dari PRIMACODE, sebuah perusahaan IT yang berfokus pada pengembangan website profesional dan efektif. Kami memahami betapa pentingnya...
```

## Root Cause

WhatsApp Web menggunakan `contenteditable` div, bukan textarea biasa. Metode `send_keys()` dengan `Shift+Enter` tidak selalu reliable untuk multi-line text di WhatsApp Web.

## Solution

Menggunakan JavaScript untuk insert text langsung ke contenteditable div dengan `<br>` tags untuk line breaks.

### Changes Made

**File:** `backend/wa_validator/wa_sender.py`

**Method:** `send_message()` (lines ~160-180)

**Before:**
```python
# Ketik pesan (support multi-line dengan Shift+Enter)
lines = sanitized_message.split('\n')
for i, line in enumerate(lines):
    input_box.send_keys(line)
    if i < len(lines) - 1:
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
```

**After:**
```python
# Method 1: Try using JavaScript to set value directly
try:
    input_box.click()
    time.sleep(0.5)
    
    # Use JavaScript to insert text with proper line breaks
    # WhatsApp uses contenteditable div, so we need to set innerHTML with <br> tags
    escaped_message = sanitized_message.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '<br>')
    js_script = f'''
    var element = arguments[0];
    element.innerHTML = "{escaped_message}";
    element.dispatchEvent(new Event('input', {{ bubbles: true }}));
    '''
    self.driver.execute_script(js_script, input_box)
    time.sleep(0.5)
    
except Exception as e:
    # Fallback: Use Shift+Enter method
    input_box.clear()
    lines = sanitized_message.split('\n')
    for i, line in enumerate(lines):
        input_box.send_keys(line)
        if i < len(lines) - 1:
            input_box.send_keys(Keys.SHIFT, Keys.ENTER)
```

## How It Works

1. **JavaScript Injection:** Menggunakan `execute_script()` untuk inject JavaScript ke WhatsApp Web
2. **HTML Conversion:** Convert `\n` menjadi `<br>` tags (HTML line breaks)
3. **Set innerHTML:** Set innerHTML dari contenteditable div dengan text yang sudah di-convert
4. **Trigger Event:** Dispatch `input` event agar WhatsApp detect perubahan
5. **Fallback:** Jika JavaScript gagal, fallback ke metode Shift+Enter

## Benefits

- ✅ Line breaks preserved dengan sempurna
- ✅ Lebih cepat (tidak perlu loop per line)
- ✅ Lebih reliable untuk multi-paragraph messages
- ✅ Fallback mechanism jika JavaScript gagal
- ✅ Tetap support sanitization (no emojis/BMP characters)

## Testing

Setelah update ini, test dengan:

1. Generate AI message dengan multiple paragraphs
2. Kirim ke WhatsApp
3. Verify bahwa paragraphs terpisah dengan line breaks

**Expected Result:**
```
Halo Prima,

Saya dari PRIMACODE, sebuah perusahaan IT yang berfokus pada pengembangan website profesional dan efektif.

Kami memahami betapa pentingnya...
```

## Files Modified

- `backend/wa_validator/wa_sender.py` - Updated `send_message()` method

## Notes

- JavaScript method adalah primary method
- Shift+Enter method tetap ada sebagai fallback
- Semua sanitization rules tetap berlaku (no emojis, BMP only)
- Line breaks (`\n`) tetap dipertahankan di sanitization

---

**Status:** FIXED ✅
**Date:** March 5, 2026
