"""
HashtagAI Terminal - An AI-powered terminal command assistant.

This module provides an interface to AI models that can generate
terminal command explanations and usage examples.
"""
from agent import Agent
from cli_parser import parse_arguments
from command_processor import process_command
from config import CONFIG
from helpfunc import (
    display_session_info,
    display_welcome_banner,
    colorize,
    ask_yes_no,
    GREEN,
    CYAN,
    YELLOW,
    RED,
)
from history_manager import update_history
from interactive_mode import interactive_mode
from model_init import initialize_model
from system_info import get_system_info


def main():
    """Main entry point for the application."""
    try:
        # Display welcome banner
        display_welcome_banner()
        
        # Parse command line arguments
        initial_prompt = parse_arguments()
        
        # Get system information
        os_info = get_system_info()
        
        # Initialize language model
        if not initialize_model():
            return
            
        # Display session information
        display_session_info(CONFIG["model"], os_info)
        
        # Create assistant instance
        assistant = Agent()
        
        # Handle initial command if provided
        if initial_prompt:
            print(colorize(f"Processing: {initial_prompt}", CYAN))
            response, cmd_result, status_code = process_command(
                initial_prompt, 
                assistant,
                None,
                os_info
            )
            history = [""]
            history = update_history(history, initial_prompt, response, cmd_result)
            
            # If user executed a command, offer to continue in interactive mode
            if status_code != 2:  # Not an informational request
                print("\n")
                if ask_yes_no("Continue in interactive mode?"):
                    interactive_mode(assistant, os_info, history)
                else:
                    print(colorize("\nThank you for using HashtagAI Terminal. Goodbye!", GREEN))
            else:
                # If it was informational only, go to interactive mode
                interactive_mode(assistant, os_info, history)
        else:
            # Start in interactive mode directly
            interactive_mode(assistant, os_info)
            
    except KeyboardInterrupt:
        print(colorize("\nOperation interrupted by user. Exiting...", YELLOW))
    except Exception as e:
        print(colorize(f"An unexpected error occurred: {str(e)}", RED))


if __name__ == "__main__":
    main()

