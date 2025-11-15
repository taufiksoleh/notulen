# Deployment Guide

This guide covers various deployment options for Notulen.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Cloud Deployment](#cloud-deployment)
3. [Production Considerations](#production-considerations)
4. [Scaling](#scaling)

## Docker Deployment

### Local Docker

The simplest way to deploy Notulen is using Docker Compose.

```bash
# 1. Clone the repository
git clone https://github.com/taufiksoleh/notulen.git
cd notulen

# 2. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 3. Build and start
docker-compose up -d

# 4. Check logs
docker-compose logs -f

# 5. Stop services
docker-compose down
```

### Production Docker Setup

For production, create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - WHISPER_MODEL=turbo
      - LLM_PROVIDER=openai
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - backend-data:/app/data
    restart: always
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdom ain.com
    restart: always
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: always

volumes:
  backend-data:
```

### OpenRouter Configuration (Recommended)

OpenRouter is the **recommended LLM provider** for Notulen due to its:
- **30x cheaper** than OpenAI GPT-4
- **100+ models** to choose from
- **Free tier** available for testing
- **Excellent Indonesian language support**

#### Getting Started with OpenRouter

1. **Get API Key**:
   - Visit https://openrouter.ai/keys
   - Sign up for a free account
   - Generate an API key
   - Add credits (free tier available)

2. **Configure Environment**:
   ```bash
   # In your backend/.env file
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=sk-or-v1-... # Your API key from https://openrouter.ai/keys
   OPENROUTER_MODEL=deepseek/deepseek-r1-0528-qwen3-8b:free  # Default model (free)
   ```

3. **Recommended Models**:

   | Model | Cost/1M tokens | Best For | Indonesian Support |
   |-------|----------------|----------|-------------------|
   | `deepseek/deepseek-r1-0528-qwen3-8b:free` | FREE | Default, general use | ⭐⭐⭐⭐⭐ |
   | `deepseek/deepseek-chat` | $0.14 input / $0.28 output | Budget-friendly, reliable | ⭐⭐⭐⭐⭐ |
   | `meta-llama/llama-3.3-70b-instruct` | $0.35 input / $0.40 output | High quality summaries | ⭐⭐⭐⭐ |
   | `qwen/qwen-2.5-72b-instruct` | $0.35 input / $0.40 output | Indonesian meetings | ⭐⭐⭐⭐⭐ |
   | `google/gemini-2.0-flash-exp:free` | FREE | Testing, development | ⭐⭐⭐ |

   Full model list: https://openrouter.ai/models

4. **Cost Estimation**:
   - Average meeting (1 hour, 10k words): ~$0.02-0.05
   - OpenAI GPT-4 equivalent: ~$0.60-1.50
   - **Savings: 95%+ for most workloads**

#### OpenRouter Production Configuration

Update your `docker-compose.prod.yml` to use OpenRouter:

```yaml
services:
  backend:
    environment:
      - WHISPER_MODEL=turbo
      - LLM_PROVIDER=openrouter
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - OPENROUTER_MODEL=${OPENROUTER_MODEL:-deepseek/deepseek-r1-0528-qwen3-8b:free}
      # Keep other providers as fallback options
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    # ... rest of config
```

#### Troubleshooting OpenRouter

1. **Invalid API Key**:
   ```bash
   # Verify your key starts with 'sk-or-v1-'
   echo $OPENROUTER_API_KEY

   # Test the API
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer $OPENROUTER_API_KEY"
   ```

2. **Insufficient Credits**:
   - Check balance: https://openrouter.ai/credits
   - Add credits or use free tier models
   - Free models: `google/gemini-2.0-flash-exp:free`

3. **Model Not Available**:
   - Check current models: https://openrouter.ai/models
   - Some models require minimum credit balance
   - Fallback to `deepseek/deepseek-r1-0528-qwen3-8b:free` or `deepseek/deepseek-chat`

4. **Slow Responses**:
   - Try a different model (some are faster)
   - Check OpenRouter status: https://status.openrouter.ai
   - Consider caching summaries for identical transcriptions

## Cloud Deployment

### Option 1: Vercel (Frontend) + Railway (Backend)

**Frontend on Vercel:**

```bash
cd frontend
npm install -g vercel
vercel login
vercel
```

Configure environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: Your backend URL

**Backend on Railway:**

1. Go to https://railway.app
2. Create new project
3. Connect your GitHub repository
4. Select `backend` directory
5. Add environment variables:
   - `WHISPER_MODEL=turbo`
   - `LLM_PROVIDER=openrouter` (recommended)
   - `OPENROUTER_API_KEY=your_openrouter_key`
   - `OPENROUTER_MODEL=deepseek/deepseek-r1-0528-qwen3-8b:free`
   - `OPENAI_API_KEY=your_key` (optional fallback)
   - `DATABASE_PATH=/app/data/notulen.db`
6. Deploy

### Option 2: Modal.com (Serverless GPU)

Create `backend/modal_deploy.py`:

```python
import modal

stub = modal.Stub("notulen")

image = modal.Image.debian_slim().pip_install(
    "fastapi",
    "uvicorn",
    "openai-whisper",
    "transformers",
    "torch",
)

@stub.function(
    image=image,
    gpu="T4",  # Or A10G for better performance
    timeout=600,
)
def transcribe(audio_bytes: bytes):
    import whisper
    model = whisper.load_model("turbo")
    # Process audio
    ...

@stub.asgi_app()
def fastapi_app():
    from main import app
    return app
```

Deploy:
```bash
modal deploy backend/modal_deploy.py
```

### Option 3: DigitalOcean App Platform

1. Create `app.yaml`:

```yaml
name: notulen
services:
  - name: backend
    github:
      repo: taufiksoleh/notulen
      branch: main
      deploy_on_push: true
    source_dir: backend
    dockerfile_path: backend/Dockerfile
    envs:
      - key: WHISPER_MODEL
        value: turbo
      - key: LLM_PROVIDER
        value: openrouter
      - key: OPENROUTER_API_KEY
        type: SECRET
      - key: OPENROUTER_MODEL
        value: deepseek/deepseek-r1-0528-qwen3-8b:free
      - key: OPENAI_API_KEY
        type: SECRET
    health_check:
      http_path: /health
    instance_count: 1
    instance_size_slug: professional-m

  - name: frontend
    github:
      repo: taufiksoleh/notulen
      branch: main
      deploy_on_push: true
    source_dir: frontend
    build_command: npm install && npm run build
    run_command: npm start
    envs:
      - key: NEXT_PUBLIC_API_URL
        value: ${backend.PUBLIC_URL}
    instance_count: 1
    instance_size_slug: basic-xs
```

2. Deploy via DigitalOcean CLI:
```bash
doctl apps create --spec app.yaml
```

### Option 4: AWS (ECS + Fargate)

**Prerequisites:**
- AWS account
- AWS CLI configured
- Docker images pushed to ECR

**Steps:**

1. Push images to ECR:
```bash
# Backend
aws ecr create-repository --repository-name notulen-backend
docker build -t notulen-backend ./backend
docker tag notulen-backend:latest {account-id}.dkr.ecr.{region}.amazonaws.com/notulen-backend:latest
docker push {account-id}.dkr.ecr.{region}.amazonaws.com/notulen-backend:latest

# Frontend
aws ecr create-repository --repository-name notulen-frontend
docker build -t notulen-frontend ./frontend
docker tag notulen-frontend:latest {account-id}.dkr.ecr.{region}.amazonaws.com/notulen-frontend:latest
docker push {account-id}.dkr.ecr.{region}.amazonaws.com/notulen-frontend:latest
```

2. Create ECS task definitions and services via AWS Console or Terraform

## Production Considerations

### Security

1. **API Keys**: Never commit API keys to git
   ```bash
   # Use environment variables
   export OPENAI_API_KEY="sk-..."
   ```

2. **CORS**: Configure proper CORS origins
   ```python
   # backend/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],  # Not "*"
       allow_credentials=True,
       allow_methods=["GET", "POST", "DELETE"],
       allow_headers=["*"],
   )
   ```

3. **HTTPS**: Always use HTTPS in production
   - Use Let's Encrypt for free SSL certificates
   - Configure nginx as reverse proxy

4. **Rate Limiting**: Implement rate limiting
   ```python
   from slowapi import Limiter

   limiter = Limiter(key_func=get_remote_address)

   @app.post("/api/transcribe")
   @limiter.limit("10/hour")
   async def transcribe_audio(...):
       ...
   ```

### Database

1. **SQLite to PostgreSQL**: For production, use PostgreSQL

   ```python
   # backend/models/database.py
   import os
   from sqlalchemy import create_engine

   DATABASE_URL = os.getenv(
       "DATABASE_URL",
       "postgresql://user:password@localhost/notulen"
   )

   engine = create_engine(DATABASE_URL)
   ```

2. **Backups**: Set up automatic backups
   ```bash
   # Cron job for PostgreSQL backups
   0 2 * * * pg_dump notulen > /backups/notulen_$(date +\%Y\%m\%d).sql
   ```

### Monitoring

1. **Application Monitoring**: Use Sentry for error tracking
   ```python
   import sentry_sdk

   sentry_sdk.init(
       dsn="your-sentry-dsn",
       traces_sample_rate=1.0,
   )
   ```

2. **Performance Monitoring**: Use Prometheus + Grafana

3. **Logging**: Structured logging with context
   ```python
   import structlog

   logger = structlog.get_logger()
   logger.info("transcription_started", meeting_id=meeting_id)
   ```

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Use nginx or cloud load balancer
   ```nginx
   upstream backend {
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   ```

2. **Async Task Queue**: For long-running transcriptions
   ```python
   # Use Celery + Redis
   from celery import Celery

   celery_app = Celery('notulen', broker='redis://localhost:6379')

   @celery_app.task
   def transcribe_task(audio_path):
       # Process transcription
       ...
   ```

### GPU Scaling

For intensive workloads:

1. **Auto-scaling GPU instances** (AWS, GCP)
2. **Serverless GPU** (Modal.com, Banana.dev)
3. **Batch processing** for non-real-time transcriptions

### Cost Optimization

1. **Model Caching**: Keep models in memory
2. **Batch Processing**: Process multiple files together
3. **On-Demand GPU**: Only use GPU when needed
4. **CDN**: Use Cloudflare or similar for frontend

```python
# Example: Model singleton
class TranscriptionService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_models()
        return cls._instance
```

## Monitoring Checklist

- [ ] Set up error tracking (Sentry)
- [ ] Configure logging aggregation
- [ ] Set up uptime monitoring
- [ ] Configure performance monitoring
- [ ] Set up database backups
- [ ] Configure alerts for critical failures
- [ ] Monitor API rate limits
- [ ] Track costs (cloud services)

## Environment-Specific Configs

**Quick Start for Production:**

Use the provided `.env.production` template:

```bash
cp .env.production backend/.env
# Edit backend/.env with your production values
```

### Development
```env
DEBUG=true
WHISPER_MODEL=base  # Faster for dev
LOG_LEVEL=DEBUG
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
```

### Staging
```env
DEBUG=false
WHISPER_MODEL=turbo
LOG_LEVEL=INFO
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
```

### Production
```env
DEBUG=false
WHISPER_MODEL=turbo
LOG_LEVEL=WARNING
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_production_key
OPENROUTER_MODEL=deepseek/deepseek-r1-0528-qwen3-8b:free
SENTRY_DSN=your_sentry_dsn
```

## Troubleshooting

### Common Issues

1. **Out of Memory**
   - Reduce Whisper model size
   - Increase Docker memory limits
   - Use GPU instead of CPU

2. **Slow Transcription**
   - Use GPU
   - Use smaller Whisper model
   - Implement async processing

3. **Database Locked**
   - Switch from SQLite to PostgreSQL
   - Reduce concurrent writes

---

For specific deployment questions, please open an issue on GitHub.
