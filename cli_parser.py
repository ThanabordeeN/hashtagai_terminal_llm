"""
Command-Line Argument Parser for HashtagAI Terminal.

This module handles parsing of command-line arguments.
"""
import argparse

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

    # If no command is provided, return None
    if not args.command:
        return None

    # Combine command and args into a single prompt
    return " ".join([args.command] + args.args)