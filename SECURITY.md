# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Features

### Data Privacy
- ✅ All data processing happens locally on your machine
- ✅ No data is sent to external servers
- ✅ WhatsApp session stored locally in `backend/wa_session/`
- ✅ No third-party API calls or tracking

### Session Security
- WhatsApp session files are stored locally
- Session files are excluded from git via `.gitignore`
- Session persists only on your local machine
- You can delete session anytime by removing `backend/wa_session/` folder

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainers directly (if contact provided)
3. Or open a private security advisory on GitHub

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and work on a fix as soon as possible.

## Best Practices for Users

### When Using This Tool

1. **Keep Your Session Private**
   - Never share your `wa_session` folder
   - Don't commit session files to git
   - Delete session if you suspect compromise

2. **Use Responsibly**
   - Don't scrape excessively
   - Respect rate limits
   - Don't spam WhatsApp numbers
   - Follow Terms of Service

3. **Protect Your Data**
   - Don't share CSV files with sensitive data
   - Use `.env` files for sensitive configuration
   - Keep your Python and Node.js dependencies updated

4. **Network Security**
   - Run on trusted networks
   - Use firewall if exposing API
   - Don't expose backend to public internet without authentication

## Known Security Considerations

### WhatsApp Session
- Session files contain authentication tokens
- If compromised, someone could access your WhatsApp Web
- **Solution**: Keep `wa_session/` folder private and secure

### Scraping
- Excessive scraping may trigger rate limits or blocks
- **Solution**: Use reasonable delays and limits

### Dependencies
- Third-party packages may have vulnerabilities
- **Solution**: Regularly update dependencies with `pip install -U` and `npm update`

## Updates

We recommend:
- Keeping dependencies up to date
- Monitoring security advisories
- Reviewing changes before updating

## Disclaimer

This tool is provided "as is" without warranty. Users are responsible for:
- Securing their own installations
- Complying with applicable laws and terms of service
- Using the tool ethically and responsibly

---

Last Updated: 2026-03-04
