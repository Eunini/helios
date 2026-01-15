# Helios AI - Intelligent Business Agent Platform

A modern, full-stack AI platform that combines voice, video, and text interfaces to provide intelligent business automation for communications, finance, operations, and insights.

## 🌟 Features

### 🎤 Voice Integration

- **Real-time Voice Transcription**: Leverage OpenAI's Whisper API for accurate speech-to-text conversion
- **One-Click Recording**: Simple voice interface for hands-free interaction
- **Automatic Task Creation**: Voice notes automatically become actionable tasks
- **Multi-language Support**: Transcribe audio in multiple languages

### 📹 Video Chat

- **Live Video Streaming**: Real-time video communication with AI agents using WebRTC
- **Performance Metrics**: Monitor latency, frame rate, and video resolution in real-time
- **Dual-Mode Communication**: Combine video with text and voice chat seamlessly
- **Web Speech API**: Built-in speech recognition and text-to-speech synthesis

### 🤖 Intelligent Agents

- **Communications Agent**: Manage customer interactions and communications
- **Finance Agent**: Handle financial analysis and reporting
- **Operations Agent**: Optimize business operations and workflows
- **Insights Agent**: Generate actionable business insights
- **Planner Agent**: Strategic planning and task management

### 📊 Dashboard

- **Customer Management**: View and manage customer data
- **Inventory Tracking**: Real-time inventory monitoring
- **Staff Directory**: Manage team information
- **Order Management**: Track and process orders
- **Business Insights**: Analytics and performance metrics

## 🏗️ Architecture

```
Helios AI Platform
├── Frontend (Next.js 14 + React 18 + TypeScript)
│   ├── Voice Recorder Component
│   ├── Video Chat Component
│   ├── Chat Interface
│   └── Dashboard Interface
├── Backend (FastAPI + Python 3.9+)
│   ├── Voice Routes (Whisper transcription)
│   ├── WebSocket Video Chat
│   ├── Business Service APIs
│   ├── Agent Orchestration
│   └── Database Layer (SQLAlchemy)
└── Infrastructure
    ├── Docker support
    ├── Environment configuration
    └── Database integration
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.9+
- **Docker** (optional)
- **API Keys**:
  - OpenAI API Key (for Whisper and voice features)
  - Anthropic API Key (optional, for Claude integration)
  - Google API Key (optional, for additional services)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Eunini/helios.git
cd helios
```

2. **Setup Environment Variables**

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Frontend
cp frontend/.env.example frontend/.env
# Edit frontend/.env if needed
```

3. **Install Backend Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

4. **Install Frontend Dependencies**

```bash
cd ../frontend
npm install
```

### Running Locally

**Terminal 1 - Start Backend Server:**

```bash
cd backend
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

**Terminal 2 - Start Frontend Dev Server:**

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 🐳 Docker Deployment

```bash
# Build and run with docker-compose
docker-compose up --build

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 📡 API Endpoints

### Voice API

- `POST /api/voice/transcribe` - Transcribe audio file
- `GET /api/voice/supported-formats` - Get supported audio formats

### Video Chat API

- `WS /api/ws/video-chat` - WebSocket for video chat
- `GET /api/ws/video-chat/sessions` - List active sessions
- `DELETE /api/ws/video-chat/sessions/{session_id}` - End session

### Business APIs

- `GET /api/agents` - List available agents
- `POST /api/tasks/` - Create new task
- `GET /api/business/customers` - Get customers
- `GET /api/business/inventory` - Get inventory status

## 🛠️ Configuration

### Backend Configuration (backend/core/config.py)

```python
# Voice Configuration
VOICE_ENABLED = True
VOICE_RATE_LIMIT_PER_MINUTE = 60
OPENAI_API_KEY = "sk-..."  # Your OpenAI API key

# Video Configuration
VIDEO_CHAT_ENABLED = True
WEBSOCKET_TIMEOUT = 300

# Database Configuration
DATABASE_URL = "sqlite:///./helios.db"
ENABLE_VECTOR_STORE = True
```

### Frontend Configuration (frontend/lib/api.ts)

The frontend automatically connects to:

- Voice endpoint: `/api/voice/transcribe`
- WebSocket endpoint: `ws://localhost:8000/api/ws/video-chat`
- Task endpoint: `/api/tasks/`

## 📦 Key Dependencies

### Frontend

- **Next.js 14**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Web APIs**: WebRTC, MediaRecorder, Web Speech API

### Backend

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM
- **WebSockets**: Real-time communication
- **OpenAI**: Whisper API integration
- **Pydantic**: Data validation

## 📚 Project Structure

```
helios/
├── frontend/                    # Next.js frontend app
│   ├── components/
│   │   ├── voice/              # Voice recorder component
│   │   ├── video/              # Video chat component
│   │   ├── dashboard/          # Dashboard components
│   │   └── ui/                 # UI component library
│   ├── app/                    # Next.js app router
│   └── lib/                    # Utilities and API helpers
├── backend/                    # FastAPI backend
│   ├── api/
│   │   ├── routes/            # API endpoint routes
│   │   │   ├── voice.py       # Voice transcription
│   │   │   ├── websocket_video.py  # Video chat
│   │   │   ├── agents.py      # Agent management
│   │   │   └── tasks.py       # Task management
│   │   └── main.py            # FastAPI app entry
│   ├── agents/                # AI agent implementations
│   ├── services/              # Business logic services
│   ├── memory/                # State and vector stores
│   ├── core/                  # Configuration and database
│   └── orchestrator/          # Workflow engine
├── docker-compose.yml          # Docker orchestration
└── README.md                   # This file
```

## 🔐 Security

- **Environment Variables**: Sensitive API keys stored in `.env`
- **CORS Protection**: Configured in FastAPI middleware
- **WebSocket Authentication**: Session-based authentication (extensible)
- **Input Validation**: Pydantic models for all inputs
- **Rate Limiting**: Per-minute and per-hour limits on voice features

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest tests/

# Run frontend tests (if configured)
cd ../frontend
npm test
```

## 📈 Performance

- **Voice Transcription**: ~2-5 seconds for typical messages
- **Video Streaming**: 1 FPS base with adaptive bitrate
- **WebSocket Latency**: <100ms typical round-trip
- **Database Queries**: Optimized with indexes and caching

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙋 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing documentation in `/docs` folder
- Review API documentation at `/docs/api` when backend is running

## 🔮 Roadmap

- [ ] Mobile app (React Native)
- [ ] Multi-language support enhancement
- [ ] Advanced analytics dashboard
- [ ] Custom agent training
- [ ] Integration with popular business tools
- [ ] Real-time collaboration features
- [ ] Advanced video codec support
- [ ] Machine learning model fine-tuning

## 📞 Contact

**Project Maintainer**: Helios AI Team
**GitHub**: https://github.com/Eunini/helios

---

**Made with ❤️ by the Helios AI Team**
