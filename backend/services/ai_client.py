import os
import logging

import httpx

logger = logging.getLogger(__name__)

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "").rstrip("/")

REQUEST_TIMEOUT = float(os.getenv("AI_SERVICE_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("AI_SERVICE_RETRIES", "2"))


def predict_text(text: str) -> dict | None:
    if not AI_SERVICE_URL:
        logger.warning("AI_SERVICE_URL not configured, skipping AI inference")
        return None

    url = f"{AI_SERVICE_URL}/predict"
    last_error = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                response = client.post(
                    url,
                    json={"text": text},
                    headers={"Content-Type": "application/json"}
                )

            if response.status_code == 200:
                data = response.json()
                return {
                    "label": data["label"],
                    "confidence": data["confidence"]
                }

            logger.error(
                f"AI service returned status {response.status_code}: "
                f"{response.text[:200]}"
            )
            return None

        except httpx.TimeoutException:
            logger.warning(
                f"AI service timeout (attempt {attempt + 1}/{MAX_RETRIES + 1})"
            )
            last_error = "timeout"

        except httpx.RequestError as e:
            logger.warning(
                f"AI service connection error (attempt {attempt + 1}/"
                f"{MAX_RETRIES + 1}): {e}"
            )
            last_error = str(e)

        if attempt < MAX_RETRIES:
            import time
            time.sleep(1)

    logger.error(
        f"AI service unavailable after {MAX_RETRIES + 1} attempts: "
        f"{last_error}"
    )
    return None
