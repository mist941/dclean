# 🐳 DClean

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.2-green.svg)](https://semver.org)

⭐ If you find this project useful, please consider giving it a star to show your support!

## Table of Contents
- [Project Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Authors](#authors)
- [Contributing](#contributing)


## Description

**DClean** is a powerful tool for analyzing Docker images and Dockerfiles.
DClean leverages **Trivy** for comprehensive vulnerability scanning and provides **actionable recommendations** to optimize your Dockerfile instructions, helping you create leaner, faster, and more secure containers.

## Installation
### Prerequisites
- Docker installed on your system
- Python 3.10 or higher
- pip (Python package manager)

### Option 1: Install from PyPI

```bash
pip install mist.dclean
```

### Option 2: Install from Source

```bash
git clone https://github.com/mist941/dclean.git
```

```bash
cd dclean
```

```bash 
pip install -e .
```
### Verify Installation

```bash
dclean version
```
You should see the following output:
```bash
dclean version 0.1.2
```

## Usage

### Analyze a Dockerfile:
```bash
dclean analyze path/to/Dockerfile
``` 
### Analysis Options

Save analysis results to a file:
```bash
dclean analyze path/to/Dockerfile --output path/to/output.txt
```
Perform deep analysis (includes vulnerability scanning):
```bash
dclean analyze path/to/Dockerfile --deep
```
### Examples

Deep analysis with colored output in terminal:
```bash
dclean analyze dockerfiles/Dockerfile --deep
```
![Terminal Output](https://raw.githubusercontent.com/mist941/dclean/refs/heads/main/examples/terminal_output.png)

Save results to a file:
```bash
dclean analyze dockerfiles/Dockerfile --deep --output examples/file_output.txt
```
📄 [View sample output file](https://github.com/mist941/dclean/blob/main/examples/file_output.txt)


## Project Structure
The DClean project is organized as follows:
```bash
dclean/
├── main.py # CLI entry point
├── analyze # Analyze Dockerfiles and Docker images
├── utils # Utility functions
├── api # API for analyzing Docker images
└── tests # Tests
```

## Technologies
DClean is built using the following technologies and tools:

- **Python 3.10+**: Core programming language
- **Click**: Command-line interface creation
- **Docker SDK for Python**: Interacting with Docker API
- **Trivy**: Vulnerability scanning for container images
- **pytest**: Testing framework
- **flake8**: Linting

## Authors

- **Ivan Statkevich** - *Initial work* - [mist941](https://github.com/mist941)

This project is maintained by [Ivan Statkevich](https://github.com/mist941). Feel free to reach out with questions or feedback.

## Contributing

🤝 Contributions are welcome! Feel free to open issues and submit pull requests.

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Create a new branch** from the `dev` branch for your feature or bugfix
4. **Make your changes** and commit them with descriptive messages
5. **Push your branch** to your GitHub fork
6. **Open a pull request** from your branch to the `dev` branch of the main repository

### Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with:

- A clear, descriptive title
- A detailed description of the issue or feature
- Steps to reproduce (for bugs)
- Any relevant logs or screenshots