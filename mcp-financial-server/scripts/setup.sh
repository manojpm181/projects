#!/bin/bash

set -e

echo "🚀 Starting Financial MCP Server Setup"

echo "======================================"

# Check Node.js

if ! command -v node &> /dev/null; then

    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."

    exit 1

fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)

if [ "$NODE_VERSION" -lt 18 ]; then

    echo "❌ Node.js version must be 18 or higher. Current version: $NODE_VERSION"

    exit 1

fi

echo "✅ Node.js $NODE_VERSION detected"

# Install dependencies

echo ""

echo "📦 Installing dependencies..."

npm install

# Check for environment file

if [ ! -f .env ]; then

    echo ""

    echo "📄 Creating .env file from template..."

    cp .env.example .env

    echo ""

    echo "⚠️  IMPORTANT: Please edit .env file with your Supabase credentials"

    echo "   1. Go to https://supabase.com"

    echo "   2. Create a new project"

    echo "   3. Get your URL and anon key"

    echo "   4. Add them to .env file"

    echo ""

    read -p "Press Enter after you've added Supabase credentials to .env..."

fi

# Build the project

echo ""

echo "🔨 Building project..."

npm run build

# Test database connection

echo ""

echo "🔗 Testing database connection..."

if node -e "

require('dotenv').config();

const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);

supabase.from('companies').select('count').limit(1)

  .then(() => {

    console.log('✅ Database connection successful');

    process.exit(0);

  })

  .catch(err => {

    console.error('❌ Database connection failed:', err.message);

    console.log('');

    console.log('Please make sure:');

    console.log('1. Your .env file has correct Supabase credentials');

    console.log('2. You have created the tables in Supabase');

    console.log('');

    console.log('To create tables, run:');

    console.log('   cat database/schema.sql | psql YOUR_SUPABASE_DB_URL');

    process.exit(1);

  });

"; then

    echo ""

    echo "🎉 Setup completed successfully!"

    echo ""

    echo "📋 Available commands:"

    echo "   npm start          - Run in stdio mode (for Claude Desktop/Cursor)"

    echo "   npm run start:sse  - Run in SSE mode (for web clients)"

    echo "   npm run dev        - Development mode with hot reload"

    echo "   npm run seed       - Seed database with sample data"

    echo "   npm test           - Run tests"

    echo ""

    echo "🔧 Next steps:"

    echo "   1. Run seed script: npm run seed"

    echo "   2. Start server: npm start"

    echo "   3. Configure your MCP client (see README.md)"

else

    echo ""

    echo "❌ Setup failed. Please check the errors above."

    exit 1

fi