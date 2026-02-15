### 📚 Conversation API
A production-grade REST API for AI-powered conversations with streaming support, built with FastAPI.

### ✨ Features
- Real-time Streaming: Server-Sent Events (SSE) with token-by-token delivery
- Multi-LLM Support: Integration with Groq API (Llama3, Mixtral, Gemma)
- Authentication: JWT-based auth with Supabase
- Conversation Management: Create, update, delete, and list conversations
- Message History: Persistent storage of all conversations
- Rate Limiting: Protection against abuse
- Auto Documentation: Swagger UI at /docs
- Docker Support: Containerized deployment ready

### 🛠️ Tech Stack
1. Framework: FastAPI (Python)
2. Database: Supabase PostgreSQL
3. Auth: Supabase Auth + JWT
4. LLM: Groq API
5. Streaming: Server-Sent Events (SSE)

### 📁 Project Structure

    conversation-api/
    ├── src/
    │   ├── main.py              # FastAPI application
    │   ├── api/                 # API endpoints
    │   │   └── v1/
    │   │       ├── endpoints/   # Route handlers
    │   │       └── schemas/     # Pydantic models
    │   ├── core/                # Configuration
    │   ├── services/            # Business logic
    │   ├── llm/                 # LLM integration
    │   └── middleware/          # Custom middleware
    ├── database/
    │   └── schema.sql           # Database schema
    ├── scripts/
    │   └── setup.sh              # Setup script
    ├── tests/                    # Test suite
    ├── .env.example              # Environment variables
    ├── requirements.txt          # Python dependencies
    └── README.md                 # Documentation
    
### 🚀 Quick Start
- Prerequisites

      Python 3.10+
- Supabase account
- Groq API key
- Installation
   - Clone the repository

          git clone https://github.com/yourusername/conversation-api
          cd conversation-api
     
- Set up virtual environment

      python3 -m venv venv
      venv\Scripts\activate
      Install dependencies

      pip install -r requirements.txt
  
- Configure environment variables

      cp .env.example .env
-  # Edit .env with your credentials


        Run database migrations

- Copy database/schema.sql and run in Supabase SQL Editor

- Start the server

      python -m src.main
  
- The API will be available at http://localhost:8000

### 📡 API Endpoints
1. Authentication
  - Method	Endpoint	Description

        POST	/api/v1/auth/register	Create new account
        POST	/api/v1/auth/login	Login and get JWT
        POST	/api/v1/auth/refresh	Refresh access token
        POST	/api/v1/auth/logout	Logout user
        GET	/api/v1/auth/me	Get current user profile
    
2. Conversations
  - Method	Endpoint	Description
    
        POST	/api/v1/conversations	Create conversation
        GET	/api/v1/conversations	List conversations
        GET	/api/v1/conversations/{id}	Get conversation
        PATCH	/api/v1/conversations/{id}	Update conversation
        DELETE	/api/v1/conversations/{id}	Delete conversation
3. Message
  - Method	Endpoint	Description
     
          GET	/api/v1/conversations/{id}/messages	Get messages
          POST	/api/v1/conversations/{id}/messages	Send message (non-streaming)
          POST	/api/v1/streaming/conversations/{id}/stream	Stream response
    
### 🔌 Usage Examples
1. Register a User

        curl -X POST http://localhost:8000/api/v1/auth/register \
          -H "Content-Type: application/json" \
          -d '{
            "email": "user@example.com",
            "password": "securepassword123",
            "full_name": "John Doe"
          }'
2. Login

        curl -X POST http://localhost:8000/api/v1/auth/login \
          -H "Content-Type: application/json" \
          -d '{
            "email": "user@example.com",
            "password": "securepassword123"
          }'
3. Create Conversation

        curl -X POST http://localhost:8000/api/v1/conversations \
          -H "Authorization: Bearer YOUR_JWT_TOKEN" \
          -H "Content-Type: application/json" \
          -d '{
            "title": "Technical Discussion"
          }'
4. Send Message (Non-streaming)

        curl -X POST http://localhost:8000/api/v1/conversations/CONVERSATION_ID/messages \
          -H "Authorization: Bearer YOUR_JWT_TOKEN" \
          -H "Content-Type: application/json" \
          -d '{
            "message": "Explain quantum computing",
            "stream": false
          }'
5. Stream Response (SSE)
        
        curl -X POST http://localhost:8000/api/v1/streaming/conversations/CONVERSATION_ID/stream \
          -H "Authorization: Bearer YOUR_JWT_TOKEN" \
          -H "Content-Type: application/json" \
          -H "Accept: text/event-stream" \
          -d '{
            "message": "Tell me a story",
            "stream": true
          }'
### 📊 Available Models
- Model	Context	Description
- llama3-8b-8192	8K tokens	Fast, general purpose
- mixtral-8x7b-32768	32K tokens	Complex reasoning
- gemma2-9b-it	8K tokens	Balanced performance

### 🔧 Configuration
- Key environment variables in .env:

      # Supabase
      SUPABASE_URL=your-project-url
      SUPABASE_ANON_KEY=your-anon-key
      SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
      
      # Groq
      GROQ_API_KEY=your-groq-api-key
      
      # JWT
      JWT_SECRET=your-jwt-secret
      
      # Rate Limiting
      RATE_LIMIT_REQUESTS=30
      RATE_LIMIT_PERIOD=60
  
###  Docker Deployment(optional)

    # Build image
    docker build -t conversation-api .
    
    # Run container
    docker run -p 8000:8000 --env-file .env conversation-api
### Testing
    
    # Run tests
    pytest
    
    # Run with coverage
    pytest --cov=src tests/
    
### Monitoring
- Health Check: GET /health
- API Documentation: GET /docs
- Request IDs: Each request gets unique X-Request-ID

### Security
- JWT authentication
- Rate limiting
- CORS protection
- Row Level Security in database
- Input validation with Pydantic

### Contributing
- Fork the repository
- Create feature branch (git checkout -b feature/amazing-feature)
- Commit changes (git commit -m 'Add amazing feature')
- Push to branch (git push origin feature/amazing-feature)
- Open a Pull Request

🙏 Acknowledgments
- FastAPI for the amazing framework
- Supabase for the backend platform
= Groq for the LLM inference API
