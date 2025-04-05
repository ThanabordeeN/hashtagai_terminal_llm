"""
Command Processor for HashtagAI Terminal.

This module handles the processing of user commands and generating responses.
"""
from helpfunc import display_results, execute_command, ask_yes_no, colorize, RED

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