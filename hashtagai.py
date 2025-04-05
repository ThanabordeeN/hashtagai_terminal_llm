"""
HashtagAI Terminal - An AI-powered terminal command assistant.

This module provides an interface to AI models that can generate
terminal command explanations and usage examples.
"""
import argparse
import dspy
import platform
import distro
import os
import time
from agent import Agent
from helpfunc import (
    display_results,
    execute_command,
    colorize,
    print_divider,
    display_session_info,
    display_welcome_banner,
    clear_screen,
    ask_yes_no,
    BLUE,
    GREEN,
    YELLOW,
    RED,
    CYAN,
    BOLD,
)
# Constants
CONFIG = {
    "model": os.getenv("LITELLM_MODEL_ID", "gemini/gemini-2.0-flash"),
    "api_key": os.getenv("PROVIDER_API_KEY", ""),
    "typing_speed": float(os.getenv("HASHTAGAI_TYPING_SPEED", "0.001")),
    "max_history": int(os.getenv("HASHTAGAI_MAX_HISTORY", "10")),
}

def initialize_model():
    """Initialize the language model with appropriate error handling."""
    if not CONFIG["api_key"]:
        print(colorize("Error: API key is required. Set the PROVIDER_API_KEY environment variable.", RED + BOLD))
        exit(1)
    
    try:
        print(colorize(f"Initializing language model: {CONFIG['model']}", CYAN))
        lm = dspy.LM(CONFIG["model"], api_key=CONFIG["api_key"])
        dspy.configure(lm=lm)
        return True
    except Exception as e:
        print(colorize(f"Error initializing language model: {str(e)}", RED + BOLD))
        return False

def get_system_info():
    """Get detailed system information."""
    os_info = platform.system() + " " + platform.release()
    
    if platform.system() == "Linux":
        try:
            os_info = distro.name(pretty=True)
        except ImportError:
            # Fallback if distro module not available
            try:
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            os_info = line.split("=")[1].strip().strip('"')
                            break
            except:
                pass
    
    return os_info

def generate_response(response, retry_callback=None):
    """Generate a response for the given prompt and execute if requested.
    
    Args:
        response: The response from the AI assistant
        retry_callback: Function to call if user wants to retry
        
    Returns:
        tuple: (command_output, success_flag) where success_flag is 1 for success, 0 for failure, 2 for no command
    """
    try:
        if not hasattr(response, 'explanation') or not hasattr(response, 'command'):
            print(colorize("Error: Invalid response format from AI", RED))
            return None, 0
        
        # Display results
        display_results(response.explanation, response.command)
        
        # Check if command is None or empty
        if not response.command or response.command.lower() == "none":
            return None, 2  # No command needed
        
        # Execute command if user wants to
        if ask_yes_no("Do you want to execute the command?"):
            return execute_command(response.command)
        
        return None, 1  # User chose not to execute
        
    except Exception as e:
        print(colorize(f"Error in generate_response: {str(e)}", RED))
        
        # Offer retry if callback provided
        if retry_callback and ask_yes_no("Would you like to try again?"):
            return retry_callback()
            
        return f"Error in generate_response: {str(e)}", 0

def parse_arguments():
    """Parse command line arguments and return the combined prompt."""
    parser = argparse.ArgumentParser(
        description="Generate terminal command responses using AI."
    )
    parser.add_argument(
        "command", 
        type=str, 
        nargs="?",  # Make the command optional
        help="The command to generate a response for."
    )
    parser.add_argument(
        "args", 
        nargs=argparse.REMAINDER, 
        help="Additional arguments for the command."
    )
    
    # Add optional flags
    parser.add_argument(
        "--interactive", "-i", 
        action="store_true",
        help="Start in interactive mode without an initial command"
    )
    parser.add_argument(
        "--version", "-v", 
        action="store_true",
        help="Display version information"
    )
    
    args = parser.parse_args()
    
    # Handle version flag
    if args.version:
        from importlib.metadata import version
        try:
            ver = version("hashtagAI")
            print(f"HashtagAI Terminal version {ver}")
        except:
            print("HashtagAI Terminal (version unknown)")
        exit(0)
        
    # Handle interactive mode or missing command
    if args.interactive or not args.command:
        return None
        
    # Combine command and args into a single prompt
    return " ".join([args.command] + args.args)

def update_history(history, user_input, response, cmd_result):
    """Update history with the latest interaction."""
    if user_input:  # Only add if there's actual input
        history.append(f"User: {user_input}")
    
    if hasattr(response, 'explanation'):
        explanation = response.explanation[:500] + "..." if len(response.explanation) > 500 else response.explanation
        history.append(f"Explanation: {explanation}")
        
    if hasattr(response, 'command') and response.command and response.command.lower() != "none":
        history.append(f"Command: {response.command}")
        
    if cmd_result is not None:
        result_str = str(cmd_result)
        cmd_output = result_str[:500] + "..." if len(result_str) > 500 else result_str
        history.append(f"Output: {cmd_output}")
    
    # Keep history at reasonable size
    if len(history) > CONFIG["max_history"] * 4:  # 4 entries per interaction
        history = history[-CONFIG["max_history"] * 4:]
        
    return history

def display_history(history):
    """Display command history in a formatted way."""
    if not history or len(history) <= 1:
        print(colorize("\nNo command history yet.", YELLOW))
        return
        
    print(colorize("\n📜 Command History:", BLUE + BOLD))
    print_divider()
    
    current_entry = []
    entry_num = 1
    
    for item in history[1:]:  # Skip the initial empty string
        prefix = item.split(":", 1)[0].strip()
        
        if prefix == "User" and current_entry:  # New user entry means we should output the previous entry
            print(colorize(f"[{entry_num}]", CYAN))
            for entry_line in current_entry:
                print(entry_line)
            print_divider("-")
            current_entry = []
            entry_num += 1
            
        # Format based on type of entry
        if prefix == "User":
            current_entry.append(colorize(f"➤ {item}", BOLD))
        elif prefix == "Explanation":
            # Truncate long explanations
            content = item.split(":", 1)[1].strip()
            if len(content) > 70:
                content = content[:67] + "..."
            current_entry.append(f"  {colorize('Answer:', BLUE)} {content}")
        elif prefix == "Command":
            current_entry.append(f"  {colorize('Command:', GREEN)} {item.split(':', 1)[1].strip()}")
        elif prefix == "Output":
            content = item.split(":", 1)[1].strip()
            if len(content) > 70:
                content = content[:67] + "..."
            current_entry.append(f"  {colorize('Output:', YELLOW)} {content}")
    
    # Print the last entry
    if current_entry:
        print(colorize(f"[{entry_num}]", CYAN))
        for entry_line in current_entry:
            print(entry_line)
        print_divider("-")

def process_command(prompt, assistant, history=None, os_info=None):
    """Process a single command and return results."""
    def retry_callback():
        # Create a retry callback that operates in the same context
        retry_response = assistant(
            input=prompt,
            history="\n".join(history) if history else None,
            operating_system=os_info
        )
        return generate_response(retry_response)
    
    # Function to handle unexpected results
    def handle_unexpected_result(cmd_result):
        if ask_yes_no("The command had unexpected results. Would you like me to try to fix it?"):
            # Create a new prompt asking to fix the issue
            fix_prompt = f"Fix this issue with the previous command: {prompt}. The command produced this unexpected result: {cmd_result}"
            fix_response = assistant(
                input=fix_prompt,
                history="\n".join(history) if history else None,
                operating_system=os_info
            )
            return generate_response(fix_response)
        return cmd_result, 1  # User chose not to fix, treat as success
    
    # Generate initial response
    response = assistant(
        input=prompt,
        history="\n".join(history) if history else None,
        operating_system=os_info
    )
    
    # Process the response
    cmd_result, status_code = generate_response(response, retry_callback)
    
    # Handle unexpected results (status_code 3)
    if status_code == 3:
        new_result, new_status = handle_unexpected_result(cmd_result)
        # If we got a new result from fixing, return that instead
        if new_status != 3:  # Avoid infinite loop if fixing also produces unexpected results
            return response, new_result, new_status
    
    return response, cmd_result, status_code

def interactive_mode(assistant, os_info,history :list = [""]):
    """Run the assistant in interactive mode."""
     # Start with empty string for easier indexing
    while True:
        print("\n" + colorize("Enter a command, type 'history' to see past commands, or 'exit' to quit:", BLUE))
        user_input = input(colorize("➤ ", BOLD + GREEN)).strip()
        
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
            display_session_info(CONFIG["model"], os_info)
            continue
            
        # Process the user's command
        try:
            # print(colorize(f"Processing: {user_input}", CYAN))
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

