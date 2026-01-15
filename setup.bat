@echo off
REM Helios Setup Script for Development (Windows)

echo ==================================
echo Helios Development Setup
echo ==================================

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.11+
    exit /b 1
)

REM Check Node version
echo Checking Node.js version...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found. Please install Node.js 18+
    exit /b 1
)

REM Backend Setup
echo.
echo Setting up backend...
cd backend

REM Create virtual environment if not exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt

REM Copy env file if not exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Warning: Please edit backend\.env with your API keys
)

REM Initialize database
echo Initializing database...
python -c "from core.database import init_db; init_db()"
echo Database initialized

cd ..

REM Frontend Setup
echo.
echo Setting up frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

REM Copy env file if not exists
if not exist ".env.local" (
    echo Creating .env.local file from template...
    copy .env.example .env.local
    echo Warning: Please edit frontend\.env.local with your API URL
)

cd ..

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Next steps:
echo 1. Edit backend\.env with your API keys:
echo    - ANTHROPIC_API_KEY=your_key
echo    - GOOGLE_API_KEY=your_key
echo.
echo 2. Edit frontend\.env.local with your API URL:
echo    - NEXT_PUBLIC_API_URL=http://localhost:8000
echo.
echo 3. Start the backend:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    uvicorn api.main:app --reload
echo.
echo 4. In another terminal, start the frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 5. Open http://localhost:3000 in your browser
echo.
echo For Docker setup, run:
echo    docker-compose up
echo.
