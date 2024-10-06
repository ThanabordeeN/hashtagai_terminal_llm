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
    version="0.2.1.1",
    packages=find_packages(),
    author="Thanabordee N. (Noun)",
    author_email="thanabordee.noun@gmail.com",
    install_requires=[  
        "openai",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "ask=hashtagai:main",
                            ],
    },
        # Long description of your library
    long_description=long_description,
    long_description_content_type='text/markdown'
)