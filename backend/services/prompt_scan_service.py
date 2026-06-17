import re
import logging
from services.ai_client import predict_text as ai_predict

logger = logging.getLogger(__name__)


def _rule_based_scan(prompt: str) -> dict:
    prompt_lower = prompt.lower()

    injection_patterns = [
        r"ignore all previous instructions",
        r"ignore all instructions",
        r"system prompt",
        r"you are now",
        r"act as if",
        r"pretend to be",
        r"bypass.*(?:restriction|filter|rule|security)",
        r"disregard.*(?:safety|guideline|policy)",
        r"override.*(?:prompt|instruction)",
        r"forget.*(?:rule|instruction|guideline)",
        r"new.*(?:instruction|prompt).*:",
        r"role.*play",
        r"simulate.*(?:admin|root|sudo)",
        r"do.*not.*(?:follow|obey|comply)",
        r"switch.*(?:mode|role)",
    ]

    password_patterns = [
        r"password\s*(?:is|=|:)\s*\S+",
        r"passwd\s*(?:is|=|:)\s*\S+",
    ]

    pii_patterns = [
        r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",
        r"\b\d{16}\b",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    ]

    secret_patterns = [
        r"sk-[A-Za-z0-9]{20,}",
        r"AKIA[0-9A-Z]{16}",
        r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        r"api[_-]?key\s*[:=]\s*[A-Za-z0-9_\-]{10,}",
    ]

    for pattern in injection_patterns:
        if re.search(pattern, prompt_lower):
            return {
                "risk_score": 70,
                "severity": "HIGH",
                "threats": ["PROMPT_INJECTION"],
                "action": "BLOCK",
                "confidence": 0.85,
                "source": "rule"
            }

    for pattern in secret_patterns:
        if re.search(pattern, prompt_lower):
            return {
                "risk_score": 90,
                "severity": "CRITICAL",
                "threats": ["API_KEY_EXPOSURE"],
                "action": "BLOCK",
                "confidence": 0.90,
                "source": "rule"
            }

    for pattern in password_patterns:
        if re.search(pattern, prompt_lower):
            return {
                "risk_score": 80,
                "severity": "HIGH",
                "threats": ["PASSWORD_EXPOSURE"],
                "action": "BLOCK",
                "confidence": 0.85,
                "source": "rule"
            }
    
    for pattern in pii_patterns:
        if re.search(pattern, prompt):
            return {
                "risk_score": 70,
                "severity": "HIGH",
                "threats": ["PII_EXPOSURE"],
                "action": "BLOCK",
                "confidence": 0.80,
                "source": "rule"
            }

    return {
        "risk_score": 0,
        "severity": "LOW",
        "threats": ["SAFE"],
        "action": "ALLOW",
        "confidence": 0.95,
        "source": "rule"
    }


def analyze_prompt(prompt: str) -> dict:
    result = ai_predict(prompt)

    if result is None:
        logger.info("AI service unavailable, using rule-based fallback")
        return _rule_based_scan(prompt)

    label = result["label"]
    confidence = result["confidence"]

    threats = [label]

    if label == "SAFE":
        risk_score = 0
        severity = "LOW"
        action = "ALLOW"

    elif label in ["PII_EXPOSURE", "PASSWORD_EXPOSURE"]:
        risk_score = 70
        severity = "HIGH"
        action = "BLOCK"

    elif label in ["API_KEY_EXPOSURE", "TOKEN_EXPOSURE"]:
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
        "confidence": confidence,
        "source": "ai"
    }
