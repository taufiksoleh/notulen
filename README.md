# Notulen - Indonesian Meeting Notes with AI

Open-source meeting notes application with automatic transcription and AI-powered summaries for Indonesian language meetings.

## Overview

Notulen is a full-stack application that provides:
- **Speech-to-Text**: Automatic transcription using state-of-the-art AI models
- **Smart Summaries**: AI-generated meeting summaries and action items
- **Cross-Platform**: Flutter app supporting Web, Android, and iOS
- **Indonesian-First**: Optimized for Indonesian language with 4.27% WER (better than Google!)

## Project Structure

```
notulen/
├── backend/              # FastAPI backend with STT models
│   ├── app/
│   │   ├── api/         # REST API endpoints
│   │   ├── models/      # Database models
│   │   ├── services/    # STT and LLM services
│   │   └── main.py      # FastAPI app
│   ├── Dockerfile
│   └── README.md
├── frontend/            # Flutter mobile & web app
│   ├── lib/
│   │   ├── models/      # Data models
│   │   ├── screens/     # UI screens
│   │   ├── services/    # API & audio services
│   │   └── main.dart    # App entry point
│   ├── pubspec.yaml
│   └── README.md
└── SPEECH_TO_TEXT_RESEARCH.md  # Research & recommendations
```

## Features

### Backend (Python/FastAPI)

- **Hybrid STT Engine**:
  - OpenAI Whisper for multilingual support
  - Indonesian Wav2vec 2.0 for superior Indonesian accuracy (4.27% WER)
  - Automatic language detection and model selection
- **LLM Integration**:
  - OpenAI GPT-4 or Anthropic Claude for summaries
  - Automatic action item extraction
  - Key discussion points identification
- **RESTful API**: Complete CRUD operations for meetings
- **Database**: SQLite (dev) or PostgreSQL (prod)
- **Docker Ready**: Easy deployment with Docker Compose

### Frontend (Flutter)

- **Cross-Platform**: Single codebase for Web, Android, iOS
- **Audio Recording**: Built-in audio recorder
- **File Upload**: Support for MP3, WAV, M4A, OGG, FLAC, WebM
- **Real-time UI**: See transcription status in real-time
- **Rich Display**: View transcripts, summaries, and action items
- **Material Design 3**: Modern, beautiful UI

## Quick Start

### Prerequisites

- **Backend**: Python 3.11+, pip
- **Frontend**: Flutter 3.0+
- **Optional**: Docker & Docker Compose, Make

### Using Makefile (Easiest)

The project includes Makefiles for easy development:

```bash
# First time setup
make setup

# Start development (backend + frontend)
make dev

# Or start backend with Docker + frontend
make dev-docker

# View all available commands
make help
```

**Common Commands:**
```bash
make install           # Install all dependencies
make dev               # Run both backend and frontend
make test              # Run all tests
make clean             # Clean all build artifacts
make docker-up         # Start backend with Docker
make frontend-web      # Run frontend on web only
make backend-dev       # Run backend only
make status            # Check project status
```

### Option 1: Docker (Recommended)

```bash
# Backend only
cd backend
docker-compose up -d
# or: make docker-up (from root)

# Access API at http://localhost:8000
```

### Option 2: Manual Setup

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# or: make dev (from backend directory)
```

**Frontend:**

```bash
cd frontend
flutter pub get
flutter pub run build_runner build
flutter run -d chrome  # For web
# or: make run-web (from frontend directory)
```

## Architecture

### How It Works

```
┌─────────────────┐
│  Flutter App    │
│  (Web/Mobile)   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────────────────────┐
│      FastAPI Backend            │
│  ┌──────────────────────────┐  │
│  │   Upload Audio File       │  │
│  └───────────┬──────────────┘  │
│              ▼                  │
│  ┌──────────────────────────┐  │
│  │  Language Detection       │  │
│  │  (Whisper tiny)           │  │
│  └───────────┬──────────────┘  │
│              ▼                  │
│     ┌────────┴────────┐        │
│     │                 │        │
│     ▼                 ▼        │
│ ┌────────┐      ┌──────────┐  │
│ │  ID?   │      │ Mixed/EN?│  │
│ │        │      │          │  │
│ │Wav2vec │      │ Whisper  │  │
│ │4.27 WER│      │ Turbo    │  │
│ └───┬────┘      └────┬─────┘  │
│     │                │        │
│     └────────┬───────┘        │
│              ▼                 │
│  ┌──────────────────────────┐ │
│  │  LLM Post-Processing     │ │
│  │  - Summary               │ │
│  │  - Action Items          │ │
│  │  - Key Points            │ │
│  └──────────────────────────┘ │
└─────────────────────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI (Python web framework)
- OpenAI Whisper (multilingual STT)
- HuggingFace Transformers (Indonesian Wav2vec)
- SQLAlchemy (ORM)
- OpenAI/Anthropic APIs (LLM summaries)

**Frontend:**
- Flutter 3.0+ (cross-platform framework)
- Riverpod (state management)
- record/flutter_sound (audio recording)
- http/dio (API client)

## Performance

### STT Model Comparison (Indonesian)

| Model | WER | Speed | Cost | Offline |
|-------|-----|-------|------|---------|
| **Indonesian Wav2vec** | **4.27%** ⭐ | 2x | $0 | ✅ |
| **Whisper Turbo** | ~8-12% | 1x | $0 | ✅ |
| Google STT | 9.22% | 1x | $0.024/min | ❌ |

**WER = Word Error Rate** (lower is better)

### Resource Requirements

**Development (CPU):**
- Processing: ~5x real-time
- RAM: 8GB recommended
- Storage: 2GB for models

**Production (GPU):**
- Processing: Real-time or faster
- GPU: NVIDIA 4GB+ VRAM
- RAM: 8GB+
- Storage: 3GB for models

## Deployment

### Backend Deployment Options

1. **Development**: Local or DigitalOcean ($5-10/month)
2. **Production CPU**: Railway, Render ($20-50/month)
3. **Production GPU**: RunPod, Vast.ai, Modal.com ($0.05-0.10/meeting)

### Frontend Deployment Options

1. **Web**: Vercel, Netlify, Firebase Hosting (Free - $5/month)
2. **Mobile**: Google Play Store, Apple App Store

## Cost Analysis

### Self-Hosted (Recommended)

**Development:**
- CPU Server: $10-20/month
- ~1000 meetings/month capacity

**Production:**
- GPU on-demand: ~$0.05-0.10 per meeting
- 1000 meetings: ~$50-100/month

**Much cheaper than cloud APIs and better accuracy for Indonesian!**

## Configuration

### Backend (.env)

```env
DATABASE_URL=sqlite:///./data/notulen.db
OPENAI_API_KEY=your_key_here  # Optional
ANTHROPIC_API_KEY=your_key_here  # Optional
WHISPER_MODEL=base
USE_INDONESIAN_MODEL=True
```

### Frontend

Edit `lib/services/api_service.dart`:
```dart
ApiService({this.baseUrl = 'http://YOUR_BACKEND_URL:8000/api/v1'});
```

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend Development

```bash
cd frontend
flutter pub get
flutter run
```

Hot reload enabled for fast development.

## Testing

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
flutter test
```

## Documentation

- **Research**: `SPEECH_TO_TEXT_RESEARCH.md` - Detailed STT model comparison
- **Backend**: `backend/README.md` - API documentation
- **Frontend**: `frontend/README.md` - Flutter app guide

## API Documentation

Interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Roadmap

### MVP (Current)
- [x] Backend API with STT
- [x] Flutter mobile & web app
- [x] Audio recording
- [x] Transcription
- [x] LLM summaries

### Phase 2
- [ ] Real-time streaming transcription
- [ ] Speaker diarization (multiple speakers)
- [ ] Export to PDF/DOCX
- [ ] Search functionality
- [ ] User authentication

### Phase 3
- [ ] Meeting collaboration
- [ ] Calendar integration
- [ ] Meeting templates
- [ ] Analytics dashboard
- [ ] Mobile offline mode

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Research

This project is based on comprehensive research of open-source STT solutions. See `SPEECH_TO_TEXT_RESEARCH.md` for:

- Detailed model comparisons
- Performance benchmarks
- Cost analysis
- Implementation recommendations

**Key Finding**: Indonesian Wav2vec 2.0 achieves **4.27% WER**, which is **54% better** than Google Speech-to-Text (9.22% WER) for Indonesian language!

## License

MIT License - see LICENSE file for details

## Credits

- **OpenAI Whisper**: https://github.com/openai/whisper
- **Indonesian NLP**: https://github.com/indonesian-nlp/multilingual-asr
- **HuggingFace**: Model hosting and transformers library
- **Flutter**: Cross-platform framework

## Support

- **Documentation**: See README files in backend/ and frontend/
- **Issues**: Create an issue on GitHub
- **Research**: Read SPEECH_TO_TEXT_RESEARCH.md

## Acknowledgments

Special thanks to:
- Indonesian NLP community for the Wav2vec model
- OpenAI for Whisper
- HuggingFace for model hosting
- All open-source contributors

---

**Built with ❤️ for the Indonesian community**

For questions or support, please open an issue on GitHub.
