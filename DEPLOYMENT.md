# Deployment Guide

Complete guide for deploying Helios to production environments.

## Overview

Helios is designed for deployment to:

- **Backend**: Railway.app (Python/FastAPI)
- **Frontend**: Vercel (Next.js)
- **Database**: PostgreSQL (managed)

## Prerequisites

- GitHub account and repository
- Railway.app account
- Vercel account
- API keys: Anthropic, Google
- Domain (optional)

## Backend Deployment (Railway.app)

### 1. Prepare Repository

```bash
# Ensure backend is in root backend/ folder
# Add Procfile for Railway
echo "web: cd backend && uvicorn api.main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

### 2. Connect to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init
```

### 3. Configure Environment

In Railway dashboard:

1. Go to Variables tab
2. Add environment variables:

```
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/helios
ANTHROPIC_API_KEY=sk-ant-xxxx
GOOGLE_API_KEY=xxxx
LOG_LEVEL=INFO
CHROMA_PERSIST_DIR=/tmp/chroma_db
ENABLE_VECTOR_STORE=True
API_HOST=0.0.0.0
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### 4. Deploy Database

```bash
# In Railway dashboard, add PostgreSQL plugin
# Note the connection string
# Set DATABASE_URL to connection string
```

### 5. Deploy Backend

```bash
# Push to GitHub (Railway integrates with GitHub)
git push origin main

# Or deploy directly
railway up
```

### 6. Configure Domain

```bash
# In Railway dashboard:
# Settings → Domains
# Add custom domain: api.yourdomain.com
```

## Frontend Deployment (Vercel)

### 1. Deploy from GitHub

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

Or use Vercel dashboard to import GitHub repository.

### 2. Environment Variables

In Vercel project settings:

```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXTAUTH_SECRET=min_32_character_secret_here
NEXTAUTH_URL=https://yourdomain.com
```

### 3. Configure Domain

```bash
# In Vercel dashboard:
# Settings → Domains
# Add yourdomain.com
# Follow DNS configuration
```

## Database Setup

### PostgreSQL on Railway

1. Add PostgreSQL plugin in Railway
2. Copy connection string
3. Set `DATABASE_URL` in Railway variables
4. Initialize schema:

```bash
# Connect to database
psql postgresql://user:pass@host:5432/helios

# Create schema (optional)
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO user;
```

### Initialize Data

```bash
# After deploying backend to Railway
railway shell

# Inside Railway shell
python -c "from core import init_db; init_db()"
```

## Environment Variables

### Backend (Railway)

| Variable           | Value                  | Example                    |
| ------------------ | ---------------------- | -------------------------- |
| ENVIRONMENT        | production             | production                 |
| DEBUG              | False                  | False                      |
| DATABASE_URL       | PostgreSQL connection  | postgresql://...           |
| ANTHROPIC_API_KEY  | From Anthropic console | sk-ant-...                 |
| GOOGLE_API_KEY     | From Google Cloud      | AIza...                    |
| LOG_LEVEL          | INFO or DEBUG          | INFO                       |
| CHROMA_PERSIST_DIR | Persistent directory   | /tmp/chroma_db             |
| ALLOW_ORIGINS      | Frontend domain        | https://app.yourdomain.com |

### Frontend (Vercel)

| Variable            | Value                | Example                    |
| ------------------- | -------------------- | -------------------------- |
| NEXT_PUBLIC_API_URL | Backend API URL      | https://api.yourdomain.com |
| NEXTAUTH_SECRET     | 32+ character secret | $(openssl rand -base64 32) |
| NEXTAUTH_URL        | Frontend domain      | https://app.yourdomain.com |

## Health Checks

### Backend Health

```bash
curl https://api.yourdomain.com/health
# Response: {"status":"healthy","timestamp":"2024-01-15T10:30:00Z"}
```

### Frontend Health

```bash
curl https://app.yourdomain.com
# Should return HTML homepage
```

## Monitoring & Logs

### Railway Logs

```bash
railway logs --follow
```

### Vercel Logs

```bash
vercel logs
```

### Application Monitoring

Monitor via:

- Railway dashboard analytics
- Vercel real-time analytics
- Application logs

## CI/CD Pipeline

### GitHub Actions

The `.github/workflows/ci.yml` runs on:

- Push to main or develop
- Pull requests

Pipeline:

1. Backend tests
2. Frontend build
3. Docker image build
4. Deploy to production (main branch only)

## Database Backups

### PostgreSQL Backups

```bash
# On Railway, use built-in backups
# Or manual backup:
pg_dump postgresql://user:pass@host:5432/helios > backup.sql

# Restore:
psql postgresql://user:pass@host:5432/helios < backup.sql
```

## Troubleshooting

### Backend won't start

```bash
# Check logs
railway logs

# Verify database connection
psql $DATABASE_URL -c "\l"

# Check environment variables
railway variables
```

### Frontend shows API errors

```bash
# Verify API URL
echo $NEXT_PUBLIC_API_URL

# Test backend connectivity
curl $NEXT_PUBLIC_API_URL/health
```

### Database connection issues

```bash
# Check PostgreSQL is running
# On Railway dashboard, verify PostgreSQL plugin is healthy

# Verify connection string
psql $DATABASE_URL
```

### Port conflicts

```bash
# Railway auto-assigns ports
# Vercel auto-assigns domains
# No manual configuration needed
```

## Performance Optimization

### Backend

```python
# Enable caching in production
CACHING_ENABLED=True
CACHE_TTL=3600

# Database connection pooling
DATABASE_POOL_SIZE=20
```

### Frontend

```
# Enable static optimization
NEXT_PUBLIC_STATIC_OPTIMIZATION=true

# Enable image optimization
IMAGES_DOMAIN=yourdomain.com
```

## Security

### Secrets Management

```bash
# Never commit .env files
# Use Railway/Vercel variable management
# Rotate secrets regularly
```

### HTTPS/TLS

- Railway auto-enables HTTPS
- Vercel auto-enables HTTPS
- Custom domains have SSL certificates

### API Security

```bash
# Implement API key authentication
# Use rate limiting
# Monitor for suspicious activity
```

## Cost Optimization

### Railway

- Free tier: $5/month credit
- Pay-as-you-go for additional usage
- Database included in free tier

### Vercel

- Free tier: unlimited deployments
- Pro: $20/month for priority support
- Function invocations: $0.50 per 1M

## Scaling

### Database Scaling

```sql
-- Add indexes
CREATE INDEX idx_products_supplier ON products(supplier);
CREATE INDEX idx_transactions_date ON transactions(created_at);
CREATE INDEX idx_customers_email ON customers(email);
```

### Application Scaling

- Railway auto-scales with traffic
- Vercel distributes across edge locations
- Add caching layer if needed

## Disaster Recovery

### Backup Strategy

1. Daily automatic backups (Railway)
2. Weekly manual backups to S3
3. Keep 30 days of backups

```bash
# Automated backup script
0 2 * * * pg_dump $DATABASE_URL | gzip > /backups/helios_$(date +\%Y\%m\%d).sql.gz
```

### Restore Procedure

1. Stop application
2. Restore from backup
3. Run database migrations
4. Start application

## Support

For deployment issues:

- Railway support: dashboard.railway.app/support
- Vercel support: vercel.com/support
- Helios docs: README.md

---

**Deployment Guide v1.0.0**
Last updated: 2024
