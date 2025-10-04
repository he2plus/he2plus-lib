"""
Tests for he2plus CLI functionality.

This module tests the command-line interface including all commands
and their integration with the core system.
"""

import pytest
import sys
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from he2plus.cli.main import cli


class TestCLI:
    """Test CLI functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
    
    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "he2plus" in result.output
        assert "Professional Development Environment Manager" in result.output
    
    def test_cli_version(self):
        """Test CLI version command."""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert "0.2.0" in result.output
    
    def test_list_command(self):
        """Test list command."""
        result = self.runner.invoke(cli, ['list', '--help'])
        assert result.exit_code == 0
        assert "list" in result.output
    
    def test_list_available(self):
        """Test list available profiles."""
        result = self.runner.invoke(cli, ['list', '--available'])
        assert result.exit_code == 0
        assert "Available Profiles" in result.output
        assert "web3-solidity" in result.output
        assert "web-nextjs" in result.output
        assert "mobile-react-native" in result.output
        assert "ml-python" in result.output
    
    def test_list_by_category(self):
        """Test list profiles by category."""
        result = self.runner.invoke(cli, ['list', '--category', 'web3'])
        assert result.exit_code == 0
        assert "web3-solidity" in result.output
    
    def test_search_command(self):
        """Test search command."""
        result = self.runner.invoke(cli, ['search', '--help'])
        assert result.exit_code == 0
        assert "search" in result.output
    
    def test_search_react(self):
        """Test searching for React profiles."""
        result = self.runner.invoke(cli, ['search', 'react'])
        assert result.exit_code == 0
        assert "react" in result.output.lower()
    
    def test_search_python(self):
        """Test searching for Python profiles."""
        result = self.runner.invoke(cli, ['search', 'python'])
        assert result.exit_code == 0
        assert "python" in result.output.lower()
    
    def test_info_command(self):
        """Test info command."""
        result = self.runner.invoke(cli, ['info', '--help'])
        assert result.exit_code == 0
        assert "info" in result.output
    
    def test_info_web3_solidity(self):
        """Test info for web3-solidity profile."""
        result = self.runner.invoke(cli, ['info', 'web3-solidity'])
        assert result.exit_code == 0
        assert "Solidity Development" in result.output
        assert "Ethereum smart contract" in result.output
        assert "Category: web3" in result.output
    
    def test_info_web_nextjs(self):
        """Test info for web-nextjs profile."""
        result = self.runner.invoke(cli, ['info', 'web-nextjs'])
        assert result.exit_code == 0
        assert "Next.js Development" in result.output
        assert "React framework" in result.output
        assert "Category: web" in result.output
    
    def test_info_mobile_react_native(self):
        """Test info for mobile-react-native profile."""
        result = self.runner.invoke(cli, ['info', 'mobile-react-native'])
        assert result.exit_code == 0
        assert "React Native Development" in result.output
        assert "Cross-platform mobile" in result.output
        assert "Category: mobile" in result.output
    
    def test_info_ml_python(self):
        """Test info for ml-python profile."""
        result = self.runner.invoke(cli, ['info', 'ml-python'])
        assert result.exit_code == 0
        assert "Python Machine Learning" in result.output
        assert "TensorFlow" in result.output
        assert "Category: ml" in result.output
    
    def test_info_nonexistent_profile(self):
        """Test info for nonexistent profile."""
        result = self.runner.invoke(cli, ['info', 'nonexistent-profile'])
        assert result.exit_code == 0
        assert "Profile not found" in result.output
    
    def test_doctor_command(self):
        """Test doctor command."""
        result = self.runner.invoke(cli, ['doctor', '--help'])
        assert result.exit_code == 0
        assert "doctor" in result.output
    
    def test_doctor_system_check(self):
        """Test doctor system check."""
        result = self.runner.invoke(cli, ['doctor'])
        assert result.exit_code == 0
        assert "System Health Check" in result.output
        assert "System Information" in result.output
        assert "Development Tools" in result.output
        assert "Package Managers" in result.output
    
    def test_doctor_with_profile(self):
        """Test doctor with specific profile."""
        result = self.runner.invoke(cli, ['doctor', '--profile', 'web3-solidity'])
        assert result.exit_code == 0
        assert "System Health Check" in result.output
    
    def test_install_command(self):
        """Test install command."""
        result = self.runner.invoke(cli, ['install', '--help'])
        assert result.exit_code == 0
        assert "install" in result.output
    
    @patch('he2plus.cli.main.InstallationEngine')
    @patch('he2plus.cli.main.SystemProfiler')
    @patch('he2plus.cli.main.ProfileRegistry')
    def test_install_profile_mock(self, mock_registry, mock_profiler, mock_engine):
        """Test install command with mocked dependencies."""
        # Mock the system profiler
        mock_system_info = Mock()
        mock_system_info.os_name = "macOS"
        mock_system_info.os_version = "15.7.1"
        mock_system_info.arch = "arm64"
        mock_system_info.ram_total_gb = 16.0
        mock_system_info.ram_available_gb = 8.0
        mock_system_info.disk_free_gb = 500.0
        mock_profiler.return_value.profile.return_value = mock_system_info
        
        # Mock the profile registry
        mock_profile = Mock()
        mock_profile.name = "Test Profile"
        mock_profile.description = "Test Description"
        mock_profile.get_components.return_value = []
        mock_profile.get_requirements.return_value = Mock()
        mock_registry.return_value.get.return_value = mock_profile
        
        # Mock the installation engine
        mock_installer = Mock()
        mock_engine.return_value = mock_installer
        
        result = self.runner.invoke(cli, ['install', 'web3-solidity', '--yes'])
        assert result.exit_code == 0
        assert "Analyzing system" in result.output
    
    def test_install_nonexistent_profile(self):
        """Test install command with nonexistent profile."""
        result = self.runner.invoke(cli, ['install', 'nonexistent-profile'])
        assert result.exit_code == 0
        assert "Profile not found" in result.output
    
    def test_update_command(self):
        """Test update command."""
        result = self.runner.invoke(cli, ['update', '--help'])
        assert result.exit_code == 0
        assert "update" in result.output
    
    def test_update_not_implemented(self):
        """Test update command (not yet implemented)."""
        result = self.runner.invoke(cli, ['update', 'web3-solidity'])
        assert result.exit_code == 0
        assert "not yet implemented" in result.output
    
    def test_verbose_flag(self):
        """Test verbose flag."""
        result = self.runner.invoke(cli, ['--verbose', 'list', '--available'])
        assert result.exit_code == 0
        assert "Available Profiles" in result.output
    
    def test_quiet_flag(self):
        """Test quiet flag."""
        result = self.runner.invoke(cli, ['--quiet', 'list', '--available'])
        assert result.exit_code == 0
        assert "Available Profiles" in result.output


class TestCLIIntegration:
    """Test CLI integration with real components."""
    
    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
    
    def test_real_system_detection(self):
        """Test real system detection through CLI."""
        result = self.runner.invoke(cli, ['doctor'])
        assert result.exit_code == 0
        
        # Should detect real system information
        assert "System Information" in result.output
        assert "OS" in result.output
        assert "Architecture" in result.output
        assert "RAM" in result.output
        assert "Disk" in result.output
    
    def test_real_profile_loading(self):
        """Test real profile loading through CLI."""
        result = self.runner.invoke(cli, ['list', '--available'])
        assert result.exit_code == 0
        
        # Should load real profiles
        assert "web3-solidity" in result.output
        assert "web-nextjs" in result.output
        assert "mobile-react-native" in result.output
        assert "ml-python" in result.output
    
    def test_real_profile_info(self):
        """Test real profile information through CLI."""
        result = self.runner.invoke(cli, ['info', 'web3-solidity'])
        assert result.exit_code == 0
        
        # Should show real profile information
        assert "Solidity Development" in result.output
        assert "Ethereum smart contract" in result.output
        assert "Category: web3" in result.output
        assert "Components" in result.output
        assert "Verification Steps" in result.output
    
    def test_real_search_functionality(self):
        """Test real search functionality through CLI."""
        result = self.runner.invoke(cli, ['search', 'react'])
        assert result.exit_code == 0
        
        # Should find React-related profiles
        assert "react" in result.output.lower()
        assert "Next.js" in result.output or "React Native" in result.output
    
    def test_real_validation(self):
        """Test real validation through CLI."""
        result = self.runner.invoke(cli, ['doctor', '--profile', 'web3-solidity'])
        assert result.exit_code == 0
        
        # Should show validation results
        assert "System Health Check" in result.output
        assert "Profile can be installed" in result.output or "Profile cannot be installed" in result.output


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
