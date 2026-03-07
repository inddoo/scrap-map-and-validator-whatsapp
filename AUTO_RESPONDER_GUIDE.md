# 🤖 Auto Responder Guide

## Overview

Auto Responder adalah fitur yang secara otomatis membalas pesan masuk dari kontak menggunakan AI (Gemini).

## How It Works

### Flow
1. **Send Message** - Kirim pesan AI-generated ke kontak
2. **Monitor** - Monitor chat selama 10 detik untuk reply
3. **Detect Reply** - Detect jika ada pesan masuk dari kontak
4. **Generate Response** - AI generate balasan berdasarkan prompt
5. **Send Response** - Kirim balasan otomatis

### Technical Details

```python
# Monitor for 10 seconds, check every 2 seconds
monitor_duration = 10  # seconds
check_interval = 2     # seconds

for i in range(5):  # 10/2 = 5 checks
    time.sleep(2)
    incoming_message = _check_for_new_message()
    
    if incoming_message:
        # Generate AI response
        ai_response = gemini.generate_auto_response(
            incoming_message=incoming_message,
            sender_data=contact_data,
            response_prompt=auto_responder_prompt
        )
        
        # Send response
        _send_auto_response(ai_response)
        break
```

## Features

### 1. Message Detection
- Detects incoming messages from contact
- Uses multiple selectors for reliability
- Gets most recent message

### 2. AI Response Generation
- Uses Gemini AI to generate contextual response
- Considers contact data (name, company, etc.)
- Follows custom prompt instructions
- Professional and friendly tone

### 3. Auto Send
- Automatically sends generated response
- Preserves line breaks
- Sanitizes message (no emojis/BMP chars)
- Proper timing and delays

## Usage

### In Web App

1. **Enable Auto Responder**
   - Toggle "Auto Responder" switch
   - Input custom prompt (optional)

2. **Set Prompt** (Optional)
   ```
   Anda adalah customer service hotel yang ramah.
   Jawab pertanyaan dengan informatif dan profesional.
   Tawarkan bantuan lebih lanjut jika diperlukan.
   ```

3. **Send Messages**
   - Generate AI messages
   - Click "Kirim Pesan"
   - Auto responder will monitor each chat

### Default Prompt

If no custom prompt provided:
```
Jawab dengan ramah dan profesional
```

## Configuration

### Monitor Duration
```python
monitor_duration = 10  # seconds to wait for reply
```

Adjust in `wa_sender.py` line ~447

### Check Interval
```python
check_interval = 2  # check every 2 seconds
```

Adjust in `wa_sender.py` line ~448

## Response Status

### Possible Statuses

1. **"Response sent"** ✅
   - Reply detected and response sent successfully

2. **"No reply received"** ℹ️
   - No reply within 10 seconds
   - Normal, not an error

3. **"Error: [message]"** ❌
   - Error during detection or sending
   - Check logs for details

## Example Scenario

### Scenario 1: Hotel Inquiry

**Your Message (AI-generated):**
```
Selamat siang Hotel d'Season Premiere Jepara,

Kami sangat menggagumi reputasi hotel Anda sebagai salah satu 
akomodasi bintang 4 terbaik yang berlokasi di Jl. Pantai Teluk 
Awur No.1 melalui promosi website indonesianaprima.online...
```

**Contact Reply:**
```
Terima kasih. Apa yang bisa kami bantu?
```

**Auto Response (AI-generated):**
```
Terima kasih atas responnya.

Kami tertarik untuk mendiskusikan peluang kerjasama dalam 
promosi digital hotel Anda. Apakah ada waktu yang tepat 
untuk kami menghubungi Anda lebih lanjut?

Terima kasih.
```

### Scenario 2: No Reply

**Your Message:** Sent ✅
**Monitor:** 10 seconds...
**Status:** "No reply received"
**Action:** Continue to next contact

## Limitations

### 1. Timing
- Only monitors for 10 seconds after sending
- If reply comes after 10s, won't be detected
- Trade-off between speed and coverage

### 2. Message Detection
- May not detect all message types (images, voice, etc.)
- Only detects text messages
- Relies on WhatsApp Web selectors (may change)

### 3. Context
- No conversation history tracking (yet)
- Each response is independent
- Can be improved with history tracking

## Best Practices

### 1. Custom Prompts
Write clear, specific prompts:

✅ **Good:**
```
Anda adalah sales representative PT Digital Solutions.
Jawab pertanyaan tentang layanan IT kami.
Jika ditanya harga, arahkan untuk konsultasi gratis.
Selalu sopan dan profesional.
```

❌ **Bad:**
```
Jawab aja
```

### 2. Monitor Duration
- 10 seconds is reasonable for most cases
- Increase if contacts typically reply slower
- Decrease for faster campaigns

### 3. Testing
- Test with 1-2 contacts first
- Verify responses are appropriate
- Adjust prompt if needed

## Troubleshooting

### Auto Responder Not Working

**Check 1: Is it enabled?**
```python
auto_responder_enabled: True
```

**Check 2: Is Gemini service available?**
```python
gemini_service = get_gemini_service()
# Should not be None
```

**Check 3: Check console logs**
```
🤖 Auto-responder active, monitoring for replies...
📨 Incoming message detected: ...
🤖 AI Response: ...
✅ Auto-response sent successfully
```

### No Reply Detected

**Possible Causes:**
1. Contact didn't reply within 10s
2. Reply is not text (image, voice, etc.)
3. WhatsApp Web selector changed

**Solution:**
- Increase monitor_duration
- Check console for errors
- Verify message detection selectors

### Response Not Sent

**Possible Causes:**
1. Input box not found
2. Message sanitization removed all content
3. WhatsApp Web error

**Solution:**
- Check console logs
- Verify WhatsApp Web is responsive
- Test manual sending first

## Advanced Configuration

### Custom Monitor Duration Per Contact

```python
# In send_ai_personalized_messages
monitor_duration = contact_data.get('monitor_duration', 10)
```

### Conversation History Tracking

```python
# Store conversation history
conversation_history = []

# Add to history
conversation_history.append({
    'role': 'bot',
    'message': sent_message
})

conversation_history.append({
    'role': 'user',
    'message': incoming_message
})

# Pass to AI
ai_response = gemini.generate_auto_response(
    incoming_message=incoming_message,
    sender_data=data,
    response_prompt=auto_responder_prompt,
    conversation_history=conversation_history  # Include history
)
```

## Files Modified

- `backend/wa_validator/wa_sender.py` - Auto responder implementation
  - `send_ai_personalized_messages()` - Main logic
  - `_check_for_new_message()` - Message detection (new)
  - `_send_auto_response()` - Send response (new)

## Summary

✅ **Implemented:** Full auto responder with AI
✅ **Features:** Detection, generation, sending
✅ **Configurable:** Custom prompts and timing
✅ **Status tracking:** Know what happened
✅ **Error handling:** Graceful failures

---

**Status:** IMPLEMENTED ✅
**Date:** March 5, 2026
**Ready:** For testing and production use
