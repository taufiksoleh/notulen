# Makefile Quick Reference Guide

This project includes comprehensive Makefiles to simplify development. Here's a quick reference.

## 🚀 Quick Start

```bash
# First time setup
make setup

# Start development (backend + frontend)
make dev

# View all available commands
make help
```

## 📋 Root Makefile Commands

Run these from the project root directory:

### Essential Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make setup` | First-time project setup |
| `make install` | Install all dependencies (backend + frontend) |
| `make dev` | Start both backend and frontend in development mode |
| `make dev-docker` | Start backend with Docker + frontend |
| `make stop` | Stop all running services |
| `make test` | Run all tests (backend + frontend) |
| `make clean` | Clean all build artifacts |
| `make status` | Check what's running |

### Docker Commands

| Command | Description |
|---------|-------------|
| `make docker-up` | Start backend with Docker Compose |
| `make docker-down` | Stop Docker containers |
| `make docker-logs` | View Docker logs |
| `make docker-build` | Build Docker images |

### Backend Commands

| Command | Description |
|---------|-------------|
| `make backend-install` | Install backend dependencies |
| `make backend-dev` | Run backend development server |
| `make backend-test` | Run backend tests |
| `make backend-clean` | Clean backend artifacts |
| `make backend-format` | Format backend code |
| `make backend-lint` | Lint backend code |
| `make backend-models` | Download STT models |
| `make backend-help` | Show all backend commands |

### Frontend Commands

| Command | Description |
|---------|-------------|
| `make frontend-install` | Install frontend dependencies |
| `make frontend-web` | Run frontend on Chrome |
| `make frontend-mobile` | Run frontend on mobile device |
| `make frontend-android` | Run frontend on Android |
| `make frontend-ios` | Run frontend on iOS |
| `make frontend-build` | Build frontend for web production |
| `make frontend-build-android` | Build Android APK |
| `make frontend-test` | Run frontend tests |
| `make frontend-clean` | Clean frontend artifacts |
| `make frontend-format` | Format frontend code |
| `make frontend-help` | Show all frontend commands |

### Utility Commands

| Command | Description |
|---------|-------------|
| `make health` | Check backend health |
| `make format` | Format all code (backend + frontend) |
| `make lint` | Lint all code |
| `make check` | Run all pre-commit checks |
| `make build-all` | Build for production (all platforms) |
| `make info` | Show project information |
| `make loc` | Count lines of code |

## 🔧 Backend Makefile Commands

Run these from the `backend/` directory:

### Development

```bash
make install        # Install dependencies
make dev            # Run development server with auto-reload
make run            # Run production server
make shell          # Open Python shell with app context
```

### Testing

```bash
make test           # Run tests
make test-cov       # Run tests with coverage report
```

### Code Quality

```bash
make format         # Format code with black
make lint           # Lint code with flake8
```

### Docker

```bash
make docker-build   # Build Docker image
make docker-up      # Start Docker containers
make docker-down    # Stop Docker containers
make docker-logs    # View Docker logs
make docker-shell   # Open shell in container
```

### Models

```bash
make download-models # Download Whisper and Wav2vec models
```

### Database

```bash
make migrate        # Run database migrations
make migrate-create # Create new migration
```

### Utilities

```bash
make clean          # Clean cache and temporary files
make health         # Check API health
make setup          # Complete first-time setup
```

## 📱 Frontend Makefile Commands

Run these from the `frontend/` directory:

### Development

```bash
make install        # Install dependencies
make get            # Get Flutter packages
make build-runner   # Generate code
make dev            # Start with watch mode
```

### Running

```bash
make run-web        # Run on Chrome
make run-android    # Run on Android
make run-ios        # Run on iOS
make run-mobile     # Run on any connected device
```

### Building

```bash
make build-web          # Build for web production
make build-android      # Build Android APK
make build-appbundle    # Build Android App Bundle
make build-ios          # Build for iOS
make build-all          # Build for all platforms
```

### Testing

```bash
make test           # Run tests
make test-cov       # Run tests with coverage
```

### Code Quality

```bash
make format         # Format Dart code
make analyze        # Analyze Dart code
make lint           # Run analyzer + format check
```

### Utilities

```bash
make clean          # Clean build artifacts
make clean-all      # Clean everything including packages
make doctor         # Run flutter doctor
make upgrade        # Upgrade dependencies
make devices        # List connected devices
```

### Deployment

```bash
make deploy-web     # Build and get deployment instructions
```

## 💡 Common Workflows

### First Time Setup

```bash
# From project root
make setup
# Edit backend/.env with your settings
# Edit frontend/lib/services/api_service.dart with backend URL
```

### Daily Development

```bash
# Option 1: Run everything
make dev

# Option 2: Backend with Docker + Frontend
make dev-docker

# Option 3: Run separately
cd backend && make dev          # Terminal 1
cd frontend && make run-web     # Terminal 2
```

### Before Committing

```bash
make check          # Format, lint, and test everything
```

### Testing

```bash
# Test everything
make test

# Test backend only
make backend-test

# Test frontend only
make frontend-test
```

### Building for Production

```bash
# Build everything
make build-all

# Build web only
make frontend-build

# Build Android only
make frontend-build-android
```

### Docker Development

```bash
# Start backend with Docker
make docker-up

# View logs
make docker-logs

# Stop containers
make docker-down
```

## 🎯 Pro Tips

1. **Use `make help`** - Every Makefile has a help command showing all available targets

2. **Tab completion** - Most shells support tab completion for Makefile targets

3. **Parallel execution** - `make -j4` runs targets in parallel (use with caution)

4. **Silent mode** - `make -s` for less verbose output

5. **Dry run** - `make -n target` shows what would be executed without running

6. **Check status** - Use `make status` to see what's currently running

7. **Quick health check** - `make health` to verify backend is responding

8. **Model downloads** - Run `make backend-models` once to pre-download STT models

## 📝 Notes

- All Makefiles include a `help` target - run `make help` in any directory
- Commands are designed to be intuitive and consistent across directories
- Most commands handle errors gracefully and provide helpful messages
- Docker commands automatically handle container lifecycle
- Build commands create production-ready artifacts

## 🔍 Troubleshooting

**Command not found:**
```bash
# Install make (Ubuntu/Debian)
sudo apt-get install build-essential

# Install make (macOS)
xcode-select --install

# Install make (Windows)
# Use WSL or install Make for Windows
```

**Port already in use:**
```bash
make stop          # Stop all services
make status        # Check what's running
```

**Models not downloading:**
```bash
cd backend
make download-models
```

**Flutter build errors:**
```bash
cd frontend
make clean
make get
make build-runner
```

**Backend not starting:**
```bash
cd backend
make clean
make install
make dev
```

## 📚 More Information

- **Root README**: `README.md`
- **Backend README**: `backend/README.md`
- **Frontend README**: `frontend/README.md`
- **Research**: `SPEECH_TO_TEXT_RESEARCH.md`

For the complete list of commands, run:
```bash
make help                    # Root
cd backend && make help      # Backend
cd frontend && make help     # Frontend
```
