"""
Utility classes and functions for he2plus library
"""

import os
import yaml
import json
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path


class Logger:
    """Enhanced logging utility for he2plus"""
    
    def __init__(self, name: str, level: str = "INFO"):
        """
        Initialize logger
        
        Args:
            name: Logger name
            level: Logging level
        """
        self.name = name
        self.level = getattr(logging, level.upper())
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Create console handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def is_active(self) -> bool:
        """Check if logger is active"""
        return self.logger.isEnabledFor(self.level)


class Config:
    """Configuration management for he2plus"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config_data = {}
        self.load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        home_dir = Path.home()
        config_dir = home_dir / ".he2plus"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.yaml")
    
    def load_config(self) -> bool:
        """
        Load configuration from file
        
        Returns:
            True if config loaded successfully, False otherwise
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                        self.config_data = yaml.safe_load(f) or {}
                    elif self.config_path.endswith('.json'):
                        self.config_data = json.load(f) or {}
                    else:
                        # Try YAML first, then JSON
                        try:
                            f.seek(0)
                            self.config_data = yaml.safe_load(f) or {}
                        except:
                            f.seek(0)
                            self.config_data = json.load(f) or {}
            else:
                # Create default config
                self.config_data = self._get_default_config()
                self.save_config()
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config_data = self._get_default_config()
            return False
    
    def save_config(self) -> bool:
        """
        Save configuration to file
        
        Returns:
            True if config saved successfully, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    yaml.dump(self.config_data, f, default_flow_style=False)
                else:
                    json.dump(self.config_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
            
        Returns:
            True if value set successfully, False otherwise
        """
        try:
            keys = key.split('.')
            config = self.config_data
            
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            return True
        except Exception as e:
            print(f"Error setting config: {e}")
            return False
    
    def is_loaded(self) -> bool:
        """Check if configuration is loaded"""
        return bool(self.config_data)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "general": {
                "log_level": "INFO",
                "auto_update": True,
                "backup_config": True
            },
            "system": {
                "platform": "auto",
                "package_manager": "auto",
                "install_path": "~/.he2plus/packages"
            },
            "dev": {
                "profiles": {
                    "default": {
                        "python": True,
                        "nodejs": True,
                        "git": True,
                        "docker": False
                    }
                }
            }
        }
