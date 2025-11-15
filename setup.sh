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
    echo "🤖 Configure your LLM provider"
    echo "================================"
    echo ""
    echo "Choose your LLM provider:"
    echo "1. OpenRouter (RECOMMENDED - Free tier, 100+ models, excellent Indonesian)"
    echo "2. OpenAI (GPT-4)"
    echo "3. Anthropic (Claude)"
    echo "4. Skip (configure manually later)"
    echo ""
    read -p "Enter your choice (1-4): " llm_choice

    case $llm_choice in
        1)
            echo ""
            echo "🌟 OpenRouter Setup"
            echo "==================="
            echo ""
            echo "OpenRouter Benefits:"
            echo "  • FREE model available (deepseek-r1-0528-qwen3-8b:free)"
            echo "  • 30x cheaper than OpenAI for paid models"
            echo "  • Excellent Indonesian language support"
            echo "  • 100+ models to choose from"
            echo ""
            echo "Get your API key from: https://openrouter.ai/keys"
            echo "(Press Ctrl+C to cancel if you need to get an API key first)"
            echo ""
            read -p "Enter your OpenRouter API key (sk-or-v1-...): " openrouter_key

            if [ ! -z "$openrouter_key" ]; then
                sed -i "s/LLM_PROVIDER=.*/LLM_PROVIDER=openrouter/" backend/.env
                sed -i "s/OPENROUTER_API_KEY=.*/OPENROUTER_API_KEY=$openrouter_key/" backend/.env
                echo ""
                echo "✅ OpenRouter configured successfully!"
                echo "   Using model: deepseek/deepseek-r1-0528-qwen3-8b:free (FREE)"
                echo ""
                echo "💡 Tip: You can change the model later in backend/.env"
                echo "   Popular models:"
                echo "   • deepseek/deepseek-r1-0528-qwen3-8b:free (free)"
                echo "   • deepseek/deepseek-chat (cheap, excellent)"
                echo "   • qwen/qwen-2.5-72b-instruct (best for Indonesian)"
            else
                echo "⚠️  No API key entered. You'll need to configure it manually."
            fi
            ;;
        2)
            echo ""
            echo "🔑 OpenAI Setup"
            echo "==============="
            echo ""
            echo "Get your API key from: https://platform.openai.com/api-keys"
            echo ""
            read -p "Enter your OpenAI API key (sk-...): " openai_key

            if [ ! -z "$openai_key" ]; then
                sed -i "s/LLM_PROVIDER=.*/LLM_PROVIDER=openai/" backend/.env
                sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$openai_key/" backend/.env
                echo ""
                echo "✅ OpenAI configured successfully!"
                echo "   Using model: gpt-4-turbo-preview"
            else
                echo "⚠️  No API key entered. You'll need to configure it manually."
            fi
            ;;
        3)
            echo ""
            echo "🔑 Anthropic Setup"
            echo "=================="
            echo ""
            echo "Get your API key from: https://console.anthropic.com/settings/keys"
            echo ""
            read -p "Enter your Anthropic API key (sk-ant-...): " anthropic_key

            if [ ! -z "$anthropic_key" ]; then
                sed -i "s/LLM_PROVIDER=.*/LLM_PROVIDER=anthropic/" backend/.env
                sed -i "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$anthropic_key/" backend/.env
                echo ""
                echo "✅ Anthropic configured successfully!"
                echo "   Using model: claude-3-5-sonnet-20241022"
            else
                echo "⚠️  No API key entered. You'll need to configure it manually."
            fi
            ;;
        4)
            echo ""
            echo "⏭️  Skipping LLM configuration"
            echo "   You can configure it later by editing backend/.env"
            ;;
        *)
            echo ""
            echo "⚠️  Invalid choice. Skipping LLM configuration."
            echo "   You can configure it later by editing backend/.env"
            ;;
    esac
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
