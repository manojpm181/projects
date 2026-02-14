#  Advanced Financial Data MCP Server

A production-grade Model Context Protocol (MCP) server providing 8 powerful financial analysis tools with real-time data from Supabase PostgreSQL.

## Features

###  8 Core Tools
1. **`get_company_profile`** - Fetch company details by ticker or name
2. **`search_companies`** - Filter companies by sector, industry, market cap
3. **`get_financial_report`** - Quarterly/annual financial statements
4. **`compare_companies`** - Side-by-side comparison of 2-5 companies
5. **`get_stock_price_history`** - Historical prices with statistics
6. **`get_analyst_ratings`** - Analyst consensus and target prices
7. **`screen_stocks`** - Advanced stock screening with custom filters
8. **`get_sector_overview`** - Sector-level analytics and top companies

###  Advanced Capabilities
- **Dual Transport**: SSE for web clients, stdio for desktop apps
- **Real Database**: Supabase PostgreSQL with 25+ real companies
- **Advanced Analytics**: Statistical calculations, consensus ratings
- **Production Ready**: Error handling, logging, validation
- **Type Safe**: Full TypeScript support with Zod validation

##  Quick Start

### 1. Prerequisites
- Node.js 18+
- Supabase account (free tier)
- Claude Desktop or Cursor (optional)

### 2. One-Command Setup

    git clone https://github.com/manojpm181/projects/mcp-financial-server
    cd mcp-financial-server
    chmod +x scripts/setup.sh
    ./scripts/setup.sh
3. Configure Supabase
- Go to supabase.com and create free account
- Create new project
    Get your:
    - Project URL (SUPABASE_URL)
    - Anon Key (SUPABASE_ANON_KEY)
    - Add to .env file

4. Run Database Setup
# Create tables (run in Supabase SQL Editor)
    cat database/schema.sql

# Seed with sample data
    npm run seed
5. Start Server

# For Claude Desktop/Cursor:
    npm start

# For web testing:
    npm run start:sse
# Visit: http://localhost:3001
🔌 Client Configuration
    Claude Desktop
Add to ~/Library/Application Support/Claude/claude_desktop_config.json:

json
{
  "mcpServers": {
    "financial-data": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-financial-server/dist/index.js"],
      "env": {
        "SUPABASE_URL": "https://your-project-ref.supabase.co",
        "SUPABASE_ANON_KEY": "your-anon-key"
      }
    }
  }
}
Cursor
Add to ~/.cursor/mcp.json:

json
{
  "mcpServers": {
    "financial-data": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-financial-server/dist/index.js"],
      "env": {
        "SUPABASE_URL": "https://your-project-ref.supabase.co",
        "SUPABASE_ANON_KEY": "your-anon-key"
      }
    }
  }
}
📊 Tool Examples
Get Company Profile
json
{
  "name": "get_company_profile",
  "arguments": {
    "identifier": "AAPL"
  }
}
Compare Companies
json
{
  "name": "compare_companies",
  "arguments": {
    "tickers": ["AAPL", "MSFT", "GOOGL"]
  }
}
Screen Stocks
json
{
  "name": "screen_stocks",
  "arguments": {
    "min_revenue": 50000,
    "min_gross_margin": 40,
    "sector": "Technology"
  }
}
🧪 Testing
bash
# Run tests
npm test

# Development with hot reload
npm run dev

# Build for production
npm run build
📁 Project Structure
text
mcp-financial-server/
├── src/                    # Source code
│   ├── index.ts           # Main server
│   ├── config/            # Configuration
│   ├── db/               # Database layer
│   ├── tools/            # 8 MCP tools
│   ├── validators/       # Input validation
│   └── utils/            # Utilities
├── database/             # SQL schemas & seeds
├── tests/               # Test suite
├── scripts/             # Setup scripts
└── docs/               # Documentation
🔒 Security
Row Level Security enabled

Input validation with Zod

No SQL injection vulnerabilities

Environment variables for secrets

Rate limiting on SSE endpoints

🚀 Deployment
bash
# Production build
npm run build

# Run in production
NODE_ENV=production npm start

# Docker (optional)
docker build -t mcp-financial-server .
docker run -p 3001:3001 --env-file .env mcp-financial-server
🆘 Troubleshooting
Database Connection Failed
Check .env file has correct Supabase credentials

Run tables creation: cat database/schema.sql | psql YOUR_DB_URL

Test connection: node -e "require('./src/db/client.ts').testConnection()"

Tools Not Working
Check server is running: npm start

Verify database has data: npm run seed

Check logs for errors

Claude Desktop Not Connecting
Ensure absolute path in config

Restart Claude Desktop after config change

Check Claude logs: Help → Debug → View Logs

📈 Sample Data
25+ real companies (AAPL, MSFT, GOOGL, etc.)

4 quarters of financial data per company

90 days of stock price history

Analyst ratings from top firms

🤝 Contributing
Fork the repository

Create feature branch

Make changes

Add tests

Submit PR

📄 License
MIT

🙏 Acknowledgments
Model Context Protocol team

Supabase for amazing backend

All contributors

Ready to analyze financial data with AI! 🚀

text

### **STEP 6: TEST THE COMPLETE SERVER**

```bash
# Build the project
npm run build

# Run in stdio mode (test in terminal)
npm start

# In another terminal, test with curl (for SSE mode)
npm run start:sse

# Test SSE endpoint
curl -X POST http://localhost:3001/message \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "get_company_profile",
      "arguments": {
        "identifier": "AAPL"
      }
    }
  }'
