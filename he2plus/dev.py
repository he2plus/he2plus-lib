"""
Development environment management for he2plus library
"""

import os
import sys
import subprocess
from typing import Dict, Any, List, Optional
from .utils import Logger


class DevEnvironment:
    """Development environment setup and management"""
    
    def __init__(self, logger: Logger, config):
        """
        Initialize development environment manager
        
        Args:
            logger: Logger instance
            config: Configuration instance
        """
        self.logger = logger
        self.config = config
        self.platform = sys.platform.lower()
        
        self.logger.info("DevEnvironment initialized")
    
    def setup_environment(self, profile: str = "default") -> bool:
        """
        Set up development environment with specified profile
        
        Args:
            profile: Environment profile to use
            
        Returns:
            True if setup was successful, False otherwise
        """
        try:
            self.logger.info(f"Setting up development environment with profile: {profile}")
            
            # Get profile configuration
            profile_config = self.config.get(f"dev.profiles.{profile}", {})
            if not profile_config:
                self.logger.warning(f"Profile {profile} not found, using default")
                profile_config = self.config.get("dev.profiles.default", {})
            
            # Setup components based on profile
            success = True
            
            if profile_config.get("python", False):
                success &= self._setup_python()
            
            if profile_config.get("nodejs", False):
                success &= self._setup_nodejs()
            
            if profile_config.get("git", False):
                success &= self._setup_git()
            
            if profile_config.get("docker", False):
                success &= self._setup_docker()
            
            if profile_config.get("brownie", False):
                success &= self._setup_brownie()
            
            if profile_config.get("hardhat", False):
                success &= self._setup_hardhat()
            
            if profile_config.get("react", False):
                success &= self._setup_react()
            
            if success:
                self.logger.info("Development environment setup completed successfully")
            else:
                self.logger.warning("Development environment setup completed with some issues")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error setting up development environment: {e}")
            return False
    
    def _setup_python(self) -> bool:
        """Set up Python development environment"""
        try:
            self.logger.info("Setting up Python environment")
            
            # Check if Python is available
            if not sys.executable:
                self.logger.error("Python not found")
                return False
            
            # Install common Python packages
            packages = [
                "pip",
                "setuptools",
                "wheel",
                "virtualenv",
                "pipenv",
                "poetry"
            ]
            
            for package in packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', package], 
                                 check=True, capture_output=True)
                    self.logger.info(f"Installed/updated {package}")
                except subprocess.CalledProcessError:
                    self.logger.warning(f"Failed to install {package}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Python: {e}")
            return False
    
    def _setup_nodejs(self) -> bool:
        """Set up Node.js development environment"""
        try:
            self.logger.info("Setting up Node.js environment")
            
            # Check if Node.js is available
            try:
                result = subprocess.run(['node', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.warning("Node.js not found, attempting to install")
                    return self._install_nodejs()
            except FileNotFoundError:
                self.logger.warning("Node.js not found, attempting to install")
                return self._install_nodejs()
            
            # Install common Node.js packages
            packages = [
                "npm",
                "yarn",
                "pnpm"
            ]
            
            for package in packages:
                try:
                    if package == "npm":
                        # npm comes with Node.js
                        continue
                    subprocess.run(['npm', 'install', '-g', package], 
                                 check=True, capture_output=True)
                    self.logger.info(f"Installed {package}")
                except subprocess.CalledProcessError:
                    self.logger.warning(f"Failed to install {package}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Node.js: {e}")
            return False
    
    def _setup_git(self) -> bool:
        """Set up Git development environment"""
        try:
            self.logger.info("Setting up Git environment")
            
            # Check if Git is available
            try:
                result = subprocess.run(['git', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.warning("Git not found, attempting to install")
                    return self._install_git()
            except FileNotFoundError:
                self.logger.warning("Git not found, attempting to install")
                return self._install_git()
            
            # Configure Git if not already configured
            self._configure_git()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Git: {e}")
            return False
    
    def _setup_docker(self) -> bool:
        """Set up Docker development environment"""
        try:
            self.logger.info("Setting up Docker environment")
            
            # Check if Docker is available
            try:
                result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.warning("Docker not found, attempting to install")
                    return self._install_docker()
            except FileNotFoundError:
                self.logger.warning("Docker not found, attempting to install")
                return self._install_docker()
            
            # Check if Docker Compose is available
            try:
                result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.warning("Docker Compose not found, attempting to install")
                    self._install_docker_compose()
            except FileNotFoundError:
                self.logger.warning("Docker Compose not found, attempting to install")
                self._install_docker_compose()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Docker: {e}")
            return False
    
    def _setup_brownie(self) -> bool:
        """Set up Brownie development environment"""
        try:
            self.logger.info("Setting up Brownie environment")
            
            # Install Brownie
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'eth-brownie'], 
                             check=True, capture_output=True)
                self.logger.info("Installed Brownie")
            except subprocess.CalledProcessError:
                self.logger.warning("Failed to install Brownie")
                return False
            
            # Initialize Brownie if not already done
            try:
                result = subprocess.run(['brownie', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    self.logger.info("Brownie is ready")
                else:
                    self.logger.warning("Brownie installation may have issues")
            except FileNotFoundError:
                self.logger.warning("Brownie command not found")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Brownie: {e}")
            return False
    
    def _setup_hardhat(self) -> bool:
        """Set up Hardhat development environment"""
        try:
            self.logger.info("Setting up Hardhat environment")
            
            # Check if Node.js is available
            try:
                result = subprocess.run(['node', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.error("Node.js required for Hardhat")
                    return False
            except FileNotFoundError:
                self.logger.error("Node.js required for Hardhat")
                return False
            
            # Install Hardhat globally
            try:
                subprocess.run(['npm', 'install', '-g', 'hardhat'], 
                             check=True, capture_output=True)
                self.logger.info("Installed Hardhat")
            except subprocess.CalledProcessError:
                self.logger.warning("Failed to install Hardhat")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Hardhat: {e}")
            return False
    
    def _setup_react(self) -> bool:
        """Set up React development environment"""
        try:
            self.logger.info("Setting up React environment")
            
            # Check if Node.js is available
            try:
                result = subprocess.run(['node', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.error("Node.js required for React")
                    return False
            except FileNotFoundError:
                self.logger.error("Node.js required for React")
                return False
            
            # Install Create React App globally
            try:
                subprocess.run(['npm', 'install', '-g', 'create-react-app'], 
                             check=True, capture_output=True)
                self.logger.info("Installed Create React App")
            except subprocess.CalledProcessError:
                self.logger.warning("Failed to install Create React App")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up React: {e}")
            return False
    
    def _install_nodejs(self) -> bool:
        """Install Node.js"""
        try:
            if self.platform == "darwin":
                # Try Homebrew first
                try:
                    subprocess.run(['brew', 'install', 'node'], check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                # Fallback to official installer
                self.logger.info("Please install Node.js manually from https://nodejs.org/")
                return False
                
            elif self.platform == "linux":
                # Try package manager
                try:
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'nodejs', 'npm'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                try:
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'nodejs', 'npm'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                self.logger.info("Please install Node.js manually from https://nodejs.org/")
                return False
                
            elif self.platform == "win32":
                self.logger.info("Please install Node.js manually from https://nodejs.org/")
                return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error installing Node.js: {e}")
            return False
    
    def _install_git(self) -> bool:
        """Install Git"""
        try:
            if self.platform == "darwin":
                # Try Homebrew first
                try:
                    subprocess.run(['brew', 'install', 'git'], check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                # Fallback to Xcode command line tools
                try:
                    subprocess.run(['xcode-select', '--install'], check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                self.logger.info("Please install Git manually from https://git-scm.com/")
                return False
                
            elif self.platform == "linux":
                # Try package manager
                try:
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'git'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                try:
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'git'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                self.logger.info("Please install Git manually from https://git-scm.com/")
                return False
                
            elif self.platform == "win32":
                self.logger.info("Please install Git manually from https://git-scm.com/")
                return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error installing Git: {e}")
            return False
    
    def _install_docker(self) -> bool:
        """Install Docker"""
        try:
            if self.platform == "darwin":
                self.logger.info("Please install Docker Desktop from https://www.docker.com/products/docker-desktop")
                return False
                
            elif self.platform == "linux":
                # Try package manager
                try:
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'docker.io'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                try:
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'docker'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                self.logger.info("Please install Docker manually from https://www.docker.com/")
                return False
                
            elif self.platform == "win32":
                self.logger.info("Please install Docker Desktop from https://www.docker.com/products/docker-desktop")
                return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error installing Docker: {e}")
            return False
    
    def _install_docker_compose(self) -> bool:
        """Install Docker Compose"""
        try:
            if self.platform == "darwin":
                # Try Homebrew first
                try:
                    subprocess.run(['brew', 'install', 'docker-compose'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                self.logger.info("Docker Compose should be included with Docker Desktop")
                return False
                
            elif self.platform == "linux":
                # Try package manager
                try:
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'docker-compose'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                try:
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'docker-compose'], 
                                 check=True, capture_output=True)
                    return True
                except subprocess.CalledProcessError:
                    pass
                
                self.logger.info("Please install Docker Compose manually")
                return False
                
            elif self.platform == "win32":
                self.logger.info("Docker Compose should be included with Docker Desktop")
                return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error installing Docker Compose: {e}")
            return False
    
    def _configure_git(self) -> bool:
        """Configure Git with basic settings"""
        try:
            # Check if Git is already configured
            try:
                result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                      capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    self.logger.info("Git is already configured")
                    return True
            except:
                pass
            
            # Set basic Git configuration
            self.logger.info("Configuring Git with basic settings")
            
            # Set user name and email (these should be configured by the user)
            # For now, just set some defaults
            subprocess.run(['git', 'config', '--global', 'user.name', 'he2plus User'], 
                         capture_output=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'user@he2plus.local'], 
                         capture_output=True)
            
            # Set some useful defaults
            subprocess.run(['git', 'config', '--global', 'init.defaultBranch', 'main'], 
                         capture_output=True)
            subprocess.run(['git', 'config', '--global', 'pull.rebase', 'false'], 
                         capture_output=True)
            
            self.logger.info("Git configured with basic settings")
            return True
            
        except Exception as e:
            self.logger.error(f"Error configuring Git: {e}")
            return False
