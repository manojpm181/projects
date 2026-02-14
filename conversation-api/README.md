# 💬 100% FREE AI Conversation API

A production-grade conversation API built entirely with **FREE services** - no credit card required!

## 🎯 Why This is Free

| Service | Free Tier | Limits |
|---------|----------|--------|
| **Groq** | 30 req/min, 14,400 req/day | Completely free, no CC |
| **Supabase** | 500MB DB, 2 concurrent | Email auth included |
| **Render** | 512MB RAM, 1 CPU | Web service hosting |
| **FastAPI** | Open source | No cost |

## ✨ Features

- ✅ **Real LLM** - Groq's Llama3, Mixtral, Gemma (FREE)
- ✅ **Real Database** - Supabase PostgreSQL (FREE)
- ✅ **Real Auth** - Supabase Auth with JWT (FREE)
- ✅ **Real Streaming** - SSE with token-by-token delivery
- ✅ **Rate Limiting** - In-memory (FREE)
- ✅ **Conversation Management** - Create, update, delete
- ✅ **Token Counting** - Approximate (FREE)
- ✅ **Swagger Docs** - Auto-generated API documentation
- ✅ **Docker Support** - Container ready
- ✅ **Deploy to Render** - One-click deployment

## 🚀 Quick Start (5 Minutes)

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/conversation-api-free
cd conversation-api-free
chmod +x scripts/setup.sh
./scripts/setup.sh




2. Configure Supabase (FREE)
Go to supabase.com → Start project

Create project: conversation-api

Copy URL and anon key to .env

Run database/schema.sql in Supabase SQL Editor

3. Configure Groq (FREE)
Go to console.groq.com → Sign up

Create API key

Copy key to .env

4. Run the API
bash
source venv/bin/activate
python -m src.main
🎉 Done! Your API is running at http://localhost:8000

📡 API Endpoints
Authentication (Supabase Auth)
text
POST   /api/v1/auth/register     # Create account
POST   /api/v1/auth/login        # Login → get JWT
POST   /api/v1/auth/refresh      # Refresh token
POST   /api/v1/auth/logout       # Logout
GET    /api/v1/auth/me           # Get profile
Conversations
text
POST   /api/v1/conversations           # Create conversation
GET    /api/v1/conversations           # List conversations
GET    /api/v1/conversations/{id}      # Get conversation
PATCH  /api/v1/conversations/{id}      # Update conversation
DELETE /api/v1/conversations/{id}      # Delete conversation
Messages
text
GET    /api/v1/conversations/{id}/messages     # Get messages
POST   /api/v1/conversations/{id}/messages     # Send (non-streaming)
POST   /api/v1/streaming/conversations/{id}/stream  # Stream response
🔌 Example Usage
1. Register User
bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
2. Login
bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
3. Create Conversation
bash
TOKEN="your-jwt-token"
curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Chat"}'
4. Stream a Message (SSE)
bash
CONV_ID="your-conversation-id"
curl -X POST "http://localhost:8000/api/v1/streaming/conversations/$CONV_ID/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"message":"Hello, AI!","stream":true}'
📊 Free Models Available
Model	Context	Speed	Best For
llama3-8b-8192	8K	⚡⚡⚡	General chat
mixtral-8x7b-32768	32K	⚡⚡	Complex reasoning
gemma2-9b-it	8K	⚡⚡⚡	Fast responses
🐳 Docker Deployment
bash
# Build image
docker build -t conversation-api-free .

# Run container
docker run -p 8000:8000 --env-file .env conversation-api-free
🚀 Deploy to Render (FREE)
Push code to GitHub

Go to render.com

Create new Web Service

Connect GitHub repository

Use render.yaml configuration

Deploy!

📁 Project Structure
text
conversation-api-free/
├── src/
│   ├── main.py              # FastAPI app
│   ├── api/                 # API endpoints
│   ├── core/                # Config & Supabase
│   ├── services/            # Business logic
│   ├── llm/                 # Groq integration
│   └── middleware/          # Rate limiting
├── database/
│   └── schema.sql           # Supabase tables
├── scripts/
│   └── setup.sh             # One-click setup
├── .env.example             # Environment template
├── requirements.txt         # Dependencies
└── README.md
🎯 Why This is Production Ready
Real LLM - Not a mock, actual Groq inference

Real Database - Persistent Supabase storage

Real Auth - Secure JWT authentication

Real Streaming - True SSE token-by-token

Rate Limiting - Prevents abuse

Error Handling - Graceful failures

Logging - Request tracking

CORS - Cross-origin support

Health Checks - Monitoring ready

Docker - Containerized deployment

⚡ Performance
Latency: 100-300ms first token (Groq is FAST)

Throughput: 30 requests/minute (free tier)

Concurrency: 2 concurrent connections (Supabase free)

Streaming: Real-time as tokens generate

🆘 Troubleshooting
Supabase Connection Failed

Check URL and anon key in .env

Run schema.sql in SQL Editor

Enable RLS policies

Groq API Failed

Verify API key in .env

Check free tier limits (30/min)

Try different model

Rate Limit Exceeded

Wait 60 seconds

Default: 30 requests/minute

Adjust in .env

📈 Monitoring
Health Check: GET /health

Request IDs: X-Request-ID header

Logs: Console output

Metrics: Coming soon

🤝 Contributing
Fork repository

Create feature branch

Commit changes

Push to branch

Open Pull Request

📄 License
MIT - Free for everyone, forever! 🎉
