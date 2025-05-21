"""
Language Model Initialization for HashtagAI Terminal.

This module handles the initialization of the language model with
appropriate error handling.
"""
import dspy
from helpfunc import colorize, RED, BOLD, CYAN
from config import CONFIG

def initialize_model():
    """Initialize the language model with appropriate error handling."""
    if not CONFIG["api_key"]:
        print(colorize("Error: API key is required. Set the PROVIDER_API_KEY environment variable.", RED + BOLD))
        exit(1)
    
    try:
        # print(colorize(f"Initializing language model: {CONFIG['model']}", CYAN))
        lm = dspy.LM(CONFIG["model"], api_key=CONFIG["api_key"])
        dspy.configure(lm=lm)
        return True
    except Exception as e:
        print(colorize(f"Error initializing language model: {str(e)}", RED + BOLD))
        return False