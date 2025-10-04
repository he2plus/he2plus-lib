"""Integration tests for CLI interface."""

import pytest
from unittest.mock import patch, Mock
from click.testing import CliRunner

from he2plus.cli.main import cli


class TestCLI:
    """Test CLI interface."""
    
    def test_cli_help(self):
        """Test CLI help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "he2plus - Professional Development Environment Manager" in result.output
        assert "Install complete development stacks with one command" in result.output
    
    def test_cli_version(self):
        """Test CLI version command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        assert "0.2.0" in result.output
    
    def test_cli_verbose_quiet(self):
        """Test CLI verbose and quiet options."""
        runner = CliRunner()
        
        # Test verbose
        result = runner.invoke(cli, ['--verbose', '--help'])
        assert result.exit_code == 0
        
        # Test quiet
        result = runner.invoke(cli, ['--quiet', '--help'])
        assert result.exit_code == 0
    
    def test_list_available_profiles(self):
        """Test list command with available profiles."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.ProfileRegistry') as mock_registry:
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            
            # Mock categories and profiles
            mock_registry_instance.get_categories.return_value = ["web3"]
            mock_profile = Mock()
            mock_profile.id = "web3-solidity"
            mock_profile.description = "Ethereum smart contract development"
            mock_registry_instance.get_by_category.return_value = [mock_profile]
            
            result = runner.invoke(cli, ['list', '--available'])
            
            assert result.exit_code == 0
            assert "Available Profiles" in result.output
            assert "WEB3" in result.output
            assert "web3-solidity" in result.output
            assert "Ethereum smart contract development" in result.output
    
    def test_list_installed_profiles(self):
        """Test list command for installed profiles."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.ProfileRegistry') as mock_registry:
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            
            result = runner.invoke(cli, ['list'])
            
            assert result.exit_code == 0
            assert "Installed Profiles" in result.output
            assert "(none installed yet)" in result.output
    
    def test_info_system(self):
        """Test info command for system information."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.SystemProfiler') as mock_profiler:
            # Mock system profiler
            mock_profiler_instance = Mock()
            mock_profiler.return_value = mock_profiler_instance
            
            # Mock system info
            mock_system_info = Mock()
            mock_system_info.os_name = "macOS"
            mock_system_info.os_version = "15.7.1"
            mock_system_info.arch = "arm64"
            mock_system_info.cpu_name = "Apple M4"
            mock_system_info.cpu_cores = 10
            mock_system_info.ram_total_gb = 16.0
            mock_system_info.disk_free_gb = 900.0
            mock_system_info.gpu_name = "Apple M4"
            mock_system_info.package_managers = ["brew", "pip", "npm"]
            mock_system_info.languages = {"python": "3.13.7", "node": "v24.9.0"}
            
            mock_profiler_instance.profile.return_value = mock_system_info
            
            result = runner.invoke(cli, ['info'])
            
            assert result.exit_code == 0
            assert "System Information" in result.output
            assert "macOS 15.7.1" in result.output
            assert "arm64" in result.output
            assert "Apple M4" in result.output
            assert "16.0 GB" in result.output
            assert "900.0 GB" in result.output
    
    def test_info_profile(self):
        """Test info command for profile information."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.ProfileRegistry') as mock_registry:
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            
            # Mock profile
            mock_profile = Mock()
            mock_profile.name = "Solidity Development"
            mock_profile.description = "Ethereum smart contract development"
            mock_profile.category = "web3"
            mock_profile.version = "1.0.0"
            mock_profile.get_requirements.return_value = Mock(
                ram_gb=4.0,
                disk_gb=10.0,
                cpu_cores=2,
                gpu_required=False
            )
            mock_profile.get_components.return_value = [
                Mock(name="Node.js 18 LTS", category="language"),
                Mock(name="npm", category="tool"),
                Mock(name="Git", category="tool")
            ]
            mock_profile.get_verification_steps.return_value = [
                Mock(name="Node.js Version", command="node --version"),
                Mock(name="npm Version", command="npm --version")
            ]
            mock_profile.get_sample_project.return_value = Mock(
                name="Hardhat Starter Kit",
                type="git_clone",
                source="https://github.com/he2plus/hardhat-starter-kit.git"
            )
            
            mock_registry_instance.get.return_value = mock_profile
            
            result = runner.invoke(cli, ['info', 'web3-solidity'])
            
            assert result.exit_code == 0
            assert "Solidity Development" in result.output
            assert "Ethereum smart contract development" in result.output
            assert "web3" in result.output
            assert "1.0.0" in result.output
            assert "4.0 GB" in result.output
            assert "10.0 GB" in result.output
            assert "2 cores" in result.output
            assert "Node.js 18 LTS" in result.output
            assert "npm" in result.output
            assert "Git" in result.output
    
    def test_info_profile_not_found(self):
        """Test info command for non-existent profile."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.ProfileRegistry') as mock_registry:
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_registry_instance.get.return_value = None
            
            result = runner.invoke(cli, ['info', 'nonexistent-profile'])
            
            assert result.exit_code == 0
            assert "Profile not found" in result.output
    
    def test_doctor(self):
        """Test doctor command."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.SystemProfiler') as mock_profiler:
            # Mock system profiler
            mock_profiler_instance = Mock()
            mock_profiler.return_value = mock_profiler_instance
            
            # Mock system info
            mock_system_info = Mock()
            mock_system_info.os_name = "macOS"
            mock_system_info.os_version = "15.7.1"
            mock_system_info.arch = "arm64"
            mock_system_info.cpu_name = "Apple M4"
            mock_system_info.cpu_cores = 10
            mock_system_info.ram_total_gb = 16.0
            mock_system_info.ram_available_gb = 8.0
            mock_system_info.disk_free_gb = 900.0
            mock_system_info.gpu_name = "Apple M4"
            mock_system_info.package_managers = ["brew", "pip", "npm"]
            
            mock_profiler_instance.profile.return_value = mock_system_info
            
            # Mock check_tool_installed
            def mock_check_tool(tool):
                if tool == "git":
                    return {"version": "git version 2.51.0"}
                elif tool == "python3":
                    return {"version": "Python 3.13.7"}
                elif tool == "node":
                    return {"version": "v24.9.0"}
                elif tool == "docker":
                    return None
                return None
            
            with patch('he2plus.cli.main.check_tool_installed', side_effect=mock_check_tool):
                result = runner.invoke(cli, ['doctor'])
                
                assert result.exit_code == 0
                assert "System Health Check" in result.output
                assert "System Information" in result.output
                assert "Development Tools" in result.output
                assert "Package Managers" in result.output
                assert "macOS 15.7.1" in result.output
                assert "Apple M4" in result.output
                assert "16.0 GB" in result.output
                assert "git version 2.51.0" in result.output
                assert "Python 3.13.7" in result.output
                assert "v24.9.0" in result.output
                assert "not installed" in result.output
    
    def test_doctor_with_profile(self):
        """Test doctor command with specific profile."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.SystemProfiler') as mock_profiler, \
             patch('he2plus.cli.main.ProfileRegistry') as mock_registry, \
             patch('he2plus.cli.main.SystemValidator') as mock_validator:
            
            # Mock system profiler
            mock_profiler_instance = Mock()
            mock_profiler.return_value = mock_profiler_instance
            mock_system_info = Mock()
            mock_profiler_instance.profile.return_value = mock_system_info
            
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_profile = Mock()
            mock_registry_instance.get.return_value = mock_profile
            
            # Mock validator
            mock_validator_instance = Mock()
            mock_validator.return_value = mock_validator_instance
            mock_validation = Mock()
            mock_validation.safe_to_install = True
            mock_validation.blocking_issues = []
            mock_validator_instance.validate.return_value = mock_validation
            
            # Mock check_tool_installed
            with patch('he2plus.cli.main.check_tool_installed', return_value=None):
                result = runner.invoke(cli, ['doctor', '--profile', 'web3-solidity'])
                
                assert result.exit_code == 0
                assert "System Health Check" in result.output
                assert "web3-solidity" in result.output
    
    def test_search(self):
        """Test search command."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.ProfileRegistry') as mock_registry:
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            
            # Mock search results
            mock_profile = Mock()
            mock_profile.name = "Solidity Development"
            mock_profile.id = "web3-solidity"
            mock_profile.description = "Ethereum smart contract development"
            mock_profile.category = "web3"
            mock_profile.get_requirements.return_value = Mock(ram_gb=4.0, disk_gb=10.0)
            
            mock_registry_instance.search.return_value = [mock_profile]
            
            result = runner.invoke(cli, ['search', 'solidity'])
            
            assert result.exit_code == 0
            assert "Search Results for 'solidity'" in result.output
            assert "Solidity Development" in result.output
            assert "web3-solidity" in result.output
            assert "Ethereum smart contract development" in result.output
            assert "web3" in result.output
            assert "4.0GB RAM" in result.output
            assert "10.0GB disk" in result.output
    
    def test_search_no_results(self):
        """Test search command with no results."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.ProfileRegistry') as mock_registry:
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_registry_instance.search.return_value = []
            
            result = runner.invoke(cli, ['search', 'nonexistent'])
            
            assert result.exit_code == 0
            assert "No profiles found matching 'nonexistent'" in result.output
    
    def test_search_no_query(self):
        """Test search command without query."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['search'])
        
        assert result.exit_code == 0
        assert "Please provide a search query" in result.output
        assert "Usage: he2plus search <query>" in result.output
    
    def test_install_profile_not_found(self):
        """Test install command with non-existent profile."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.SystemProfiler') as mock_profiler, \
             patch('he2plus.cli.main.ProfileRegistry') as mock_registry:
            
            # Mock system profiler
            mock_profiler_instance = Mock()
            mock_profiler.return_value = mock_profiler_instance
            mock_system_info = Mock()
            mock_profiler_instance.profile.return_value = mock_system_info
            
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_registry_instance.get.return_value = None
            
            result = runner.invoke(cli, ['install', 'nonexistent-profile'])
            
            assert result.exit_code == 0
            assert "Profile not found" in result.output
            assert "Run 'he2plus list --available'" in result.output
    
    def test_install_insufficient_resources(self):
        """Test install command with insufficient resources."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.SystemProfiler') as mock_profiler, \
             patch('he2plus.cli.main.ProfileRegistry') as mock_registry, \
             patch('he2plus.cli.main.SystemValidator') as mock_validator:
            
            # Mock system profiler
            mock_profiler_instance = Mock()
            mock_profiler.return_value = mock_profiler_instance
            mock_system_info = Mock()
            mock_system_info.os_name = "macOS"
            mock_system_info.os_version = "15.7.1"
            mock_system_info.arch = "arm64"
            mock_system_info.ram_total_gb = 16.0
            mock_system_info.ram_available_gb = 8.0
            mock_system_info.disk_free_gb = 900.0
            mock_profiler_instance.profile.return_value = mock_system_info
            
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_profile = Mock()
            mock_profile.name = "Test Profile"
            mock_registry_instance.get.return_value = mock_profile
            
            # Mock validator
            mock_validator_instance = Mock()
            mock_validator.return_value = mock_validator_instance
            mock_validation = Mock()
            mock_validation.safe_to_install = False
            mock_validation.blocking_issues = ["Insufficient RAM: 2GB available, 4GB required"]
            mock_validator_instance.validate.return_value = mock_validation
            
            result = runner.invoke(cli, ['install', 'test-profile'])
            
            assert result.exit_code == 0
            assert "Cannot install Test Profile" in result.output
            assert "Insufficient RAM" in result.output
    
    def test_install_success(self):
        """Test install command with success."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.SystemProfiler') as mock_profiler, \
             patch('he2plus.cli.main.ProfileRegistry') as mock_registry, \
             patch('he2plus.cli.main.SystemValidator') as mock_validator, \
             patch('he2plus.cli.main.verify_profile') as mock_verify:
            
            # Mock system profiler
            mock_profiler_instance = Mock()
            mock_profiler.return_value = mock_profiler_instance
            mock_system_info = Mock()
            mock_system_info.os_name = "macOS"
            mock_system_info.os_version = "15.7.1"
            mock_system_info.arch = "arm64"
            mock_system_info.ram_total_gb = 16.0
            mock_system_info.ram_available_gb = 8.0
            mock_system_info.disk_free_gb = 900.0
            mock_profiler_instance.profile.return_value = mock_system_info
            
            # Mock registry
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_profile = Mock()
            mock_profile.name = "Test Profile"
            mock_profile.description = "A test profile"
            mock_profile.get_components.return_value = [
                Mock(name="Component 1", category="tool"),
                Mock(name="Component 2", category="package")
            ]
            mock_profile.get_requirements.return_value = Mock(ram_gb=4.0, disk_gb=10.0)
            mock_profile.get_estimated_download_size.return_value = 100.0
            mock_profile.get_estimated_install_time.return_value = 30
            mock_profile.get_next_steps.return_value = ["Step 1", "Step 2"]
            mock_registry_instance.get.return_value = mock_profile
            
            # Mock validator
            mock_validator_instance = Mock()
            mock_validator.return_value = mock_validator_instance
            mock_validation = Mock()
            mock_validation.safe_to_install = True
            mock_validation.blocking_issues = []
            mock_validation.warnings = []
            mock_validator_instance.validate.return_value = mock_validation
            
            # Mock verify_profile
            mock_verify.return_value = True
            
            result = runner.invoke(cli, ['install', 'test-profile', '--yes'])
            
            assert result.exit_code == 0
            assert "Analyzing system" in result.output
            assert "Installation Plan" in result.output
            assert "Test Profile" in result.output
            assert "A test profile" in result.output
            assert "Components: 2" in result.output
            assert "Installing" in result.output
            assert "All profiles installed successfully" in result.output
    
    def test_remove_not_implemented(self):
        """Test remove command (not yet implemented)."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['remove', 'test-profile'])
        
        assert result.exit_code == 0
        assert "Profile removal not yet implemented" in result.output
        assert "This feature will be available in a future version" in result.output
    
    def test_update_not_implemented(self):
        """Test update command (not yet implemented)."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['update', 'test-profile'])
        
        assert result.exit_code == 0
        assert "Profile updates not yet implemented" in result.output
        assert "This feature will be available in a future version" in result.output
    
    def test_info_json_output(self):
        """Test info command with JSON output."""
        runner = CliRunner()
        
        with patch('he2plus.cli.main.SystemProfiler') as mock_profiler:
            # Mock system profiler
            mock_profiler_instance = Mock()
            mock_profiler.return_value = mock_profiler_instance
            
            # Mock system info
            mock_system_info = Mock()
            mock_system_info.os_name = "macOS"
            mock_system_info.os_version = "15.7.1"
            mock_system_info.arch = "arm64"
            mock_system_info.cpu_name = "Apple M4"
            mock_system_info.cpu_cores = 10
            mock_system_info.ram_total_gb = 16.0
            mock_system_info.disk_free_gb = 900.0
            mock_system_info.gpu_name = "Apple M4"
            mock_system_info.package_managers = ["brew", "pip", "npm"]
            mock_system_info.languages = {"python": "3.13.7", "node": "v24.9.0"}
            
            mock_profiler_instance.profile.return_value = mock_system_info
            
            result = runner.invoke(cli, ['info', '--json'])
            
            assert result.exit_code == 0
            assert '"os_name": "macOS"' in result.output
            assert '"os_version": "15.7.1"' in result.output
            assert '"arch": "arm64"' in result.output
            assert '"cpu_name": "Apple M4"' in result.output
            assert '"cpu_cores": 10' in result.output
            assert '"ram_total_gb": 16.0' in result.output
            assert '"disk_free_gb": 900.0' in result.output
            assert '"gpu_name": "Apple M4"' in result.output
            assert '"package_managers": ["brew", "pip", "npm"]' in result.output
            assert '"languages": {"python": "3.13.7", "node": "v24.9.0"}' in result.output
