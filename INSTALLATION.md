# 📦 Installation Guide

## Quick Installation

### From PyPI (Recommended)

```bash
pip install he2plus
```

### From Source

```bash
# Clone the repository
git clone https://github.com/prakhar/he2plus.git
cd he2plus

# Install in development mode
pip install -e .

# Or install with all dependencies
pip install -r requirements.txt
```

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB
- **Disk**: 5GB free space
- **OS**: macOS 10.14+, Windows 10+, or Linux (Ubuntu 18.04+)

### Recommended Requirements
- **Python**: 3.11 or higher
- **RAM**: 8GB or more
- **Disk**: 20GB free space
- **OS**: Latest version of macOS, Windows, or Linux

## Platform-Specific Installation

### macOS

```bash
# Using Homebrew (recommended)
brew install python
pip install he2plus

# Using pyenv
pyenv install 3.11.0
pyenv global 3.11.0
pip install he2plus
```

### Windows

```bash
# Using Chocolatey
choco install python
pip install he2plus

# Using Scoop
scoop install python
pip install he2plus

# Using Microsoft Store
# Install Python from Microsoft Store, then:
pip install he2plus
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install he2plus
pip3 install he2plus

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Linux (CentOS/RHEL/Fedora)

```bash
# CentOS/RHEL
sudo yum install python3 python3-pip
pip3 install he2plus

# Fedora
sudo dnf install python3 python3-pip
pip3 install he2plus
```

## Virtual Environment (Recommended)

### Using venv

```bash
# Create virtual environment
python -m venv he2plus-env

# Activate virtual environment
# On macOS/Linux:
source he2plus-env/bin/activate
# On Windows:
he2plus-env\Scripts\activate

# Install he2plus
pip install he2plus
```

### Using conda

```bash
# Create conda environment
conda create -n he2plus python=3.11

# Activate environment
conda activate he2plus

# Install he2plus
pip install he2plus
```

### Using poetry

```bash
# Create new project
poetry new my-project
cd my-project

# Add he2plus as dependency
poetry add he2plus

# Install dependencies
poetry install
```

## Verification

After installation, verify that he2plus is working correctly:

```bash
# Check version
he2plus --version

# Run system diagnostics
he2plus doctor

# List available profiles
he2plus list --available
```

## Troubleshooting

### Common Issues

#### Permission Errors

```bash
# On macOS/Linux, use --user flag
pip install --user he2plus

# Or use sudo (not recommended)
sudo pip install he2plus
```

#### Python Not Found

```bash
# Check Python installation
python --version
python3 --version

# Add Python to PATH
export PATH="/usr/local/bin:$PATH"
```

#### pip Not Found

```bash
# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# Or use package manager
# macOS: brew install python
# Ubuntu: sudo apt install python3-pip
# Windows: Download from python.org
```

#### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf he2plus-env
python -m venv he2plus-env
source he2plus-env/bin/activate
pip install he2plus
```

### Getting Help

If you encounter issues:

1. Check the [FAQ](README.md#faq)
2. Search [GitHub Issues](https://github.com/prakhar/he2plus/issues)
3. Create a new issue with:
   - Your OS and version
   - Python version
   - Error message
   - Steps to reproduce

## Development Installation

For contributing to he2plus:

```bash
# Clone repository
git clone https://github.com/prakhar/he2plus.git
cd he2plus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 he2plus/
black he2plus/
```

## Uninstallation

```bash
# Uninstall he2plus
pip uninstall he2plus

# Remove virtual environment
rm -rf he2plus-env

# Remove configuration files (optional)
rm -rf ~/.he2plus
```

## Next Steps

After installation:

1. **Explore profiles**: `he2plus list --available`
2. **Check system**: `he2plus doctor`
3. **Install a profile**: `he2plus install web-nextjs`
4. **Get help**: `he2plus --help`

Welcome to he2plus! 🚀
