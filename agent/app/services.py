import asyncio
import logging
from typing import AsyncIterable

from livekit.agents.pipeline import VoicePipelineAgent
from aiohttp.client_exceptions import ClientError
from livekit.agents._exceptions import APIConnectionError
from google.genai.errors import ClientError as GeminiError

from app.prompts import FALLBACK_MESSAGES
from app.client import APIClient
from app.backend import validate_endpoint, base_url

logger = logging.getLogger("voice-agent")


async def validate_llm_output_length(
    assistant: VoicePipelineAgent,
    text: str | AsyncIterable[str],
) -> str:
    """Callback to trim the length of llm output"""
    backend_client = APIClient(base_url)
    if isinstance(text, AsyncIterable):
        try:
            chunks = []
            async for chunk in text:
                chunks.append(chunk)
            text = "".join(chunks)

        except APIConnectionError as e:
            logger.warning(f"LLM API connection error: {e}")
            return FALLBACK_MESSAGES["llm_error"]

        except GeminiError as e:
            logger.warning(f"LLM API processing error: {e}")
            return FALLBACK_MESSAGES["llm_processing_error"]

        except asyncio.TimeoutError:
            logger.warning("Timeout while collecting LLM output chunks")
            return FALLBACK_MESSAGES["timeout"]

        except Exception as e:
            logger.exception(f"Unexpected error processing LLM output: {e}")
            return FALLBACK_MESSAGES["backend_error"]

    try:
        response = await backend_client.post(validate_endpoint, {"text": text})
        validated_text = response.get("text", text)
    except ClientError:
        return text

    return validated_text
