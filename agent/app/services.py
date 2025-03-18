from typing import AsyncIterable

from livekit.agents.pipeline import VoicePipelineAgent
from aiohttp.client_exceptions import ClientError

from app.client import APIClient
from app.backend import validate_endpoint, base_url


async def validate_llm_output_length(
    assistant: VoicePipelineAgent,
    text: str | AsyncIterable[str],
) -> str:
    """Callback to trim the length of llm output"""
    backend_client = APIClient(base_url)
    if isinstance(text, AsyncIterable):
        text = "".join([chunk async for chunk in text])

    try:
        response = await backend_client.post(validate_endpoint, {"text": text})
        validated_text = response.get("text", text)
    except ClientError:
        return text

    return validated_text
