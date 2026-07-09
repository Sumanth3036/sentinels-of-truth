import json
import re
from typing import Any

from openai import OpenAI

from app.config import GROQ_API_KEY, GROQ_MODEL

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not set")
        _client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )
    return _client


def _strip_json_fences(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text


def call_llm(system: str, user: str, json_mode: bool = True) -> dict[str, Any]:
    """Call Groq LLM with one retry. Returns parsed JSON dict when json_mode=True."""
    last_error: Exception | None = None

    for attempt in range(2):
        try:
            kwargs: dict[str, Any] = {
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.3,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = _get_client().chat.completions.create(**kwargs)
            content = response.choices[0].message.content or ""

            if json_mode:
                cleaned = _strip_json_fences(content)
                return json.loads(cleaned)
            return {"content": content}

        except Exception as exc:
            last_error = exc
            if attempt == 0:
                continue
            raise RuntimeError(f"LLM call failed after retry: {exc}") from last_error

    raise RuntimeError(f"LLM call failed: {last_error}")
