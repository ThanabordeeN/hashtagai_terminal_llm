import os
import openai
import re
import time
import argparse


operating_system = os.name

PROMPT = f"""You are an AI agent with expertise in using the terminal {operating_system} . Your task is to provide concise explanations and terminal  commands in response to user queries about {operating_system} terminal operations.

Follow these steps to generate your response:

1. Analyze the user's query and determine the appropriate {operating_system} terminal command or explanation.
2. Provide a brief explanation of the solution or concept.
3. Include the exact terminal command to accomplish the task or demonstrate the concept.

Format your response as follows:
1. Begin with an <Explanation> tag containing a concise explanation of the solution or concept. This should be no more than 2-3 sentences.
2. End your response with a <code> tag containing the exact terminal command to be used.

Here's an example of how your response should be structured:

<Explanation>To update all packages on your {operating_system} system, you can use the dnf package manager. The following command will check for updates and install them for all installed packages.</Explanation>
<code>sudo dnf update</code>

Remember to keep your explanations brief and to the point, focusing on the most relevant information for the user's query. Always provide the exact terminal command as the last line of your response, enclosed in <code> tags."""

class llm_terminal:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL","https://api.together.xyz/v1")
        try:
            self.client = openai.OpenAI(
                                        api_key=os.getenv("PROVIDER_API_KEY"),
                                        base_url=self.base_url
            ) 
        except Exception as e:
            log_error_message(e)
            
            
    def generate_response(self, prompt):
        model = os.getenv("MODEL_ID","mistralai/Mistral-7B-Instruct-v0.3")
        
        try:
            respose = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": prompt},
            ],
            )        
        except Exception as e:
            log_error_message(e)
        print(print_yellow_text("Provider: "), end="")
        print(print_yellow_text(self.base_url), end=" ")
        print(print_yellow_text("Model:"), end=" ")
        print(print_yellow_text(model))
        explanation = find_explained_text(respose.choices[0].message.content)

        code = find_code_text(respose.choices[0].message.content)
        print(print_green_text("#AI Assistant:"))
        print(print_blue_text("Explanation:"))
        for char in explanation:
            print(char, end="", flush=True)
            time.sleep(0.001)

        print("\n" + print_blue_text("Command:"))
        for char in code:
            print(print_red_text(char), end="", flush=True)
            time.sleep(0.001)
        print("\n")

        
def find_explained_text(response):
    pattern = r"<Explanation>(.*?)</Explanation>"
    text = re.findall(pattern, response, re.DOTALL)
    return "".join(text).strip()

def find_code_text(response):
    pattern = r"<code>(.*?)</code>"
    text = re.findall(pattern, response)
    return "".join(text).strip()

def print_green_text(text) -> str:
    return f"\033[92m{text}\033[0m"

def print_blue_text(text)-> str:
    return f"\033[94m{text}\033[0m"

def print_red_text(text) -> str:
    return f"\033[91m{text}\033[0m"

def print_yellow_text(text) -> str:
    return f"\033[93m{text}\033[0m"
def log_error_message(message):
    """Logs an error message in a user-friendly format, highlighting missing API key and providing instructions for configuration."""

    print(print_red_text("**ERROR: Missing API Key**"))
    print(print_yellow_text("The API key required to access the provider is missing or invalid."))

    print("\n**Steps to Resolve:**")
    print(print_green_text(1), ".Set the PROVIDER_API_KEY environment variable:")
    print(print_blue_text(f"\t- export PROVIDER_API_KEY='YOUR_API_KEY' or set PROVIDER_API_KEY='YOUR_API_KEY' for CMD "))  # Example usage
    print(print_yellow_text("\t\tYou can find your API key in the Providers dashboard."))

    print(print_green_text(2), ".Optional Configuration (default values provided):")
    print(print_blue_text(f"\t- BASE_URL (default: https://api.together.xyz/v1):"))
    print(print_blue_text("\t\texport BASE_URL='https://api.openai.com/v1'"))  # Example
    print(print_blue_text(f"\t- MODEL_ID (default: not set):"))
    print(print_blue_text("\t\texport MODEL_ID='meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo'"))  # Example

    print("\n**Environment Variables Summary:**")
    print(print_green_text("  - PROVIDER_API_KEY: Your Model API key."))
    print(print_green_text("  - BASE_URL: The base URL for the Providers API (optional)."))
    print(print_green_text("  - MODEL_ID: The ID of the Model to use (optional)."))

    print("\n**Additional Information:**")
    print(print_green_text("- For more information, refer to the documentation."))

    print("\n**Error Details:**")
    print(print_blue_text(f"{message}"))

    # Terminate execution with a clear exit message
    print(print_red_text("Exiting program due to missing API key."))
    exit()



def main():
    parser = argparse.ArgumentParser(description="Generate terminal command responses using OpenAI.")
    parser.add_argument("command", type=str, help="The command to generate a response for.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments for the command.")
    args = parser.parse_args()
    
    prompt = " ".join([args.command] + args.args)
    terminal = llm_terminal()
    terminal.generate_response(prompt)

