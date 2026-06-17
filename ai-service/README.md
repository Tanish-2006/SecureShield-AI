# SecureShield AI - Prediction Service

## Overview
Standalone microservice for AI-powered prompt threat detection using DistilBERT.

## API

### `POST /predict`
```json
{
  "text": "Your prompt text here"
}
```
Returns:
```json
{
  "label": "PROMPT_INJECTION",
  "confidence": 0.9876
}
```

### `GET /health`
Returns service health status.

## Deployment

### Render
1. Create a new Web Service on Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Use at least 1GB RAM instance

### Docker
```bash
docker build -t secureshield-ai-service .
docker run -p 8001:8001 secureshield-ai-service
```

## Environment Variables
- `PORT` - Server port (default: 8001)

## Model
- Base: `distilbert-base-uncased`
- Labels: SAFE, PROMPT_INJECTION, PII_EXPOSURE, PASSWORD_EXPOSURE, API_KEY_EXPOSURE, TOKEN_EXPOSURE
- Max sequence length: 128
