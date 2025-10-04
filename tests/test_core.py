"""
Comprehensive tests for he2plus core components.

This module tests all core functionality including system detection,
validation, installation engine, and profile management.
"""

import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from he2plus.core.system import SystemProfiler, SystemInfo
from he2plus.core.validator import SystemValidator, ProfileRequirements, ValidationResult
from he2plus.core.installer import InstallationEngine, PackageManager, HomebrewManager, APTManager, ChocolateyManager, VerificationResult
from he2plus.profiles.registry import ProfileRegistry
from he2plus.profiles.base import BaseProfile, Component, VerificationStep, SampleProject


class TestSystemProfiler:
    """Test system profiling functionality."""
    
    def test_system_profiler_initialization(self):
        """Test SystemProfiler initialization."""
        profiler = SystemProfiler()
        assert profiler is not None
    
    def test_system_profiling(self):
        """Test system profiling returns valid SystemInfo."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        assert isinstance(system_info, SystemInfo)
        assert system_info.os_name is not None
        assert system_info.arch is not None
        assert system_info.ram_total_gb > 0
        assert system_info.disk_free_gb > 0
        assert system_info.cpu_cores > 0
    
    def test_os_detection(self):
        """Test OS detection works correctly."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Should detect a valid OS
        assert system_info.os_name in ["macOS", "Windows", "Linux"]
        assert system_info.os_version is not None
    
    def test_architecture_detection(self):
        """Test architecture detection."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Should detect a valid architecture
        assert system_info.arch in ["x86_64", "arm64", "arm", "i386", "amd64"]
    
    def test_memory_detection(self):
        """Test memory detection."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Should have reasonable memory values
        assert system_info.ram_total_gb > 0
        assert system_info.ram_available_gb > 0
        assert system_info.ram_available_gb <= system_info.ram_total_gb
    
    def test_disk_detection(self):
        """Test disk space detection."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Should have reasonable disk values
        assert system_info.disk_total_gb > 0
        assert system_info.disk_free_gb > 0
        assert system_info.disk_free_gb <= system_info.disk_total_gb
    
    def test_cpu_detection(self):
        """Test CPU detection."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Should have reasonable CPU values
        assert system_info.cpu_cores > 0
        assert system_info.cpu_name is not None
    
    def test_package_manager_detection(self):
        """Test package manager detection."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Should detect at least one package manager
        assert len(system_info.package_managers) > 0
        assert isinstance(system_info.package_managers, list)


class TestSystemValidator:
    """Test system validation functionality."""
    
    def test_validator_initialization(self):
        """Test SystemValidator initialization."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        validator = SystemValidator(system_info)
        
        assert validator is not None
        assert validator.system == system_info
    
    def test_requirements_validation(self):
        """Test requirements validation."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        validator = SystemValidator(system_info)
        
        # Test with reasonable requirements
        requirements = ProfileRequirements(
            ram_gb=1.0,
            disk_gb=1.0,
            cpu_cores=1,
            gpu_required=False
        )
        
        result = validator.validate(requirements)
        
        assert isinstance(result, ValidationResult)
        assert result.safe_to_install is True
        assert len(result.blocking_issues) == 0
    
    def test_insufficient_ram_validation(self):
        """Test validation with insufficient RAM."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        validator = SystemValidator(system_info)
        
        # Test with excessive RAM requirements
        requirements = ProfileRequirements(
            ram_gb=1000.0,  # Unrealistic requirement
            disk_gb=1.0,
            cpu_cores=1,
            gpu_required=False
        )
        
        result = validator.validate(requirements)
        
        assert isinstance(result, ValidationResult)
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert any("RAM" in issue for issue in result.blocking_issues)
    
    def test_insufficient_disk_validation(self):
        """Test validation with insufficient disk space."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        validator = SystemValidator(system_info)
        
        # Test with excessive disk requirements
        requirements = ProfileRequirements(
            ram_gb=1.0,
            disk_gb=10000.0,  # Unrealistic requirement
            cpu_cores=1,
            gpu_required=False
        )
        
        result = validator.validate(requirements)
        
        assert isinstance(result, ValidationResult)
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert any("disk" in issue.lower() for issue in result.blocking_issues)
    
    def test_insufficient_cpu_validation(self):
        """Test validation with insufficient CPU cores."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        validator = SystemValidator(system_info)
        
        # Test with excessive CPU requirements
        requirements = ProfileRequirements(
            ram_gb=1.0,
            disk_gb=1.0,
            cpu_cores=100,  # Unrealistic requirement
            gpu_required=False
        )
        
        result = validator.validate(requirements)
        
        assert isinstance(result, ValidationResult)
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert any("CPU" in issue for issue in result.blocking_issues)


class TestInstallationEngine:
    """Test installation engine functionality."""
    
    def test_installation_engine_initialization(self):
        """Test InstallationEngine initialization."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        engine = InstallationEngine(system_info)
        
        assert engine is not None
        assert engine.system == system_info
        assert engine.install_dir is not None
    
    def test_package_manager_detection(self):
        """Test package manager detection in installation engine."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        engine = InstallationEngine(system_info)
        
        # Should have at least one package manager
        assert len(engine.package_managers) > 0
        assert "homebrew" in engine.package_managers or "apt" in engine.package_managers or "chocolatey" in engine.package_managers
    
    def test_component_installation_planning(self):
        """Test component installation planning."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        engine = InstallationEngine(system_info)
        
        # Create a test component
        component = Component(
            id="tool.git",
            name="Git",
            description="Version control system",
            category="tool",
            download_size_mb=30.0,
            install_time_minutes=3,
            install_methods=["package_manager", "official"]
        )
        
        # Test package name mapping
        package_name = engine._get_package_name(component)
        assert package_name == "git"
    
    def test_verification_step_execution(self):
        """Test verification step execution."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        engine = InstallationEngine(system_info)
        
        # Create a test verification step
        verification_step = VerificationStep(
            name="Git Version",
            command="git --version",
            contains_text="git version"
        )
        
        # Test verification
        result = engine.verify_component(None, verification_step)
        
        assert isinstance(result, VerificationResult)
        # Should succeed if git is installed
        if shutil.which("git"):
            assert result.success is True
        else:
            assert result.success is False


class TestProfileRegistry:
    """Test profile registry functionality."""
    
    def test_registry_initialization(self):
        """Test ProfileRegistry initialization."""
        registry = ProfileRegistry()
        assert registry is not None
        assert not registry._loaded
    
    def test_profile_loading(self):
        """Test profile loading."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        assert registry._loaded is True
        assert len(registry._profiles) > 0
        assert len(registry._categories) > 0
    
    def test_profile_retrieval(self):
        """Test profile retrieval by ID."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        # Test getting a known profile
        profile = registry.get("web3-solidity")
        assert profile is not None
        assert profile.id == "web3-solidity"
    
    def test_profile_listing(self):
        """Test profile listing."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        # Test getting all profiles
        all_profiles = registry.get_all()
        assert len(all_profiles) > 0
        
        # Test getting profiles by category
        web3_profiles = registry.get_by_category("web3")
        assert len(web3_profiles) > 0
    
    def test_profile_categories(self):
        """Test profile category listing."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        categories = registry.get_categories()
        assert len(categories) > 0
        assert "web3" in categories
    
    def test_profile_search(self):
        """Test profile search functionality."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        # Test searching for profiles
        results = registry.search("solidity")
        assert len(results) > 0
        
        # Test searching for non-existent profiles
        results = registry.search("nonexistent")
        assert len(results) == 0


class TestBaseProfile:
    """Test base profile functionality."""
    
    def test_profile_initialization(self):
        """Test profile initialization."""
        # Create a test profile class
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
        
        profile = TestProfile()
        assert profile.id == "test-profile"
        assert profile.name == "Test Profile"
        assert profile.description == "A test profile"
        assert profile.category == "test"
    
    def test_component_management(self):
        """Test component management in profiles."""
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
                
                self.components = [
                    Component(
                        id="tool.test",
                        name="Test Tool",
                        description="A test tool",
                        category="tool",
                        download_size_mb=10.0,
                        install_time_minutes=2,
                        install_methods=["package_manager"]
                    )
                ]
        
        profile = TestProfile()
        components = profile.get_components()
        
        assert len(components) == 1
        assert components[0].id == "tool.test"
        assert components[0].name == "Test Tool"
    
    def test_verification_steps(self):
        """Test verification steps in profiles."""
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
                
                self.verification_steps = [
                    VerificationStep(
                        name="Test Verification",
                        command="echo 'test'",
                        contains_text="test"
                    )
                ]
        
        profile = TestProfile()
        steps = profile.get_verification_steps()
        
        assert len(steps) == 1
        assert steps[0].name == "Test Verification"
        assert steps[0].command == "echo 'test'"
    
    def test_sample_project(self):
        """Test sample project in profiles."""
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
                
                self.sample_project = SampleProject(
                    name="Test Project",
                    description="A test project",
                    type="create_app",
                    source="echo 'test'",
                    directory="~/test-project"
                )
        
        profile = TestProfile()
        sample_project = profile.get_sample_project()
        
        assert sample_project is not None
        assert sample_project.name == "Test Project"
        assert sample_project.type == "create_app"


class TestPackageManagers:
    """Test package manager functionality."""
    
    def test_homebrew_manager(self):
        """Test Homebrew package manager."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        manager = HomebrewManager(system_info)
        
        assert manager is not None
        assert isinstance(manager.is_available(), bool)
    
    def test_apt_manager(self):
        """Test APT package manager."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        manager = APTManager(system_info)
        
        assert manager is not None
        assert isinstance(manager.is_available(), bool)
    
    def test_chocolatey_manager(self):
        """Test Chocolatey package manager."""
        profiler = SystemProfiler()
        system_info = profiler.profile()
        manager = ChocolateyManager(system_info)
        
        assert manager is not None
        assert isinstance(manager.is_available(), bool)


class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_end_to_end_profile_loading(self):
        """Test end-to-end profile loading and validation."""
        # Load system information
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Load profiles
        registry = ProfileRegistry()
        registry.load_profiles()
        
        # Get a profile
        profile = registry.get("web3-solidity")
        assert profile is not None
        
        # Validate system requirements
        validator = SystemValidator(system_info)
        validation = validator.validate(profile.get_requirements())
        
        assert isinstance(validation, ValidationResult)
        # Should be safe to install on most systems
        assert validation.safe_to_install is True
    
    def test_installation_engine_integration(self):
        """Test installation engine integration."""
        # Load system information
        profiler = SystemProfiler()
        system_info = profiler.profile()
        
        # Create installation engine
        engine = InstallationEngine(system_info)
        
        # Create a test component
        component = Component(
            id="tool.git",
            name="Git",
            description="Version control system",
            category="tool",
            download_size_mb=30.0,
            install_time_minutes=3,
            install_methods=["package_manager", "official"]
        )
        
        # Test component installation planning
        package_name = engine._get_package_name(component)
        assert package_name == "git"
    
    def test_cli_integration(self):
        """Test CLI integration."""
        # Test that the CLI module can be imported
        try:
            from he2plus.cli.main import cli
            assert cli is not None
        except ImportError:
            pytest.fail("CLI module could not be imported")


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
