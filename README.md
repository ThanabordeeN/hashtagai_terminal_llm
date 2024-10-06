
# hashtagAI

hashtagAI is a command-line tool that generates terminal command responses using various providers' language models.

## Installation

To install the package, run:

```sh
pip install hashtagAI
```

## Usage

After installation, you can use the `ask` command to generate terminal command responses. The `ask` command takes a terminal command as input and provides a concise explanation and the exact terminal command to accomplish the task.

### Example

```shell
ask How do I update all packages on Fedora?
```

### Output

```
#AI Assistant:
Explanation:
To update all packages on your Fedora system, you can use the dnf package manager. The following command will check for updates and install them for all installed packages.

Command:
sudo dnf update
```

## Configuration

Ensure you have set the required environment variables:

- `PROVIDER_API_KEY`: Your Model API key.
- `BASE_URL`: The base URL for the Providers API (optional, default: `https://api.together.xyz/v1`).
- `MODEL_ID`: The ID of the Model to use (optional, default: `google/gemma-2-9b-it`).

### Example

```sh
export PROVIDER_API_KEY='YOUR_API_KEY'
export BASE_URL='https://api.together.xyz/v1'
export MODEL_ID='meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo'
```

## Development

To contribute to this project, follow these steps:

1. Clone the repository.
2. Install the dependencies:

```sh
pip install -r 

requirements.txt


```

3. Make your changes and submit a pull request.

## License

This project is licensed under the MIT License.

## Author

Thanabordee N. (Noun)
```

Feel free to modify the content as needed.