# Troubleshooting Guide

This guide helps you resolve common issues when setting up and running Notulen.

## Docker Build Issues

### npm ci fails with ECONNRESET or network errors

**Symptoms:**
- Error: `npm error code ECONNRESET`
- Error: `npm error network aborted`
- TAR_ENTRY_ERROR with package files
- ENOTEMPTY errors during cleanup

**Solutions:**

1. **Clean Docker cache and rebuild:**
   ```bash
   docker-compose down --volumes
   docker system prune -f
   docker-compose up -d --build
   ```

2. **Check your internet connection:**
   - Ensure you have a stable internet connection
   - Try running the build again (the Dockerfile now includes automatic retries)

3. **If behind a proxy:**
   ```bash
   # Set proxy in your environment
   export HTTP_PROXY=http://proxy.example.com:8080
   export HTTPS_PROXY=http://proxy.example.com:8080
   docker-compose up -d --build
   ```

4. **Increase Docker memory:**
   - Open Docker Desktop settings
   - Increase memory allocation to at least 4GB
   - Restart Docker

### Docker build is very slow

**Solutions:**

1. **Use BuildKit for faster builds:**
   ```bash
   DOCKER_BUILDKIT=1 docker-compose up -d --build
   ```

2. **Clean up old images:**
   ```bash
   docker system prune -a -f
   ```

## Application Issues

### Frontend can't connect to backend

**Symptoms:**
- API calls fail in the browser
- Network errors in console

**Solutions:**

1. **Check if backend is running:**
   ```bash
   docker-compose ps
   ```

2. **Check backend logs:**
   ```bash
   docker-compose logs backend
   ```

3. **Verify environment variables:**
   - Check `frontend/.env` has correct `NEXT_PUBLIC_API_URL`
   - Default should be `http://localhost:8000`

### LLM API errors

**Symptoms:**
- Transcription works but summarization fails
- "API key invalid" errors

**Solutions:**

1. **Verify your API key:**
   - Check `backend/.env`
   - Ensure `LLM_PROVIDER` is set correctly
   - Verify the corresponding API key is valid

2. **Test your API key:**
   ```bash
   # For OpenRouter
   curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
        https://openrouter.ai/api/v1/models

   # For OpenAI
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

### Whisper transcription fails

**Symptoms:**
- Audio upload works but transcription fails
- Out of memory errors

**Solutions:**

1. **Use a smaller Whisper model:**
   - Edit `backend/.env`
   - Change `WHISPER_MODEL=turbo` to `WHISPER_MODEL=base`

2. **Increase Docker memory:**
   - Larger models (medium, large) need more RAM
   - Allocate at least 8GB for large models

## Database Issues

### Database locked errors

**Solutions:**

1. **Restart the backend:**
   ```bash
   docker-compose restart backend
   ```

2. **If issue persists, reset database:**
   ```bash
   docker-compose down --volumes
   docker-compose up -d
   ```
   ⚠️ **Warning:** This will delete all your data!

## Getting Help

If you're still experiencing issues:

1. **Check logs:**
   ```bash
   # All services
   docker-compose logs -f

   # Specific service
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

2. **Report an issue:**
   - Visit the GitHub issues page
   - Include:
     - Error messages
     - Log output
     - Steps to reproduce
     - Your environment (OS, Docker version)

## Clean Slate Restart

If all else fails, start fresh:

```bash
# Stop all containers
docker-compose down --volumes

# Remove all Notulen images
docker images | grep notulen | awk '{print $3}' | xargs docker rmi -f

# Clean Docker system
docker system prune -a -f

# Start fresh
./setup.sh
```
