#!/bin/bash
# Helios Setup Script for Development

set -e

echo "=================================="
echo "Helios Development Setup"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [[ $python_version == 3.11* ]] || [[ $python_version == 3.12* ]]; then
    echo -e "${GREEN}✓ Python $python_version found${NC}"
else
    echo "❌ Python 3.11+ required (found $python_version)"
    exit 1
fi

# Check Node version
echo -e "${YELLOW}Checking Node.js version...${NC}"
node_version=$(node --version 2>&1 | cut -d'v' -f2 | cut -d'.' -f1)

if [[ $node_version -ge 18 ]]; then
    echo -e "${GREEN}✓ Node.js $(node --version) found${NC}"
else
    echo "❌ Node.js 18+ required"
    exit 1
fi

# Backend Setup
echo -e "${YELLOW}Setting up backend...${NC}"
cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Copy env file if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env with your API keys${NC}"
fi

# Initialize database
echo "Initializing database..."
python -c "from core.database import init_db; init_db()"
echo -e "${GREEN}✓ Database initialized${NC}"

cd ..

# Frontend Setup
echo -e "${YELLOW}Setting up frontend...${NC}"
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install > /dev/null 2>&1 || npm install

# Copy env file if not exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file from template..."
    cp .env.example .env.local
    echo -e "${YELLOW}⚠ Please edit frontend/.env.local with your API URL${NC}"
fi

cd ..

echo ""
echo -e "${GREEN}=================================="
echo "Setup Complete!"
echo "==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys:"
echo "   - ANTHROPIC_API_KEY=your_key"
echo "   - GOOGLE_API_KEY=your_key"
echo ""
echo "2. Edit frontend/.env.local with your API URL:"
echo "   - NEXT_PUBLIC_API_URL=http://localhost:8000"
echo ""
echo "3. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   uvicorn api.main:app --reload"
echo ""
echo "4. In another terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "5. Open http://localhost:3000 in your browser"
echo ""
echo "For Docker setup, run:"
echo "   docker-compose up"
echo ""
