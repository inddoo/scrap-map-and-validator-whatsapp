# 🔄 Gemini Package Update Guide

## Problem

```
FutureWarning: All support for the `google.generativeai` package has ended.
Please switch to the `google.genai` package as soon as possible.

Error: 404 models/gemini-1.5-flash is not found for API version v1beta
```

## Root Cause

1. **Deprecated Package:** `google-generativeai` sudah tidak di-support lagi
2. **Wrong API Version:** Old package menggunakan v1beta yang sudah deprecated
3. **Model Format:** Format model name berbeda di package baru

## Solution

Migrate dari `google-generativeai` ke `google-genai` (package baru yang official)

## Changes Made

### 1. Update requirements.txt

**BEFORE:**
```
google-generativeai==0.3.2
```

**AFTER:**
```
google-genai
```

### 2. Update gemini_service.py

**BEFORE:**
```python
import google.generativeai as genai

genai.configure(api_key=api_key)
self.model = genai.GenerativeModel('gemini-1.5-flash')

response = self.model.generate_content(prompt)
```

**AFTER:**
```python
from google import genai
from google.genai import types

self.client = genai.Client(api_key=api_key)
self.model_name = 'gemini-1.5-flash'

response = self.client.models.generate_content(
    model=self.model_name,
    contents=prompt
)
```

## Installation Steps

### Option 1: Using Batch Script (Windows)

```bash
cd backend
update_gemini.bat
```

### Option 2: Manual Installation

```bash
cd backend

# Uninstall old package
pip uninstall -y google-generativeai

# Install new package
pip install google-genai

# Verify installation
pip show google-genai
```

### Option 3: Fresh Install

```bash
cd backend
pip install -r requirements.txt
```

## Key Differences

### Old Package (google-generativeai)
- ❌ Deprecated and no longer maintained
- ❌ Uses v1beta API (outdated)
- ❌ Different model format: `models/gemini-1.5-flash`
- ❌ `GenerativeModel` class
- ❌ `configure()` for API key

### New Package (google-genai)
- ✅ Official and actively maintained
- ✅ Uses latest stable API
- ✅ Simpler model format: `gemini-1.5-flash`
- ✅ `Client` class with better structure
- ✅ Direct client initialization

## API Changes

### Initialization
```python
# OLD
import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# NEW
from google import genai
client = genai.Client(api_key=api_key)
model_name = 'gemini-1.5-flash'
```

### Generate Content
```python
# OLD
response = model.generate_content(prompt)

# NEW
response = client.models.generate_content(
    model=model_name,
    contents=prompt
)
```

### Access Response
```python
# SAME for both
text = response.text
```

## Testing After Update

### 1. Check Installation
```bash
pip show google-genai
```

Expected output:
```
Name: google-genai
Version: 1.x.x
Summary: Google Generative AI Python Client
```

### 2. Test Import
```bash
python -c "from google import genai; print('✓ Import successful')"
```

### 3. Test API Connection
```bash
cd backend
python check_gemini_models.py
```

### 4. Test Full Integration
1. Start backend server
2. Open web app
3. Generate AI message with 1 contact
4. Should work without errors

## Troubleshooting

### Error: "No module named 'google.genai'"
**Solution:**
```bash
pip install google-genai
```

### Error: "Cannot import name 'types'"
**Solution:** Update to latest version
```bash
pip install --upgrade google-genai
```

### Error: Still getting old package warnings
**Solution:** Force uninstall old package
```bash
pip uninstall -y google-generativeai
pip cache purge
pip install google-genai
```

### Error: "Client object has no attribute 'models'"
**Solution:** Check package version
```bash
pip show google-genai
# Should be 1.x.x or higher
pip install --upgrade google-genai
```

## Benefits of New Package

1. ✅ **Future-proof:** Will receive updates and bug fixes
2. ✅ **Better API:** Cleaner and more intuitive
3. ✅ **Faster:** Optimized performance
4. ✅ **More features:** Access to latest Gemini capabilities
5. ✅ **Better error handling:** More descriptive error messages

## Files Modified

- `backend/requirements.txt` - Updated package dependency
- `backend/ai/gemini_service.py` - Migrated to new API
- `backend/update_gemini.bat` - Installation script (new)

## Migration Checklist

- [x] Update requirements.txt
- [x] Update import statements
- [x] Update client initialization
- [x] Update generate_content calls
- [x] Test error handling
- [x] Create installation script
- [x] Document changes

## Next Steps

1. **Run update script:**
   ```bash
   cd backend
   update_gemini.bat
   ```

2. **Restart backend server**

3. **Test AI generation** with 1 contact

4. **Verify no warnings** in console

---

**Status:** UPDATED ✅
**Date:** March 5, 2026
**Package:** google-genai (latest)
