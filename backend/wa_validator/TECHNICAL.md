# Technical Documentation - WhatsApp Query Method

## Cara Kerja Detail

### 1. Arsitektur Sistem

```
User Input (Nomor Telepon)
    ↓
FastAPI Backend
    ↓
WAQueryChecker (Python + Selenium)
    ↓
Chrome Browser (WhatsApp Web)
    ↓
window.Store.QueryExist.queryExist()
    ↓
WhatsApp Server (Query Internal)
    ↓
Response (Status, Business Info)
    ↓
Parse & Return ke User
```

### 2. WhatsApp Web Internal API

WhatsApp Web memiliki object `window.Store` yang berisi berbagai fungsi internal:

```javascript
window.Store = {
  Chat: {...},           // Manage chats
  Msg: {...},            // Manage messages
  Contact: {...},        // Manage contacts
  QueryExist: {...},     // Query nomor existence ← YANG KITA PAKAI
  Wap: {...},            // WhatsApp Protocol
  // ... dan banyak lagi
}
```

### 3. Store.QueryExist.queryExist()

Fungsi ini digunakan WhatsApp Web untuk mengecek apakah nomor valid sebelum membuka chat:

```javascript
// Format nomor: 62xxx@c.us
window.Store.QueryExist.queryExist('6281234567890@c.us')
  .then((result) => {
    console.log(result);
  });
```

Response structure:
```javascript
{
  wid: '6281234567890@c.us',  // WhatsApp ID
  status: 200,                 // 200 = exists, 404 = not found
  biz: true,                   // true = business, false = personal
  vname: 'Toko ABC',          // Verified name (business name)
  notify: 'John Doe'          // Display name
}
```

### 4. Store Injection

Jika `window.Store` belum tersedia (karena WhatsApp Web belum fully loaded), kita inject script untuk expose Store:

```javascript
// Cari webpack modules
if (typeof webpackChunkwhatsapp_web_client !== 'undefined') {
  webpackChunkwhatsapp_web_client.push([
    ['parasite'],
    {},
    function(e) {
      // Extract modules
      let modules = [];
      for (let idx in e.m) {
        modules.push(e(idx));
      }
      
      // Find Store object
      getStore(modules);
    }
  ]);
}
```

Script ini:
1. Hook ke webpack chunk loader WhatsApp Web
2. Extract semua modules yang di-load
3. Cari module yang berisi Store object
4. Expose ke `window.Store`

### 5. Flow Validasi

#### Step 1: Setup Driver
```python
options = Options()
options.add_argument(f'--user-data-dir={user_data_dir}')
driver = webdriver.Chrome(options=options)
```

#### Step 2: Login WhatsApp Web
```python
driver.get('https://web.whatsapp.com')
# Wait for chat list (indicator sudah login)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Chat list"]'))
)
```

#### Step 3: Wait for Store Ready
```python
# Check if Store available
result = driver.execute_script("""
    return typeof window.Store !== 'undefined' && 
           typeof window.Store.QueryExist !== 'undefined';
""")

# If not, inject Store
if not result:
    inject_store_script()
```

#### Step 4: Query Number
```python
wid = f"{clean_phone}@c.us"

query_script = f"""
return new Promise((resolve) => {{
    window.Store.QueryExist.queryExist('{wid}').then((result) => {{
        resolve({{
            success: true,
            status: result.status,
            isBusiness: result.biz || false,
            businessName: result.vname || ''
        }});
    }}).catch((err) => {{
        resolve({{ error: err.toString() }});
    }});
}});
"""

result = driver.execute_script(query_script)
```

#### Step 5: Parse Result
```python
if result.get('status') == 200:
    has_whatsapp = True
    is_business = result.get('isBusiness', False)
    business_name = result.get('businessName', '')
else:
    has_whatsapp = False
```

### 6. Normalisasi Nomor

```python
def clean_phone_number(phone: str) -> str:
    # Remove non-digit
    phone = re.sub(r'\D', '', str(phone))
    
    # Add country code
    if not phone.startswith('62'):
        if phone.startswith('0'):
            phone = '62' + phone[1:]  # 0812 → 62812
        else:
            phone = '62' + phone       # 812 → 62812
    
    return phone
```

Input → Output:
- `081234567890` → `6281234567890`
- `+62 812-3456-7890` → `6281234567890`
- `0274123456` → `62274123456`

### 7. Rate Limiting

WhatsApp memiliki rate limit untuk query:

```python
# Delay antar query
time.sleep(1.5)  # 1.5 detik antar nomor

# Estimasi safe rate:
# - 30-40 nomor/menit
# - 500-600 nomor/jam
```

Jika terkena rate limit:
- Response akan lambat
- Bisa dapat error 429 (Too Many Requests)
- Solusi: Tambah delay atau bagi batch

### 8. Session Management

Session WhatsApp Web disimpan di Chrome user data directory:

```
wa_session/
├── Default/
│   ├── Cookies
│   ├── Local Storage/
│   └── IndexedDB/
└── ...
```

Benefit:
- Login sekali, bisa dipakai berkali-kali
- Tidak perlu scan QR setiap kali
- Session bertahan sampai logout manual

### 9. Error Handling

```python
try:
    result = driver.execute_script(query_script)
    
    if result.get('error'):
        # Handle error
        if 'Store not available' in result['error']:
            # Inject Store
            inject_store_script()
            # Retry
        elif 'timeout' in result['error']:
            # Retry dengan delay
            time.sleep(5)
        else:
            # Log error
            
except Exception as e:
    # Handle exception
    print(f"Error: {e}")
```

### 10. Security Considerations

#### Aman:
- ✅ Session lokal (tidak dikirim ke server lain)
- ✅ Hanya akses WhatsApp Web resmi
- ✅ Menggunakan fungsi yang sudah ada di WhatsApp Web

#### Risiko:
- ⚠️ Melanggar ToS WhatsApp (unofficial usage)
- ⚠️ Akun bisa di-ban jika abuse
- ⚠️ Rate limit ketat

#### Best Practices:
- Gunakan delay yang cukup (1-2 detik)
- Jangan query terlalu banyak sekaligus
- Gunakan untuk internal use only
- Jangan jual sebagai service

### 11. Debugging

Enable debug mode:

```python
# Save screenshot
driver.save_screenshot('debug.png')

# Save page source
with open('debug.html', 'w') as f:
    f.write(driver.page_source)

# Check Store availability
store_check = driver.execute_script("""
    return {
        hasStore: typeof window.Store !== 'undefined',
        hasQueryExist: typeof window.Store?.QueryExist !== 'undefined',
        storeKeys: window.Store ? Object.keys(window.Store) : []
    };
""")
print(store_check)
```

### 12. Performance Optimization

#### Parallel Processing (Future Enhancement):

```python
from concurrent.futures import ThreadPoolExecutor

def validate_batch(numbers, batch_size=10):
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Split into batches
        batches = [numbers[i:i+batch_size] 
                   for i in range(0, len(numbers), batch_size)]
        
        # Process batches in parallel
        results = list(executor.map(validate_numbers, batches))
    
    return results
```

Catatan: Hati-hati dengan rate limit!

### 13. Alternative Methods

Jika Query method tidak work:

1. **Open Chat Method** (wa_checker_fixed.py)
   - Buka chat satu per satu
   - Cek keberadaan input box
   - Lebih lambat tapi lebih reliable

2. **API Method** (wa_checker_api.py)
   - Hanya validasi format
   - Tidak bisa confirm existence
   - Tidak perlu browser

3. **Official API** (Meta Business API)
   - Perlu token berbayar
   - Rate limit lebih tinggi
   - Lebih reliable dan legal

## Kesimpulan

Query Method adalah sweet spot antara:
- Kecepatan (1-2s/nomor)
- Akurasi (langsung dari server)
- Kemudahan (tidak perlu API token)

Tapi ingat: Ini unofficial method, gunakan dengan bijak!
