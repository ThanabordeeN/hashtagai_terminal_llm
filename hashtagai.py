import os
import openai
import re
import time
import argparse

PROMPT = """You are an AI agent with expertise in using the terminal on Fedora Linux. Your task is to provide concise explanations and terminal commands in response to user queries about Fedora terminal operations.

Follow these steps to generate your response:

1. Analyze the user's query and determine the appropriate Fedora terminal command or explanation.
2. Provide a brief explanation of the solution or concept.
3. Include the exact terminal command to accomplish the task or demonstrate the concept.

Format your response as follows:
1. Begin with an <Explanation> tag containing a concise explanation of the solution or concept. This should be no more than 2-3 sentences.
2. End your response with a <code> tag containing the exact terminal command to be used.

Here's an example of how your response should be structured:

<Explanation>To update all packages on your Fedora system, you can use the dnf package manager. The following command will check for updates and install them for all installed packages.</Explanation>
<code>sudo dnf update</code>

Remember to keep your explanations brief and to the point, focusing on the most relevant information for the user's query. Always provide the exact terminal command as the last line of your response, enclosed in <code> tags."""

class llm_terminal:
    def __init__(self):
        try:
            self.client = openai.OpenAI(
            api_key=os.getenv("TOGETHER_API_KEY"),
            base_url=os.getenv("BASE_URL","https://api.together.xyz/v1")) 
        except Exception as e:
            print("Error: API key is missing or invalid.")
            print("Please set the TOGETHER_API_KEY environment variable.")
            print("You can find your API key in the Together dashboard.")
            print("For more information, refer to the documentation.")
            print(f"Error details: {e}")
            exit()
    def generate_response(self, prompt):
        respose = self.client.chat.completions.create(
        model=os.getenv("MODEL_ID","meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"),
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": prompt},
        ],
        )        
        explanation = find_explained_text(respose.choices[0].message.content)

        code = find_code_text(respose.choices[0].message.content)
        print(print_green_text("#AI Assistant:"))
        print(print_blue_text("Explanation:"))
        for char in explanation:
            print(char, end="", flush=True)
            time.sleep(0.005)

        print("\n" + print_blue_text("Command:"))
        for char in code:
            print(char, end="", flush=True)
            time.sleep(0.005)
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


def main():
    parser = argparse.ArgumentParser(description="Generate terminal command responses using OpenAI.")
    parser.add_argument("command", type=str, help="The command to generate a response for.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments for the command.")
    args = parser.parse_args()

    prompt = " ".join([args.command] + args.args)
    terminal = llm_terminal()
    terminal.generate_response(prompt)

