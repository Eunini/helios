# Helios Backend API

An AI-powered autonomous operations manager for small retail businesses in emerging markets.

## Overview

Helios Backend is a production-grade FastAPI application that coordinates multiple AI agents to automate business operations including inventory management, financial tracking, customer service, and business intelligence.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Vector Store**: Chromadb
- **LLM**: Claude 3.5 Sonnet (Anthropic) / Gemini (Google)
- **Agent Framework**: LangChain + LangGraph
- **Task Queue**: In-memory (can be extended with Celery/Redis)

## Project Structure

```
backend/
├── agents/              # AI agent implementations
│   ├── base_agent.py   # Abstract agent class
│   ├── planner_agent.py
│   ├── operations_agent.py
│   ├── finance_agent.py
│   ├── communications_agent.py
│   └── insight_agent.py
├── orchestrator/        # Task coordination
│   ├── task_manager.py  # Queue and routing
│   └── workflow_engine.py
├── memory/             # Data and vector store
│   ├── business_model.py   # Pydantic/SQLAlchemy models
│   ├── vector_store.py     # Chroma integration
│   └── state_store.py      # Business state persistence
├── services/           # Business logic
│   ├── inventory_service.py
│   ├── customer_service.py
│   ├── staff_service.py
│   ├── order_service.py
│   └── report_service.py
├── api/               # FastAPI endpoints
│   ├── main.py        # App entry point
│   ├── routes/
│   │   ├── tasks.py
│   │   ├── business.py
│   │   └── agents.py
│   └── middleware/
│       └── auth.py
├── core/              # Configuration and utilities
│   ├── config.py
│   ├── logger.py
│   └── database.py
├── tests/             # Unit tests
├── requirements.txt
└── Dockerfile
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or Poetry
- (Optional) PostgreSQL for production

### Setup Steps

1. **Clone and navigate to backend**

```bash
cd backend
```

2. **Create virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

5. **Initialize database**

```bash
python -c "from core import init_db; init_db()"
```

6. **Run development server**

```bash
uvicorn api.main:app --reload
```

Server will start at http://localhost:8000

## API Documentation

### Interactive Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health Check

```bash
GET /health
```

### Task Management

#### Submit Task

```bash
POST /api/tasks/
{
  "description": "Add 50 bottles of Coke, N100 each",
  "priority": "normal"  # low, normal, high, critical
}
```

#### Get Task Status

```bash
GET /api/tasks/{task_id}
```

#### Get Queue Status

```bash
GET /api/tasks/queue/status
```

#### Process Next Task

```bash
POST /api/tasks/process-next
```

### Business Data

#### Products (Inventory)

**Create Product**

```bash
POST /api/business/products
{
  "name": "Coca-Cola",
  "price": 100,
  "quantity": 50,
  "reorder_level": 10,
  "supplier": "ABC Distributor",
  "category": "Beverages"
}
```

**List Products**

```bash
GET /api/business/products?category=Beverages
```

**Add Stock**

```bash
POST /api/business/products/{product_id}/add-stock?quantity=20
```

**Get Low Stock Products**

```bash
GET /api/business/products/low-stock
```

#### Customers

**Create Customer**

```bash
POST /api/business/customers
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+234801234567"
}
```

**List Customers**

```bash
GET /api/business/customers
```

**Get Top Customers**

```bash
GET /api/business/customers/top?limit=10
```

#### Staff

**Create Staff Member**

```bash
POST /api/business/staff
{
  "name": "Jane Smith",
  "role": "cashier",
  "email": "jane@example.com",
  "status": "active"
}
```

**List Staff**

```bash
GET /api/business/staff?status=active
```

#### Transactions

**Create Transaction**

```bash
POST /api/business/transactions
{
  "customer_id": "cust-123",
  "customer_name": "John Doe",
  "items": [
    {
      "product_id": "prod-1",
      "product_name": "Coca-Cola",
      "quantity": 2,
      "unit_price": 100,
      "total": 200
    }
  ],
  "subtotal": 200,
  "tax": 20,
  "total": 220,
  "payment_method": "cash"
}
```

**List Transactions**

```bash
GET /api/business/transactions?limit=100
```

### Business State & Reports

**Get Current Business State**

```bash
GET /api/business/state
```

**Get Daily Summary**

```bash
GET /api/business/reports/daily
```

**Get Comprehensive Report**

```bash
GET /api/business/reports/comprehensive
```

**Get Inventory Report**

```bash
GET /api/business/reports/inventory
```

**Get Customer Report**

```bash
GET /api/business/reports/customers
```

### Agents

**List Agents**

```bash
GET /api/agents/
```

**Get Agent Status**

```bash
GET /api/agents/{agent_name}
```

**Get Queue Status**

```bash
GET /api/agents/queue/status
```

## Agent System

### Overview

The agent system consists of 5 specialized agents that work together:

#### 1. PlannerAgent

- Analyzes incoming tasks
- Determines which agents are needed
- Creates execution plan
- Routes to appropriate agents

#### 2. OperationsAgent

- Manages inventory updates
- Processes stock movements
- Handles logistics
- Tracks product flow

#### 3. FinanceAgent

- Records financial transactions
- Manages cash flow
- Tracks expenses and revenue
- Updates financial state

#### 4. CommunicationsAgent

- Notifies customers
- Alerts staff
- Sends messages
- Manages notifications

#### 5. InsightAgent

- Analyzes business data
- Generates recommendations
- Identifies trends
- Provides intelligence

### Workflow Example

```
User Input: "We received 100 bottles of Sprite from ABC, N80 each"

1. PlannerAgent analyzes:
   - Identifies as inventory + financial transaction
   - Plans execution: OperationsAgent + FinanceAgent

2. OperationsAgent executes:
   - Updates inventory (add 100 Sprite)
   - Logs to vector memory
   - Returns operation status

3. FinanceAgent executes:
   - Records N8,000 expense
   - Updates cash flow
   - Returns financial status

4. System response:
   - Stores in database
   - Updates vector memory
   - Returns combined result to user
```

## Memory System

### Vector Store (Chroma)

Stores business context for semantic search:

- Product information
- Customer history
- Transaction patterns
- Business insights
- Operation logs

### State Store

Persists business state:

- Product inventory
- Customer data
- Staff information
- Transaction history
- Financial metrics

## Configuration

### Environment Variables

```
# API
ENVIRONMENT=development|production
DEBUG=True|False
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR

# Database
DATABASE_URL=sqlite:///./helios.db  # or postgresql://...

# LLM
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048

# Vector Store
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION_NAME=helios_business_memory

# Features
ENABLE_VECTOR_STORE=True
ENABLE_WEBSOCKETS=True
MAX_TASK_QUEUE_SIZE=100
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_agents.py::test_planner_agent_initialization
```

## Production Deployment

### Docker

```bash
# Build image
docker build -t helios-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/helios \
  -e ANTHROPIC_API_KEY=your_key \
  helios-backend
```

### Railway Deployment

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Create project
railway init

# Deploy
railway up
```

### Environment for Production

1. Switch to PostgreSQL
2. Use environment variables for secrets
3. Enable CORS for production domain
4. Disable DEBUG mode
5. Set up monitoring and logging

## Troubleshooting

### LLM API Issues

**Error**: `ANTHROPIC_API_KEY not found`

- Solution: Add API key to .env file

### Database Issues

**Error**: `database is locked`

- Solution: Close other connections; use PostgreSQL for production

### Vector Store Issues

**Error**: `No module named chromadb`

- Solution: `pip install chromadb`

## Development

### Code Style

Code follows:

- Black formatting
- Ruff linting
- Type hints

```bash
# Format code
black .

# Lint
ruff check .

# Fix linting issues
ruff check . --fix
```

### Adding New Endpoints

1. Create service class in `services/`
2. Add Pydantic model in `memory/business_model.py`
3. Create route in `api/routes/`
4. Import and include router in `api/main.py`

## API Response Format

### Success Response

```json
{
  "status": "success",
  "data": { ... }
}
```

### Error Response

```json
{
  "detail": "Error message"
}
```

## License

Proprietary - Helios AI

## Support

For issues and questions, contact: support@helios.ai
