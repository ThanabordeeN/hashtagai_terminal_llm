from setuptools import setup, find_packages
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name="hashtagAI",
    version="0.3.1",  # Version bump for significant UI improvements
    packages=find_packages(where="."),
    py_modules=["hashtagai", "__init__", 
                "helpfunc", "agent" , "cli_parser", 
                "command_processor", "history_manager", 
                "system_info", "model_init", "config", 
                "interactive_mode"],
    author="Thanabordee N. (Noun)",
    author_email="thanabordee.noun@gmail.com",
    install_requires=[  
        "dspy",
        "distro",  # For better OS detection on Linux
        "importlib-metadata",  # For version information
    ],
    entry_points={
        "console_scripts": [
            "ask=hashtagai:main",
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)