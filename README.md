# hashtagAI

hashtagAI is a command-line tool that generates terminal command responses using Various providers's language model.

## Installation

To install the package, run:

```sh
pip install hashtagAI
```

## Usage

After installation, you can use the [`ask`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fvar%2Fdata%2Fpython%2Fbin%2Fask%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2264dbf808-7a30-42cd-9b30-cfc2c438b28a%22%5D "/var/data/python/bin/ask") command to generate terminal command responses. The [`ask`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fvar%2Fdata%2Fpython%2Fbin%2Fask%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2264dbf808-7a30-42cd-9b30-cfc2c438b28a%22%5D "/var/data/python/bin/ask") command takes a terminal command as input and provides a concise explanation and the exact terminal command to accomplish the task.

### Example

```sh
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

## Development

To contribute to this project, follow these steps:

1. Clone the repository.
2. Install the dependencies:

```sh
pip install -r requirements.txt
```

3. Make your changes and submit a pull request.

## License

This project is licensed under the MIT License.

## Author

Thanabordee N. (Noun)
