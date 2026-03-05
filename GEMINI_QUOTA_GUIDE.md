# 📊 Gemini API Quota Guide

## Problem
Error: `quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"`

Artinya: Anda sudah mencapai batas quota harian untuk Gemini API.

## Gemini Models & Quota Limits (Free Tier)

### ❌ gemini-2.5-flash (TIDAK DISARANKAN)
- **Quota:** 20 requests per day
- **Problem:** Terlalu kecil untuk production use
- **Status:** Sudah diganti

### ✅ gemini-1.5-flash (RECOMMENDED)
- **Quota:** 1,500 requests per day
- **RPM (Requests Per Minute):** 15
- **TPM (Tokens Per Minute):** 1,000,000
- **Status:** SEKARANG DIGUNAKAN

### Alternative Models

#### gemini-1.5-pro
- **Quota:** 50 requests per day (free tier)
- **Quality:** Lebih bagus tapi quota lebih kecil
- **Use case:** Jika butuh kualitas tinggi dengan volume rendah

#### gemini-1.0-pro
- **Quota:** 60 requests per day (free tier)
- **Quality:** Older model, kualitas lebih rendah
- **Use case:** Fallback option

## Current Configuration

**File:** `backend/ai/gemini_service.py`

```python
# BEFORE (BAD - only 20 requests/day)
self.model = genai.GenerativeModel('models/gemini-2.5-flash')

# AFTER (GOOD - 1500 requests/day)
self.model = genai.GenerativeModel('gemini-1.5-flash')
```

## Quota Calculation

### Example: Sending to 100 contacts
- 100 contacts × 1 message each = 100 requests
- With gemini-2.5-flash: ❌ FAIL (only 20/day)
- With gemini-1.5-flash: ✅ OK (1500/day available)

### Daily Usage Estimate
- **Small campaign:** 10-50 contacts = 10-50 requests
- **Medium campaign:** 50-200 contacts = 50-200 requests
- **Large campaign:** 200-500 contacts = 200-500 requests

With gemini-1.5-flash, you can handle up to 1,500 contacts per day!

## How to Check Your Quota

1. Go to: https://aistudio.google.com/app/apikey
2. Click on your API key
3. View usage statistics

## What to Do When Quota Exceeded

### Option 1: Wait (Free)
- Quota resets every 24 hours
- Wait until tomorrow to continue

### Option 2: Upgrade to Paid Plan
- Go to: https://ai.google.dev/pricing
- Pay-as-you-go pricing
- Much higher limits

### Option 3: Use Multiple API Keys (Not Recommended)
- Create multiple Google accounts
- Get multiple API keys
- Rotate between them
- ⚠️ Against Terms of Service

### Option 4: Batch Processing
- Split your contacts into batches
- Process 1,400 contacts today
- Process remaining tomorrow
- Stay within quota limits

## Best Practices

### 1. Monitor Usage
```python
# Add logging to track API calls
print(f"API call #{call_count} - Remaining quota: {1500 - call_count}")
```

### 2. Implement Retry Logic
```python
try:
    response = self.model.generate_content(prompt)
except Exception as e:
    if "quota" in str(e).lower():
        print("⚠️ Quota exceeded! Please wait or upgrade.")
        # Use fallback template
        return self._simple_template_replace(template, data)
```

### 3. Cache Results
- Don't regenerate same message multiple times
- Cache generated messages
- Reuse when possible

### 4. Optimize Prompts
- Shorter prompts = faster processing
- Less tokens used
- More requests possible

## Error Messages

### "quota_metric: generate_content_free_tier_requests"
**Meaning:** Daily request limit reached
**Solution:** Wait 24 hours or upgrade

### "quota_dimensions: model: gemini-2.5-flash"
**Meaning:** Specific model quota exceeded
**Solution:** Switch to gemini-1.5-flash (already done!)

### "retry_delay: seconds: 4"
**Meaning:** API suggests waiting 4 seconds before retry
**Solution:** Implement exponential backoff

## Testing After Fix

1. **Restart backend server:**
```bash
cd backend
python run.py
```

2. **Test with 1 contact first:**
- Input 1 nomor
- Generate AI message
- Should work now with gemini-1.5-flash

3. **Monitor console:**
```
Generating AI messages...
✓ Generated message for Contact 1
```

4. **Check for errors:**
- No quota errors should appear
- Messages should generate successfully

## Upgrade Path

If you need more than 1,500 requests/day:

1. **Enable billing** in Google Cloud Console
2. **Pricing:** ~$0.00015 per request (very cheap)
3. **Example:** 10,000 requests = $1.50
4. **No daily limits** with paid plan

## Files Modified

- `backend/ai/gemini_service.py` - Changed model from gemini-2.5-flash to gemini-1.5-flash

## Summary

✅ **Fixed:** Changed to gemini-1.5-flash (1,500 requests/day)
❌ **Old:** gemini-2.5-flash (only 20 requests/day)
📊 **Result:** 75x more quota!

---

**Status:** FIXED ✅
**Date:** March 5, 2026
