import dspy

class TerminalAssistant(dspy.Signature):
    """Terminal Assistant for generating helpful command responses."""
    history: str = dspy.InputField(desc="Previous commands and outputs for context")
    operating_system: str = dspy.InputField(desc="Current operating system details")
    input: str = dspy.InputField(desc="User query or command request")
    explanation: str = dspy.OutputField(desc="Clear explanation of what the command does and why it's appropriate and Answer to the user's query")
    command: str = dspy.OutputField(desc="Executable command to run. Return 'None' if no command is needed or if the request is informational only")


class Agent(dspy.Module):
    def forward(self, input: str, operating_system: str, history: str = None) -> dspy.Prediction:
        """Generate a response based on user input, OS info, and conversation history."""
        assistant = dspy.ChainOfThought(TerminalAssistant)
        
        # Create prompt with system context
        system_prompt = "You are a helpful terminal assistant that provides clear explanations "
        system_prompt += f"for users on {operating_system}. Respond with executable commands when appropriate, "
        system_prompt += "or 'None' if the query is informational only."
        
        # Generate response with more context
        response = assistant(
            input=input,
            history=history,
            operating_system=operating_system
        )
        
        return response