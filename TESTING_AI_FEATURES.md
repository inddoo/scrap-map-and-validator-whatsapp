# 🧪 Testing AI Features

## Pre-requisites

✅ Backend running (`python run.py`)
✅ Frontend running (`npm run dev`)
✅ Gemini API key configured in `.env`
✅ WhatsApp Web initialized and logged in

---

## Test 1: Backend AI Service

### Run Test Script
```bash
cd backend
python test_ai_integration.py
```

### Expected Output
```
============================================================
🤖 AI GEMINI INTEGRATION TEST
============================================================

✅ GEMINI_API_KEY found: AIzaSyXXXX...
✅ Gemini service initialized successfully

============================================================
TEST: AI Message Generation
============================================================

Template: Buatkan pesan promosi untuk {name}...
Data: {'phone': '628123456789', 'name': 'John Doe', ...}
Generating message...

------------------------------------------------------------
GENERATED MESSAGE:
------------------------------------------------------------
Halo Pak John Doe! 👋

Saya dari PT Digital Solutions ingin menawarkan...
[AI generated message]
------------------------------------------------------------

✅ Message generation successful!

[More tests...]

✅ ALL TESTS COMPLETED!
```

### If Tests Fail

**Error: "GEMINI_API_KEY not found"**
```bash
# Check .env file
cat .env | grep GEMINI_API_KEY

# If not found, add it
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

**Error: "Module not found: google.generativeai"**
```bash
pip install google-generativeai
```

**Error: "Rate limit exceeded"**
- Wait 1 minute
- Free tier: 60 requests/minute
- Reduce test frequency

---

## Test 2: API Endpoints

### Test Generate Messages Endpoint

```bash
curl -X POST http://localhost:8000/ai/generate-messages \
  -H "Content-Type: application/json" \
  -d '{
    "template": "Halo {name} dari {company}!",
    "csv_data": [
      {"phone": "628111", "name": "Alice", "company": "PT AAA"},
      {"phone": "628222", "name": "Bob", "company": "CV BBB"}
    ],
    "context": "Kami perusahaan IT"
  }'
```

### Expected Response
```json
{
  "success": true,
  "messages": [
    {
      "phone": "628111",
      "name": "Alice",
      "company": "PT AAA",
      "generated_message": "Halo Alice dari PT AAA! ..."
    },
    {
      "phone": "628222",
      "name": "Bob",
      "company": "CV BBB",
      "generated_message": "Halo Bob dari CV BBB! ..."
    }
  ]
}
```

### Test Auto Responder Endpoint

```bash
curl -X POST http://localhost:8000/ai/auto-responder \
  -H "Content-Type: application/json" \
  -d '{
    "incoming_message": "Halo, berapa harga website?",
    "sender_phone": "628123456789",
    "sender_data": {
      "name": "John",
      "company": "PT ABC"
    },
    "response_prompt": "Anda customer service yang ramah"
  }'
```

### Expected Response
```json
{
  "success": true,
  "response_message": "Halo John! Terima kasih sudah bertanya..."
}
```

---

## Test 3: Frontend Integration

### Step-by-Step Test

#### 1. Initialize WhatsApp
- Go to "WA Validator" tab
- Click "Inisialisasi WhatsApp"
- Scan QR code
- Wait for "WhatsApp siap digunakan!"

#### 2. Go to WA Sender Tab
- Click "📨 WA Auto Sender" tab
- Should see the interface

#### 3. Upload Test CSV
- Use `test_ai_sender.csv`
- Click "📤 Upload CSV"
- Should see: "✅ CSV Berhasil Dimuat! Berhasil memuat 5 nomor"

#### 4. Verify CSV Preview
- Should see table with all columns
- Should see 5 rows
- Each row should have delete button

#### 5. Enable AI
- Check ✅ "Gunakan AI untuk Generate Pesan Personal"
- AI section should appear

#### 6. Write Template
```
Buatkan pesan untuk {name} dari {company}.
Tawarkan layanan IT dengan diskon 20%.
Profesional tapi ramah.
```

#### 7. Add Context (Optional)
```
Kami PT Digital Solutions, fokus automation software.
```

#### 8. Generate AI Messages
- Click "🤖 Generate Pesan AI"
- Should see loading spinner
- Wait 10-30 seconds
- Should see: "🤖 AI Berhasil Generate Pesan!"

#### 9. Review Generated Messages
- Should see preview of 3 messages
- Each message should be different
- Each message should include name from CSV

#### 10. Enable Auto Responder (Optional)
- Check ✅ "Aktifkan Auto Responder AI"
- Write prompt:
```
Anda customer service yang ramah.
Jawab pertanyaan dengan informatif.
```

#### 11. Send Messages
- Click "🤖 Kirim Pesan AI (5 nomor)"
- Should see loading
- Monitor console for progress
- Should see success modal

---

## Test 4: Error Handling

### Test Invalid API Key
1. Set wrong API key in `.env`
2. Try to generate messages
3. Should see error: "Gagal generate pesan AI"

### Test Empty CSV
1. Upload CSV with no data
2. Should see: "CSV Kosong"

### Test CSV Without Phone Column
1. Upload CSV without "phone" column
2. Should see: "CSV harus memiliki kolom 'phone'!"

### Test Empty Template
1. Don't write template
2. Try to generate
3. Should see: "Template Kosong"

### Test WhatsApp Not Initialized
1. Don't initialize WhatsApp
2. Try to send messages
3. Should see: "WhatsApp Belum Diinisialisasi"

---

## Test 5: Performance Test

### Small Batch (5 contacts)
- Upload 5 contacts
- Generate messages
- Expected time: 10-30 seconds
- Send messages
- Expected time: 1-2 minutes (with 5-10s delay)

### Medium Batch (20 contacts)
- Upload 20 contacts
- Generate messages
- Expected time: 30-60 seconds
- Send messages
- Expected time: 5-10 minutes

### Large Batch (50 contacts)
- Upload 50 contacts
- Generate messages
- Expected time: 1-2 minutes
- Send messages
- Expected time: 10-20 minutes

**Note:** Don't test with more than 50 contacts to avoid WhatsApp ban!

---

## Test 6: Message Quality Test

### Test Different Templates

#### Template 1: Simple
```
Halo {name}! Kami tawarkan diskon 20% untuk {company}.
```
**Expected:** Short, direct message

#### Template 2: Detailed
```
Buatkan pesan sales untuk {name} dari {company}.
Jelaskan benefit produk kami.
Ajak untuk meeting.
Gunakan emoji.
Max 3 paragraf.
```
**Expected:** Longer, more detailed message with emoji

#### Template 3: Formal
```
Buatkan surat formal untuk {name} ({position}) dari {company}.
Undang ke event bisnis.
Bahasa sangat formal dan profesional.
```
**Expected:** Very formal, professional tone

### Verify Message Quality
- ✅ Includes name from CSV
- ✅ Includes company from CSV
- ✅ Follows template instructions
- ✅ Appropriate tone
- ✅ Proper grammar
- ✅ Relevant emoji (if requested)
- ✅ Reasonable length

---

## Test 7: Auto Responder Test

### Setup
1. Send AI messages with auto responder enabled
2. Reply to one of the messages from your phone
3. Check if AI responds

### Test Scenarios

#### Scenario 1: Price Inquiry
**You send:** "Berapa harga untuk website?"
**AI should:** Explain pricing or offer to discuss

#### Scenario 2: Feature Question
**You send:** "Apa saja fitur yang tersedia?"
**AI should:** List features or offer demo

#### Scenario 3: Rejection
**You send:** "Tidak tertarik, terima kasih"
**AI should:** Politely acknowledge and offer future contact

---

## Troubleshooting

### Issue: Messages Not Personal
**Solution:**
- Make template more specific
- Add more context
- Include more CSV fields in template

### Issue: AI Too Slow
**Solution:**
- Reduce batch size
- Check internet connection
- Verify API key is valid

### Issue: Messages Too Long
**Solution:**
- Add "Max 2-3 paragraf" to template
- Be more specific about length

### Issue: Wrong Tone
**Solution:**
- Specify tone clearly: "profesional", "ramah", "formal"
- Give examples in template

### Issue: Auto Responder Not Working
**Solution:**
- Check WhatsApp Web still logged in
- Verify prompt is clear
- Check console for errors

---

## Success Criteria

✅ All backend tests pass
✅ API endpoints return correct responses
✅ CSV upload works correctly
✅ AI generates unique messages for each contact
✅ Messages include CSV data correctly
✅ Messages follow template instructions
✅ Send functionality works
✅ Auto responder responds appropriately
✅ Error handling works correctly
✅ Performance is acceptable

---

## Reporting Issues

If you find bugs:
1. Note the exact steps to reproduce
2. Check console for error messages
3. Check backend logs
4. Include CSV sample (anonymized)
5. Include template used
6. Include error message

---

**Happy Testing! 🧪**
