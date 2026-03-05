@echo off
REM AI Features Setup Script for Windows
REM This script helps you setup AI features quickly

echo.
echo 🤖 AI Features Setup
echo ====================
echo.

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Error: backend directory not found
    echo    Please run this script from project root
    exit /b 1
)

cd backend

REM Check if .env exists
if exist ".env" (
    echo ✅ .env file already exists
) else (
    echo 📝 Creating .env file from .env.example...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✅ .env file created
    ) else (
        echo ❌ Error: .env.example not found
        exit /b 1
    )
)

REM Check if GEMINI_API_KEY is set
findstr /C:"GEMINI_API_KEY=your_gemini_api_key_here" .env >nul
if %errorlevel% equ 0 (
    echo.
    echo ⚠️  GEMINI_API_KEY not configured yet
    echo.
    echo Please follow these steps:
    echo 1. Visit: https://makersuite.google.com/app/apikey
    echo 2. Login with your Google Account
    echo 3. Click 'Create API Key'
    echo 4. Copy the API key
    echo.
    set /p api_key="Enter your Gemini API key (or press Enter to skip): "
    
    if not "!api_key!"=="" (
        powershell -Command "(Get-Content .env) -replace 'GEMINI_API_KEY=your_gemini_api_key_here', 'GEMINI_API_KEY=!api_key!' | Set-Content .env"
        echo ✅ API key saved to .env
    ) else (
        echo ⚠️  Skipped. You can edit .env file manually later.
    )
) else (
    echo ✅ GEMINI_API_KEY already configured
)

REM Check if google-generativeai is installed
echo.
echo 📦 Checking dependencies...
python -c "import google.generativeai" 2>nul
if %errorlevel% equ 0 (
    echo ✅ google-generativeai already installed
) else (
    echo 📥 Installing google-generativeai...
    pip install google-generativeai
    if %errorlevel% equ 0 (
        echo ✅ google-generativeai installed successfully
    ) else (
        echo ❌ Failed to install google-generativeai
        exit /b 1
    )
)

REM Test AI integration
echo.
echo 🧪 Testing AI integration...
if exist "test_ai_integration.py" (
    python test_ai_integration.py
) else (
    echo ⚠️  test_ai_integration.py not found, skipping tests
)

echo.
echo ====================
echo ✅ Setup Complete!
echo ====================
echo.
echo Next steps:
echo 1. Start backend: python run.py
echo 2. Start frontend: npm run dev
echo 3. Go to WA Auto Sender tab
echo 4. Upload CSV and try AI features
echo.
echo 📖 Documentation:
echo    - AI_QUICK_START.md
echo    - backend\AI_FEATURES_GUIDE.md
echo    - EXAMPLE_AI_USAGE.md
echo.

cd ..
pause
