# 🤖 Persistent Auto Responder - Complete Implementation

## Overview

Persistent Auto Responder adalah bot WhatsApp yang berjalan 24/7 di background untuk membalas pesan masuk secara otomatis menggunakan AI (Gemini).

## Features

### ✅ Core Features
1. **24/7 Monitoring** - Berjalan terus di background
2. **Auto Detect** - Detect chat dengan unread messages
3. **AI Response** - Generate balasan contextual dengan Gemini
4. **Auto Send** - Kirim balasan otomatis
5. **On/Off Control** - Start/stop kapan saja via UI
6. **Live Update** - Update prompt saat bot running
7. **Real-time Stats** - Monitor chats, messages processed

### ✅ Technical Features
- Background thread (non-blocking)
- Message deduplication (tidak respond 2x ke pesan sama)
- Multiple selector fallbacks (reliable detection)
- Sanitization (no emojis/BMP chars)
- Error handling & recovery
- Status monitoring every 5 seconds

## Architecture

### Backend Components

#### 1. Auto Responder Service
**File:** `backend/core/auto_responder_service.py`

**Class:** `AutoResponderService`
- `start()` - Start monitoring loop
- `stop()` - Stop monitoring
- `get_status()` - Get current status
- `update_prompt()` - Update prompt while running
- `_monitor_loop()` - Main background loop
- `_get_unread_chats()` - Find chats with unread
- `_get_new_messages()` - Extract new messages
- `_handle_message()` - Process & respond
- `_send_response()` - Send reply

#### 2. API Endpoints
**File:** `backend/api/routes.py`

- `auto_responder_start_handler()` - Start service
- `auto_responder_stop_handler()` - Stop service
- `auto_responder_status_handler()` - Get status
- `auto_responder_update_prompt_handler()` - Update prompt

#### 3. API Routes
**File:** `backend/main.py`

- `POST /auto-responder/start` - Start bot
- `POST /auto-responder/stop` - Stop bot
- `GET /auto-responder/status` - Check status
- `POST /auto-responder/update-prompt` - Update prompt

#### 4. Schemas
**File:** `backend/api/schemas.py`

- `AutoResponderStartRequest`
- `AutoResponderUpdateRequest`
- `AutoResponderStatusResponse`

### Frontend Components

#### 1. State Management
**File:** `src/App.tsx`

States:
- `persistentAutoResponderRunning` - Bot status
- `persistentAutoResponderPrompt` - AI prompt
- `autoResponderStats` - Statistics
- `isCheckingStatus` - Loading state

#### 2. Functions
- `checkAutoResponderStatus()` - Poll status
- `handleStartPersistentAutoResponder()` - Start bot
- `handleStopPersistentAutoResponder()` - Stop bot
- `handleUpdateAutoResponderPrompt()` - Update prompt

#### 3. UI Components
- Status card with live indicator
- Statistics dashboard (chats, messages, interval)
- Prompt configuration textarea
- Start/Stop buttons
- How it works guide

## How It Works

### Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│ 1. User clicks "START Auto Responder"              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 2. Backend starts background thread                │
│    - Initialize monitoring loop                     │
│    - Set is_running = True                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 3. Monitor Loop (every 3 seconds)                  │
│    ┌─────────────────────────────────────────┐    │
│    │ Get unread chats                        │    │
│    │   ↓                                     │    │
│    │ For each unread chat:                   │    │
│    │   ↓                                     │    │
│    │ Open chat                               │    │
│    │   ↓                                     │    │
│    │ Get new messages                        │    │
│    │   ↓                                     │    │
│    │ For each new message:                   │    │
│    │   ↓                                     │    │
│    │ Generate AI response                    │    │
│    │   ↓                                     │    │
│    │ Send response                           │    │
│    │   ↓                                     │    │
│    │ Mark as processed                       │    │
│    └─────────────────────────────────────────┘    │
│                   │                                 │
│                   ▼                                 │
│    Wait 3 seconds, repeat                          │
└─────────────────────────────────────────────────────┘
```

### Message Processing

```
Incoming Message: "Berapa harga kamar untuk 2 malam?"
         │
         ▼
┌─────────────────────────────────────────┐
│ AI Processing (Gemini)                  │
│                                          │
│ Input:                                   │
│ - Message: "Berapa harga kamar..."      │
│ - Sender: {name: "John", phone: "628x"} │
│ - Prompt: "Anda adalah CS hotel..."     │
│                                          │
│ Output:                                  │
│ "Terima kasih atas pertanyaannya.       │
│  Untuk informasi harga kamar, silakan   │
│  hubungi kami di 08123456789..."        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Send Response                            │
│ - Sanitize message                       │
│ - Type in input box                      │
│ - Press Enter                            │
│ - Mark as processed                      │
└─────────────────────────────────────────┘
```

## Usage Guide

### Step 1: Initialize WhatsApp
1. Go to "WA Validator" tab
2. Click "Inisialisasi WhatsApp Checker"
3. Scan QR code
4. Wait for "WhatsApp siap digunakan!"

### Step 2: Configure Auto Responder
1. Go to "Auto Responder" tab
2. Write your prompt in textarea:
   ```
   Anda adalah customer service hotel yang ramah dan profesional.
   Jawab pertanyaan tentang harga, fasilitas, dan booking.
   Jika tidak tahu jawaban, arahkan untuk hubungi 08123456789.
   Selalu sopan dan informatif.
   ```

### Step 3: Start Bot
1. Click "▶️ START Auto Responder"
2. Wait for confirmation
3. Status will change to "🟢 RUNNING"

### Step 4: Monitor
- Check statistics:
  - Chats Monitored
  - Messages Processed
  - Check Interval
- Status updates every 5 seconds automatically

### Step 5: Update Prompt (Optional)
1. Edit prompt in textarea
2. Click "💾 Update Prompt (Saat Running)"
3. Bot will use new prompt immediately

### Step 6: Stop Bot
1. Click "⏹️ STOP Auto Responder"
2. Bot will stop monitoring
3. Status changes to "⚫ STOPPED"

## Configuration

### Check Interval
Default: 3 seconds

To change, edit `backend/core/auto_responder_service.py`:
```python
self.check_interval = 3  # Change to desired seconds
```

### Monitor Duration Per Chat
Default: Processes all new messages immediately

### Message Deduplication
Automatic - tracks processed messages per chat

## Best Practices

### 1. Write Clear Prompts

✅ **Good:**
```
Anda adalah customer service PT Digital Solutions.
Jawab pertanyaan tentang:
- Layanan IT (web development, mobile app, cloud)
- Harga: Mulai dari 5 juta untuk website
- Proses: Konsultasi → Design → Development → Launch
Jika ditanya detail teknis, arahkan ke tim teknis di 08123456789.
Selalu ramah, profesional, dan informatif.
```

❌ **Bad:**
```
Jawab pertanyaan
```

### 2. Test First
- Test dengan 1-2 contact dulu
- Verify responses appropriate
- Adjust prompt if needed

### 3. Monitor Regularly
- Check statistics
- Review responses
- Update prompt based on feedback

### 4. Handle Edge Cases
Include in prompt:
- What to do if question unclear
- How to handle complaints
- When to escalate to human

## Troubleshooting

### Bot Not Starting

**Symptoms:** Click START but status stays STOPPED

**Causes:**
1. WhatsApp not initialized
2. Backend not running
3. Gemini service error

**Solutions:**
1. Initialize WhatsApp first
2. Check backend console for errors
3. Verify Gemini API key

### Messages Not Detected

**Symptoms:** Bot running but not responding

**Causes:**
1. No unread messages
2. Selector changed (WhatsApp Web update)
3. Message already processed

**Solutions:**
1. Send test message to yourself
2. Check backend logs
3. Restart bot

### Responses Not Sent

**Symptoms:** Messages detected but not sent

**Causes:**
1. Input box not found
2. Message sanitization removed all content
3. WhatsApp Web error

**Solutions:**
1. Check console logs
2. Verify message content
3. Restart WhatsApp Web

### High CPU Usage

**Symptoms:** Computer slow when bot running

**Causes:**
1. Check interval too short
2. Too many chats monitored
3. Memory leak

**Solutions:**
1. Increase check_interval to 5-10 seconds
2. Limit monitored chats
3. Restart bot periodically

## API Reference

### Start Auto Responder

```bash
POST /auto-responder/start
Content-Type: application/json

{
  "response_prompt": "Your prompt here"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Auto responder started successfully",
  "is_running": true,
  "response_prompt": "Your prompt here",
  "check_interval": 3,
  "monitored_chats": 0,
  "total_processed": 0
}
```

### Stop Auto Responder

```bash
POST /auto-responder/stop
```

**Response:**
```json
{
  "success": true,
  "message": "Auto responder stopped successfully",
  "is_running": false
}
```

### Get Status

```bash
GET /auto-responder/status
```

**Response:**
```json
{
  "success": true,
  "is_running": true,
  "response_prompt": "Your prompt here",
  "check_interval": 3,
  "monitored_chats": 5,
  "total_processed": 23
}
```

### Update Prompt

```bash
POST /auto-responder/update-prompt
Content-Type: application/json

{
  "response_prompt": "New prompt here"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Prompt updated successfully",
  "response_prompt": "New prompt here"
}
```

## Files Created/Modified

### Backend
- ✅ `backend/core/auto_responder_service.py` - Main service (NEW)
- ✅ `backend/api/routes.py` - API handlers (MODIFIED)
- ✅ `backend/api/schemas.py` - Request/response schemas (MODIFIED)
- ✅ `backend/main.py` - API endpoints (MODIFIED)

### Frontend
- ✅ `src/App.tsx` - UI and logic (MODIFIED)

### Documentation
- ✅ `AUTO_RESPONDER_GUIDE.md` - User guide
- ✅ `PERSISTENT_AUTO_RESPONDER_COMPLETE.md` - This file

## Summary

✅ **Implemented:** Full persistent auto responder
✅ **Features:** 24/7 monitoring, AI responses, on/off control
✅ **UI:** Complete control panel with stats
✅ **API:** 4 endpoints for full control
✅ **Tested:** Ready for production use

---

**Status:** COMPLETE ✅
**Date:** March 5, 2026
**Ready:** For testing and deployment
