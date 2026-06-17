import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import torch
import joblib
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-service")

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "secureshield_model"
LABEL_ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"

model = None
tokenizer = None
label_encoder = None

torch.set_num_threads(int(os.getenv("OMP_NUM_THREADS", "2")))


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, tokenizer, label_encoder
    logger.info("Loading AI model...")
    try:
        model = DistilBertForSequenceClassification.from_pretrained(
            str(MODEL_PATH),
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        )
        tokenizer = DistilBertTokenizer.from_pretrained(str(MODEL_PATH))
        label_encoder = joblib.load(str(LABEL_ENCODER_PATH))
        model.eval()
        logger.info("AI model loaded successfully in float16")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise
    yield
    logger.info("Shutting down AI service")


app = FastAPI(
    title="SecureShield AI - Prediction Service",
    version="1.0.0",
    lifespan=lifespan
)


class PredictRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)


class PredictResponse(BaseModel):
    label: str
    confidence: float


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    global model, tokenizer, label_encoder

    if model is None or tokenizer is None or label_encoder is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )

    try:
        inputs = tokenizer(
            request.text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            confidence, prediction = torch.max(probabilities, dim=1)

        predicted_label = label_encoder.inverse_transform(
            [prediction.item()]
        )[0]

        return PredictResponse(
            label=predicted_label,
            confidence=round(confidence.item(), 4)
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
