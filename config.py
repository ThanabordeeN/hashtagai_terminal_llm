"""
Configuration settings for HashtagAI Terminal.

This module stores configuration constants and environment variables used
throughout the application.
"""
import os

# Configuration settings
CONFIG = {
    "model": os.getenv("LITELLM_MODEL_ID", "gemini/gemini-2.0-flash"),
    "api_key": os.getenv("PROVIDER_API_KEY", ""),
    "typing_speed": float(os.getenv("HASHTAGAI_TYPING_SPEED", "0.001")),
    "max_history": int(os.getenv("HASHTAGAI_MAX_HISTORY", "10")),
}