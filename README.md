# SocialMediaPro

SocialMediaPro is an India-focused SaaS platform for SMBs to run Google Ads and Meta Ads from a single control panel with subscription billing via Razorpay.

## Architecture

- **Backend**: FastAPI + PostgreSQL + Redis + Celery
- **Frontend**: Next.js + Tailwind CSS
- **Infra**: Docker Compose for local, AWS ECS/RDS/ElastiCache for production
- **Security**: JWT auth, RBAC, AES-256-like symmetric encryption (Fernet/AES under the hood), webhook signature verification, auth rate limiting

## Repository Layout

- `backend/app/main.py` - API entrypoint
- `backend/app/api/` - routers/controllers
- `backend/app/services/` - application services
- `backend/app/repositories/` - DB access layer
- `backend/app/models/` - SQLAlchemy models
- `backend/app/schemas/` - request/response schemas
- `backend/app/oauth/` - OAuth callbacks for Google/Meta
- `backend/app/billing/` - billing domain package
- `backend/app/tasks/` - Celery jobs
- `frontend/pages/` - Next.js pages
- `frontend/components/` - shared UI components
- `frontend/services/` - HTTP clients
- `database/migrations/` - SQL migrations
- `docker/` - Docker artifacts
- `tests/` - backend unit tests

## Local Development

### 1) Prerequisites
- Docker + Docker Compose
- Node.js 20+
- Python 3.12+

### 2) Start backend stack
```bash
cd docker
docker compose up --build
```

### 3) Run frontend
```bash
cd frontend
npm install
npm run dev
```

Backend: `http://localhost:8000`  
Frontend: `http://localhost:3000`

## Environment Variables
Use `backend/.env.example` as base:
- JWT: `JWT_SECRET_KEY`, `ACCESS_TOKEN_EXP_MINUTES`, `REFRESH_TOKEN_EXP_MINUTES`
- Encryption: `TOKEN_ENCRYPTION_KEY` (32 bytes)
- Razorpay: `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`
- OAuth: Google + Meta client IDs/secrets/redirect URIs

## API Capabilities

- JWT signup/login/refresh
- Organization creation and RBAC role assignment (Owner/Admin/Analyst)
- OAuth token ingestion for Google Ads and Meta Marketing APIs (encrypted at rest)
- Campaign wizard launch endpoint with subscription enforcement
- Campaign pause/resume/edit status endpoint
- Reporting endpoint with normalized metrics
- Razorpay subscription creation + webhook validation
- Celery background reporting collector with retries

## AWS Deployment (Mumbai `ap-south-1`)

1. **Container Registry**: Push backend image to ECR.
2. **Compute**: Deploy API + worker on ECS Fargate (separate services).
3. **Database**: PostgreSQL on RDS (Multi-AZ for prod).
4. **Cache/Queue**: Redis via ElastiCache.
5. **Secrets**: Store env vars in AWS Secrets Manager; inject into ECS task definitions.
6. **Load Balancer**: ALB in front of API service with HTTPS cert from ACM.
7. **Frontend**: Deploy Next.js to Vercel or ECS/Amplify.
8. **Observability**: CloudWatch Logs, alarms for task failures and API 5xx.

## Staging Setup

- Separate AWS account or VPC namespace.
- Distinct RDS/Redis instances.
- `ENVIRONMENT=staging` and unique secrets.
- Enable sandbox Razorpay keys and test ad accounts.
- Run migration SQL from `database/migrations/001_initial.sql` before smoke tests.

## Testing

```bash
pip install -r backend/requirements.txt
PYTHONPATH=backend pytest -q tests/backend
```

## Notes

- Razorpay GST invoice generation is represented through transaction persistence and payload storage; invoice rendering can be expanded with a PDF service.
- Platform API payloads are implemented with realistic endpoint contracts and can be enriched with additional campaign/ad set/ad creative fields.
