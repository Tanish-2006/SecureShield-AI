import re
from ai.predict import predict_text

def analyze_prompt(prompt: str):

    prediction = predict_text(prompt)

    label = prediction["label"]
    confidence = prediction["confidence"]

    threats = [label]

    if label == "SAFE":
        risk_score = 0
        severity = "LOW"
        action = "ALLOW"

    elif label in [
        "PII_EXPOSURE",
        "PASSWORD_EXPOSURE"
    ]:
        risk_score = 70
        severity = "HIGH"
        action = "BLOCK"

    elif label in [
        "API_KEY_EXPOSURE",
        "TOKEN_EXPOSURE"
    ]:
        risk_score = 90
        severity = "CRITICAL"
        action = "BLOCK"

    elif label == "PROMPT_INJECTION":
        risk_score = 95
        severity = "CRITICAL"
        action = "BLOCK"

    else:
        risk_score = 50
        severity = "MEDIUM"
        action = "BLOCK"

    return {
        "risk_score": risk_score,
        "severity": severity,
        "threats": threats,
        "action": action,
        "confidence": confidence
    }