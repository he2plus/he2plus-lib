"""
Git tool installer for he2plus.

This module handles Git installation and configuration including
SSH key setup and global configuration.
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
class GitInstallation:
    """Represents a Git installation."""
    
    version: str
    path: Path
    is_system: bool
    is_configured: bool = False
    has_ssh_key: bool = False


@dataclass
class InstallResult:
    """Result of Git installation."""
    
    success: bool
    version: Optional[str] = None
    path: Optional[Path] = None
    method: Optional[str] = None
    error: Optional[str] = None
    warnings: List[str] = None
    ssh_key_created: bool = False
    global_config_set: bool = False
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class GitInstaller:
    """Install and configure Git."""
    
    def __init__(self, system_info: SystemInfo):
        self.system = system_info
        self.logger = logger.bind(component="git_installer")
    
    def is_installed(self) -> Optional[GitInstallation]:
        """Check if Git is installed."""
        self.logger.debug("Checking Git installation")
        
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse version from output
                output = result.stdout.strip()
                version = output.split()[2]  # "git version 2.39.0" -> "2.39.0"
                
                path = self._find_git_path()
                is_system = self._is_system_git(path)
                is_configured = self._is_configured()
                has_ssh_key = self._has_ssh_key()
                
                return GitInstallation(
                    version=version,
                    path=path,
                    is_system=is_system,
                    is_configured=is_configured,
                    has_ssh_key=has_ssh_key
                )
        
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return None
    
    def install(self, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Git."""
        self.logger.info("Installing Git")
        
        # Check if already installed
        existing = self.is_installed()
        if existing:
            progress.console.print(f"✓ Git {existing.version} already installed at {existing.path}")
            return InstallResult(
                success=True,
                version=existing.version,
                path=existing.path,
                method="existing"
            )
        
        # Choose installation method
        method = self._choose_installation_method()
        
        try:
            if method == "package_manager":
                return self._install_package_manager(progress, task_id)
            elif method == "official":
                return self._install_official(progress, task_id)
            else:
                return InstallResult(
                    success=False,
                    error="No suitable installation method found for Git"
                )
        
        except Exception as e:
            self.logger.error("Git installation failed", error=str(e))
            return InstallResult(
                success=False,
                error=str(e)
            )
    
    def _choose_installation_method(self) -> str:
        """Choose the best installation method for the system."""
        system = platform.system().lower()
        
        # Check for package managers first
        if system == "darwin" and "brew" in self.system.package_managers:
            return "package_manager"
        elif system == "linux" and any(pm in self.system.package_managers for pm in ["apt", "yum", "dnf"]):
            return "package_manager"
        elif system == "windows" and any(pm in self.system.package_managers for pm in ["choco", "winget"]):
            return "package_manager"
        
        # Fall back to official installer
        return "official"
    
    def _install_package_manager(self, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Git using system package manager."""
        self.logger.info("Installing Git via package manager")
        
        system = platform.system().lower()
        
        try:
            if system == "darwin" and "brew" in self.system.package_managers:
                # Homebrew on macOS
                progress.update(task_id, description="Installing Git via Homebrew...")
                subprocess.run(
                    ["brew", "install", "git"],
                    check=True,
                    capture_output=True
                )
            
            elif system == "linux":
                # Linux package managers
                if "apt" in self.system.package_managers:
                    progress.update(task_id, description="Installing Git via apt...")
                    subprocess.run(
                        ["sudo", "apt", "update"], check=True, capture_output=True
                    )
                    subprocess.run(
                        ["sudo", "apt", "install", "-y", "git"],
                        check=True,
                        capture_output=True
                    )
                elif "yum" in self.system.package_managers:
                    progress.update(task_id, description="Installing Git via yum...")
                    subprocess.run(
                        ["sudo", "yum", "install", "-y", "git"],
                        check=True,
                        capture_output=True
                    )
                elif "dnf" in self.system.package_managers:
                    progress.update(task_id, description="Installing Git via dnf...")
                    subprocess.run(
                        ["sudo", "dnf", "install", "-y", "git"],
                        check=True,
                        capture_output=True
                    )
            
            elif system == "windows":
                # Windows package managers
                if "choco" in self.system.package_managers:
                    progress.update(task_id, description="Installing Git via Chocolatey...")
                    subprocess.run(
                        ["choco", "install", "git", "-y"],
                        check=True,
                        capture_output=True
                    )
                elif "winget" in self.system.package_managers:
                    progress.update(task_id, description="Installing Git via winget...")
                    subprocess.run(
                        ["winget", "install", "Git.Git"],
                        check=True,
                        capture_output=True
                    )
            
            # Verify installation
            installed = self.is_installed()
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
                    error="Package manager installation completed but Git not found"
                )
        
        except subprocess.CalledProcessError as e:
            return InstallResult(
                success=False,
                error=f"Package manager installation failed: {e.stderr.decode() if e.stderr else str(e)}"
            )
    
    def _install_official(self, progress: Progress, task_id: TaskID) -> InstallResult:
        """Install Git using official installer."""
        self.logger.info("Installing Git via official installer")
        
        system = platform.system().lower()
        
        try:
            if system == "darwin":
                # macOS - download and install from git-scm.com
                progress.update(task_id, description="Downloading Git installer...")
                # This would require downloading the installer and running it
                # For now, we'll use a simplified approach
                return InstallResult(
                    success=False,
                    error="Official installer not implemented for macOS. Please install Git manually from git-scm.com"
                )
            
            elif system == "windows":
                # Windows - download and install from git-scm.com
                progress.update(task_id, description="Downloading Git installer...")
                # This would require downloading the installer and running it
                return InstallResult(
                    success=False,
                    error="Official installer not implemented for Windows. Please install Git manually from git-scm.com"
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
    
    def configure(self, name: str, email: str, progress: Progress, task_id: TaskID) -> bool:
        """Configure Git with user name and email."""
        self.logger.info("Configuring Git", name=name, email=email)
        
        try:
            # Set global user name
            progress.update(task_id, description="Setting Git user name...")
            subprocess.run(
                ["git", "config", "--global", "user.name", name],
                check=True,
                capture_output=True
            )
            
            # Set global user email
            progress.update(task_id, description="Setting Git user email...")
            subprocess.run(
                ["git", "config", "--global", "user.email", email],
                check=True,
                capture_output=True
            )
            
            # Set default branch name
            progress.update(task_id, description="Setting default branch name...")
            subprocess.run(
                ["git", "config", "--global", "init.defaultBranch", "main"],
                check=True,
                capture_output=True
            )
            
            # Set pull strategy
            progress.update(task_id, description="Setting pull strategy...")
            subprocess.run(
                ["git", "config", "--global", "pull.rebase", "false"],
                check=True,
                capture_output=True
            )
            
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.error("Git configuration failed", error=str(e))
            return False
    
    def setup_ssh_key(self, email: str, progress: Progress, task_id: TaskID) -> bool:
        """Set up SSH key for Git."""
        self.logger.info("Setting up SSH key", email=email)
        
        try:
            # Check if SSH key already exists
            ssh_dir = Path.home() / ".ssh"
            ssh_key_path = ssh_dir / "id_ed25519"
            
            if ssh_key_path.exists():
                progress.console.print("✓ SSH key already exists")
                return True
            
            # Create .ssh directory if it doesn't exist
            ssh_dir.mkdir(mode=0o700, exist_ok=True)
            
            # Generate SSH key
            progress.update(task_id, description="Generating SSH key...")
            subprocess.run(
                ["ssh-keygen", "-t", "ed25519", "-C", email, "-f", str(ssh_key_path), "-N", ""],
                check=True,
                capture_output=True
            )
            
            # Set proper permissions
            ssh_key_path.chmod(0o600)
            (ssh_dir / "id_ed25519.pub").chmod(0o644)
            
            # Start SSH agent and add key
            progress.update(task_id, description="Adding SSH key to agent...")
            subprocess.run(
                ["ssh-add", str(ssh_key_path)],
                check=True,
                capture_output=True
            )
            
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.error("SSH key setup failed", error=str(e))
            return False
    
    def get_ssh_public_key(self) -> Optional[str]:
        """Get the SSH public key."""
        try:
            ssh_key_path = Path.home() / ".ssh" / "id_ed25519.pub"
            if ssh_key_path.exists():
                return ssh_key_path.read_text().strip()
        except Exception:
            pass
        return None
    
    def verify(self) -> bool:
        """Verify Git installation."""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return "git version" in result.stdout
        except:
            return False
    
    def _find_git_path(self) -> Path:
        """Find the path to Git executable."""
        try:
            result = subprocess.run(
                ["which", "git"] if platform.system() != "Windows" else ["where", "git"],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip().split('\n')[0])
        except:
            return Path("git")
    
    def _is_system_git(self, path: Path) -> bool:
        """Check if Git is a system installation."""
        system_paths = [
            "/usr/bin",
            "/usr/local/bin",
            "C:\\Program Files\\Git",
            "C:\\Program Files (x86)\\Git"
        ]
        
        return any(str(path).startswith(sys_path) for sys_path in system_paths)
    
    def _is_configured(self) -> bool:
        """Check if Git is configured with user name and email."""
        try:
            # Check if user.name is set
            result = subprocess.run(
                ["git", "config", "--global", "user.name"],
                capture_output=True,
                text=True,
                check=True
            )
            name = result.stdout.strip()
            
            # Check if user.email is set
            result = subprocess.run(
                ["git", "config", "--global", "user.email"],
                capture_output=True,
                text=True,
                check=True
            )
            email = result.stdout.strip()
            
            return bool(name and email)
        
        except:
            return False
    
    def _has_ssh_key(self) -> bool:
        """Check if SSH key exists."""
        ssh_key_path = Path.home() / ".ssh" / "id_ed25519"
        return ssh_key_path.exists()
    
    def get_config(self) -> Dict[str, str]:
        """Get Git configuration."""
        config = {}
        
        try:
            # Get all global config
            result = subprocess.run(
                ["git", "config", "--global", "--list"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value
        
        except:
            pass
        
        return config
    
    def test_github_connection(self) -> bool:
        """Test connection to GitHub."""
        try:
            result = subprocess.run(
                ["ssh", "-T", "git@github.com"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # GitHub returns exit code 1 for successful authentication
            return result.returncode == 1 and "successfully authenticated" in result.stderr
        except:
            return False
    
    def get_recommended_setup_commands(self) -> List[str]:
        """Get recommended setup commands for Git."""
        commands = []
        
        # Check if Git is installed
        if not self.is_installed():
            commands.append("Install Git first")
            return commands
        
        # Check configuration
        if not self._is_configured():
            commands.append("git config --global user.name 'Your Name'")
            commands.append("git config --global user.email 'your.email@example.com'")
        
        # Check SSH key
        if not self._has_ssh_key():
            commands.append("ssh-keygen -t ed25519 -C 'your.email@example.com'")
            commands.append("ssh-add ~/.ssh/id_ed25519")
            commands.append("cat ~/.ssh/id_ed25519.pub")
            commands.append("Add the public key to your GitHub account")
        
        # Test connection
        if not self.test_github_connection():
            commands.append("ssh -T git@github.com")
        
        return commands
