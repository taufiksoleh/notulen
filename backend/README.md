# Notulen Backend API

Speech-to-Text API for Indonesian Meeting Notes using OpenAI Whisper and Indonesian Wav2vec 2.0.

## Features

- **Hybrid STT Engine**: Supports both OpenAI Whisper and Indonesian Wav2vec 2.0
- **Automatic Language Detection**: Detects language and chooses the best model
- **LLM Post-Processing**: Generates summaries and extracts action items using GPT-4 or Claude
- **RESTful API**: Built with FastAPI
- **Database**: SQLite (default) or PostgreSQL support
- **Docker Ready**: Easy deployment with Docker

## Tech Stack

- **Framework**: FastAPI
- **STT Models**:
  - OpenAI Whisper (multilingual)
  - Indonesian Wav2vec 2.0 (Indonesian-specific, 4.27% WER)
- **LLM**: OpenAI GPT-4 or Anthropic Claude (optional)
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Audio Processing**: librosa, soundfile

## Installation

### Local Setup

1. **Clone the repository**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the server**:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**:
```bash
docker-compose up -d
```

2. **View logs**:
```bash
docker-compose logs -f
```

3. **Stop the service**:
```bash
docker-compose down
```

## Configuration

Edit `.env` file or set environment variables:

```env
# Database
DATABASE_URL=sqlite:///./data/notulen.db
# Or PostgreSQL: postgresql://user:password@localhost:5432/notulen

# API Keys (optional - for LLM summaries)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Model Settings
WHISPER_MODEL=base  # Options: tiny, base, small, medium, large, turbo
USE_INDONESIAN_MODEL=True

# Upload Settings
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=104857600  # 100MB
```

## API Endpoints

### Health Check
```http
GET /api/v1/health
```

### Create Meeting
```http
POST /api/v1/meetings
Content-Type: multipart/form-data

Fields:
- title (string, required)
- description (string, optional)
- audio_file (file, required)
- language (string, optional, default: "id")
- use_indonesian_model (boolean, optional, default: true)
```

### List Meetings
```http
GET /api/v1/meetings?skip=0&limit=100
```

### Get Meeting Details
```http
GET /api/v1/meetings/{meeting_id}
```

### Delete Meeting
```http
DELETE /api/v1/meetings/{meeting_id}
```

### Regenerate Summary
```http
POST /api/v1/meetings/{meeting_id}/regenerate-summary
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Models

### Whisper Models

| Model  | Size  | VRAM  | Speed | Best For |
|--------|-------|-------|-------|----------|
| tiny   | 39M   | ~1GB  | 10x   | Testing  |
| base   | 74M   | ~1GB  | 7x    | Development |
| small  | 244M  | ~2GB  | 4x    | Balanced |
| medium | 769M  | ~5GB  | 2x    | Production |
| turbo  | 809M  | ~6GB  | 8x    | Recommended |

### Indonesian Wav2vec 2.0

- **Model**: `indonesian-nlp/wav2vec2-large-xlsr-indonesian`
- **WER**: 4.27% (with language model)
- **Size**: ~1.2GB
- **Best for**: Pure Indonesian language meetings

## How It Works

1. **Upload**: Client uploads audio file via multipart form
2. **Language Detection**: System detects language using Whisper
3. **Transcription**:
   - If Indonesian → Use Indonesian Wav2vec (best accuracy)
   - If mixed/other → Use Whisper (multilingual)
4. **LLM Processing** (optional):
   - Generate summary
   - Extract action items
   - Identify key discussion points
5. **Response**: Return complete meeting data with transcription and summary

## Performance

### CPU Only
- Processing: ~5x real-time (5 min for 1 min audio)
- Suitable for development and low-volume usage

### GPU (Recommended for Production)
- Processing: Real-time or faster
- Recommended: NVIDIA GPU with 4GB+ VRAM
- Supports CUDA acceleration

## Deployment

### Production Checklist

1. **Use PostgreSQL** instead of SQLite
2. **Set DEBUG=False** in production
3. **Use strong SECRET_KEY**
4. **Enable HTTPS** (use reverse proxy like Nginx)
5. **Set proper CORS** origins (replace `allow_origins=["*"]`)
6. **Use GPU** for better performance
7. **Set up monitoring** and logging
8. **Backup database** regularly

### Recommended Hosting

- **CPU-only**: DigitalOcean, Railway, Render ($5-50/month)
- **GPU**: RunPod, Vast.ai, Modal.com ($0.05-0.10 per meeting)
- **Database**: Supabase, Railway (PostgreSQL)

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   └── config.py          # Configuration
│   ├── models/
│   │   ├── __init__.py        # Database setup
│   │   ├── meeting.py         # Meeting model
│   │   └── schemas.py         # Pydantic schemas
│   ├── services/
│   │   ├── stt_service.py     # Speech-to-Text
│   │   └── llm_service.py     # LLM summaries
│   └── main.py                # FastAPI app
├── uploads/                    # Audio files
├── data/                       # SQLite database
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Troubleshooting

### Model Download Issues

Models are downloaded automatically on first use. If you face issues:

```python
# Manually download Whisper model
import whisper
whisper.load_model("base")

# Manually download Indonesian model
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
Wav2Vec2Processor.from_pretrained("indonesian-nlp/wav2vec2-large-xlsr-indonesian")
Wav2Vec2ForCTC.from_pretrained("indonesian-nlp/wav2vec2-large-xlsr-indonesian")
```

### GPU Support

To enable GPU support with Docker:

```yaml
# Uncomment in docker-compose.yml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

### Memory Issues

If you encounter out-of-memory errors:
1. Use smaller Whisper model (tiny or base)
2. Set `USE_INDONESIAN_MODEL=False`
3. Process files in batches
4. Increase system swap space

## License

MIT License

## Credits

- **OpenAI Whisper**: https://github.com/openai/whisper
- **Indonesian Wav2vec 2.0**: https://github.com/indonesian-nlp/multilingual-asr
- **Research**: See `SPEECH_TO_TEXT_RESEARCH.md` in root directory
