#!/usr/bin/env python3
"""
he2plus - Professional Development Environment Manager
Setup script for PyPI distribution
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    requirements = []
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#"):
                    requirements.append(line)
    except FileNotFoundError:
        # Fallback to minimal requirements if file not found
        requirements = [
            "click>=8.1.0",
            "rich>=13.7.0",
            "psutil>=5.9.0",
            "requests>=2.31.0",
            "aiohttp>=3.9.0",
            "pyyaml>=6.0",
            "structlog>=24.1.0",
            "inquirer>=3.4.1",
            "blessed>=1.22.0",
            "colorama>=0.4.6",
        ]
    return requirements

setup(
    name="he2plus",
    version="0.3.0",
    author="Prakhar Tripathi",
    author_email="dptmywork@gmail.com",
    description="Professional Development Environment Manager - From zero to deploy in one command",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/he2plus/he2plus-lib",
    project_urls={
        "Bug Reports": "https://github.com/he2plus/he2plus-lib/issues",
        "Source": "https://github.com/he2plus/he2plus-lib",
        "Documentation": "https://he2plus.dev",
        "Twitter": "https://twitter.com/he2plus",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "he2plus=he2plus.cli.main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "he2plus": [
            "profiles/*.yaml",
            "templates/*",
            "config/*.yaml",
        ],
    },
    keywords=[
        "development",
        "environment",
        "setup",
        "automation",
        "devops",
        "web3",
        "machine-learning",
        "mobile",
        "web-development",
        "blockchain",
        "docker",
        "kubernetes",
        "python",
        "nodejs",
        "rust",
        "golang",
    ],
)