"""
Node.js language installer for he2plus.

This module handles Node.js installation and version management across
different platforms using nvm, official installers, and package managers.
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
class NodeInstallation:
    """Represents a Node.js installation."""
    
    version: str
    path: Path
    npm_version: str
    is_system: bool
    is_nvm: bool = False
    is_volta: bool = False


@dataclass
class InstallResult:
    """Result of Node.js installation."""
    
    success: bool
    version: Optional[str] = None
    npm_version: Optional[str] = None
    path: Optional[Path] = None
    method: Optional[str] = None
    error: Optional[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class NodeInstaller:
    """Install and manage Node.js versions."""
    
    SUPPORTED_VERSIONS = ["16", "18", "20", "21"]
    PREFERRED_VERSION = "18"
    LTS_VERSIONS = ["16", "18", "20"]
    
    def __init__(self, system_info: SystemInfo):
        self.system = system_info
        self.logger = logger.bind(component="node_installer")
    
    def is_installed(self, version: str) -> Optional[NodeInstallation]:
        """Check if Node.js version is installed."""
        self.logger.debug("Checking Node.js installation", version=version)
        
        # Try different Node.js executables
        node_commands = ["node", "nodejs"]
        
        for cmd in node_commands:
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
                    
                    # Extract version number (remove 'v' prefix)
                    installed_version = output.lstrip('v')
                    
                    # Check if it matches the requested version
                    if self._version_matches(installed_version, version):
                        path = self._find_node_path(cmd)
                        npm_version = self._get_npm_version()
                        is_system = self._is_system_node(path)
                        is_nvm = self._is_nvm_node(path)
                        is_volta = self._is_volta_node(path)
                        
                        return NodeInstallation(
                            version=installed_version,
                            path=path,
                            npm_version=npm_version,
                            is_system=is_system,
                            is_nvm=is_nvm,
                            is_volta=is_volta
                        )
            
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        return None
    
    def install(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Node.js version."""
        self.logger.info("Installing Node.js", version=version)
        
        # Check if already installed
        existing = self.is_installed(version)
        if existing:
            progress.console.print(f"✓ Node.js {version} already installed at {existing.path}")
            return InstallResult(
                success=True,
                version=existing.version,
                npm_version=existing.npm_version,
                path=existing.path,
                method="existing"
            )
        
        # Choose installation method
        method = self._choose_installation_method(version)
        
        try:
            if method == "nvm":
                return self._install_nvm(version, progress, task_id)
            elif method == "volta":
                return self._install_volta(version, progress, task_id)
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
            self.logger.error("Node.js installation failed", version=version, error=str(e))
            return InstallResult(
                success=False,
                error=str(e)
            )
    
    def _choose_installation_method(self, version: str) -> str:
        """Choose the best installation method for the system."""
        system = platform.system().lower()
        
        # Check for nvm first (best for version management)
        if self._has_nvm():
            return "nvm"
        
        # Check for volta
        if self._has_volta():
            return "volta"
        
        # Check for package managers
        if system == "darwin" and "brew" in self.system.package_managers:
            return "package_manager"
        elif system == "linux" and any(pm in self.system.package_managers for pm in ["apt", "yum", "dnf"]):
            return "package_manager"
        elif system == "windows" and any(pm in self.system.package_managers for pm in ["choco", "winget"]):
            return "package_manager"
        
        # Fall back to official installer
        return "official"
    
    def _install_nvm(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Node.js using nvm."""
        self.logger.info("Installing Node.js via nvm", version=version)
        
        try:
            # Install Node.js version
            progress.update(task_id, description=f"Installing Node.js {version}...")
            result = subprocess.run(
                ["nvm", "install", version],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Use the version
            progress.update(task_id, description="Setting as active version...")
            subprocess.run(["nvm", "use", version], check=True, capture_output=True)
            
            # Set as default if this is the first Node.js installation
            if not self._has_any_node():
                progress.update(task_id, description="Setting as default version...")
                subprocess.run(["nvm", "alias", "default", version], check=True, capture_output=True)
            
            # Verify installation
            installed = self.is_installed(version)
            if installed:
                progress.update(task_id, description="Verifying installation...")
                return InstallResult(
                    success=True,
                    version=installed.version,
                    npm_version=installed.npm_version,
                    path=installed.path,
                    method="nvm"
                )
            else:
                return InstallResult(
                    success=False,
                    error="Installation completed but Node.js not found"
                )
        
        except subprocess.CalledProcessError as e:
            return InstallResult(
                success=False,
                error=f"nvm installation failed: {e.stderr.decode() if e.stderr else str(e)}"
            )
    
    def _install_volta(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Node.js using volta."""
        self.logger.info("Installing Node.js via volta", version=version)
        
        try:
            # Install Node.js version
            progress.update(task_id, description=f"Installing Node.js {version}...")
            result = subprocess.run(
                ["volta", "install", f"node@{version}"],
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
                    npm_version=installed.npm_version,
                    path=installed.path,
                    method="volta"
                )
            else:
                return InstallResult(
                    success=False,
                    error="Volta installation completed but Node.js not found"
                )
        
        except subprocess.CalledProcessError as e:
            return InstallResult(
                success=False,
                error=f"volta installation failed: {e.stderr.decode() if e.stderr else str(e)}"
            )
    
    def _install_package_manager(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Node.js using system package manager."""
        self.logger.info("Installing Node.js via package manager", version=version)
        
        system = platform.system().lower()
        
        try:
            if system == "darwin" and "brew" in self.system.package_managers:
                # Homebrew on macOS
                progress.update(task_id, description="Installing via Homebrew...")
                subprocess.run(
                    ["brew", "install", "node"],
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
                        ["sudo", "apt", "install", "-y", "nodejs", "npm"],
                        check=True,
                        capture_output=True
                    )
                elif "yum" in self.system.package_managers:
                    progress.update(task_id, description="Installing via yum...")
                    subprocess.run(
                        ["sudo", "yum", "install", "-y", "nodejs", "npm"],
                        check=True,
                        capture_output=True
                    )
                elif "dnf" in self.system.package_managers:
                    progress.update(task_id, description="Installing via dnf...")
                    subprocess.run(
                        ["sudo", "dnf", "install", "-y", "nodejs", "npm"],
                        check=True,
                        capture_output=True
                    )
            
            elif system == "windows":
                # Windows package managers
                if "choco" in self.system.package_managers:
                    progress.update(task_id, description="Installing via Chocolatey...")
                    subprocess.run(
                        ["choco", "install", "nodejs", "-y"],
                        check=True,
                        capture_output=True
                    )
                elif "winget" in self.system.package_managers:
                    progress.update(task_id, description="Installing via winget...")
                    subprocess.run(
                        ["winget", "install", "OpenJS.NodeJS"],
                        check=True,
                        capture_output=True
                    )
            
            # Verify installation
            installed = self.is_installed(version)
            if installed:
                return InstallResult(
                    success=True,
                    version=installed.version,
                    npm_version=installed.npm_version,
                    path=installed.path,
                    method="package_manager"
                )
            else:
                return InstallResult(
                    success=False,
                    error="Package manager installation completed but Node.js not found"
                )
        
        except subprocess.CalledProcessError as e:
            return InstallResult(
                success=False,
                error=f"Package manager installation failed: {e.stderr.decode() if e.stderr else str(e)}"
            )
    
    def _install_official(self, version: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Node.js using official installer."""
        self.logger.info("Installing Node.js via official installer", version=version)
        
        system = platform.system().lower()
        
        try:
            if system == "darwin":
                # macOS - download and install from nodejs.org
                progress.update(task_id, description="Downloading Node.js installer...")
                # This would require downloading the installer and running it
                # For now, we'll use a simplified approach
                return InstallResult(
                    success=False,
                    error="Official installer not implemented for macOS. Please install Node.js manually from nodejs.org"
                )
            
            elif system == "windows":
                # Windows - download and install from nodejs.org
                progress.update(task_id, description="Downloading Node.js installer...")
                # This would require downloading the installer and running it
                return InstallResult(
                    success=False,
                    error="Official installer not implemented for Windows. Please install Node.js manually from nodejs.org"
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
        """Verify Node.js installation."""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            installed_version = result.stdout.strip().lstrip('v')
            return self._version_matches(installed_version, version)
        except:
            return False
    
    def _version_matches(self, installed_version: str, requested_version: str) -> bool:
        """Check if installed version matches requested version."""
        # Handle version strings like "18.19.0" vs "18"
        installed_parts = installed_version.split(".")
        requested_parts = requested_version.split(".")
        
        # Compare major version
        return (len(installed_parts) >= 1 and 
                len(requested_parts) >= 1 and
                installed_parts[0] == requested_parts[0])
    
    def _find_node_path(self, command: str) -> Path:
        """Find the path to Node.js executable."""
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
    
    def _get_npm_version(self) -> str:
        """Get npm version."""
        try:
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return result.stdout.strip()
        except:
            return "unknown"
    
    def _is_system_node(self, path: Path) -> bool:
        """Check if Node.js is a system installation."""
        system_paths = [
            "/usr/bin",
            "/usr/local/bin",
            "C:\\Program Files\\nodejs",
            "C:\\Program Files (x86)\\nodejs"
        ]
        
        return any(str(path).startswith(sys_path) for sys_path in system_paths)
    
    def _is_nvm_node(self, path: Path) -> bool:
        """Check if Node.js is managed by nvm."""
        return ".nvm" in str(path)
    
    def _is_volta_node(self, path: Path) -> bool:
        """Check if Node.js is managed by volta."""
        return "volta" in str(path).lower()
    
    def _has_nvm(self) -> bool:
        """Check if nvm is available."""
        return shutil.which("nvm") is not None
    
    def _has_volta(self) -> bool:
        """Check if volta is available."""
        return shutil.which("volta") is not None
    
    def _has_any_node(self) -> bool:
        """Check if any Node.js version is installed."""
        for version in self.SUPPORTED_VERSIONS:
            if self.is_installed(version):
                return True
        return False
    
    def get_installed_versions(self) -> List[NodeInstallation]:
        """Get all installed Node.js versions."""
        installed = []
        
        for version in self.SUPPORTED_VERSIONS:
            installation = self.is_installed(version)
            if installation:
                installed.append(installation)
        
        return installed
    
    def get_recommended_version(self) -> str:
        """Get the recommended Node.js version for this system."""
        # Check if preferred version is available
        if self.is_installed(self.PREFERRED_VERSION):
            return self.PREFERRED_VERSION
        
        # Check for any installed version
        installed = self.get_installed_versions()
        if installed:
            return installed[0].version
        
        # Return preferred version for installation
        return self.PREFERRED_VERSION
    
    def install_npm_package(self, package: str, global_install: bool = False) -> bool:
        """Install an npm package."""
        try:
            cmd = ["npm", "install"]
            if global_install:
                cmd.append("-g")
            cmd.append(package)
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error("npm package installation failed", package=package, error=str(e))
            return False
    
    def get_npm_packages(self) -> List[Dict[str, str]]:
        """Get list of globally installed npm packages."""
        try:
            result = subprocess.run(
                ["npm", "list", "-g", "--depth=0", "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            import json
            data = json.loads(result.stdout)
            packages = []
            
            if "dependencies" in data:
                for name, info in data["dependencies"].items():
                    packages.append({
                        "name": name,
                        "version": info.get("version", "unknown")
                    })
            
            return packages
        except:
            return []
