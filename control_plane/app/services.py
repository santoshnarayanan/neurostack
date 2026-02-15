import requests
import time
from app.config import config
from app.logger import get_logger

logger = get_logger("neurostack.services")

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_model(model: str, prompt: str):
    start_time = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()

        result = response.json()["response"]
        latency_ms = (time.time() - start_time) * 1000

        # Basic token approximation (word-based)
        token_count = len(result.split())
        latency_sec = latency_ms / 1000
        tokens_per_sec = token_count / latency_sec if latency_sec > 0 else 0

        logger.info(
            f"model={model} latency_ms={round(latency_ms,2)} "
            f"tokens={token_count} tokens_per_sec={round(tokens_per_sec,2)}"
        )

        return result, latency_ms, round(tokens_per_sec, 2)

    except requests.exceptions.RequestException as e:
        logger.error(f"Model call failed: {str(e)}")
        return f"Error contacting model: {str(e)}", 0.0, 0.0


def generate_response(model: str, prompt: str):
    result, latency_ms, tokens_per_sec = call_model(model, prompt)

    return {
        "model": model,
        "response": result,
        "latency_ms": round(latency_ms, 2),
        "tokens_per_sec": tokens_per_sec
    }


def compare_models(prompt: str):
    models = config["comparison_models"]
    results = {}

    for model in models:
        result, _, _ = call_model(model, prompt)
        results[model] = result

    return {"results": results}
