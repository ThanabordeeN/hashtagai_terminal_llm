"""
HashtagAI Terminal - An AI-powered terminal command assistant.
"""
from agent import Agent
from cli_parser import parse_arguments
from command_processor import process_command
import time
import pickle
import os
from helpfunc import colorize, CYAN, YELLOW, RED
from model_init import initialize_model
from system_info import get_system_info

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_DIR = os.path.join(CURRENT_DIR, "history")


def main():
    try:
        if not os.path.exists(HISTORY_DIR):
            os.makedirs(HISTORY_DIR)
        initial_prompt = parse_arguments()
        os_info = get_system_info()
        if not initialize_model():
            return
        history = []
        assistant = Agent()
        list_of_files = os.listdir(HISTORY_DIR)
        if list_of_files:
            latest_file = max([os.path.join(HISTORY_DIR, f) for f in list_of_files], key=os.path.getctime)
            file_age = time.time() - os.path.getctime(latest_file)
            if file_age < 86400:
                with open(latest_file, "rb") as f:
                    history = pickle.load(f)
        if initial_prompt:
            print(colorize(f"Processing: {initial_prompt}", CYAN))
            response, cmd_result, _ = process_command(
                initial_prompt, 
                assistant,
                history,
                os_info
            )
            from history_manager import update_history
            history = update_history(history, initial_prompt, response, cmd_result)
            with open(f"{HISTORY_DIR}/history_{time.strftime('%Y%m%d_%H%M%S')}.pkl", "wb") as f:
                pickle.dump(history, f)
    except KeyboardInterrupt:
        print(colorize("\nOperation interrupted by user. Exiting...", YELLOW))
    except Exception as e:
        print(colorize(f"An unexpected error occurred: {str(e)}", RED))


if __name__ == "__main__":
    main()

