# Helios Architecture

## System Overview

Helios is a modern, cloud-native architecture designed for autonomous business operations management. The system uses a multi-agent AI framework with vector-based memory, event-driven orchestration, and a reactive frontend.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HELIOS SYSTEM ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ CLIENT TIER                                                          │
├──────────────────────────────────────────────────────────────────────┤
│  Next.js Frontend (http://localhost:3000)                            │
│  ├─ Landing Page (/)                                                │
│  ├─ Dashboard (/dashboard)                                          │
│  │  ├─ Real-time Metrics (Cash, Inventory, Sales, Customers)      │
│  │  ├─ Chat Interface (AI Interaction)                            │
│  │  └─ Recent Transactions                                        │
│  ├─ Inventory Management (/dashboard/inventory)                    │
│  ├─ Customer Management (/dashboard/customers)                     │
│  ├─ Staff Management (/dashboard/staff)                            │
│  └─ Business Insights (/dashboard/insights)                        │
└────────────────┬─────────────────────────────────────────────────────┘
                 │
          HTTP/REST + WebSocket
                 │
┌────────────────▼─────────────────────────────────────────────────────┐
│ API TIER                                                             │
├──────────────────────────────────────────────────────────────────────┤
│  FastAPI Application (http://localhost:8000)                        │
│  ├─ CORS Middleware (Development/Production)                       │
│  ├─ Authentication Middleware (API Key)                            │
│  └─ Routes                                                          │
│     ├─ /api/tasks/ (Task Submission & Management)                 │
│     ├─ /api/business/ (Business Data CRUD)                        │
│     │  ├─ /products, /customers, /staff, /transactions           │
│     │  └─ /reports, /state                                       │
│     └─ /api/agents/ (Agent Control & Monitoring)                 │
└────────────────┬─────────────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR TIER                                                      │
├────────────────────────────────────────────────────────────────────────┤
│  Task Manager                    │  Workflow Engine                    │
│  ├─ Task Queue (FIFO)           │  ├─ Multi-step Workflows          │
│  ├─ Agent Registry              │  ├─ Step Execution                │
│  ├─ Status Tracking             │  ├─ Error Handling                │
│  └─ Result Aggregation          │  └─ Execution History             │
└────────────────┬──────────────────────┬────────────────────────────────┘
                 │                      │
                 ▼                      ▼
┌──────────────────────────────────────────────────────────────────────┐
│ AGENT TIER                                                           │
├──────────────────────────────────────────────────────────────────────┤
│  Base Agent (Abstract Class)                                         │
│  ├─ PlannerAgent           (Task Analysis & Coordination)          │
│  ├─ OperationsAgent        (Inventory & Logistics)                 │
│  ├─ FinanceAgent           (Transactions & Cash Flow)              │
│  ├─ CommunicationsAgent    (Notifications & Messages)              │
│  └─ InsightAgent           (Analytics & Recommendations)           │
│                                                                      │
│  Each Agent:                                                        │
│  ├─ LLM Integration (Claude 3.5 Sonnet / Gemini)                  │
│  ├─ Memory Access (Vector Store)                                   │
│  ├─ Business Context (Database)                                    │
│  ├─ Execution Logging                                              │
│  └─ Error Handling                                                 │
└────────────────┬──────────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│ SERVICE TIER                                                         │
├──────────────────────────────────────────────────────────────────────┤
│  Business Services (Database Operations)                             │
│  ├─ InventoryService      (Products, Stock Management)             │
│  ├─ CustomerService       (Customer CRM)                           │
│  ├─ StaffService          (Employee Management)                    │
│  ├─ OrderService          (Transaction Processing)                 │
│  └─ ReportService         (Business Intelligence)                  │
│                                                                      │
│  Memory Services                                                     │
│  ├─ VectorStore           (Semantic Search via Chroma)             │
│  └─ StateStore            (Metrics Persistence)                    │
└────────────────┬──────────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│ DATA TIER                                                            │
├──────────────────────────────────────────────────────────────────────┤
│  Relational Database                                                 │
│  ├─ Products Table          (name, price, quantity, supplier)      │
│  ├─ Customers Table         (contact, purchase_history)            │
│  ├─ Staff Table             (role, performance, status)            │
│  ├─ Transactions Table      (items, amounts, payment)              │
│  ├─ BusinessMetrics Table   (snapshots for analytics)              │
│  └─ Tasks Table             (status, results, logs)                │
│                                                                      │
│  Vector Database (Chroma)                                           │
│  ├─ Product Documents       (embeddings for semantic search)       │
│  ├─ Customer Documents      (embeddings for recommendations)       │
│  ├─ Transaction Documents   (embeddings for pattern matching)      │
│  └─ Context Documents       (general business knowledge)           │
└────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Frontend Architecture

**Technology Stack:**

- Framework: Next.js 14 with App Router
- Language: TypeScript
- Styling: Tailwind CSS
- HTTP Client: Axios
- State: React Hooks + Client-side Fetching

**Component Hierarchy:**

```
App (Root Layout)
├── Landing Page
└── Dashboard
    ├── Sidebar (Navigation)
    ├── Header (User Info & Date)
    └── Main Content
        ├── Metrics Grid (StatsCards)
        ├── Chat Interface
        ├── Recent Transactions Table
        └── [Feature Pages: Inventory, Customers, Staff, Insights]
```

**Data Flow:**

1. User submits task in ChatInterface
2. Frontend calls `api.submitTask(description)`
3. Axios wrapper sends POST to `/api/tasks/`
4. Frontend polls `getTaskStatus(taskId)` every 1-2 seconds
5. Dashboard updates with real-time metrics via `getBusinessState()`
6. Auto-refresh on 30-second interval

### 2. Backend Architecture

**Technology Stack:**

- Framework: FastAPI 0.104+
- Language: Python 3.11+ with Type Hints
- ASGI Server: Uvicorn
- Database: SQLAlchemy ORM with SQLite/PostgreSQL
- LLM: LangChain with Claude 3.5 Sonnet
- Vector DB: Chromadb

**Request Flow:**

```
1. HTTP Request → FastAPI App
2. CORS Middleware → Validation
3. Auth Middleware → API Key Check
4. Route Handler → Service Call
5. Service Layer → Database Query
6. ORM → SQLAlchemy → Database
7. Response → JSON Serialization
```

**Task Processing Pipeline:**

```
1. POST /api/tasks/ {description, priority}
   ↓
2. TaskManager.submit_task()
   ├─ Create Task record (status: pending)
   ├─ Queue task (FIFO or priority)
   └─ Return {task_id, status}
   ↓
3. Frontend polls GET /api/tasks/{task_id}
   ↓
4. When task reaches front of queue:
   POST /api/tasks/process-next
   ↓
5. TaskManager.process_next_task()
   ├─ Retrieve task from queue
   ├─ Call PlannerAgent.execute(task)
   │  └─ Parse task → determine agents needed
   │  └─ Return plan {agents: [...], steps: [...]}
   ├─ Execute selected agents in sequence:
   │  ├─ OperationsAgent.execute() → update inventory
   │  ├─ FinanceAgent.execute() → record transaction
   │  └─ CommunicationsAgent.execute() → queue notifications
   ├─ Store results in database
   ├─ Update task status: completed
   └─ Return aggregated result
   ↓
6. Frontend receives result and displays to user
```

### 3. Agent Architecture

**Base Agent Pattern:**

```python
class BaseAgent:
    async def execute(task: Task) -> AgentResult:
        # 1. Retrieve business context from vector store
        context = retrieve_business_context()

        # 2. Build LLM prompt with context and task
        prompt = build_prompt(task, context)

        # 3. Call LLM for analysis/decision making
        llm_result = llm.invoke(prompt)

        # 4. Parse and validate result
        result = parse_result(llm_result)

        # 5. Execute business logic
        execute_business_logic(result)

        # 6. Store execution in memory
        store_memory(task, result)

        # 7. Return result with status
        return AgentResult(status, data, logs)
```

**Agent Specializations:**

| Agent               | Responsibility                    | Key Methods                        | LLM Task                               |
| ------------------- | --------------------------------- | ---------------------------------- | -------------------------------------- |
| PlannerAgent        | Task analysis, agent coordination | execute(), \_parse_plan()          | "Which agents needed for this task?"   |
| OperationsAgent     | Inventory operations              | execute(), \_process_inventory()   | "Parse inventory quantities from task" |
| FinanceAgent        | Transaction processing            | execute(), \_process_transaction() | "Extract financial details and type"   |
| CommunicationsAgent | Notifications                     | execute(), \_route_message()       | "Who should receive this message?"     |
| InsightAgent        | Analytics                         | execute(), \_analyze_metrics()     | "What insights from these metrics?"    |

### 4. Memory Architecture

**Vector Store (Chromadb):**

- Purpose: Semantic search and context retrieval
- Documents: Products, customers, transactions, business rules
- Query: Context-aware embeddings for agent decision-making
- Persistence: Disk-based for durability

**Example Query:**

```
Agent asks: "Find products similar to Sprite"
Vector search returns: [Coke, Fanta, Pepsi] with similarity scores
Agent uses: Top match for supplier/pricing decisions
```

**State Store (SQLAlchemy):**

- Purpose: Persistent business metrics snapshots
- Data: Daily cash, inventory value, sales count
- Retention: Historical data for trend analysis
- Query: Time-series aggregations for reports

### 5. Database Schema

**Core Tables:**

```
products
├─ id (UUID, PK)
├─ name (String)
├─ price (Decimal)
├─ quantity (Integer)
├─ supplier (String)
├─ reorder_level (Integer)
└─ category (String)

customers
├─ id (UUID, PK)
├─ name (String)
├─ email (String, UNIQUE)
├─ phone (String)
├─ total_purchases (Decimal)
├─ purchase_count (Integer)
└─ last_purchase_date (DateTime)

staff
├─ id (UUID, PK)
├─ name (String)
├─ role (String)
├─ email (String)
├─ status (Enum: active, inactive, on_leave)
├─ performance_rating (Float 0-5)
└─ hire_date (DateTime)

transactions
├─ id (UUID, PK)
├─ customer_id (FK)
├─ items (JSON: [{product_id, quantity, price}])
├─ subtotal (Decimal)
├─ tax (Decimal)
├─ total (Decimal)
├─ payment_method (String)
├─ created_at (DateTime)
└─ notes (Text)

business_metrics
├─ id (UUID, PK)
├─ date (Date)
├─ daily_cash (Decimal)
├─ inventory_value (Decimal)
├─ sales_count (Integer)
├─ transaction_count (Integer)
└─ created_at (DateTime)

tasks
├─ id (UUID, PK)
├─ description (Text)
├─ priority (Enum: low, normal, high, critical)
├─ status (Enum: pending, processing, completed, failed)
├─ result (JSON)
├─ created_at (DateTime)
└─ updated_at (DateTime)
```

## Data Flow Examples

### Example 1: Inventory Addition

```
User Input: "Received 100 bottles of Sprite from supplier ABC at N80 each"

1. Frontend: submitTask(description, "normal")
   → POST /api/tasks/

2. Backend: TaskManager queues task

3. Processing:
   PlannerAgent:
   ├─ Analyzes: "inventory addition + supplier"
   ├─ Determines: Need OperationsAgent + FinanceAgent
   └─ Returns: plan with agents and steps

   OperationsAgent:
   ├─ Parses: "100 bottles", "Sprite", "ABC supplier"
   ├─ Calls: InventoryService.add_stock("Sprite", 100)
   ├─ Updates: product.quantity = 100
   └─ Stores: "Received 100 Sprite" in vector memory

   FinanceAgent:
   ├─ Parses: "N80 each" = N8,000 total
   ├─ Calls: OrderService.create_transaction(supplier, N8000, expense)
   ├─ Updates: business_metrics.daily_cash -= 8000
   └─ Stores: "Expense: Sprite N8000" in memory

4. Result:
   {
     "status": "success",
     "agents_executed": ["OperationsAgent", "FinanceAgent"],
     "summary": "Added 100 Sprite bottles (N8,000). Inventory updated.",
     "metrics_updated": {
       "products": 1,
       "transactions": 1,
       "cash_impact": -8000
     }
   }

5. Frontend: Displays "✓ Added 100 Sprite bottles. Cash: ₦250,000 → ₦242,000"
```

### Example 2: Daily Report Generation

```
User: Clicks "Get Daily Report"

1. Frontend: getDailyReport()
   → GET /api/business/reports/daily

2. Backend: ReportService
   ├─ Queries: transactions from last 24 hours
   ├─ Aggregates: sales_count, total_revenue, avg_transaction
   ├─ Queries: inventory changes
   ├─ Queries: staff activity (if available)
   └─ Calculates: cash_position, margin

3. Database:
   SELECT COUNT(*) as sales_count,
          SUM(total) as total_revenue,
          AVG(total) as avg_transaction
   FROM transactions
   WHERE created_at >= NOW() - INTERVAL '1 day'

4. Result:
   {
     "date": "2024-01-15",
     "sales_summary": {
       "transaction_count": 45,
       "total_revenue": 125000,
       "avg_transaction": 2777.78
     },
     "inventory_summary": {
       "products_sold": 12,
       "items_sold": 156
     },
     "cash_summary": {
       "opening": 250000,
       "sales_in": 125000,
       "expenses_out": 45000,
       "closing": 330000
     }
   }

5. Frontend: Displays metrics in cards and chart
```

## Deployment Architecture

### Development

```
Localhost
├─ Backend: localhost:8000 (FastAPI + Uvicorn)
├─ Frontend: localhost:3000 (Next.js dev server)
└─ Database: SQLite (helios.db)
```

### Production

```
Cloud Infrastructure
├─ Backend (Railway.app)
│  ├─ Container: Python 3.11 + FastAPI
│  ├─ Database: PostgreSQL
│  └─ Domain: api.yourdomain.com
│
├─ Frontend (Vercel)
│  ├─ Edge: Global CDN
│  ├─ Build: Static optimization
│  └─ Domain: app.yourdomain.com
│
└─ Monitoring
   ├─ Logs: CloudWatch / Vercel Logs
   ├─ Errors: Sentry
   └─ Metrics: New Relic / Datadog
```

## Security Architecture

```
Request
├─ TLS/HTTPS (enforced in production)
├─ CORS Middleware (whitelist domains)
├─ Auth Middleware (API key or JWT)
├─ Input Validation (Pydantic models)
├─ SQL Injection Prevention (SQLAlchemy ORM)
└─ Rate Limiting (middleware-based)
```

## Scalability Considerations

### Horizontal Scaling

- Backend: Railway auto-scales containers
- Frontend: Vercel edge locations
- Database: PostgreSQL read replicas

### Vertical Scaling

- Increase Railway memory/CPU
- Optimize database indexes
- Cache frequently accessed data

### Queue Optimization

- Current: In-memory FIFO
- Future: Redis or AWS SQS for distributed queue
- Priority queue for critical tasks

## Monitoring & Observability

```
Application Metrics
├─ Request count & latency
├─ Error rates & types
├─ Database query performance
├─ Agent execution time
└─ Vector search latency

Business Metrics
├─ Daily cash position
├─ Inventory value
├─ Sales trends
├─ Customer metrics
└─ Staff performance

System Metrics
├─ CPU & memory usage
├─ Database connections
├─ API response times
└─ Error rates
```

## Integration Points

**External Services:**

- **Anthropic API**: Claude model calls
- **Google API**: Gemini model calls (fallback)
- **PostgreSQL**: Production database
- **Email Service**: Future notifications (SendGrid/AWS SES)
- **SMS Service**: Future notifications (Twilio)
- **Payment Gateway**: Future integration (Stripe/Paystack)

---

**Helios Architecture v1.0.0**

This architecture is designed for scalability, maintainability, and extensibility while supporting the core mission of automating retail operations through AI agents.
