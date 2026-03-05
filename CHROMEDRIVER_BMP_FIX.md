# 🔧 ChromeDriver BMP Character Fix

## Problem

Error: `ChromeDriver only supports characters in the BMP`

This error occurs when trying to send messages with emojis or special characters that are outside the Basic Multilingual Plane (BMP). ChromeDriver doesn't support characters with Unicode code points > 0xFFFF.

## Solution

We've implemented automatic character sanitization that:

1. **Filters unsupported characters** - Removes characters outside BMP before sending
2. **Guides AI** - Instructs Gemini to use only simple emojis
3. **Logs warnings** - Notifies when message is sanitized

## What Characters Are Affected?

### ❌ NOT Supported (Outside BMP)
- Complex emojis: 🎉 🚀 🎊 🎯 🔥 💯 🙏 🤝 🎁 🌟
- Emoji combinations: 👨‍💼 👩‍💻 🏃‍♂️
- Some special symbols

### ✅ Supported (Inside BMP)
- Simple emojis: 😊 👋 ✅ ❌ 💼 📱 ⚠️ 🎯 📝 📊
- Basic text characters
- Numbers and punctuation
- Most common symbols

## How It Works

### 1. Message Sanitization

```python
def _sanitize_message(self, message: str) -> str:
    """Remove characters outside BMP"""
    sanitized = ''.join(char for char in message if ord(char) <= 0xFFFF)
    return sanitized
```

### 2. AI Prompt Update

AI is now instructed to:
```
"Gunakan emoji SEDERHANA saja (😊 👋 ✅ ❌ 💼 📱 dll)
HINDARI emoji kompleks atau karakter khusus"
```

### 3. Automatic Warning

When unsupported characters are detected:
```
⚠️ Message sanitized (removed unsupported characters)
```

## Testing

### Before Fix
```
Message: "Halo! 🎉 Promo spesial 🚀"
Result: ERROR - ChromeDriver only supports characters in the BMP
```

### After Fix
```
Message: "Halo! 🎉 Promo spesial 🚀"
Sanitized: "Halo!  Promo spesial "
Result: ✅ Message sent successfully
Warning: ⚠️ Message sanitized
```

## Best Practices

### ✅ DO:

1. **Use Simple Emojis**
   ```
   ✅ "Halo! 😊 Ada promo spesial nih 👋"
   ✅ "Terima kasih! ✅ Sudah kami proses 📱"
   ```

2. **Test Messages First**
   - Send to 1-2 numbers first
   - Check if emojis appear correctly
   - Adjust if needed

3. **Provide Clear Instructions to AI**
   ```
   "Buatkan pesan dengan emoji sederhana seperti 😊 👋 ✅"
   ```

### ❌ DON'T:

1. **Avoid Complex Emojis**
   ```
   ❌ "Promo 🎉🎊🎁🌟💯"
   ❌ "Team kami 👨‍💼👩‍💻"
   ```

2. **Don't Use Emoji Combinations**
   ```
   ❌ Skin tone modifiers: 👋🏻 👋🏼
   ❌ Gender modifiers: 🏃‍♂️ 🏃‍♀️
   ```

## Recommended Emojis

### Safe to Use (BMP)
```
Faces: 😊 😃 😄 😁 😆 😅 😂 🙂 🙃 😉 😌 😍
Hands: 👋 👍 👎 👏 🙏 ✋ 👌 ✌️
Symbols: ✅ ❌ ⚠️ ❗ ❓ 💯 🔥 ⭐
Objects: 📱 💼 📝 📊 📈 📉 🎯 🏆
```

### Avoid (Outside BMP)
```
Complex: 🎉 🎊 🎁 🚀 🌟 🤝 🙌 🎈
Combinations: 👨‍💼 👩‍💻 🏃‍♂️ 👋🏻
```

## Troubleshooting

### Issue: Message sent but emojis missing

**Cause:** Emojis were outside BMP and got filtered

**Solution:**
1. Check console for warning: "Message sanitized"
2. Use simpler emojis from recommended list
3. Update AI instructions to avoid complex emojis

### Issue: Still getting BMP error

**Cause:** Backend not restarted after fix

**Solution:**
1. Stop backend (Ctrl+C)
2. Restart: `python run.py`
3. Try again

### Issue: AI still generates complex emojis

**Cause:** AI prompt not specific enough

**Solution:**
Add to context:
```
"PENTING: Gunakan HANYA emoji sederhana seperti 😊 👋 ✅ ❌
JANGAN gunakan emoji kompleks seperti 🎉 🚀 🎊"
```

## Alternative Solutions

### Option 1: Use Text Instead of Emojis
```
Instead of: "Promo spesial! 🎉🎊"
Use: "Promo spesial! (Terbatas)"
```

### Option 2: Use ASCII Art
```
Instead of: "Terima kasih! 🙏"
Use: "Terima kasih! :)"
```

### Option 3: Use Symbols
```
Instead of: "Checklist ✅"
Use: "Checklist [v]"
```

## Technical Details

### BMP (Basic Multilingual Plane)
- Unicode range: U+0000 to U+FFFF
- Includes most common characters
- Supported by ChromeDriver

### Outside BMP
- Unicode range: U+10000 and above
- Includes many emojis
- NOT supported by ChromeDriver

### Why This Limitation?

ChromeDriver uses older Unicode handling that doesn't support supplementary planes. This is a known limitation and won't be fixed in ChromeDriver.

## Future Improvements

Potential solutions:
1. Use WhatsApp Web API (if available)
2. Switch to Playwright (better Unicode support)
3. Implement emoji mapping (complex → simple)
4. Pre-process all AI outputs

## Summary

✅ **Fixed:** Automatic character sanitization
✅ **Updated:** AI prompts to use simple emojis
✅ **Added:** Warning when characters are removed
✅ **Documented:** Safe emoji list

**Result:** Messages now send successfully without BMP errors! 🎊

---

**Note:** Some emojis may be removed during sanitization. This is expected behavior to ensure message delivery.
