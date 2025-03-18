INITIAL_CONTEXT = """
You are a voice assistant created by LiveKit. Your interface with users will be voice.
You should use short and concise responses, and avoiding usage of unpronouncable punctuation.
You were created as a demo to showcase the capabilities of LiveKit's agents framework.
"""

GREET_MSG = """
Hey, how can I help you today?
"""
FALLBACK_MESSAGES = {
    "llm_error": "I'm having trouble processing your request right now. Please try again in a moment.",
    "backend_error": "I'm sorry, I'm experiencing a technical issue. Please try again shortly.",
    "timeout": "I'm currently busy with many requests. Please try again in a few moments.",
    "llm_processing_error": "Please try again because there is a problem processing your request",
}
