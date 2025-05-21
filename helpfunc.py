# ANSI color codes and terminal utilities
import subprocess
import time
import os
import platform
import shutil

# Color constants
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Terminal dimensions
TERMINAL_WIDTH = shutil.get_terminal_size().columns

def colorize(text: str, color_code: str) -> str:
    """Apply ANSI color formatting to text."""
    return f"{color_code}{text}{RESET}"

def print_divider(char: str = "─", color: str = BLUE) -> None:
    """Print a divider line across the terminal width."""
    print(colorize(char * TERMINAL_WIDTH, color))

def display_session_info(model: str, os_info: str) -> None:
    """Display information about the current session."""
    print_divider()
    print(f"{colorize('HashtagAI Terminal', BOLD + GREEN)} - {colorize('Model:', YELLOW)} {colorize(model, CYAN)}")
    print(f"{colorize('OS:', YELLOW)} {colorize(os_info, CYAN)}")
    print_divider()

def display_results(explanation: str, code: str) -> None:
    """Display the explanation and command with typewriter effect."""
    print("\n" + colorize("📝 Explanation:", BOLD + BLUE))
    typewriter_print(explanation)

    if code and code.lower() != "none":
        print("\n" + colorize("💻 Command:", BOLD + BLUE))
        typewriter_print(colorize(code, MAGENTA))
    else:
        print("\n" + colorize("ℹ️  No command needed for this request.", YELLOW) + "\n")

def typewriter_print(text: str, delay: float = 0.001) -> None:
    """Display text with a typewriter effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)

def ask_yes_no(question: str) -> bool:
    """Ask a yes/no question and return True for yes, False for no."""
    while True:
        user_input = input(f"\n{colorize(question, YELLOW)} {colorize('[y/n]', CYAN)}: ").strip().lower()
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        print(colorize("Please enter 'y' for yes or 'n' for no.", RED))

def execute_command(command: str) -> tuple:
    """Execute a terminal command and return the output and success flag.

    """
    if not command or command.lower() == "none":
        print(colorize("No valid command to execute.", YELLOW))
        return None, 2  # Special code for no command

    try:
        print(colorize("Executing command...", CYAN))
        print_divider("-")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        
        # Detect potential issues with the output
        potential_error_keywords = ["error", "not found", "cannot find", "failed", "unexpected", "invalid"]
        has_unexpected_result = False
        
        # Check if output contains error keywords despite successful execution
        if output:
            lowercase_output = output.lower()
            if any(keyword in lowercase_output for keyword in potential_error_keywords):
                has_unexpected_result = True
                print(colorize(output, YELLOW))
                print(colorize("\nCommand executed but may have unexpected results.", YELLOW))
            else:
                print(colorize(output, GREEN))
        else:
            print(colorize("Command executed successfully with no output.", GREEN))
        
        print_divider("-")
        
        # Return appropriate status code
        if has_unexpected_result:
            return output, 3  # Success but with potentially unexpected results
        return output, 1  # Complete success
        
    except subprocess.CalledProcessError as e:
        print_divider("-")
        error_output = e.stderr.strip() or "Unknown error occurred"
        print(colorize(f"Error: {error_output}", RED))
        print_divider("-")
        return f"Error executing command: {error_output}", 0  # Error

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')


