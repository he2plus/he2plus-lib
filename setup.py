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
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="he2plus",
    version="0.2.0",
    author="Prakhar Tripathi",
    author_email="prakhar@he2plus.dev",
    description="Professional Development Environment Manager - From zero to deploy in one command",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/prakhar/he2plus",
    project_urls={
        "Bug Reports": "https://github.com/prakhar/he2plus/issues",
        "Source": "https://github.com/prakhar/he2plus",
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