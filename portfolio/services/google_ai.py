"""Small boundary around the Google Gen AI SDK."""

import logging
import os

from google import genai
from google.genai import types


logger = logging.getLogger(__name__)


class AssistantConfigurationError(Exception):
    """The assistant cannot run with the current server configuration."""


class AssistantProviderError(Exception):
    """The provider could not return a usable answer."""


def generate_reply(system_instruction, messages):
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    model = os.getenv("GOOGLE_AI_MODEL", "").strip()
    if not api_key or not model:
        missing = [
            name for name, value in (("GOOGLE_API_KEY", api_key), ("GOOGLE_AI_MODEL", model))
            if not value
        ]
        logger.error("Portfolio assistant is missing configuration: %s", ", ".join(missing))
        raise AssistantConfigurationError

    contents = [
        types.Content(
            role="model" if turn["role"] == "assistant" else "user",
            parts=[types.Part.from_text(text=turn["content"])],
        )
        for turn in messages
    ]
    try:
        with genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=15000)) as client:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=400,
                    temperature=0.3,
                ),
            )
            reply = response.text
    except Exception as exc:
        # Provider exceptions can include request details; only log their type.
        logger.error("Portfolio assistant provider failed: %s", type(exc).__name__)
        raise AssistantProviderError from None

    if not isinstance(reply, str) or not reply.strip():
        logger.error("Portfolio assistant provider returned an empty text response")
        raise AssistantProviderError
    return reply.strip()
