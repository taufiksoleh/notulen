.PHONY: help install dev stop clean test backend-* frontend-*

# Default target
help:
	@echo "Notulen Project Makefile"
	@echo "========================"
	@echo ""
	@echo "Full Stack Commands:"
	@echo "  install          - Install all dependencies (backend + frontend)"
	@echo "  dev              - Run both backend and frontend in development mode"
	@echo "  stop             - Stop all running services"
	@echo "  test             - Run all tests (backend + frontend)"
	@echo "  clean            - Clean all build artifacts"
	@echo "  docker-up        - Start backend with Docker"
	@echo "  docker-down      - Stop Docker containers"
	@echo ""
	@echo "Backend Commands (prefix: backend-):"
	@echo "  backend-install  - Install backend dependencies"
	@echo "  backend-dev      - Run backend development server"
	@echo "  backend-test     - Run backend tests"
	@echo "  backend-clean    - Clean backend artifacts"
	@echo "  backend-help     - Show all backend commands"
	@echo ""
	@echo "Frontend Commands (prefix: frontend-):"
	@echo "  frontend-install - Install frontend dependencies"
	@echo "  frontend-web     - Run frontend on web"
	@echo "  frontend-mobile  - Run frontend on mobile"
	@echo "  frontend-build   - Build frontend for production"
	@echo "  frontend-test    - Run frontend tests"
	@echo "  frontend-clean   - Clean frontend artifacts"
	@echo "  frontend-help    - Show all frontend commands"
	@echo ""
	@echo "Quick Start:"
	@echo "  make install     - First time setup"
	@echo "  make dev         - Start development (backend + frontend web)"
	@echo ""

# Install all dependencies
install: backend-install frontend-install
	@echo ""
	@echo "✓ All dependencies installed!"
	@echo "Run 'make dev' to start development"

# Run both backend and frontend
dev:
	@echo "Starting development environment..."
	@echo "Backend will start on http://localhost:8000"
	@echo "Frontend will start on http://localhost:XXXX"
	@echo ""
	@echo "Press Ctrl+C to stop"
	@trap 'make stop' INT; \
	(cd backend && make dev) & \
	sleep 3 && \
	(cd frontend && make run-web)

# Start backend with Docker and frontend
dev-docker:
	@echo "Starting backend with Docker..."
	cd backend && make docker-up
	@echo ""
	@echo "Waiting for backend to be ready..."
	@sleep 5
	@echo ""
	@echo "Starting frontend..."
	cd frontend && make run-web

# Stop all services
stop:
	@echo "Stopping all services..."
	@pkill -f "uvicorn" 2>/dev/null || true
	@pkill -f "flutter" 2>/dev/null || true
	@cd backend && make docker-down 2>/dev/null || true
	@echo "All services stopped"

# Run all tests
test: backend-test frontend-test
	@echo ""
	@echo "✓ All tests completed!"

# Clean all artifacts
clean: backend-clean frontend-clean
	@echo ""
	@echo "✓ All artifacts cleaned!"

# Docker commands
docker-up:
	cd backend && make docker-up

docker-down:
	cd backend && make docker-down

docker-logs:
	cd backend && make docker-logs

docker-build:
	cd backend && make docker-build

# Backend commands
backend-install:
	@echo "Installing backend dependencies..."
	cd backend && make install

backend-dev:
	cd backend && make dev

backend-test:
	@echo "Running backend tests..."
	cd backend && make test

backend-clean:
	@echo "Cleaning backend artifacts..."
	cd backend && make clean

backend-help:
	cd backend && make help

backend-format:
	cd backend && make format

backend-lint:
	cd backend && make lint

backend-models:
	cd backend && make download-models

# Frontend commands
frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && make install

frontend-web:
	cd frontend && make run-web

frontend-mobile:
	cd frontend && make run-mobile

frontend-android:
	cd frontend && make run-android

frontend-ios:
	cd frontend && make run-ios

frontend-build:
	cd frontend && make build-web

frontend-build-android:
	cd frontend && make build-android

frontend-build-ios:
	cd frontend && make build-ios

frontend-test:
	@echo "Running frontend tests..."
	cd frontend && make test

frontend-clean:
	@echo "Cleaning frontend artifacts..."
	cd frontend && make clean

frontend-help:
	cd frontend && make help

frontend-format:
	cd frontend && make format

frontend-analyze:
	cd frontend && make analyze

# Setup for first time
setup: install
	@echo ""
	@echo "Setting up project..."
	cd backend && cp .env.example .env 2>/dev/null || true
	@echo ""
	@echo "✓ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit backend/.env with your configuration"
	@echo "2. Update frontend API URL in frontend/lib/services/api_service.dart"
	@echo "3. Run 'make dev' to start development"

# Quick checks
status:
	@echo "Project Status:"
	@echo "==============="
	@echo ""
	@echo "Backend:"
	@curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1 && echo "  ✓ Running" || echo "  ✗ Not running"
	@echo ""
	@echo "Docker:"
	@docker ps | grep -q notulen && echo "  ✓ Running" || echo "  ✗ Not running"
	@echo ""
	@echo "Flutter:"
	@which flutter > /dev/null 2>&1 && echo "  ✓ Installed" || echo "  ✗ Not installed"
	@echo ""
	@echo "Python:"
	@python3 --version 2>&1 | head -1 || echo "  ✗ Not installed"

# Health check
health:
	@echo "Checking backend health..."
	@curl -s http://localhost:8000/api/v1/health | python3 -m json.tool || echo "Backend is not running"

# Format all code
format: backend-format frontend-format
	@echo "✓ All code formatted!"

# Lint all code
lint: backend-lint frontend-analyze
	@echo "✓ All code linted!"

# Pre-commit checks
check: format lint test
	@echo ""
	@echo "✓ All checks passed! Ready to commit."

# Build for production
build-all: frontend-build frontend-build-android
	@echo ""
	@echo "✓ Production builds completed!"
	@echo ""
	@echo "Outputs:"
	@echo "  Web:     frontend/build/web/"
	@echo "  Android: frontend/build/app/outputs/flutter-apk/app-release.apk"

# Deploy (assumes backend is on Docker)
deploy-local: docker-up frontend-build
	@echo ""
	@echo "✓ Local deployment ready!"
	@echo ""
	@echo "Backend:  http://localhost:8000"
	@echo "Frontend: Serve frontend/build/web/ with any static server"

# Show project info
info:
	@echo "Notulen - Indonesian Meeting Notes"
	@echo "===================================="
	@echo ""
	@echo "Backend:  FastAPI + Whisper + Wav2vec"
	@echo "Frontend: Flutter (Web + Mobile)"
	@echo ""
	@echo "Directories:"
	@echo "  backend/   - Python FastAPI server"
	@echo "  frontend/  - Flutter application"
	@echo ""
	@echo "Documentation:"
	@echo "  README.md                    - Main documentation"
	@echo "  backend/README.md            - Backend guide"
	@echo "  frontend/README.md           - Frontend guide"
	@echo "  SPEECH_TO_TEXT_RESEARCH.md   - STT research"
	@echo ""
	@echo "Run 'make help' for available commands"

# Count lines of code
loc:
	@echo "Lines of Code:"
	@echo "=============="
	@echo ""
	@echo "Backend:"
	@find backend/app -name "*.py" | xargs wc -l | tail -1
	@echo ""
	@echo "Frontend:"
	@find frontend/lib -name "*.dart" | xargs wc -l | tail -1
	@echo ""
	@echo "Total:"
	@find backend/app frontend/lib -name "*.py" -o -name "*.dart" | xargs wc -l | tail -1
