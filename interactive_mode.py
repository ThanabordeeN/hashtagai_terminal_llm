"""
Interactive Mode Manager for HashtagAI Terminal.

This module handles the interactive command session.
"""
from helpfunc import colorize, clear_screen, BLUE, GREEN, BOLD, YELLOW, CYAN, RED
from history_manager import update_history, display_history
from command_processor import process_command

def interactive_mode(assistant, os_info, history=None):
    """Run the assistant in interactive mode.
    
    Args:
        assistant: The AI assistant instance
        os_info: Current operating system information
        history: Existing command history (if any)
    """
    if history is None:
        history = [""]  # Start with empty string for easier indexing
    
    while True:
        print("\n" + colorize("Enter a command, type 'history' to see past commands, or 'exit' to quit:", BLUE))
        user_input = input(colorize("➤  ", BOLD + GREEN)).strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit"]:
            print(colorize("\nThank you for using HashtagAI Terminal. Goodbye!", GREEN))
            break
            
        if user_input.lower() == "history":
            display_history(history)
            continue
            
        if user_input.lower() == "clear":
            clear_screen()
            from helpfunc import display_session_info
            from config import CONFIG
            display_session_info(CONFIG["model"], os_info)
            continue
            
        # Process the user's command
        try:
            response, cmd_result, status_code = process_command(
                user_input, 
                assistant, 
                history,
                os_info
            )
            
            # Update history with this interaction
            history = update_history(history, user_input, response, cmd_result)
            
        except KeyboardInterrupt:
            print(colorize("\nOperation interrupted.", YELLOW))
        except Exception as e:
            print(colorize(f"Error: {str(e)}", RED))