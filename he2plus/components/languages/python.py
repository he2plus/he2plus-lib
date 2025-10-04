"""
Python language installer for he2plus.

This module handles Python installation and version management across
different platforms using pyenv, official installers, and package managers.
"""

import subprocess
import shutil
import platform
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any
import structlog
from rich.progress import Progress, TaskID

from ...core.system import SystemInfo

logger = structlog.get_logger(__name__)


@dataclass
class PythonInstallation:
    """Represents a Python installation."""
    
    version: str
    path: Path
    is_system: bool
    is_pyenv: bool = False
    is_conda: bool = False
    is_poetry: bool = False


@dataclass
class InstallResult:
    """Result of Python installation."""
    
    success: bool
    version: Optional[str] = None
    path: Optional[Path] = None
    method: Optional[str] = None
    error: Optional[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class PythonInstaller:
    """Install and manage Python versions."""
    
    SUPPORTED_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]
    PREFERRED_VERSION = "3.11"
    
    def __init__(self, system_info: SystemInfo):
        self.system = system_info
        self.logger = logger.bind(component="python_installer")
    
    def is_installed(self, version: str) -> Optional[PythonInstallation]:
        """Check if Python version is installed."""
        self.logger.debug("Checking Python installation", version=version)
        
        # Try different Python executables
        python_commands = [
            f"python{version}",
            f"python{version.replace('.', '')}",
            "python3",
            "python"
        ]
        
        for cmd in python_commands:
            try:
                result = subprocess.run(
                    [cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    # Parse version from output
                    output = result.stdout.strip()
                    if not output:
                        output = result.stderr.strip()
                    
                    # Extract version number
                    version_parts = output.split()
                    if len(version_parts) >= 2:
                        installed_version = version_parts[1]
                        
                        # Check if it matches the requested version
                        if self._version_matches(installed_version, version):
                            path = self._find_python_path(cmd)
                            is_system = self._is_system_python(path)
                            is_pyenv = self._is_pyenv_python(path)
                            is_conda = self._is_conda_python(path)
                            
                            return PythonInstallation(
                                version=installed_version,
                                path=path,
                                is_system=is_system,
                                is_pyenv=is_pyenv,
                                is_conda=is_conda
                            )
            
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        return None
    
    def install(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Python version."""
        self.logger.info("Installing Python", version=version)
        
        # Check if already installed
        existing = self.is_installed(version)
        if existing:
            progress.console.print(f"✓ Python {version} already installed at {existing.path}")
            return InstallResult(
                success=True,
                version=existing.version,
                path=existing.path,
                method="existing"
            )
        
        # Choose installation method
        method = self._choose_installation_method(version)
        
        try:
            if method == "pyenv":
                return self._install_pyenv(version, progress, task_id)
            elif method == "conda":
                return self._install_conda(version, progress, task_id)
            elif method == "official":
                return self._install_official(version, progress, task_id)
            elif method == "package_manager":
                return self._install_package_manager(version, progress, task_id)
            else:
                return InstallResult(
                    success=False,
                    error=f"No suitable installation method found for {version}"
                )
        
        except Exception as e:
            self.logger.error("Python installation failed", version=version, error=str(e))
            return InstallResult(
                success=False,
                error=str(e)
            )
    
    def _choose_installation_method(self, version: str) -> str:
        """Choose the best installation method for the system."""
        system = platform.system().lower()
        
        # Check for pyenv first (best for version management)
        if self._has_pyenv():
            return "pyenv"
        
        # Check for conda
        if self._has_conda():
            return "conda"
        
        # Check for package managers
        if system == "darwin" and "brew" in self.system.package_managers:
            return "package_manager"
        elif system == "linux" and any(pm in self.system.package_managers for pm in ["apt", "yum", "dnf"]):
            return "package_manager"
        elif system == "windows" and any(pm in self.system.package_managers for pm in ["choco", "winget"]):
            return "package_manager"
        
        # Fall back to official installer
        return "official"
    
    def _install_pyenv(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Python using pyenv."""
        self.logger.info("Installing Python via pyenv", version=version)
        
        try:
            # Update pyenv
            progress.update(task_id, description="Updating pyenv...")
            subprocess.run(["pyenv", "update"], check=True, capture_output=True)
            
            # Install Python version
            progress.update(task_id, description=f"Installing Python {version}...")
            result = subprocess.run(
                ["pyenv", "install", version],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Set as global version if this is the first Python installation
            if not self._has_any_python():
                progress.update(task_id, description="Setting as global version...")
                subprocess.run(["pyenv", "global", version], check=True)
            
            # Verify installation
            installed = self.is_installed(version)
            if installed:
                progress.update(task_id, description="Verifying installation...")
                return InstallResult(
                    success=True,
                    version=installed.version,
                    path=installed.path,
                    method="pyenv"
                )
            else:
                return InstallResult(
                    success=False,
                    error="Installation completed but Python not found"
                )
        
        except subprocess.CalledProcessError as e:
            return InstallResult(
                success=False,
                error=f"pyenv installation failed: {e.stderr.decode() if e.stderr else str(e)}"
            )
    
    def _install_conda(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Python using conda."""
        self.logger.info("Installing Python via conda", version=version)
        
        try:
            # Create conda environment with specific Python version
            env_name = f"python{version.replace('.', '')}"
            progress.update(task_id, description=f"Creating conda environment...")
            
            result = subprocess.run(
                ["conda", "create", "-n", env_name, f"python={version}", "-y"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Verify installation
            installed = self.is_installed(version)
            if installed:
                return InstallResult(
                    success=True,
                    version=installed.version,
                    path=installed.path,
                    method="conda"
                )
            else:
                return InstallResult(
                    success=False,
                    error="Conda installation completed but Python not found"
                )
        
        except subprocess.CalledProcessError as e:
            return InstallResult(
                success=False,
                error=f"conda installation failed: {e.stderr.decode() if e.stderr else str(e)}"
            )
    
    def _install_package_manager(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Python using system package manager."""
        self.logger.info("Installing Python via package manager", version=version)
        
        system = platform.system().lower()
        
        try:
            if system == "darwin" and "brew" in self.system.package_managers:
                # Homebrew on macOS
                progress.update(task_id, description="Installing via Homebrew...")
                subprocess.run(
                    ["brew", "install", f"python@{version}"],
                    check=True,
                    capture_output=True
                )
            
            elif system == "linux":
                # Linux package managers
                if "apt" in self.system.package_managers:
                    progress.update(task_id, description="Installing via apt...")
                    subprocess.run(
                        ["sudo", "apt", "update"], check=True, capture_output=True
                    )
                    subprocess.run(
                        ["sudo", "apt", "install", "-y", f"python{version}"],
                        check=True,
                        capture_output=True
                    )
                elif "yum" in self.system.package_managers:
                    progress.update(task_id, description="Installing via yum...")
                    subprocess.run(
                        ["sudo", "yum", "install", "-y", f"python{version}"],
                        check=True,
                        capture_output=True
                    )
                elif "dnf" in self.system.package_managers:
                    progress.update(task_id, description="Installing via dnf...")
                    subprocess.run(
                        ["sudo", "dnf", "install", "-y", f"python{version}"],
                        check=True,
                        capture_output=True
                    )
            
            elif system == "windows":
                # Windows package managers
                if "choco" in self.system.package_managers:
                    progress.update(task_id, description="Installing via Chocolatey...")
                    subprocess.run(
                        ["choco", "install", "python", "--version", version, "-y"],
                        check=True,
                        capture_output=True
                    )
                elif "winget" in self.system.package_managers:
                    progress.update(task_id, description="Installing via winget...")
                    subprocess.run(
                        ["winget", "install", "Python.Python.3.11"],
                        check=True,
                        capture_output=True
                    )
            
            # Verify installation
            installed = self.is_installed(version)
            if installed:
                return InstallResult(
                    success=True,
                    version=installed.version,
                    path=installed.path,
                    method="package_manager"
                )
            else:
                return InstallResult(
                    success=False,
                    error="Package manager installation completed but Python not found"
                )
        
        except subprocess.CalledProcessError as e:
            return InstallResult(
                success=False,
                error=f"Package manager installation failed: {e.stderr.decode() if e.stderr else str(e)}"
            )
    
    def _install_official(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Python using official installer."""
        self.logger.info("Installing Python via official installer", version=version)
        
        system = platform.system().lower()
        
        try:
            if system == "darwin":
                # macOS - download and install from python.org
                progress.update(task_id, description="Downloading Python installer...")
                # This would require downloading the installer and running it
                # For now, we'll use a simplified approach
                return InstallResult(
                    success=False,
                    error="Official installer not implemented for macOS. Please install Python manually from python.org"
                )
            
            elif system == "windows":
                # Windows - download and install from python.org
                progress.update(task_id, description="Downloading Python installer...")
                # This would require downloading the installer and running it
                return InstallResult(
                    success=False,
                    error="Official installer not implemented for Windows. Please install Python manually from python.org"
                )
            
            else:
                return InstallResult(
                    success=False,
                    error="Official installer not supported on this platform"
                )
        
        except Exception as e:
            return InstallResult(
                success=False,
                error=f"Official installer failed: {str(e)}"
            )
    
    def verify(self, version: str) -> bool:
        """Verify Python installation."""
        try:
            result = subprocess.run(
                [f"python{version}", "-c", "import sys; print(sys.version)"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return version in result.stdout
        except:
            return False
    
    def _version_matches(self, installed_version: str, requested_version: str) -> bool:
        """Check if installed version matches requested version."""
        # Handle version strings like "3.11.0" vs "3.11"
        installed_parts = installed_version.split(".")
        requested_parts = requested_version.split(".")
        
        # Compare major and minor versions
        return (len(installed_parts) >= 2 and 
                len(requested_parts) >= 2 and
                installed_parts[0] == requested_parts[0] and
                installed_parts[1] == requested_parts[1])
    
    def _find_python_path(self, command: str) -> Path:
        """Find the path to Python executable."""
        try:
            result = subprocess.run(
                ["which", command] if platform.system() != "Windows" else ["where", command],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip().split('\n')[0])
        except:
            return Path(command)
    
    def _is_system_python(self, path: Path) -> bool:
        """Check if Python is a system installation."""
        system_paths = [
            "/usr/bin",
            "/usr/local/bin",
            "C:\\Python",
            "C:\\Program Files\\Python"
        ]
        
        return any(str(path).startswith(sys_path) for sys_path in system_paths)
    
    def _is_pyenv_python(self, path: Path) -> bool:
        """Check if Python is managed by pyenv."""
        return ".pyenv" in str(path)
    
    def _is_conda_python(self, path: Path) -> bool:
        """Check if Python is managed by conda."""
        return "conda" in str(path).lower() or "anaconda" in str(path).lower()
    
    def _has_pyenv(self) -> bool:
        """Check if pyenv is available."""
        return shutil.which("pyenv") is not None
    
    def _has_conda(self) -> bool:
        """Check if conda is available."""
        return shutil.which("conda") is not None
    
    def _has_any_python(self) -> bool:
        """Check if any Python version is installed."""
        for version in self.SUPPORTED_VERSIONS:
            if self.is_installed(version):
                return True
        return False
    
    def get_installed_versions(self) -> List[PythonInstallation]:
        """Get all installed Python versions."""
        installed = []
        
        for version in self.SUPPORTED_VERSIONS:
            installation = self.is_installed(version)
            if installation:
                installed.append(installation)
        
        return installed
    
    def get_recommended_version(self) -> str:
        """Get the recommended Python version for this system."""
        # Check if preferred version is available
        if self.is_installed(self.PREFERRED_VERSION):
            return self.PREFERRED_VERSION
        
        # Check for any installed version
        installed = self.get_installed_versions()
        if installed:
            return installed[0].version
        
        # Return preferred version for installation
        return self.PREFERRED_VERSION
