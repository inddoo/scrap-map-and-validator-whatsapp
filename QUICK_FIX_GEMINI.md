# ⚡ Quick Fix: Update Gemini Package

## Problem
```
FutureWarning: google.generativeai package has ended support
Error: 404 models/gemini-1.5-flash is not found
```

## Quick Solution

### Step 1: Update Package
```bash
cd backend
pip uninstall -y google-generativeai
pip install google-genai
```

### Step 2: Restart Server
```bash
python run.py
```

### Step 3: Test
- Generate AI message dengan 1 nomor
- Should work now!

## What Changed
- ✅ Package: `google-generativeai` → `google-genai`
- ✅ API: Old v1beta → New stable API
- ✅ Model: Better format and quota (1500/day)

## Files Updated
- `backend/requirements.txt`
- `backend/ai/gemini_service.py`

---
**Run the commands above and restart your server!**
