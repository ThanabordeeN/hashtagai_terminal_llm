"""
History Manager for HashtagAI Terminal.

This module manages the command history functionality.
"""
from helpfunc import colorize, print_divider, BLUE, BOLD, YELLOW, CYAN, GREEN

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
    max_history_size = 10  # Default value
    if isinstance(history, list) and len(history) > 0 and hasattr(history[0], "max_history"):
        max_history_size = history[0].max_history
    
    if len(history) > max_history_size * 4:  # 4 entries per interaction
        history = history[-max_history_size * 4:]
        
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
            current_entry.append(colorize(f"➤  {item}", BOLD))
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