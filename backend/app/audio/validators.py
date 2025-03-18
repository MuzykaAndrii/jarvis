from app.audio.config import MAX_DURATION_SECONDS, WORDS_PER_MIN


def validate_expected_audio_length(text: str) -> str:
    words = text.split()
    estimated_duration = (len(words) / WORDS_PER_MIN) * 60  # Convert minutes to seconds

    if estimated_duration > MAX_DURATION_SECONDS:
        midpoint = len(words) // 2
        trim_range = WORDS_PER_MIN // 2
        text = " ".join(words[midpoint - trim_range : midpoint + trim_range])

    return text
