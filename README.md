# Notulen - Indonesian Meeting Note Taker

AI-powered meeting notes application with advanced speech-to-text capabilities optimized for Indonesian language.

## Features

- **Hybrid Speech-to-Text Engine**
  - Indonesian Wav2vec 2.0 for pure Indonesian (4.27% WER - better than Google STT!)
  - OpenAI Whisper Turbo for multilingual support
  - Automatic language detection and intelligent model routing

- **AI-Powered Summaries**
  - Automatic meeting summarization using GPT-4, Claude, or OpenRouter
  - OpenRouter support: Access 100+ AI models (DeepSeek, Llama, Qwen, Gemini, etc.)
  - Budget-friendly: Free tier + pay-as-you-go (30x cheaper than OpenAI!)
  - Action item extraction
  - Key points identification

- **Flexible Recording Options**
  - Real-time audio recording in browser
  - Audio file upload support (MP3, WAV, M4A, WebM)
  - Timestamped transcriptions

- **Modern UI**
  - Clean, responsive interface built with Next.js 14
  - Real-time transcription progress
  - Easy meeting management

## Architecture

```
┌─────────────────────────────────────┐
│   Frontend (Next.js 14)             │
│   - Audio Recording                 │
│   - File Upload                     │
│   - Meeting Management              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Backend (FastAPI)                 │
│   - STT Processing                  │
│   - LLM Integration                 │
│   - Database Management             │
└──────────────┬──────────────────────┘
               │
         ┌─────┴─────┐
         │           │
         ▼           ▼
┌──────────────┐  ┌──────────────────┐
│  Indonesian  │  │ Whisper Turbo    │
│  Wav2vec 2.0 │  │ (Multilingual)   │
└──────────────┘  └──────────────────┘
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- API key for summaries (choose one):
  - **OpenRouter** (Recommended) - Free tier + very cheap pay-as-you-go
  - OpenAI - Premium quality
  - Anthropic Claude - Good balance

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/taufiksoleh/notulen.git
   cd notulen
   ```

2. **Set up environment variables**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your API keys

   # Frontend
   cp frontend/.env.example frontend/.env
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run the server
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Run development server
npm run dev
```

## Configuration

### Backend Environment Variables

```env
# Whisper Model (tiny, base, small, medium, large, turbo)
WHISPER_MODEL=turbo

# LLM Provider (openai, anthropic, or openrouter)
LLM_PROVIDER=openrouter

# OpenRouter (RECOMMENDED for budget) - Get key at https://openrouter.ai/keys
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat  # Free tier available!
# Other models: meta-llama/llama-3.3-70b-instruct, qwen/qwen-2.5-72b-instruct

# OpenAI (if using OpenAI)
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Anthropic (if using Claude)
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Database
DATABASE_PATH=data/notulen.db
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

### Transcription
```
POST /api/transcribe
- Upload audio file for transcription
- Supports: MP3, WAV, M4A, WebM
- Returns: Transcription with timestamps
```

### Summarization
```
POST /api/summarize
- Generate AI summary for a meeting
- Extracts action items and key points
```

### Meetings Management
```
GET  /api/meetings          - List all meetings
GET  /api/meetings/{id}     - Get meeting details
DELETE /api/meetings/{id}   - Delete a meeting
```

### Health Check
```
GET /health                 - Service health status
```

## Performance

Based on the research in [SPEECH_TO_TEXT_RESEARCH.md](SPEECH_TO_TEXT_RESEARCH.md):

| Model | WER | Speed | Best For |
|-------|-----|-------|----------|
| Indonesian Wav2vec 2.0 | **4.27%** | 2x real-time | Pure Indonesian |
| Whisper Turbo | ~8-12% | Real-time | Multilingual |
| Google STT | 9.22% | Real-time | Cloud API |

## Cost Estimates

### Self-Hosted (Recommended)
- Development: $48/month (CPU-only server)
- Production: $170/month (GPU on-demand)
- Serverless GPU: $0.05-0.10 per meeting

### With LLM APIs (Per Meeting Summary)
- **OpenRouter (DeepSeek)**: ~$0.001-0.01 per summary ⭐ **CHEAPEST!**
- **OpenRouter (Llama/Qwen)**: ~$0.003-0.015 per summary
- OpenAI GPT-4: ~$0.02-0.05 per summary
- Anthropic Claude: ~$0.01-0.03 per summary

### OpenRouter Free Tier
- 50 free requests/day (no credit card)
- 1,000 requests/day after $10 one-time purchase
- Free models: DeepSeek V3, Gemini 2.0 Flash, and more!

## Deployment

### Docker Deployment (Recommended)

```bash
# Production build
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Cloud Deployment Options

**Frontend (Vercel)**
```bash
cd frontend
vercel deploy
```

**Backend Options:**
- Railway.app (Easy deployment)
- Render.com (Free tier available)
- Modal.com (Serverless GPU)
- RunPod (GPU instances)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guides.

## Development

### Project Structure

```
notulen/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── services/
│   │   ├── transcription.py    # STT service
│   │   └── llm_processor.py    # LLM integration
│   ├── models/
│   │   └── database.py         # Database models
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # Main page
│   │   ├── layout.tsx         # Layout
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── AudioRecorder.tsx  # Recording component
│   │   ├── FileUploader.tsx   # Upload component
│   │   ├── MeetingsList.tsx   # Meetings list
│   │   └── MeetingView.tsx    # Meeting details
│   ├── lib/
│   │   └── api.ts             # API client
│   └── package.json
├── docker-compose.yml
└── README.md
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Technology Stack

- **Frontend**: Next.js 14, React, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python 3.11
- **STT Models**: Whisper, Indonesian Wav2vec 2.0
- **LLM**: OpenRouter (100+ models), OpenAI GPT-4, or Anthropic Claude
- **Database**: SQLite (upgradable to PostgreSQL)
- **Deployment**: Docker, Docker Compose

## Roadmap

### Phase 1: MVP (Current) ✅
- [x] Basic transcription (Whisper)
- [x] Audio recording and upload
- [x] Meeting storage
- [x] AI summaries

### Phase 2: Enhanced Features
- [ ] Indonesian Wav2vec 2.0 integration
- [ ] Real-time streaming transcription
- [ ] Speaker diarization
- [ ] Multiple language support in one meeting

### Phase 3: Enterprise Features
- [ ] User authentication
- [ ] Team collaboration
- [ ] Custom model fine-tuning
- [ ] Export to PDF/DOCX
- [ ] Calendar integration

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Research

This project is based on comprehensive research of open-source STT solutions. See [SPEECH_TO_TEXT_RESEARCH.md](SPEECH_TO_TEXT_RESEARCH.md) for detailed analysis.

## Support

- GitHub Issues: https://github.com/taufiksoleh/notulen/issues
- Documentation: https://github.com/taufiksoleh/notulen/wiki

## Acknowledgments

- OpenAI Whisper team
- Indonesian NLP community
- Hugging Face for model hosting
- Meta AI for Wav2vec 2.0

---

Built with ❤️ for the Indonesian tech community
