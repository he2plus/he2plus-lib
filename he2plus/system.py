"""
System management utilities for he2plus library
"""

import os
import sys
import platform
import subprocess
import psutil
from typing import Dict, Any, List, Optional
from .utils import Logger


class SystemManager:
    """System management and automation utilities"""
    
    def __init__(self, logger: Logger, config):
        """
        Initialize system manager
        
        Args:
            logger: Logger instance
            config: Configuration instance
        """
        self.logger = logger
        self.config = config
        self.platform = platform.system().lower()
        self.arch = platform.machine().lower()
        
        self.logger.info(f"SystemManager initialized for {self.platform} {self.arch}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information
        
        Returns:
            Dictionary containing system information
        """
        try:
            info = {
                "platform": self.platform,
                "architecture": self.arch,
                "python_version": sys.version,
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "disk_usage": psutil.disk_usage('/').percent,
                "hostname": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
            }
            
            # Platform-specific information
            if self.platform == "darwin":  # macOS
                info.update(self._get_macos_info())
            elif self.platform == "linux":
                info.update(self._get_linux_info())
            elif self.platform == "windows":
                info.update(self._get_windows_info())
            
            return info
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}
    
    def _get_macos_info(self) -> Dict[str, Any]:
        """Get macOS-specific information"""
        try:
            result = subprocess.run(['sw_vers'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                macos_info = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        macos_info[key.strip().lower().replace(' ', '_')] = value.strip()
                return macos_info
        except Exception as e:
            self.logger.warning(f"Could not get macOS info: {e}")
        return {}
    
    def _get_linux_info(self) -> Dict[str, Any]:
        """Get Linux-specific information"""
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                linux_info = {}
                for line in lines:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        linux_info[key.lower()] = value.strip('"')
                return linux_info
        except Exception as e:
            self.logger.warning(f"Could not get Linux info: {e}")
        return {}
    
    def _get_windows_info(self) -> Dict[str, Any]:
        """Get Windows-specific information"""
        try:
            result = subprocess.run(['systeminfo'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                windows_info = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        windows_info[key.strip().lower().replace(' ', '_')] = value.strip()
                return windows_info
        except Exception as e:
            self.logger.warning(f"Could not get Windows info: {e}")
        return {}
    
    def check_dependencies(self) -> Dict[str, bool]:
        """
        Check if required dependencies are available
        
        Returns:
            Dictionary mapping dependency names to availability status
        """
        dependencies = {
            "python": self._check_python(),
            "pip": self._check_pip(),
            "git": self._check_git(),
            "curl": self._check_curl(),
            "wget": self._check_wget(),
        }
        
        # Platform-specific dependencies
        if self.platform == "darwin":
            dependencies.update({
                "homebrew": self._check_homebrew(),
                "xcode": self._check_xcode(),
            })
        elif self.platform == "linux":
            dependencies.update({
                "apt": self._check_apt(),
                "yum": self._check_yum(),
                "dnf": self._check_dnf(),
            })
        elif self.platform == "windows":
            dependencies.update({
                "chocolatey": self._check_chocolatey(),
                "winget": self._check_winget(),
            })
        
        return dependencies
    
    def _check_python(self) -> bool:
        """Check if Python is available"""
        return sys.executable is not None
    
    def _check_pip(self) -> bool:
        """Check if pip is available"""
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_git(self) -> bool:
        """Check if git is available"""
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_curl(self) -> bool:
        """Check if curl is available"""
        try:
            subprocess.run(['curl', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_wget(self) -> bool:
        """Check if wget is available"""
        try:
            subprocess.run(['wget', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_homebrew(self) -> bool:
        """Check if Homebrew is available"""
        try:
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_xcode(self) -> bool:
        """Check if Xcode command line tools are available"""
        try:
            subprocess.run(['xcode-select', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_apt(self) -> bool:
        """Check if apt is available"""
        try:
            subprocess.run(['apt', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_yum(self) -> bool:
        """Check if yum is available"""
        try:
            subprocess.run(['yum', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_dnf(self) -> bool:
        """Check if dnf is available"""
        try:
            subprocess.run(['dnf', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_chocolatey(self) -> bool:
        """Check if Chocolatey is available"""
        try:
            subprocess.run(['choco', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_winget(self) -> bool:
        """Check if winget is available"""
        try:
            subprocess.run(['winget', '--version'], capture_output=True, check=True)
            return True
        except:
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
            if method == "auto":
                method = self._detect_best_method(package)
            
            self.logger.info(f"Installing {package} using {method}")
            
            if method == "pip":
                return self._install_via_pip(package)
            elif method == "brew":
                return self._install_via_brew(package)
            elif method == "apt":
                return self._install_via_apt(package)
            elif method == "yum":
                return self._install_via_yum(package)
            elif method == "dnf":
                return self._install_via_dnf(package)
            elif method == "choco":
                return self._install_via_chocolatey(package)
            elif method == "winget":
                return self._install_via_winget(package)
            else:
                self.logger.error(f"Unknown installation method: {method}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error installing package {package}: {e}")
            return False
    
    def _detect_best_method(self, package: str) -> str:
        """Detect the best installation method for a package"""
        dependencies = self.check_dependencies()
        
        if self.platform == "darwin" and dependencies.get("homebrew"):
            return "brew"
        elif self.platform == "linux" and dependencies.get("apt"):
            return "apt"
        elif self.platform == "linux" and dependencies.get("dnf"):
            return "dnf"
        elif self.platform == "linux" and dependencies.get("yum"):
            return "yum"
        elif self.platform == "windows" and dependencies.get("chocolatey"):
            return "choco"
        elif self.platform == "windows" and dependencies.get("winget"):
            return "winget"
        else:
            return "pip"
    
    def _install_via_pip(self, package: str) -> bool:
        """Install package via pip"""
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Pip installation failed: {e}")
            return False
    
    def _install_via_brew(self, package: str) -> bool:
        """Install package via Homebrew"""
        try:
            result = subprocess.run(['brew', 'install', package], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Homebrew installation failed: {e}")
            return False
    
    def _install_via_apt(self, package: str) -> bool:
        """Install package via apt"""
        try:
            result = subprocess.run(['sudo', 'apt', 'install', '-y', package], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"APT installation failed: {e}")
            return False
    
    def _install_via_yum(self, package: str) -> bool:
        """Install package via yum"""
        try:
            result = subprocess.run(['sudo', 'yum', 'install', '-y', package], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"YUM installation failed: {e}")
            return False
    
    def _install_via_dnf(self, package: str) -> bool:
        """Install package via dnf"""
        try:
            result = subprocess.run(['sudo', 'dnf', 'install', '-y', package], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"DNF installation failed: {e}")
            return False
    
    def _install_via_chocolatey(self, package: str) -> bool:
        """Install package via Chocolatey"""
        try:
            result = subprocess.run(['choco', 'install', package, '-y'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Chocolatey installation failed: {e}")
            return False
    
    def _install_via_winget(self, package: str) -> bool:
        """Install package via winget"""
        try:
            result = subprocess.run(['winget', 'install', package], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Winget installation failed: {e}")
            return False
