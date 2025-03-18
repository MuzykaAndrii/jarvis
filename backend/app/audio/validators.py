import logging

from app.audio.config import MAX_DURATION_SECONDS, WORDS_PER_MIN


logger = logging.getLogger(__name__)


def validate_expected_audio_length(text: str) -> str:
    """
    Validates and truncates text to ensure it doesn't exceed the maximum allowed audio duration.
    """
    logger.info(f"Input text: {text}")

    if not text or not text.strip():
        return text

    words = text.split()
    total_words = len(words)
    estimated_duration = (
        total_words / WORDS_PER_MIN
    ) * 60  # Convert minutes to seconds

    logger.info(
        f"Estimated duration: {estimated_duration:.2f}s, max duration: {MAX_DURATION_SECONDS}s, word count: {total_words}"
    )

    max_words = int((MAX_DURATION_SECONDS / 60) * WORDS_PER_MIN)

    if estimated_duration > MAX_DURATION_SECONDS:
        truncated_text = " ".join(words[:max_words])

        if max_words > 3:
            truncated_text = truncated_text.rstrip(".!?,;") + "..."

        logger.info(
            f"Text truncated from {total_words} to {max_words} words to fit {MAX_DURATION_SECONDS}s limit"
        )
        logger.info(f"Output text: {truncated_text}")
        return truncated_text

    return text
