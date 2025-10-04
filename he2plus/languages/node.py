"""
Node.js Installer for he2plus
Smart Node.js installation with LTS support and version management
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple
from ..core.system_profiler import SystemInfo, get_system_info


class NodeInstaller:
    """Smart Node.js installer with LTS support and version management"""
    
    # Supported Node.js versions (LTS and current)
    SUPPORTED_VERSIONS = ['16', '18', '20', '21']
    
    # Recommended versions for different use cases
    RECOMMENDED_VERSIONS = {
        'web3': '18',    # Good compatibility with Hardhat and Web3 tools
        'ml': '18',      # Stable for ML tooling
        'web': '20',     # Latest LTS for web development
        'mobile': '18',  # React Native compatibility
        'general': '18'  # LTS version
    }
    
    def __init__(self):
        """Initialize the Node.js installer"""
        self.system_info = get_system_info()
    
    def get_installed_versions(self) -> List[str]:
        """
        Get list of installed Node.js versions
        
        Returns:
            List of installed Node.js versions
        """
        return self.system_info.node_versions
    
    def is_version_installed(self, version: str) -> bool:
        """
        Check if a specific Node.js version is installed
        
        Args:
            version: Node.js version to check (e.g., '18')
            
        Returns:
            True if version is installed, False otherwise
        """
        return version in self.get_installed_versions()
    
    def get_recommended_version(self, use_case: str = 'general') -> str:
        """
        Get recommended Node.js version for a use case
        
        Args:
            use_case: Use case ('web3', 'ml', 'web', 'mobile', 'general')
            
        Returns:
            Recommended Node.js version
        """
        return self.RECOMMENDED_VERSIONS.get(use_case, '18')
    
    def install_node(self, version: str, use_case: str = 'general') -> bool:
        """
        Install Node.js with specified version
        
        Args:
            version: Node.js version to install
            use_case: Use case for installation
            
        Returns:
            True if installation successful, False otherwise
        """
        if self.is_version_installed(version):
            print(f"✅ Node.js {version} already installed")
            return True
        
        print(f"📦 Installing Node.js {version}...")
        
        try:
            if self.system_info.os_name == 'darwin':  # macOS
                return self._install_node_macos(version)
            elif self.system_info.os_name == 'linux':
                return self._install_node_linux(version)
            elif self.system_info.os_name == 'windows':
                return self._install_node_windows(version)
            else:
                print(f"❌ Unsupported OS: {self.system_info.os_name}")
                return False
        except Exception as e:
            print(f"❌ Failed to install Node.js {version}: {e}")
            return False
    
    def _install_node_macos(self, version: str) -> bool:
        """Install Node.js on macOS"""
        try:
            # Try Homebrew first
            if 'Homebrew' in self.system_info.package_managers:
                print("🍺 Using Homebrew to install Node.js...")
                result = subprocess.run(
                    ['brew', 'install', 'node'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Node.js installed via Homebrew")
                    return True
                else:
                    print(f"⚠️  Homebrew installation failed: {result.stderr}")
            
            # Try nvm
            if self._is_nvm_available():
                print("📦 Using nvm to install Node.js...")
                result = subprocess.run(
                    ['nvm', 'install', version],
                    capture_output=True, text=True, timeout=600
                )
                if result.returncode == 0:
                    subprocess.run(['nvm', 'use', version], check=False)
                    subprocess.run(['nvm', 'alias', 'default', version], check=False)
                    print(f"✅ Node.js {version} installed via nvm")
                    return True
                else:
                    print(f"⚠️  nvm installation failed: {result.stderr}")
            
            # Try fnm
            if self._is_fnm_available():
                print("📦 Using fnm to install Node.js...")
                result = subprocess.run(
                    ['fnm', 'install', version],
                    capture_output=True, text=True, timeout=600
                )
                if result.returncode == 0:
                    subprocess.run(['fnm', 'use', version], check=False)
                    subprocess.run(['fnm', 'default', version], check=False)
                    print(f"✅ Node.js {version} installed via fnm")
                    return True
                else:
                    print(f"⚠️  fnm installation failed: {result.stderr}")
            
            # Fallback to nodejs.org installer
            print("🌐 Downloading from nodejs.org...")
            return self._install_node_org_macos(version)
            
        except Exception as e:
            print(f"❌ macOS installation failed: {e}")
            return False
    
    def _install_node_linux(self, version: str) -> bool:
        """Install Node.js on Linux"""
        try:
            # Try system package manager first
            if 'APT' in self.system_info.package_managers:
                print("📦 Using APT to install Node.js...")
                result = subprocess.run(
                    ['sudo', 'apt', 'update'],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    result = subprocess.run(
                        ['sudo', 'apt', 'install', '-y', 'nodejs', 'npm'],
                        capture_output=True, text=True, timeout=300
                    )
                    if result.returncode == 0:
                        print(f"✅ Node.js installed via APT")
                        return True
            
            elif 'YUM' in self.system_info.package_managers:
                print("📦 Using YUM to install Node.js...")
                result = subprocess.run(
                    ['sudo', 'yum', 'install', '-y', 'nodejs', 'npm'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Node.js installed via YUM")
                    return True
            
            elif 'DNF' in self.system_info.package_managers:
                print("📦 Using DNF to install Node.js...")
                result = subprocess.run(
                    ['sudo', 'dnf', 'install', '-y', 'nodejs', 'npm'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Node.js installed via DNF")
                    return True
            
            # Try nvm as fallback
            if self._is_nvm_available():
                print("📦 Using nvm to install Node.js...")
                result = subprocess.run(
                    ['nvm', 'install', version],
                    capture_output=True, text=True, timeout=600
                )
                if result.returncode == 0:
                    subprocess.run(['nvm', 'use', version], check=False)
                    subprocess.run(['nvm', 'alias', 'default', version], check=False)
                    print(f"✅ Node.js {version} installed via nvm")
                    return True
            
            # Try fnm as fallback
            if self._is_fnm_available():
                print("📦 Using fnm to install Node.js...")
                result = subprocess.run(
                    ['fnm', 'install', version],
                    capture_output=True, text=True, timeout=600
                )
                if result.returncode == 0:
                    subprocess.run(['fnm', 'use', version], check=False)
                    subprocess.run(['fnm', 'default', version], check=False)
                    print(f"✅ Node.js {version} installed via fnm")
                    return True
            
            print("❌ No suitable package manager found")
            return False
            
        except Exception as e:
            print(f"❌ Linux installation failed: {e}")
            return False
    
    def _install_node_windows(self, version: str) -> bool:
        """Install Node.js on Windows"""
        try:
            # Try winget first
            if 'Winget' in self.system_info.package_managers:
                print("📦 Using winget to install Node.js...")
                result = subprocess.run(
                    ['winget', 'install', 'OpenJS.NodeJS'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Node.js installed via winget")
                    return True
            
            # Try Chocolatey
            if 'Chocolatey' in self.system_info.package_managers:
                print("📦 Using Chocolatey to install Node.js...")
                result = subprocess.run(
                    ['choco', 'install', 'nodejs'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"✅ Node.js installed via Chocolatey")
                    return True
            
            # Fallback to nodejs.org installer
            print("🌐 Downloading from nodejs.org...")
            return self._install_node_org_windows(version)
            
        except Exception as e:
            print(f"❌ Windows installation failed: {e}")
            return False
    
    def _install_node_org_macos(self, version: str) -> bool:
        """Install Node.js from nodejs.org on macOS"""
        try:
            # Download and install from nodejs.org
            url = f"https://nodejs.org/dist/v{version}.0.0/node-v{version}.0.0.pkg"
            
            print(f"📥 Downloading Node.js {version} from nodejs.org...")
            print("⚠️  Manual installation required:")
            print(f"   1. Open: {url}")
            print("   2. Download and run the installer")
            print("   3. Follow the installation wizard")
            print("   4. Restart your terminal")
            
            return False  # Manual installation required
            
        except Exception as e:
            print(f"❌ nodejs.org installation failed: {e}")
            return False
    
    def _install_node_org_windows(self, version: str) -> bool:
        """Install Node.js from nodejs.org on Windows"""
        try:
            # Download and install from nodejs.org
            url = f"https://nodejs.org/dist/v{version}.0.0/node-v{version}.0.0-x64.msi"
            
            print(f"📥 Downloading Node.js {version} from nodejs.org...")
            print("⚠️  Manual installation required:")
            print(f"   1. Open: {url}")
            print("   2. Download and run the installer")
            print("   3. Follow the installation wizard")
            print("   4. Restart your terminal")
            
            return False  # Manual installation required
            
        except Exception as e:
            print(f"❌ nodejs.org installation failed: {e}")
            return False
    
    def _is_nvm_available(self) -> bool:
        """Check if nvm is available"""
        try:
            result = subprocess.run(
                ['nvm', '--version'],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _is_fnm_available(self) -> bool:
        """Check if fnm is available"""
        try:
            result = subprocess.run(
                ['fnm', '--version'],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def setup_npm(self, version: str) -> bool:
        """
        Setup npm for the specified Node.js version
        
        Args:
            version: Node.js version
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Upgrade npm
            result = subprocess.run(
                ['npm', 'install', '-g', 'npm@latest'],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                print(f"✅ npm upgraded for Node.js {version}")
                return True
            else:
                print(f"⚠️  npm upgrade failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ npm setup failed: {e}")
            return False
    
    def install_global_packages(self, packages: List[str]) -> bool:
        """
        Install global npm packages
        
        Args:
            packages: List of packages to install globally
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for package in packages:
                print(f"📦 Installing {package} globally...")
                result = subprocess.run(
                    ['npm', 'install', '-g', package],
                    capture_output=True, text=True, timeout=300
                )
                
                if result.returncode == 0:
                    print(f"✅ {package} installed globally")
                else:
                    print(f"❌ Failed to install {package}: {result.stderr}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Global package installation failed: {e}")
            return False
    
    def create_project(self, project_name: str, template: str = 'basic') -> bool:
        """
        Create a new Node.js project
        
        Args:
            project_name: Project name
            template: Project template ('basic', 'express', 'react', 'vue')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project_path = Path.home() / project_name
            project_path.mkdir(exist_ok=True)
            
            # Initialize npm project
            result = subprocess.run(
                ['npm', 'init', '-y'],
                cwd=project_path,
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode != 0:
                print(f"❌ Failed to initialize npm project: {result.stderr}")
                return False
            
            # Install template-specific packages
            if template == 'express':
                result = subprocess.run(
                    ['npm', 'install', 'express'],
                    cwd=project_path,
                    capture_output=True, text=True, timeout=300
                )
            elif template == 'react':
                result = subprocess.run(
                    ['npx', 'create-react-app', '.'],
                    cwd=project_path,
                    capture_output=True, text=True, timeout=600
                )
            elif template == 'vue':
                result = subprocess.run(
                    ['npm', 'install', '-g', '@vue/cli'],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    result = subprocess.run(
                        ['vue', 'create', '.'],
                        cwd=project_path,
                        capture_output=True, text=True, timeout=600
                    )
            
            if result.returncode == 0:
                print(f"✅ Project '{project_name}' created with {template} template")
                return True
            else:
                print(f"❌ Failed to create project: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Project creation failed: {e}")
            return False
    
    def verify_installation(self, version: str) -> bool:
        """
        Verify Node.js installation
        
        Args:
            version: Node.js version to verify
            
        Returns:
            True if installation is working, False otherwise
        """
        try:
            # Check Node.js version
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                installed_version = result.stdout.strip()
                print(f"✅ Node.js {version} verified: {installed_version}")
                
                # Check npm
                result = subprocess.run(
                    ['npm', '--version'],
                    capture_output=True, text=True, timeout=10
                )
                
                if result.returncode == 0:
                    npm_version = result.stdout.strip()
                    print(f"✅ npm verified: {npm_version}")
                    return True
                else:
                    print(f"⚠️  npm not working for Node.js {version}")
                    return False
            else:
                print(f"❌ Node.js {version} not working")
                return False
                
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False


def install_node_for_use_case(use_case: str) -> bool:
    """
    Convenience function to install Node.js for a specific use case
    
    Args:
        use_case: Use case ('web3', 'ml', 'web', 'mobile', 'general')
        
    Returns:
        True if successful, False otherwise
    """
    installer = NodeInstaller()
    recommended_version = installer.get_recommended_version(use_case)
    
    print(f"📦 Installing Node.js {recommended_version} for {use_case} development...")
    
    # Install Node.js
    if not installer.install_node(recommended_version, use_case):
        return False
    
    # Setup npm
    if not installer.setup_npm(recommended_version):
        return False
    
    # Verify installation
    if not installer.verify_installation(recommended_version):
        return False
    
    print(f"✅ Node.js {recommended_version} ready for {use_case} development!")
    return True


if __name__ == "__main__":
    # Test the Node.js installer
    installer = NodeInstaller()
    
    print("📦 Node.js Installer Test")
    print("=" * 50)
    
    # Show installed versions
    installed = installer.get_installed_versions()
    print(f"Installed versions: {', '.join(installed) if installed else 'None'}")
    
    # Show recommended versions
    for use_case in ['web3', 'ml', 'web', 'mobile', 'general']:
        recommended = installer.get_recommended_version(use_case)
        print(f"Recommended for {use_case}: Node.js {recommended}")
    
    # Test installation for web3
    print(f"\n🧪 Testing Web3 Node.js installation...")
    success = install_node_for_use_case('web3')
    print(f"Installation {'successful' if success else 'failed'}")
