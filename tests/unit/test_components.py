"""Unit tests for component installers."""

import pytest
from unittest.mock import patch, Mock
from pathlib import Path

from he2plus.components.languages.python import PythonInstaller, PythonInstallation, InstallResult
from he2plus.components.languages.node import NodeInstaller, NodeInstallation, InstallResult as NodeInstallResult
from he2plus.components.tools.git import GitInstaller, GitInstallation, InstallResult as GitInstallResult


class TestPythonInstaller:
    """Test PythonInstaller class."""
    
    def test_python_installer_creation(self, mock_system_info):
        """Test PythonInstaller creation."""
        installer = PythonInstaller(mock_system_info)
        
        assert installer.system == mock_system_info
        assert installer.SUPPORTED_VERSIONS == ["3.8", "3.9", "3.10", "3.11", "3.12"]
        assert installer.PREFERRED_VERSION == "3.11"
    
    def test_is_installed_success(self, mock_system_info, mock_subprocess):
        """Test PythonInstaller is_installed with successful detection."""
        # Mock subprocess.run to return successful version check
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Python 3.11.0\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        # Mock _find_python_path
        with patch.object(PythonInstaller, '_find_python_path', return_value=Path("/usr/bin/python3")):
            # Mock _is_system_python, _is_pyenv_python, _is_conda_python
            with patch.object(PythonInstaller, '_is_system_python', return_value=True), \
                 patch.object(PythonInstaller, '_is_pyenv_python', return_value=False), \
                 patch.object(PythonInstaller, '_is_conda_python', return_value=False):
                
                installer = PythonInstaller(mock_system_info)
                installation = installer.is_installed("3.11")
                
                assert installation is not None
                assert installation.version == "3.11.0"
                assert installation.path == Path("/usr/bin/python3")
                assert installation.is_system is True
                assert installation.is_pyenv is False
                assert installation.is_conda is False
    
    def test_is_installed_not_found(self, mock_system_info, mock_subprocess):
        """Test PythonInstaller is_installed when Python not found."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = PythonInstaller(mock_system_info)
        installation = installer.is_installed("3.11")
        
        assert installation is None
    
    def test_choose_installation_method_pyenv(self, mock_system_info):
        """Test PythonInstaller _choose_installation_method with pyenv."""
        with patch.object(PythonInstaller, '_has_pyenv', return_value=True):
            installer = PythonInstaller(mock_system_info)
            method = installer._choose_installation_method("3.11")
            
            assert method == "pyenv"
    
    def test_choose_installation_method_conda(self, mock_system_info):
        """Test PythonInstaller _choose_installation_method with conda."""
        with patch.object(PythonInstaller, '_has_pyenv', return_value=False), \
             patch.object(PythonInstaller, '_has_conda', return_value=True):
            
            installer = PythonInstaller(mock_system_info)
            method = installer._choose_installation_method("3.11")
            
            assert method == "conda"
    
    def test_choose_installation_method_package_manager(self, mock_system_info):
        """Test PythonInstaller _choose_installation_method with package manager."""
        with patch.object(PythonInstaller, '_has_pyenv', return_value=False), \
             patch.object(PythonInstaller, '_has_conda', return_value=False):
            
            installer = PythonInstaller(mock_system_info)
            method = installer._choose_installation_method("3.11")
            
            assert method == "package_manager"
    
    def test_choose_installation_method_official(self, mock_system_info):
        """Test PythonInstaller _choose_installation_method with official installer."""
        # Create system without package managers
        no_pm_system = mock_system_info
        no_pm_system.package_managers = []
        
        with patch.object(PythonInstaller, '_has_pyenv', return_value=False), \
             patch.object(PythonInstaller, '_has_conda', return_value=False):
            
            installer = PythonInstaller(no_pm_system)
            method = installer._choose_installation_method("3.11")
            
            assert method == "official"
    
    def test_install_pyenv_success(self, mock_system_info, mock_subprocess):
        """Test PythonInstaller _install_pyenv with success."""
        # Mock subprocess.run for pyenv commands
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Success\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        # Mock is_installed to return successful installation
        with patch.object(PythonInstaller, 'is_installed', return_value=Mock(version="3.11.0", path=Path("/usr/bin/python3"))), \
             patch.object(PythonInstaller, '_has_any_python', return_value=False):
            
            installer = PythonInstaller(mock_system_info)
            progress = Mock()
            task_id = Mock()
            
            result = installer._install_pyenv("3.11", progress, task_id)
            
            assert result.success is True
            assert result.version == "3.11.0"
            assert result.method == "pyenv"
    
    def test_install_pyenv_failure(self, mock_system_info, mock_subprocess):
        """Test PythonInstaller _install_pyenv with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stderr = b"pyenv install failed"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = PythonInstaller(mock_system_info)
        progress = Mock()
        task_id = Mock()
        
        result = installer._install_pyenv("3.11", progress, task_id)
        
        assert result.success is False
        assert "pyenv installation failed" in result.error
    
    def test_verify_success(self, mock_system_info, mock_subprocess):
        """Test PythonInstaller verify with success."""
        # Mock subprocess.run to return successful verification
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "3.11.0 (main, Oct 24 2023, 00:00:00)"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = PythonInstaller(mock_system_info)
        result = installer.verify("3.11")
        
        assert result is True
    
    def test_verify_failure(self, mock_system_info, mock_subprocess):
        """Test PythonInstaller verify with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = PythonInstaller(mock_system_info)
        result = installer.verify("3.11")
        
        assert result is False
    
    def test_version_matches(self, mock_system_info):
        """Test PythonInstaller _version_matches."""
        installer = PythonInstaller(mock_system_info)
        
        assert installer._version_matches("3.11.0", "3.11") is True
        assert installer._version_matches("3.11.1", "3.11") is True
        assert installer._version_matches("3.10.0", "3.11") is False
        assert installer._version_matches("2.11.0", "3.11") is False
    
    def test_get_installed_versions(self, mock_system_info):
        """Test PythonInstaller get_installed_versions."""
        # Mock is_installed to return some installations
        def mock_is_installed(version):
            if version in ["3.10", "3.11"]:
                return Mock(version=f"{version}.0", path=Path(f"/usr/bin/python{version}"))
            return None
        
        with patch.object(PythonInstaller, 'is_installed', side_effect=mock_is_installed):
            installer = PythonInstaller(mock_system_info)
            installations = installer.get_installed_versions()
            
            assert len(installations) == 2
            assert any(inst.version == "3.10.0" for inst in installations)
            assert any(inst.version == "3.11.0" for inst in installations)
    
    def test_get_recommended_version(self, mock_system_info):
        """Test PythonInstaller get_recommended_version."""
        # Mock is_installed to return preferred version
        with patch.object(PythonInstaller, 'is_installed', return_value=Mock(version="3.11.0")):
            installer = PythonInstaller(mock_system_info)
            version = installer.get_recommended_version()
            
            assert version == "3.11.0"
        
        # Mock is_installed to return None (no Python installed)
        with patch.object(PythonInstaller, 'is_installed', return_value=None):
            installer = PythonInstaller(mock_system_info)
            version = installer.get_recommended_version()
            
            assert version == "3.11"  # Preferred version for installation


class TestNodeInstaller:
    """Test NodeInstaller class."""
    
    def test_node_installer_creation(self, mock_system_info):
        """Test NodeInstaller creation."""
        installer = NodeInstaller(mock_system_info)
        
        assert installer.system == mock_system_info
        assert installer.SUPPORTED_VERSIONS == ["16", "18", "20", "21"]
        assert installer.PREFERRED_VERSION == "18"
        assert installer.LTS_VERSIONS == ["16", "18", "20"]
    
    def test_is_installed_success(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller is_installed with successful detection."""
        # Mock subprocess.run to return successful version check
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "v18.19.0\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        # Mock _find_node_path and _get_npm_version
        with patch.object(NodeInstaller, '_find_node_path', return_value=Path("/usr/bin/node")), \
             patch.object(NodeInstaller, '_get_npm_version', return_value="10.2.3"), \
             patch.object(NodeInstaller, '_is_system_node', return_value=True), \
             patch.object(NodeInstaller, '_is_nvm_node', return_value=False), \
             patch.object(NodeInstaller, '_is_volta_node', return_value=False):
            
            installer = NodeInstaller(mock_system_info)
            installation = installer.is_installed("18")
            
            assert installation is not None
            assert installation.version == "18.19.0"
            assert installation.npm_version == "10.2.3"
            assert installation.path == Path("/usr/bin/node")
            assert installation.is_system is True
            assert installation.is_nvm is False
            assert installation.is_volta is False
    
    def test_is_installed_not_found(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller is_installed when Node.js not found."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        installation = installer.is_installed("18")
        
        assert installation is None
    
    def test_choose_installation_method_nvm(self, mock_system_info):
        """Test NodeInstaller _choose_installation_method with nvm."""
        with patch.object(NodeInstaller, '_has_nvm', return_value=True):
            installer = NodeInstaller(mock_system_info)
            method = installer._choose_installation_method("18")
            
            assert method == "nvm"
    
    def test_choose_installation_method_volta(self, mock_system_info):
        """Test NodeInstaller _choose_installation_method with volta."""
        with patch.object(NodeInstaller, '_has_nvm', return_value=False), \
             patch.object(NodeInstaller, '_has_volta', return_value=True):
            
            installer = NodeInstaller(mock_system_info)
            method = installer._choose_installation_method("18")
            
            assert method == "volta"
    
    def test_choose_installation_method_package_manager(self, mock_system_info):
        """Test NodeInstaller _choose_installation_method with package manager."""
        with patch.object(NodeInstaller, '_has_nvm', return_value=False), \
             patch.object(NodeInstaller, '_has_volta', return_value=False):
            
            installer = NodeInstaller(mock_system_info)
            method = installer._choose_installation_method("18")
            
            assert method == "package_manager"
    
    def test_install_nvm_success(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller _install_nvm with success."""
        # Mock subprocess.run for nvm commands
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Success\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        # Mock is_installed to return successful installation
        with patch.object(NodeInstaller, 'is_installed', return_value=Mock(version="18.19.0", npm_version="10.2.3", path=Path("/usr/bin/node"))), \
             patch.object(NodeInstaller, '_has_any_node', return_value=False):
            
            installer = NodeInstaller(mock_system_info)
            progress = Mock()
            task_id = Mock()
            
            result = installer._install_nvm("18", progress, task_id)
            
            assert result.success is True
            assert result.version == "18.19.0"
            assert result.npm_version == "10.2.3"
            assert result.method == "nvm"
    
    def test_install_nvm_failure(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller _install_nvm with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stderr = b"nvm install failed"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        progress = Mock()
        task_id = Mock()
        
        result = installer._install_nvm("18", progress, task_id)
        
        assert result.success is False
        assert "nvm installation failed" in result.error
    
    def test_verify_success(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller verify with success."""
        # Mock subprocess.run to return successful verification
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "v18.19.0\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        result = installer.verify("18")
        
        assert result is True
    
    def test_verify_failure(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller verify with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        result = installer.verify("18")
        
        assert result is False
    
    def test_version_matches(self, mock_system_info):
        """Test NodeInstaller _version_matches."""
        installer = NodeInstaller(mock_system_info)
        
        assert installer._version_matches("18.19.0", "18") is True
        assert installer._version_matches("18.20.0", "18") is True
        assert installer._version_matches("17.0.0", "18") is False
        assert installer._version_matches("19.0.0", "18") is False
    
    def test_get_npm_version(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller _get_npm_version."""
        # Mock subprocess.run to return npm version
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "10.2.3\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        version = installer._get_npm_version()
        
        assert version == "10.2.3"
    
    def test_get_npm_version_failure(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller _get_npm_version with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        version = installer._get_npm_version()
        
        assert version == "unknown"
    
    def test_install_npm_package_success(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller install_npm_package with success."""
        # Mock subprocess.run to return success
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        result = installer.install_npm_package("express")
        
        assert result is True
    
    def test_install_npm_package_failure(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller install_npm_package with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        result = installer.install_npm_package("nonexistent-package")
        
        assert result is False
    
    def test_get_npm_packages(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller get_npm_packages."""
        # Mock subprocess.run to return npm list output
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = '{"dependencies": {"express": {"version": "4.18.0"}, "lodash": {"version": "4.17.21"}}}'
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        packages = installer.get_npm_packages()
        
        assert len(packages) == 2
        assert any(pkg["name"] == "express" and pkg["version"] == "4.18.0" for pkg in packages)
        assert any(pkg["name"] == "lodash" and pkg["version"] == "4.17.21" for pkg in packages)
    
    def test_get_npm_packages_failure(self, mock_system_info, mock_subprocess):
        """Test NodeInstaller get_npm_packages with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = NodeInstaller(mock_system_info)
        packages = installer.get_npm_packages()
        
        assert packages == []


class TestGitInstaller:
    """Test GitInstaller class."""
    
    def test_git_installer_creation(self, mock_system_info):
        """Test GitInstaller creation."""
        installer = GitInstaller(mock_system_info)
        
        assert installer.system == mock_system_info
    
    def test_is_installed_success(self, mock_system_info, mock_subprocess):
        """Test GitInstaller is_installed with successful detection."""
        # Mock subprocess.run to return successful version check
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "git version 2.51.0\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        # Mock _find_git_path, _is_configured, _has_ssh_key
        with patch.object(GitInstaller, '_find_git_path', return_value=Path("/usr/bin/git")), \
             patch.object(GitInstaller, '_is_configured', return_value=True), \
             patch.object(GitInstaller, '_has_ssh_key', return_value=True), \
             patch.object(GitInstaller, '_is_system_git', return_value=True):
            
            installer = GitInstaller(mock_system_info)
            installation = installer.is_installed()
            
            assert installation is not None
            assert installation.version == "2.51.0"
            assert installation.path == Path("/usr/bin/git")
            assert installation.is_system is True
            assert installation.is_configured is True
            assert installation.has_ssh_key is True
    
    def test_is_installed_not_found(self, mock_system_info, mock_subprocess):
        """Test GitInstaller is_installed when Git not found."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        installation = installer.is_installed()
        
        assert installation is None
    
    def test_choose_installation_method_package_manager(self, mock_system_info):
        """Test GitInstaller _choose_installation_method with package manager."""
        installer = GitInstaller(mock_system_info)
        method = installer._choose_installation_method()
        
        assert method == "package_manager"
    
    def test_choose_installation_method_official(self, mock_system_info):
        """Test GitInstaller _choose_installation_method with official installer."""
        # Create system without package managers
        no_pm_system = mock_system_info
        no_pm_system.package_managers = []
        
        installer = GitInstaller(no_pm_system)
        method = installer._choose_installation_method()
        
        assert method == "official"
    
    def test_install_package_manager_success(self, mock_system_info, mock_subprocess):
        """Test GitInstaller _install_package_manager with success."""
        # Mock subprocess.run for package manager commands
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Success\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        # Mock is_installed to return successful installation
        with patch.object(GitInstaller, 'is_installed', return_value=Mock(version="2.51.0", path=Path("/usr/bin/git"))):
            installer = GitInstaller(mock_system_info)
            progress = Mock()
            task_id = Mock()
            
            result = installer._install_package_manager(progress, task_id)
            
            assert result.success is True
            assert result.version == "2.51.0"
            assert result.method == "package_manager"
    
    def test_install_package_manager_failure(self, mock_system_info, mock_subprocess):
        """Test GitInstaller _install_package_manager with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stderr = b"brew install failed"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        progress = Mock()
        task_id = Mock()
        
        result = installer._install_package_manager(progress, task_id)
        
        assert result.success is False
        assert "Package manager installation failed" in result.error
    
    def test_configure_success(self, mock_system_info, mock_subprocess):
        """Test GitInstaller configure with success."""
        # Mock subprocess.run for git config commands
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        progress = Mock()
        task_id = Mock()
        
        result = installer.configure("John Doe", "john@example.com", progress, task_id)
        
        assert result is True
    
    def test_configure_failure(self, mock_system_info, mock_subprocess):
        """Test GitInstaller configure with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        progress = Mock()
        task_id = Mock()
        
        result = installer.configure("John Doe", "john@example.com", progress, task_id)
        
        assert result is False
    
    def test_setup_ssh_key_success(self, mock_system_info, mock_subprocess, temp_dir):
        """Test GitInstaller setup_ssh_key with success."""
        # Mock subprocess.run for ssh-keygen and ssh-add commands
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        # Mock Path.home to return temp directory
        with patch('pathlib.Path.home', return_value=temp_dir):
            installer = GitInstaller(mock_system_info)
            progress = Mock()
            task_id = Mock()
            
            result = installer.setup_ssh_key("john@example.com", progress, task_id)
            
            assert result is True
    
    def test_setup_ssh_key_failure(self, mock_system_info, mock_subprocess):
        """Test GitInstaller setup_ssh_key with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        progress = Mock()
        task_id = Mock()
        
        result = installer.setup_ssh_key("john@example.com", progress, task_id)
        
        assert result is False
    
    def test_get_ssh_public_key_success(self, temp_dir):
        """Test GitInstaller get_ssh_public_key with success."""
        # Create mock SSH key file
        ssh_dir = temp_dir / ".ssh"
        ssh_dir.mkdir()
        ssh_key_file = ssh_dir / "id_ed25519.pub"
        ssh_key_file.write_text("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJl3dIeudNqd0DPMRD9C7i7c5k2LxtTFsdQ7J1YqGj8K john@example.com")
        
        with patch('pathlib.Path.home', return_value=temp_dir):
            installer = GitInstaller(Mock())
            public_key = installer.get_ssh_public_key()
            
            assert public_key == "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJl3dIeudNqd0DPMRD9C7i7c5k2LxtTFsdQ7J1YqGj8K john@example.com"
    
    def test_get_ssh_public_key_not_found(self, temp_dir):
        """Test GitInstaller get_ssh_public_key when key not found."""
        with patch('pathlib.Path.home', return_value=temp_dir):
            installer = GitInstaller(Mock())
            public_key = installer.get_ssh_public_key()
            
            assert public_key is None
    
    def test_verify_success(self, mock_system_info, mock_subprocess):
        """Test GitInstaller verify with success."""
        # Mock subprocess.run to return successful verification
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "git version 2.51.0\n"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        result = installer.verify()
        
        assert result is True
    
    def test_verify_failure(self, mock_system_info, mock_subprocess):
        """Test GitInstaller verify with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        result = installer.verify()
        
        assert result is False
    
    def test_test_github_connection_success(self, mock_system_info, mock_subprocess):
        """Test GitInstaller test_github_connection with success."""
        # Mock subprocess.run to return successful authentication
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 1  # GitHub returns 1 for successful auth
            mock_result.stderr = "Hi username! You've successfully authenticated"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        result = installer.test_github_connection()
        
        assert result is True
    
    def test_test_github_connection_failure(self, mock_system_info, mock_subprocess):
        """Test GitInstaller test_github_connection with failure."""
        # Mock subprocess.run to return failure
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 255
            mock_result.stderr = "Permission denied"
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        installer = GitInstaller(mock_system_info)
        result = installer.test_github_connection()
        
        assert result is False
    
    def test_get_recommended_setup_commands(self, mock_system_info):
        """Test GitInstaller get_recommended_setup_commands."""
        # Mock is_installed, _is_configured, _has_ssh_key, test_github_connection
        with patch.object(GitInstaller, 'is_installed', return_value=None), \
             patch.object(GitInstaller, '_is_configured', return_value=False), \
             patch.object(GitInstaller, '_has_ssh_key', return_value=False), \
             patch.object(GitInstaller, 'test_github_connection', return_value=False):
            
            installer = GitInstaller(mock_system_info)
            commands = installer.get_recommended_setup_commands()
            
            assert "Install Git first" in commands
        
        # Mock Git installed but not configured
        with patch.object(GitInstaller, 'is_installed', return_value=Mock()), \
             patch.object(GitInstaller, '_is_configured', return_value=False), \
             patch.object(GitInstaller, '_has_ssh_key', return_value=False), \
             patch.object(GitInstaller, 'test_github_connection', return_value=False):
            
            installer = GitInstaller(mock_system_info)
            commands = installer.get_recommended_setup_commands()
            
            assert "git config --global user.name" in commands
            assert "git config --global user.email" in commands
            assert "ssh-keygen" in commands
            assert "ssh-add" in commands
