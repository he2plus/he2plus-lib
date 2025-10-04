# Contributing to he2plus

Thank you for your interest in contributing to he2plus! This document provides guidelines and information for contributors.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Add tests for your changes
6. Ensure all tests pass
7. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/he2plus.git
cd he2plus

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=he2plus

# Run specific test file
pytest tests/test_core.py
```

### Code Style

We use the following tools for code quality:

- **Black** for code formatting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black he2plus tests examples

# Check linting
flake8 he2plus tests examples

# Check types
mypy he2plus
```

## Contributing Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions small and focused

### Testing

- Write tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Test both success and failure cases

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions and classes
- Update examples if needed
- Keep the changelog up to date

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add new system information gathering
fix: resolve package installation issue on Windows
docs: update installation instructions
test: add tests for configuration management
```

### Pull Request Process

1. Ensure your branch is up to date with the main branch
2. Run all tests and ensure they pass
3. Update documentation as needed
4. Provide a clear description of your changes
5. Reference any related issues

## Project Structure

```
he2plus/
├── he2plus/           # Main package
│   ├── __init__.py    # Package initialization
│   ├── core.py        # Core functionality
│   ├── system.py      # System management
│   ├── dev.py         # Development environment
│   ├── utils.py       # Utilities
│   └── cli.py         # Command-line interface
├── tests/             # Test files
├── examples/          # Usage examples
├── docs/              # Documentation
├── setup.py           # Package setup
├── requirements.txt   # Dependencies
└── README.md          # Project documentation
```

## Areas for Contribution

- **New Features**: Add new functionality to solve developer problems
- **Bug Fixes**: Fix existing issues
- **Documentation**: Improve documentation and examples
- **Testing**: Add more test coverage
- **Performance**: Optimize existing code
- **Cross-platform**: Improve cross-platform compatibility

## Getting Help

- Check existing issues and discussions
- Create a new issue for bugs or feature requests
- Join our community discussions

## License

By contributing to he2plus, you agree that your contributions will be licensed under the MIT License.
