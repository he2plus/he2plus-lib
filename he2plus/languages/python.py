"""
Python Installer for he2plus
Smart Python installation with version detection and cross-platform support
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple
from ..core.system_profiler import SystemInfo, get_system_info


class PythonInstaller:
    """Smart Python installer with version detection and cross-platform support"""
    
    # Supported Python versions (LTS and recent)
    SUPPORTED_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
    
    # Recommended versions for different use cases
    RECOMMENDED_VERSIONS = {
        'web3': '3.11',  # Vyper works best with 3.11
        'ml': '3.10',    # Good ML library support
        'web': '3.11',   # Latest features
        'general': '3.11'  # Latest stable
    }
    
    def __init__(self):
        """Initialize the Python installer"""
        self.system_info = get_system_info()
    
    def get_installed_versions(self) -> List[str]:
        """
        Get list of installed Python versions
        
        Returns:
            List of installed Python versions
        """
        return self.system_info.python_versions
    
    def is_version_installed(self, version: str) -> bool:
        """
        Check if a specific Python version is installed
        
        Args:
            version: Python version to check (e.g., '3.11')
            
        Returns:
            True if version is installed, False otherwise
        """
        return version in self.get_installed_versions()
    
    def get_recommended_version(self, use_case: str = 'general') -> str:
        """
        Get recommended Python version for a use case
        
        Args:
            use_case: Use case ('web3', 'ml', 'web', 'general')
            
        Returns:
            Recommended Python version
        """
        return self.RECOMMENDED_VERSIONS.get(use_case, '3.11')
    
    def install_python(self, version: str, use_case: str = 'general') -> bool:
        """
        Install Python with specified version
        
        Args:
            version: Python version to install
            use_case: Use case for installation
            
        Returns:
            True if installation successful, False otherwise
        """
        if self.is_version_installed(version):
            print(f"✅ Python {version} already installed")
            return True
        
        print(f"📦 Installing Python {version}...")
        
        try:
            if self.system_info.os_name == 'darwin':  # macOS
                return self._install_python_macos(version)
            elif self.system_info.os_name == 'linux':
                return self._install_python_linux(version)
            elif self.system_info.os_name == 'windows':
                return self._install_python_windows(version)
            else:
                print(f"❌ Unsupported OS: {self.system_info.os_name}")
                return False
        except Exception as e:
            print(f"❌ Failed to install Python {version}: {e}")
            return False
    
    def _install_python_macos(self, version: str) -> bool:
        """Install Python on macOS"""
        try:
            # Try Homebrew first
            if 'Homebrew' in self.system_info.package_managers:
                print("🍺 Using Homebrew to install Python...")
                result = subprocess.run(
                    ['brew', 'install', f'python@{version}'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Python {version} installed via Homebrew")
                    return True
                else:
                    print(f"⚠️  Homebrew installation failed: {result.stderr}")
            
            # Try pyenv
            if self._is_pyenv_available():
                print("🐍 Using pyenv to install Python...")
                result = subprocess.run(
                    ['pyenv', 'install', version],
                    capture_output=True, text=True, timeout=600
                )
                if result.returncode == 0:
                    subprocess.run(['pyenv', 'global', version], check=False)
                    print(f"✅ Python {version} installed via pyenv")
                    return True
                else:
                    print(f"⚠️  pyenv installation failed: {result.stderr}")
            
            # Fallback to python.org installer
            print("🌐 Downloading from python.org...")
            return self._install_python_org_macos(version)
            
        except Exception as e:
            print(f"❌ macOS installation failed: {e}")
            return False
    
    def _install_python_linux(self, version: str) -> bool:
        """Install Python on Linux"""
        try:
            # Try system package manager first
            if 'APT' in self.system_info.package_managers:
                print("📦 Using APT to install Python...")
                result = subprocess.run(
                    ['sudo', 'apt', 'update'],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    result = subprocess.run(
                        ['sudo', 'apt', 'install', '-y', f'python{version}', f'python{version}-pip'],
                        capture_output=True, text=True, timeout=300
                    )
                    if result.returncode == 0:
                        print(f"✅ Python {version} installed via APT")
                        return True
            
            elif 'YUM' in self.system_info.package_managers:
                print("📦 Using YUM to install Python...")
                result = subprocess.run(
                    ['sudo', 'yum', 'install', '-y', f'python{version}', f'python{version}-pip'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Python {version} installed via YUM")
                    return True
            
            elif 'DNF' in self.system_info.package_managers:
                print("📦 Using DNF to install Python...")
                result = subprocess.run(
                    ['sudo', 'dnf', 'install', '-y', f'python{version}', f'python{version}-pip'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Python {version} installed via DNF")
                    return True
            
            # Try pyenv as fallback
            if self._is_pyenv_available():
                print("🐍 Using pyenv to install Python...")
                result = subprocess.run(
                    ['pyenv', 'install', version],
                    capture_output=True, text=True, timeout=600
                )
                if result.returncode == 0:
                    subprocess.run(['pyenv', 'global', version], check=False)
                    print(f"✅ Python {version} installed via pyenv")
                    return True
            
            print("❌ No suitable package manager found")
            return False
            
        except Exception as e:
            print(f"❌ Linux installation failed: {e}")
            return False
    
    def _install_python_windows(self, version: str) -> bool:
        """Install Python on Windows"""
        try:
            # Try winget first
            if 'Winget' in self.system_info.package_managers:
                print("📦 Using winget to install Python...")
                result = subprocess.run(
                    ['winget', 'install', 'Python.Python.3.11'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Python {version} installed via winget")
                    return True
            
            # Try Chocolatey
            if 'Chocolatey' in self.system_info.package_managers:
                print("📦 Using Chocolatey to install Python...")
                result = subprocess.run(
                    ['choco', 'install', 'python', '--version', version],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Python {version} installed via Chocolatey")
                    return True
            
            # Fallback to python.org installer
            print("🌐 Downloading from python.org...")
            return self._install_python_org_windows(version)
            
        except Exception as e:
            print(f"❌ Windows installation failed: {e}")
            return False
    
    def _install_python_org_macos(self, version: str) -> bool:
        """Install Python from python.org on macOS"""
        try:
            # Download and install from python.org
            url = f"https://www.python.org/ftp/python/{version}/python-{version}-macos11.pkg"
            if self.system_info.architecture == 'arm64':
                url = f"https://www.python.org/ftp/python/{version}/python-{version}-macos11.pkg"
            
            print(f"📥 Downloading Python {version} from python.org...")
            print("⚠️  Manual installation required:")
            print(f"   1. Open: {url}")
            print("   2. Download and run the installer")
            print("   3. Follow the installation wizard")
            print("   4. Restart your terminal")
            
            return False  # Manual installation required
            
        except Exception as e:
            print(f"❌ python.org installation failed: {e}")
            return False
    
    def _install_python_org_windows(self, version: str) -> bool:
        """Install Python from python.org on Windows"""
        try:
            # Download and install from python.org
            url = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
            
            print(f"📥 Downloading Python {version} from python.org...")
            print("⚠️  Manual installation required:")
            print(f"   1. Open: {url}")
            print("   2. Download and run the installer")
            print("   3. Check 'Add Python to PATH'")
            print("   4. Follow the installation wizard")
            print("   5. Restart your terminal")
            
            return False  # Manual installation required
            
        except Exception as e:
            print(f"❌ python.org installation failed: {e}")
            return False
    
    def _is_pyenv_available(self) -> bool:
        """Check if pyenv is available"""
        try:
            result = subprocess.run(
                ['pyenv', '--version'],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def setup_pip(self, version: str) -> bool:
        """
        Setup pip for the specified Python version
        
        Args:
            version: Python version
            
        Returns:
            True if successful, False otherwise
        """
        try:
            python_cmd = f"python{version}"
            if self.system_info.os_name == 'windows':
                python_cmd = f"py -{version}"
            
            # Upgrade pip
            result = subprocess.run(
                [python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip'],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                print(f"✅ pip upgraded for Python {version}")
                return True
            else:
                print(f"⚠️  pip upgrade failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ pip setup failed: {e}")
            return False
    
    def create_virtual_environment(self, version: str, env_name: str = 'he2plus-env') -> bool:
        """
        Create a virtual environment with the specified Python version
        
        Args:
            version: Python version
            env_name: Virtual environment name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            python_cmd = f"python{version}"
            if self.system_info.os_name == 'windows':
                python_cmd = f"py -{version}"
            
            # Create virtual environment
            result = subprocess.run(
                [python_cmd, '-m', 'venv', env_name],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                print(f"✅ Virtual environment '{env_name}' created with Python {version}")
                return True
            else:
                print(f"❌ Virtual environment creation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Virtual environment creation failed: {e}")
            return False
    
    def install_packages(self, version: str, packages: List[str]) -> bool:
        """
        Install packages for the specified Python version
        
        Args:
            version: Python version
            packages: List of packages to install
            
        Returns:
            True if successful, False otherwise
        """
        try:
            python_cmd = f"python{version}"
            if self.system_info.os_name == 'windows':
                python_cmd = f"py -{version}"
            
            for package in packages:
                print(f"📦 Installing {package}...")
                result = subprocess.run(
                    [python_cmd, '-m', 'pip', 'install', package],
                    capture_output=True, text=True, timeout=300
                )
                
                if result.returncode == 0:
                    print(f"✅ {package} installed successfully")
                else:
                    print(f"❌ Failed to install {package}: {result.stderr}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Package installation failed: {e}")
            return False
    
    def verify_installation(self, version: str) -> bool:
        """
        Verify Python installation
        
        Args:
            version: Python version to verify
            
        Returns:
            True if installation is working, False otherwise
        """
        try:
            python_cmd = f"python{version}"
            if self.system_info.os_name == 'windows':
                python_cmd = f"py -{version}"
            
            # Check Python version
            result = subprocess.run(
                [python_cmd, '--version'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                installed_version = result.stdout.strip()
                print(f"✅ Python {version} verified: {installed_version}")
                
                # Check pip
                result = subprocess.run(
                    [python_cmd, '-m', 'pip', '--version'],
                    capture_output=True, text=True, timeout=10
                )
                
                if result.returncode == 0:
                    pip_version = result.stdout.strip()
                    print(f"✅ pip verified: {pip_version}")
                    return True
                else:
                    print(f"⚠️  pip not working for Python {version}")
                    return False
            else:
                print(f"❌ Python {version} not working")
                return False
                
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False


def install_python_for_use_case(use_case: str) -> bool:
    """
    Convenience function to install Python for a specific use case
    
    Args:
        use_case: Use case ('web3', 'ml', 'web', 'general')
        
    Returns:
        True if successful, False otherwise
    """
    installer = PythonInstaller()
    recommended_version = installer.get_recommended_version(use_case)
    
    print(f"🐍 Installing Python {recommended_version} for {use_case} development...")
    
    # Install Python
    if not installer.install_python(recommended_version, use_case):
        return False
    
    # Setup pip
    if not installer.setup_pip(recommended_version):
        return False
    
    # Verify installation
    if not installer.verify_installation(recommended_version):
        return False
    
    print(f"✅ Python {recommended_version} ready for {use_case} development!")
    return True


if __name__ == "__main__":
    # Test the Python installer
    installer = PythonInstaller()
    
    print("🐍 Python Installer Test")
    print("=" * 50)
    
    # Show installed versions
    installed = installer.get_installed_versions()
    print(f"Installed versions: {', '.join(installed) if installed else 'None'}")
    
    # Show recommended versions
    for use_case in ['web3', 'ml', 'web', 'general']:
        recommended = installer.get_recommended_version(use_case)
        print(f"Recommended for {use_case}: Python {recommended}")
    
    # Test installation for web3
    print(f"\n🧪 Testing Web3 Python installation...")
    success = install_python_for_use_case('web3')
    print(f"Installation {'successful' if success else 'failed'}")
