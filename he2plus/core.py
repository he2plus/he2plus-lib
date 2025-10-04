"""
Core functionality for he2plus library
"""

import os
import sys
from typing import Dict, Any, Optional
from .utils import Logger, Config
from .system import SystemManager
from .dev import DevEnvironment
from .welcome import WelcomeSystem


class He2Plus:
    """
    Main class for he2plus library
    
    This class provides the primary interface for all he2plus functionality.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the He2Plus instance
        
        Args:
            config_path: Optional path to configuration file
        """
        self.logger = Logger("he2plus")
        self.config = Config(config_path)
        self.system = SystemManager(self.logger, self.config)
        self.dev = DevEnvironment(self.logger, self.config)
        self.welcome = WelcomeSystem(self.logger, self.system)
        
        self.logger.info("He2Plus initialized successfully")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information
        
        Returns:
            Dictionary containing system information
        """
        return self.system.get_system_info()
    
    def setup_dev_environment(self, profile: str = "default") -> bool:
        """
        Set up development environment
        
        Args:
            profile: Environment profile to use
            
        Returns:
            True if setup was successful, False otherwise
        """
        try:
            self.logger.info(f"Setting up development environment with profile: {profile}")
            return self.dev.setup_environment(profile)
        except Exception as e:
            self.logger.error(f"Failed to setup development environment: {e}")
            return False
    
    def install_package(self, package: str, method: str = "auto") -> bool:
        """
        Install a package using the specified method
        
        Args:
            package: Package name to install
            method: Installation method (auto, pip, brew, apt, etc.)
            
        Returns:
            True if installation was successful, False otherwise
        """
        try:
            self.logger.info(f"Installing package: {package} using method: {method}")
            return self.system.install_package(package, method)
        except Exception as e:
            self.logger.error(f"Failed to install package {package}: {e}")
            return False
    
    def check_dependencies(self) -> Dict[str, bool]:
        """
        Check if all required dependencies are available
        
        Returns:
            Dictionary mapping dependency names to availability status
        """
        return self.system.check_dependencies()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the he2plus system
        
        Returns:
            Dictionary containing system status information
        """
        from . import __version__
        return {
            "version": __version__,
            "system_info": self.get_system_info(),
            "dependencies": self.check_dependencies(),
            "config_loaded": self.config.is_loaded(),
            "logger_active": self.logger.is_active(),
        }
    
    def run_onboarding(self) -> Dict[str, Any]:
        """
        Run the interactive onboarding process
        
        Returns:
            Onboarding results
        """
        return self.welcome.run_onboarding()
    
    def show_shell_commands(self) -> None:
        """Show shell commands reference guide"""
        self.welcome.show_shell_commands_guide()
