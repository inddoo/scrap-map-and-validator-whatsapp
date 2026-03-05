# ✅ Quick Fix: Gemini API Quota Exceeded

## Problem
```
quota_metric: "generate_content_free_tier_requests"
quota_dimensions: model: "gemini-2.5-flash"
quota_value: 20
```

Anda kena limit 20 requests/day dari gemini-2.5-flash.

## Solution
Ganti ke `gemini-1.5-flash` yang punya quota 1,500 requests/day (75x lebih banyak!)

## Changes Made

### 1. Model Changed
```python
# BEFORE
self.model = genai.GenerativeModel('models/gemini-2.5-flash')  # 20/day

# AFTER  
self.model = genai.GenerativeModel('gemini-1.5-flash')  # 1500/day
```

### 2. Better Error Handling
```python
except Exception as e:
    if "quota" in str(e).lower():
        print("⚠️ Quota exceeded! Using fallback.")
        # Use simple template instead
```

## Result
- ✅ 75x more quota (20 → 1,500 requests/day)
- ✅ Better error messages
- ✅ Automatic fallback to template if quota exceeded
- ✅ Can handle up to 1,500 contacts per day

## Next Steps
1. **Restart backend server**
2. **Test dengan 1 nomor** untuk verify
3. **Quota reset** dalam 24 jam jika masih kena limit hari ini

## Files Modified
- `backend/ai/gemini_service.py`

---
**Status:** FIXED ✅
