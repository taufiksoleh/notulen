#!/bin/bash

# Notulen Setup Script
# This script helps you get started with Notulen quickly

set -e

echo "🎙️  Welcome to Notulen Setup"
echo "================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Setup environment variables
echo "Setting up environment variables..."

# Backend .env
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "📝 Created backend/.env from template"
    echo ""
    echo "⚠️  Please edit backend/.env and configure your LLM provider:"
    echo ""
    echo "   RECOMMENDED: OpenRouter (30x cheaper, 100+ models)"
    echo "   - Set LLM_PROVIDER=openrouter"
    echo "   - Get API key from https://openrouter.ai/keys"
    echo "   - Set OPENROUTER_API_KEY=your_key"
    echo "   - Default model: deepseek/deepseek-chat (free/cheap)"
    echo ""
    echo "   OR use OpenAI:"
    echo "   - Set LLM_PROVIDER=openai"
    echo "   - Set OPENAI_API_KEY=your_key"
    echo ""
    echo "   OR use Anthropic:"
    echo "   - Set LLM_PROVIDER=anthropic"
    echo "   - Set ANTHROPIC_API_KEY=your_key"
    echo ""
    read -p "Press Enter to open backend/.env in your default editor..."
    ${EDITOR:-nano} backend/.env
else
    echo "✅ backend/.env already exists"
fi

# Frontend .env
if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "✅ Created frontend/.env from template"
else
    echo "✅ frontend/.env already exists"
fi

echo ""

# Ask if user wants to start with Docker
echo "Setup complete! 🎉"
echo ""
echo "Choose how to run Notulen:"
echo "1. Docker Compose (recommended)"
echo "2. Manual setup (development)"
echo "3. Exit"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Notulen with Docker Compose..."
        docker-compose up -d
        echo ""
        echo "✅ Notulen is running!"
        echo ""
        echo "Access the application:"
        echo "  Frontend: http://localhost:3000"
        echo "  Backend:  http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop:      docker-compose down"
        ;;
    2)
        echo ""
        echo "Manual setup instructions:"
        echo ""
        echo "Backend:"
        echo "  cd backend"
        echo "  python -m venv venv"
        echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
        echo "  pip install -r requirements.txt"
        echo "  uvicorn main:app --reload"
        echo ""
        echo "Frontend (in another terminal):"
        echo "  cd frontend"
        echo "  npm install"
        echo "  npm run dev"
        echo ""
        ;;
    3)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "Happy transcribing! 🚀"
