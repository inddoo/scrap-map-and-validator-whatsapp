#!/bin/bash

# AI Features Setup Script
# This script helps you setup AI features quickly

echo "🤖 AI Features Setup"
echo "===================="
echo ""

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Error: backend directory not found"
    echo "   Please run this script from project root"
    exit 1
fi

cd backend

# Check if .env exists
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    echo "📝 Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env file created"
    else
        echo "❌ Error: .env.example not found"
        exit 1
    fi
fi

# Check if GEMINI_API_KEY is set
if grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
    echo ""
    echo "⚠️  GEMINI_API_KEY not configured yet"
    echo ""
    echo "Please follow these steps:"
    echo "1. Visit: https://makersuite.google.com/app/apikey"
    echo "2. Login with your Google Account"
    echo "3. Click 'Create API Key'"
    echo "4. Copy the API key"
    echo ""
    read -p "Enter your Gemini API key (or press Enter to skip): " api_key
    
    if [ ! -z "$api_key" ]; then
        # Replace the placeholder with actual API key
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/GEMINI_API_KEY=your_gemini_api_key_here/GEMINI_API_KEY=$api_key/" .env
        else
            # Linux
            sed -i "s/GEMINI_API_KEY=your_gemini_api_key_here/GEMINI_API_KEY=$api_key/" .env
        fi
        echo "✅ API key saved to .env"
    else
        echo "⚠️  Skipped. You can edit .env file manually later."
    fi
else
    echo "✅ GEMINI_API_KEY already configured"
fi

# Check if google-generativeai is installed
echo ""
echo "📦 Checking dependencies..."
if python -c "import google.generativeai" 2>/dev/null; then
    echo "✅ google-generativeai already installed"
else
    echo "📥 Installing google-generativeai..."
    pip install google-generativeai
    if [ $? -eq 0 ]; then
        echo "✅ google-generativeai installed successfully"
    else
        echo "❌ Failed to install google-generativeai"
        exit 1
    fi
fi

# Test AI integration
echo ""
echo "🧪 Testing AI integration..."
if [ -f "test_ai_integration.py" ]; then
    python test_ai_integration.py
else
    echo "⚠️  test_ai_integration.py not found, skipping tests"
fi

echo ""
echo "===================="
echo "✅ Setup Complete!"
echo "===================="
echo ""
echo "Next steps:"
echo "1. Start backend: python run.py"
echo "2. Start frontend: npm run dev"
echo "3. Go to WA Auto Sender tab"
echo "4. Upload CSV and try AI features"
echo ""
echo "📖 Documentation:"
echo "   - AI_QUICK_START.md"
echo "   - backend/AI_FEATURES_GUIDE.md"
echo "   - EXAMPLE_AI_USAGE.md"
echo ""
