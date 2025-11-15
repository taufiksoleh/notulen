# Contributing to Notulen

Thank you for considering contributing to Notulen! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help each other learn and grow

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/taufiksoleh/notulen/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check [Issues](https://github.com/taufiksoleh/notulen/issues) for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/taufiksoleh/notulen.git
   cd notulen
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests
   cd frontend
   npm test
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

   Commit message format:
   - `Add: new feature`
   - `Fix: bug description`
   - `Update: improvement description`
   - `Docs: documentation changes`
   - `Refactor: code refactoring`

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Link related issues

## Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8 mypy

# Run tests
pytest

# Format code
black .

# Lint
flake8 .
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Lint
npm run lint

# Format
npm run format
```

## Code Style

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Write docstrings for functions and classes
- Maximum line length: 100 characters

Example:
```python
def transcribe_audio(
    audio_path: str,
    language: str = "auto"
) -> Dict[str, Any]:
    """
    Transcribe audio file to text.

    Args:
        audio_path: Path to audio file
        language: Language code (default: "auto")

    Returns:
        Dictionary containing transcription results
    """
    ...
```

### TypeScript (Frontend)

- Use TypeScript strict mode
- Define interfaces for data structures
- Use functional components with hooks
- Follow React best practices

Example:
```typescript
interface Meeting {
  id: string
  title: string
  created_at: string
}

export default function MeetingsList({ onSelect }: Props) {
  const [meetings, setMeetings] = useState<Meeting[]>([])
  ...
}
```

## Testing

### Backend Tests

```python
# tests/test_transcription.py
import pytest
from services.transcription import TranscriptionService

def test_language_detection():
    service = TranscriptionService()
    result = service._detect_language("test_audio.mp3")
    assert result in ["id", "en", "ja"]
```

### Frontend Tests

```typescript
// components/__tests__/AudioRecorder.test.tsx
import { render, screen } from '@testing-library/react'
import AudioRecorder from '../AudioRecorder'

test('renders record button', () => {
  render(<AudioRecorder onComplete={() => {}} />)
  expect(screen.getByText('Start Recording')).toBeInTheDocument()
})
```

## Documentation

- Update README.md if adding features
- Add comments for complex logic
- Update API documentation
- Include examples for new features

## Review Process

1. Maintainers will review your PR
2. Address requested changes
3. Once approved, PR will be merged
4. Your contribution will be acknowledged

## Areas for Contribution

### High Priority
- [ ] Indonesian Wav2vec 2.0 integration
- [ ] Real-time streaming transcription
- [ ] Speaker diarization
- [ ] Mobile app (React Native)

### Medium Priority
- [ ] Export to PDF/DOCX
- [ ] Calendar integration
- [ ] Team collaboration features
- [ ] Custom model fine-tuning

### Good First Issues
- [ ] UI/UX improvements
- [ ] Documentation improvements
- [ ] Test coverage
- [ ] Bug fixes

## Questions?

- Open an issue for questions
- Join discussions in GitHub Discussions
- Email: [your-email@example.com]

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in documentation

Thank you for contributing to Notulen! 🚀
