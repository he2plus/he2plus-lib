"""
Core installation engine for he2plus.

This module provides the main installation engine that coordinates
downloads, installations, and verification of development tools.
"""

import os
import sys
import subprocess
import shutil
import tempfile
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from urllib.parse import urlparse
import structlog
import requests
from rich.progress import Progress, TaskID

from .system import SystemInfo
from ..profiles.base import Component, VerificationStep

logger = structlog.get_logger(__name__)


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    file_path: Optional[Path] = None
    size_bytes: int = 0
    checksum: Optional[str] = None
    error: Optional[str] = None


@dataclass
class InstallResult:
    """Result of an installation operation."""
    success: bool
    version: Optional[str] = None
    path: Optional[Path] = None
    method: Optional[str] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """Result of a verification operation."""
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None


class PackageManager:
    """Interface for package managers."""
    
    def __init__(self, system_info: SystemInfo):
        self.system = system_info
        self.logger = logger.bind(package_manager=self.__class__.__name__)
    
    def is_available(self) -> bool:
        """Check if this package manager is available."""
        raise NotImplementedError
    
    def install(self, package: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install a package using this package manager."""
        raise NotImplementedError
    
    def is_installed(self, package: str) -> bool:
        """Check if a package is installed."""
        raise NotImplementedError
    
    def get_version(self, package: str) -> Optional[str]:
        """Get the version of an installed package."""
        raise NotImplementedError


class HomebrewManager(PackageManager):
    """Homebrew package manager for macOS."""
    
    def is_available(self) -> bool:
        """Check if Homebrew is available."""
        return shutil.which("brew") is not None
    
    def install(self, package: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install a package using Homebrew."""
        if not self.is_available():
            return InstallResult(
                success=False,
                error="Homebrew not available"
            )
        
        try:
            progress.update(task_id, description=f"Installing {package} with Homebrew...")
            
            result = subprocess.run(
                ["brew", "install", package],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes
            )
            
            if result.returncode == 0:
                version = self.get_version(package)
                return InstallResult(
                    success=True,
                    version=version,
                    method="homebrew"
                )
            else:
                return InstallResult(
                    success=False,
                    error=f"Homebrew installation failed: {result.stderr}"
                )
        
        except subprocess.TimeoutExpired:
            return InstallResult(
                success=False,
                error="Homebrew installation timed out"
            )
        except Exception as e:
            return InstallResult(
                success=False,
                error=f"Homebrew installation error: {str(e)}"
            )
    
    def is_installed(self, package: str) -> bool:
        """Check if a package is installed via Homebrew."""
        if not self.is_available():
            return False
        
        try:
            result = subprocess.run(
                ["brew", "list", package],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def get_version(self, package: str) -> Optional[str]:
        """Get the version of an installed package."""
        if not self.is_available():
            return None
        
        try:
            result = subprocess.run(
                ["brew", "list", "--versions", package],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # Parse version from output like "package 1.2.3"
                parts = result.stdout.strip().split()
                if len(parts) >= 2:
                    return parts[1]
        except:
            pass
        
        return None


class APTManager(PackageManager):
    """APT package manager for Debian/Ubuntu."""
    
    def is_available(self) -> bool:
        """Check if APT is available."""
        return shutil.which("apt") is not None
    
    def install(self, package: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install a package using APT."""
        if not self.is_available():
            return InstallResult(
                success=False,
                error="APT not available"
            )
        
        try:
            progress.update(task_id, description=f"Installing {package} with APT...")
            
            # Update package list first
            subprocess.run(
                ["sudo", "apt", "update"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            result = subprocess.run(
                ["sudo", "apt", "install", "-y", package],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                version = self.get_version(package)
                return InstallResult(
                    success=True,
                    version=version,
                    method="apt"
                )
            else:
                return InstallResult(
                    success=False,
                    error=f"APT installation failed: {result.stderr}"
                )
        
        except subprocess.TimeoutExpired:
            return InstallResult(
                success=False,
                error="APT installation timed out"
            )
        except Exception as e:
            return InstallResult(
                success=False,
                error=f"APT installation error: {str(e)}"
            )
    
    def is_installed(self, package: str) -> bool:
        """Check if a package is installed via APT."""
        if not self.is_available():
            return False
        
        try:
            result = subprocess.run(
                ["dpkg", "-l", package],
                capture_output=True,
                text=True
            )
            return "ii" in result.stdout
        except:
            return False
    
    def get_version(self, package: str) -> Optional[str]:
        """Get the version of an installed package."""
        if not self.is_available():
            return None
        
        try:
            result = subprocess.run(
                ["dpkg", "-s", package],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        return line.split(':', 1)[1].strip()
        except:
            pass
        
        return None


class ChocolateyManager(PackageManager):
    """Chocolatey package manager for Windows."""
    
    def is_available(self) -> bool:
        """Check if Chocolatey is available."""
        return shutil.which("choco") is not None
    
    def install(self, package: str, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install a package using Chocolatey."""
        if not self.is_available():
            return InstallResult(
                success=False,
                error="Chocolatey not available"
            )
        
        try:
            progress.update(task_id, description=f"Installing {package} with Chocolatey...")
            
            result = subprocess.run(
                ["choco", "install", package, "-y"],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                version = self.get_version(package)
                return InstallResult(
                    success=True,
                    version=version,
                    method="chocolatey"
                )
            else:
                return InstallResult(
                    success=False,
                    error=f"Chocolatey installation failed: {result.stderr}"
                )
        
        except subprocess.TimeoutExpired:
            return InstallResult(
                success=False,
                error="Chocolatey installation timed out"
            )
        except Exception as e:
            return InstallResult(
                success=False,
                error=f"Chocolatey installation error: {str(e)}"
            )
    
    def is_installed(self, package: str) -> bool:
        """Check if a package is installed via Chocolatey."""
        if not self.is_available():
            return False
        
        try:
            result = subprocess.run(
                ["choco", "list", "--local-only", package],
                capture_output=True,
                text=True
            )
            return package in result.stdout
        except:
            return False
    
    def get_version(self, package: str) -> Optional[str]:
        """Get the version of an installed package."""
        if not self.is_available():
            return None
        
        try:
            result = subprocess.run(
                ["choco", "list", "--local-only", package],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if package in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            return parts[1]
        except:
            pass
        
        return None


class GitHubReleaseInstaller:
    """Installer for tools distributed via GitHub releases."""
    
    def __init__(self, system_info: SystemInfo):
        self.system = system_info
        self.logger = logger.bind(installer="github_release")
        self.temp_dir = Path(tempfile.gettempdir()) / "he2plus_downloads"
        self.temp_dir.mkdir(exist_ok=True)
    
    def get_latest_release(self, repo: str) -> Optional[Dict[str, Any]]:
        """Get the latest release information from GitHub."""
        try:
            url = f"https://api.github.com/repos/{repo}/releases/latest"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error("Failed to get GitHub release", repo=repo, error=str(e))
            return None
    
    def download_asset(self, asset_url: str, filename: str, progress: Progress, task_id: TaskID) -> DownloadResult:
        """Download an asset from GitHub release."""
        try:
            file_path = self.temp_dir / filename
            
            progress.update(task_id, description=f"Downloading {filename}...")
            
            response = requests.get(asset_url, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress.update(task_id, completed=downloaded, total=total_size)
            
            return DownloadResult(
                success=True,
                file_path=file_path,
                size_bytes=downloaded
            )
        
        except Exception as e:
            return DownloadResult(
                success=False,
                error=f"Download failed: {str(e)}"
            )
    
    def install_binary(self, file_path: Path, install_dir: Path, binary_name: str) -> InstallResult:
        """Install a binary from a downloaded file."""
        try:
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # Handle different file types
            if file_path.suffix == '.zip':
                import zipfile
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(install_dir)
            elif file_path.suffix == '.tar.gz':
                import tarfile
                with tarfile.open(file_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(install_dir)
            elif file_path.suffix == '.exe':
                # Windows executable
                binary_path = install_dir / binary_name
                shutil.copy2(file_path, binary_path)
            else:
                # Assume it's a binary
                binary_path = install_dir / binary_name
                shutil.copy2(file_path, binary_path)
                binary_path.chmod(0o755)
            
            # Find the actual binary
            binary_path = self._find_binary(install_dir, binary_name)
            if binary_path:
                return InstallResult(
                    success=True,
                    path=binary_path,
                    method="github_release"
                )
            else:
                return InstallResult(
                    success=False,
                    error="Binary not found after extraction"
                )
        
        except Exception as e:
            return InstallResult(
                success=False,
                error=f"Installation failed: {str(e)}"
            )
    
    def _find_binary(self, install_dir: Path, binary_name: str) -> Optional[Path]:
        """Find the binary in the extracted directory."""
        # Look for the binary in common locations
        possible_paths = [
            install_dir / binary_name,
            install_dir / f"{binary_name}.exe",
            install_dir / "bin" / binary_name,
            install_dir / "bin" / f"{binary_name}.exe"
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_file():
                return path
        
        # Search recursively
        for path in install_dir.rglob(binary_name):
            if path.is_file():
                return path
        
        for path in install_dir.rglob(f"{binary_name}.exe"):
            if path.is_file():
                return path
        
        return None


class InstallationEngine:
    """Main installation engine that coordinates all installation methods."""
    
    def __init__(self, system_info: SystemInfo):
        self.system = system_info
        self.logger = logger.bind(component="installation_engine")
        
        # Initialize package managers
        self.package_managers = {
            "homebrew": HomebrewManager(system_info),
            "apt": APTManager(system_info),
            "chocolatey": ChocolateyManager(system_info)
        }
        
        # Initialize GitHub release installer
        self.github_installer = GitHubReleaseInstaller(system_info)
        
        # Installation directory
        self.install_dir = Path.home() / ".he2plus" / "tools"
        self.install_dir.mkdir(parents=True, exist_ok=True)
    
    def install_component(self, component: Component, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install a single component using the best available method."""
        self.logger.info("Installing component", component=component.id, name=component.name)
        
        # Try different installation methods in order of preference
        for method in component.install_methods:
            if method == "package_manager":
                result = self._install_via_package_manager(component, progress, task_id)
                if result.success:
                    return result
            elif method == "github_release":
                result = self._install_via_github_release(component, progress, task_id)
                if result.success:
                    return result
            elif method == "official":
                result = self._install_via_official(component, progress, task_id)
                if result.success:
                    return result
        
        return InstallResult(
            success=False,
            error=f"No suitable installation method found for {component.name}"
        )
    
    def _install_via_package_manager(self, component: Component, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install component via package manager."""
        # Determine the best package manager for this system
        system = self.system.os_name.lower()
        
        if system == "macos" and "homebrew" in [pm for pm in self.package_managers.keys() if self.package_managers[pm].is_available()]:
            pm = self.package_managers["homebrew"]
        elif system == "linux" and "apt" in [pm for pm in self.package_managers.keys() if self.package_managers[pm].is_available()]:
            pm = self.package_managers["apt"]
        elif system == "windows" and "chocolatey" in [pm for pm in self.package_managers.keys() if self.package_managers[pm].is_available()]:
            pm = self.package_managers["chocolatey"]
        else:
            return InstallResult(
                success=False,
                error="No suitable package manager available"
            )
        
        # Map component to package name
        package_name = self._get_package_name(component)
        if not package_name:
            return InstallResult(
                success=False,
                error=f"No package name mapping for {component.id}"
            )
        
        return pm.install(package_name, progress, task_id)
    
    def _install_via_github_release(self, component: Component, progress: TaskID) -> InstallResult:
        """Install component via GitHub release."""
        # This would need to be configured per component
        # For now, return not implemented
        return InstallResult(
            success=False,
            error="GitHub release installation not yet implemented for this component"
        )
    
    def _install_via_official(self, component: Component, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install component via official installer."""
        # This would need to be configured per component
        # For now, return not implemented
        return InstallResult(
            success=False,
            error="Official installer not yet implemented for this component"
        )
    
    def _get_package_name(self, component: Component) -> Optional[str]:
        """Get the package name for a component in the system's package manager."""
        # Map component IDs to package names
        package_mapping = {
            # Core tools
            "tool.git": "git",
            "language.python": "python3",
            "language.python.3.11": "python3",
            "language.node": "nodejs",
            "language.node.18": "nodejs",
            "tool.docker": "docker",
            "tool.curl": "curl",
            "tool.wget": "wget",
            "tool.jq": "jq",
            "tool.gh": "gh",
            "tool.aws": "awscli",
            "tool.terraform": "terraform",
            "tool.kubectl": "kubectl",
            "tool.helm": "helm",
            "tool.docker-compose": "docker-compose",
            
            # Package managers
            "tool.npm": "npm",
            "tool.yarn": "yarn",
            "tool.pnpm": "pnpm",
            "tool.pip": "python3-pip",
            "tool.pipx": "pipx",
            "tool.conda": "miniconda",
            "tool.mamba": "mamba",
            "tool.poetry": "poetry",
            "tool.pipenv": "pipenv",
            "tool.virtualenv": "python3-venv",
            
            # Languages and runtimes
            "tool.rust": "rust",
            "tool.go": "golang",
            "tool.java": "openjdk-11-jdk",
            "language.typescript": "typescript",
            
            # Build tools
            "tool.maven": "maven",
            "tool.gradle": "gradle",
            "tool.make": "make",
            "tool.cmake": "cmake",
            "tool.gcc": "gcc",
            "tool.clang": "clang",
            
            # Version managers
            "tool.nvm": "nvm",
            "tool.pyenv": "pyenv",
            "tool.rbenv": "rbenv",
            "tool.nodenv": "nodenv",
            "tool.volta": "volta",
            "tool.fnm": "fnm",
            "tool.asdf": "asdf",
            "tool.sdkman": "sdkman",
            
            # Development tools
            "tool.vscode": "code",
            "tool.jupyter": "jupyter",
            "tool.jupyter-lab": "jupyterlab",
            "tool.jupyter-notebook": "notebook",
            "tool.eslint": "eslint",
            "tool.prettier": "prettier",
            "tool.husky": "husky",
            "tool.jest": "jest",
            "tool.cypress": "cypress",
            "tool.playwright": "playwright",
            "tool.detox": "detox",
            "tool.maestro": "maestro",
            "tool.flipper": "flipper",
            "tool.react-native-debugger": "react-native-debugger",
            
            # CLI tools
            "tool.react-native-cli": "react-native-cli",
            "tool.expo-cli": "expo-cli",
            "tool.vercel-cli": "vercel",
            "tool.netlify-cli": "netlify-cli",
            "tool.android-studio": "android-studio",
            "tool.android-sdk": "android-sdk",
            "tool.xcode": "xcode",
            "tool.ios-simulator": "ios-simulator",
            "tool.cocoapods": "cocoapods",
            
            # Python tools
            "tool.pytest": "pytest",
            "tool.black": "black",
            "tool.flake8": "flake8",
            "tool.mypy": "mypy",
            
            # Python packages (for pip)
            "library.tensorflow": "tensorflow",
            "library.pytorch": "torch",
            "library.scikit-learn": "scikit-learn",
            "library.keras": "keras",
            "library.pandas": "pandas",
            "library.numpy": "numpy",
            "library.scipy": "scipy",
            "library.polars": "polars",
            "library.matplotlib": "matplotlib",
            "library.seaborn": "seaborn",
            "library.plotly": "plotly",
            "library.bokeh": "bokeh",
            "library.transformers": "transformers",
            "library.datasets": "datasets",
            "library.accelerate": "accelerate",
            "library.optuna": "optuna",
            "library.opencv": "opencv-python",
            "library.pillow": "pillow",
            "library.albumentations": "albumentations",
            "library.nltk": "nltk",
            "library.spacy": "spacy",
            "library.gensim": "gensim",
            "library.prophet": "prophet",
            "library.statsmodels": "statsmodels",
            "library.fastapi": "fastapi",
            "library.streamlit": "streamlit",
            "library.gradio": "gradio",
            "library.mlflow": "mlflow",
            "library.sqlalchemy": "sqlalchemy",
            "library.redis": "redis",
            "library.cupy": "cupy",
            "library.rapids": "rapids",
            
            # Node.js packages (for npm)
            "framework.nextjs": "next",
            "library.react": "react",
            "library.react-dom": "react-dom",
            "library.tailwindcss": "tailwindcss",
            "library.styled-components": "styled-components",
            "library.zustand": "zustand",
            "library.redux-toolkit": "@reduxjs/toolkit",
            "library.prisma": "prisma",
            "library.drizzle": "drizzle-orm",
            "library.next-auth": "next-auth",
            "library.clerk": "@clerk/nextjs",
            
            # React Native packages
            "framework.react-native": "react-native",
            "library.react-native-reanimated": "react-native-reanimated",
            "library.react-native-gesture-handler": "react-native-gesture-handler",
            "library.react-navigation": "@react-navigation/native",
            "library.react-native-elements": "react-native-elements",
            "library.native-base": "native-base",
            "library.tamagui": "@tamagui/core",
            "library.apollo-client": "@apollo/client",
            "library.axios": "axios",
            "library.react-native-async-storage": "@react-native-async-storage/async-storage",
            "library.realm": "realm",
            "library.react-native-push-notification": "react-native-push-notification",
            "library.react-native-camera": "react-native-camera",
            "library.react-native-image-picker": "react-native-image-picker",
            "library.flipper-plugin-react-native-performance": "flipper-plugin-react-native-performance",
        }
        
        return package_mapping.get(component.id)
    
    def verify_component(self, component: Component, verification_step: VerificationStep) -> VerificationResult:
        """Verify that a component is properly installed."""
        if not verification_step.command:
            return VerificationResult(success=True)
        
        try:
            result = subprocess.run(
                verification_step.command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                
                # Check expected output if specified
                if verification_step.expected_output:
                    if output == verification_step.expected_output:
                        return VerificationResult(success=True, output=output)
                    else:
                        return VerificationResult(
                            success=False,
                            error=f"Expected '{verification_step.expected_output}', got '{output}'"
                        )
                
                # Check contains text if specified
                if verification_step.contains_text:
                    if verification_step.contains_text in output:
                        return VerificationResult(success=True, output=output)
                    else:
                        return VerificationResult(
                            success=False,
                            error=f"Output does not contain '{verification_step.contains_text}'"
                        )
                
                return VerificationResult(success=True, output=output)
            else:
                return VerificationResult(
                    success=False,
                    error=f"Command failed with return code {result.returncode}: {result.stderr}"
                )
        
        except subprocess.TimeoutExpired:
            return VerificationResult(
                success=False,
                error="Verification command timed out"
            )
        except Exception as e:
            return VerificationResult(
                success=False,
                error=f"Verification failed: {str(e)}"
            )
    
    def cleanup(self):
        """Clean up temporary files and directories."""
        try:
            if self.github_installer.temp_dir.exists():
                shutil.rmtree(self.github_installer.temp_dir)
        except Exception as e:
            self.logger.warning("Failed to cleanup temporary files", error=str(e))
