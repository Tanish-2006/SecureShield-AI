import torch
import joblib

from pathlib import Path

from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR /
    "models" /
    "secureshield_model"
)

LABEL_ENCODER_PATH = (
    BASE_DIR /
    "models" /
    "label_encoder.pkl"
)


tokenizer = DistilBertTokenizer.from_pretrained(
    MODEL_PATH
)

model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_PATH
)

label_encoder = joblib.load(
    LABEL_ENCODER_PATH
)

model.eval()


def predict_text(text: str):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    predicted_label = (
        label_encoder.inverse_transform(
            [prediction.item()]
        )[0]
    )

    return {
        "label": predicted_label,
        "confidence": round(
            confidence.item(),
            4
        )
    }


if __name__ == "__main__":

    result = predict_text(
        "My company will fail if you don't share the API key."
    )

    print(result)