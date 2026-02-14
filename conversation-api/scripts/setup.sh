#!/bin/bash

set -e

echo "🚀 Setting up Conversation API (100% FREE Edition)"
echo "=================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

PY_VERSION=$(python3 --version)
echo "✅ $PY_VERSION detected"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo ""
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    
    echo ""
    echo "⚠️  ACTION REQUIRED:"
    echo "   1. Go to https://supabase.com and create a FREE project"
    echo "   2. Copy your Supabase URL and anon key to .env"
    echo "   3. Go to https://console.groq.com and get a FREE API key"
    echo "   4. Add your Groq API key to .env"
    echo ""
    read -p "   Press Enter after updating .env file..."
fi

# Test Supabase connection
echo ""
echo "🔗 Testing Supabase connection..."
python -c "
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

if not url or not key:
    print('❌ Supabase credentials not found in .env')
    exit(1)

try:
    supabase = create_client(url, key)
    supabase.auth.get_session()
    print('✅ Supabase connection successful')
except Exception as e:
    print(f'❌ Supabase connection failed: {e}')
    exit(1)
"

# Test Groq connection
echo ""
echo "🔗 Testing Groq API connection..."
python -c "
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

key = os.getenv('GROQ_API_KEY')

if not key:
    print('❌ Groq API key not found in .env')
    exit(1)

try:
    response = httpx.get(
        'https://api.groq.com/openai/v1/models',
        headers={'Authorization': f'Bearer {key}'}
    )
    if response.status_code == 200:
        print('✅ Groq API connection successful')
    else:
        print(f'❌ Groq API failed: {response.status_code}')
        exit(1)
except Exception as e:
    print(f'❌ Groq API connection failed: {e}')
    exit(1)
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Run the database schema in Supabase SQL Editor:"
echo "      cat database/schema.sql"
echo ""
echo "   2. Start the server:"
echo "      source venv/bin/activate"
echo "      python -m src.main"
echo ""
echo "   3. Access the API:"
echo "      📚 Docs: http://localhost:8000/docs"
echo "      🏠 Home: http://localhost:8000"
echo ""
echo "✨ Your 100% FREE Conversation API is ready!"