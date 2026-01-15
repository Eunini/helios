# Requirements for Helios Development

## System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2 recommended)
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 10GB available space

## Software Requirements

### Backend

**Python Environment:**

- Python 3.11 or 3.12
- pip (Python package manager)
- virtualenv or venv

**Python Dependencies** (see `backend/requirements.txt`):

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
anthropic==0.7.6
google-generativeai==0.3.0
langchain==0.1.0
langchain-anthropic==0.1.1
langchain-google-genai==0.0.6
chromadb==0.4.18
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

**Optional:**

- PostgreSQL 15+ (for production)
- Docker & Docker Compose (for containerization)

### Frontend

**Node.js:**

- Node.js 18.x or later
- npm 9.x or later

**Node Dependencies** (see `frontend/package.json`):

```
next==14.0.4
react==18.2.0
react-dom==18.2.0
typescript==5.3.3
tailwindcss==3.4.1
autoprefixer==10.4.16
postcss==8.4.32
axios==1.6.2
next-auth==4.24.9
```

### Development Tools

**Code Quality:**

- ruff (Python linter)
- black (Python formatter)
- ESLint (JavaScript linter)
- Prettier (JavaScript formatter)

**Testing:**

- pytest (Python testing)
- jest (JavaScript testing - future)

**Version Control:**

- Git 2.x or later

## API Keys Required

1. **Anthropic API**

   - Sign up: https://console.anthropic.com
   - Get API key from console
   - Set in `ANTHROPIC_API_KEY` environment variable

2. **Google Generative AI**
   - Sign up: https://ai.google.dev
   - Get API key from console
   - Set in `GOOGLE_API_KEY` environment variable

Both are optional (at least one is required for AI features).

## Installation Steps

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL
```

## Verification

### Backend Verification

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Check imports work
python -c "from api.main import app; print('Backend OK')"

# Run tests
pytest tests/

# Start server
uvicorn api.main:app --reload
# Should see: "Uvicorn running on http://127.0.0.1:8000"
```

### Frontend Verification

```bash
cd frontend

# Check imports work
npm run type-check

# Build test
npm run build

# Start server
npm run dev
# Should see: "ready - started server on 0.0.0.0:3000"
```

## Docker Setup (Alternative)

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

### Verification

```bash
docker --version
docker-compose --version
```

### Start Services

```bash
docker-compose up
```

Services will be available at:

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Database: postgres://user:pass@db:5432/helios

## Environment Variables

### Backend (.env)

```
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=sqlite:///./helios.db
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
LOG_LEVEL=INFO
CHROMA_PERSIST_DIR=./chroma_db
ENABLE_VECTOR_STORE=True
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your_32_char_secret_here
NEXTAUTH_URL=http://localhost:3000
```

## Troubleshooting

### Python issues

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall packages
pip install -r requirements.txt --force-reinstall

# Check virtual environment
which python  # Should be in venv/
```

### Node issues

```bash
# Check Node version
node --version  # Should be 18+

# Clear npm cache
npm cache clean --force

# Reinstall packages
rm -rf node_modules package-lock.json
npm install
```

### Database issues

```bash
# Reset SQLite database
rm backend/helios.db

# Reinitialize
python -c "from core.database import init_db; init_db()"
```

### Port conflicts

```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process if needed
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

## Performance Tips

1. **Python Performance**

   - Use Python 3.12 for better performance
   - Enable caching in production

2. **Node Performance**

   - Use npm ci for CI/CD (instead of npm install)
   - Enable SWC for faster builds

3. **Database Performance**

   - Use PostgreSQL for production
   - Add proper indexes
   - Enable connection pooling

4. **Development**
   - Use hot reload (uvicorn --reload, npm run dev)
   - Run tests only for changed files
   - Use TypeScript strict mode for early error detection

## Next Steps

1. Complete initial setup with `./setup.sh` or `setup.bat`
2. Configure API keys in .env files
3. Start backend and frontend
4. Visit http://localhost:3000
5. Read QUICKSTART.md for first steps

## Support

- Documentation: See README.md and ARCHITECTURE.md
- API Docs: http://localhost:8000/docs (when running)
- Issues: Create GitHub issue
- Contact: support@helios.ai

---

**Requirements v1.0.0**
