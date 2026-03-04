# Contributing to Google Maps Scraper & WhatsApp Validator

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** - Descriptive and specific
- **Steps to reproduce** - Detailed steps to reproduce the issue
- **Expected behavior** - What you expected to happen
- **Actual behavior** - What actually happened
- **Screenshots** - If applicable
- **Environment** - OS, Python version, Node version, browser version
- **Logs** - Relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear description** - What enhancement you'd like to see
- **Use case** - Why this would be useful
- **Possible implementation** - If you have ideas on how to implement it
- **Alternatives** - Other solutions you've considered

### Pull Requests

1. **Fork the repository**
2. **Create a branch** - `git checkout -b feature/AmazingFeature`
3. **Make your changes**
4. **Test thoroughly** - Ensure nothing breaks
5. **Commit** - `git commit -m 'Add some AmazingFeature'`
6. **Push** - `git push origin feature/AmazingFeature`
7. **Open a Pull Request**

#### Pull Request Guidelines

- Follow the existing code style
- Write clear commit messages
- Update documentation if needed
- Add tests if applicable
- Keep PRs focused on a single feature/fix
- Reference related issues

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Chrome/Chromium

### Setup Steps

1. **Clone your fork**
```bash
git clone https://github.com/yourusername/google-maps-scraper-wa-validator.git
cd google-maps-scraper-wa-validator
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

3. **Install frontend dependencies**
```bash
cd ..
npm install
```

4. **Run in development mode**
```bash
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend
npm run dev
```

## Code Style

### Python
- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions/classes
- Keep functions focused and small

### TypeScript/React
- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable

### General
- Write clear, self-documenting code
- Add comments for complex logic
- Use meaningful variable names
- Keep files organized

## Project Structure

```
.
├── backend/
│   ├── api/          # API routes and schemas
│   ├── config/       # Configuration
│   ├── core/         # Core functionality
│   ├── scrapers/     # Maps scraper
│   └── wa_validator/ # WhatsApp validator
│
├── src/
│   ├── components/   # React components
│   ├── config/       # Frontend config
│   ├── services/     # API services
│   ├── types/        # TypeScript types
│   └── utils/        # Utility functions
```

## Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
npm test
```

### Manual Testing
- Test both Maps Scraper and WA Validator
- Test with different inputs
- Test error cases
- Test on different browsers/OS

## Documentation

When adding features:
- Update README.md if needed
- Add inline code comments
- Update API documentation
- Add examples if applicable

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add CSV column deletion feature
fix: Fix WhatsApp validation for invalid numbers
docs: Update installation instructions
refactor: Simplify scraper logic
test: Add tests for CSV parser
```

Prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (formatting)
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙏
