"""
he2plus - Professional Development Environment Manager

From zero to deploy in one command. No configuration, no frustration, just code.
"""

__version__ = "0.2.0"
__author__ = "Prakhar Tripathi"
__email__ = "prakhar@he2plus.dev"
__description__ = "Professional Development Environment Manager"

from .core.system import SystemProfiler
from .core.validator import SystemValidator
from .profiles.registry import ProfileRegistry

__all__ = [
    "SystemProfiler",
    "SystemValidator", 
    "ProfileRegistry",
]