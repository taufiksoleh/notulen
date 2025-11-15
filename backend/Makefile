.PHONY: help install dev test clean docker-build docker-up docker-down docker-logs format lint

# Default target
help:
	@echo "Backend Makefile Commands:"
	@echo "=========================="
	@echo "install          - Install Python dependencies"
	@echo "dev              - Run development server with auto-reload"
	@echo "run              - Run production server"
	@echo "test             - Run tests"
	@echo "test-cov         - Run tests with coverage"
	@echo "format           - Format code with black"
	@echo "lint             - Lint code with flake8"
	@echo "clean            - Clean up cache and temporary files"
	@echo "docker-build     - Build Docker image"
	@echo "docker-up        - Start Docker containers"
	@echo "docker-down      - Stop Docker containers"
	@echo "docker-logs      - View Docker logs"
	@echo "docker-shell     - Open shell in Docker container"
	@echo "download-models  - Download STT models"
	@echo "migrate          - Run database migrations"
	@echo "shell            - Open Python shell with app context"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-cov httpx black flake8 isort

# Run development server
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run production server
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

# Format code
format:
	black app/
	isort app/

# Lint code
lint:
	flake8 app/ --max-line-length=100 --exclude=__pycache__,*.pyc
	black --check app/

# Clean cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f data/*.db 2>/dev/null || true
	@echo "Cleaned cache and temporary files"

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "Backend is running at http://localhost:8000"
	@echo "API docs at http://localhost:8000/docs"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec api /bin/bash

docker-restart:
	docker-compose restart

# Download models
download-models:
	@echo "Downloading Whisper model..."
	python -c "import whisper; whisper.load_model('base')"
	@echo "Downloading Indonesian Wav2vec model..."
	python -c "from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC; \
		Wav2Vec2Processor.from_pretrained('indonesian-nlp/wav2vec2-large-xlsr-indonesian'); \
		Wav2Vec2ForCTC.from_pretrained('indonesian-nlp/wav2vec2-large-xlsr-indonesian')"
	@echo "Models downloaded successfully!"

# Database migrations (if using alembic)
migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

# Python shell with app context
shell:
	python -i -c "from app.main import app; from app.models import *; from app.core.config import settings"

# Setup everything for first time
setup: install
	mkdir -p uploads data
	cp .env.example .env
	@echo "Setup complete! Edit .env file with your configuration."
	@echo "Run 'make dev' to start the development server."

# Check health
health:
	@curl -s http://localhost:8000/api/v1/health | python -m json.tool || echo "Server is not running"

# Watch logs in development
logs:
	tail -f logs/*.log 2>/dev/null || echo "No logs found"
