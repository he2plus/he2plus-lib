"""Unit tests for resource validation module."""

import pytest

from he2plus.core.validator import SystemValidator, ProfileRequirements, ValidationResult


class TestProfileRequirements:
    """Test ProfileRequirements dataclass."""
    
    def test_default_requirements(self):
        """Test default profile requirements."""
        req = ProfileRequirements()
        
        assert req.ram_gb == 4.0
        assert req.disk_gb == 10.0
        assert req.cpu_cores == 2
        assert req.gpu_required is False
        assert req.gpu_vendor is None
        assert req.cuda_required is False
        assert req.metal_required is False
        assert req.min_os_version is None
        assert req.supported_archs == ["x86_64", "arm64", "arm"]
        assert req.internet_required is True
        assert req.download_size_mb == 0.0
    
    def test_custom_requirements(self):
        """Test custom profile requirements."""
        req = ProfileRequirements(
            ram_gb=8.0,
            disk_gb=20.0,
            cpu_cores=4,
            gpu_required=True,
            gpu_vendor="NVIDIA",
            cuda_required=True,
            metal_required=False,
            min_os_version="10.15",
            supported_archs=["x86_64"],
            internet_required=False,
            download_size_mb=1000.0
        )
        
        assert req.ram_gb == 8.0
        assert req.disk_gb == 20.0
        assert req.cpu_cores == 4
        assert req.gpu_required is True
        assert req.gpu_vendor == "NVIDIA"
        assert req.cuda_required is True
        assert req.metal_required is False
        assert req.min_os_version == "10.15"
        assert req.supported_archs == ["x86_64"]
        assert req.internet_required is False
        assert req.download_size_mb == 1000.0


class TestSystemValidator:
    """Test SystemValidator class."""
    
    def test_validate_sufficient_resources(self, mock_system_info, mock_profile_requirements):
        """Test validation with sufficient system resources."""
        validator = SystemValidator(mock_system_info)
        result = validator.validate(mock_profile_requirements)
        
        assert result.safe_to_install is True
        assert len(result.blocking_issues) == 0
        assert result.ram_sufficient is True
        assert result.disk_sufficient is True
        assert result.cpu_sufficient is True
        assert result.gpu_sufficient is True
    
    def test_validate_insufficient_ram(self, mock_system_info, mock_profile_requirements):
        """Test validation with insufficient RAM."""
        # Create system with low RAM
        low_ram_system = mock_system_info
        low_ram_system.ram_total_gb = 2.0
        low_ram_system.ram_available_gb = 1.0
        
        validator = SystemValidator(low_ram_system)
        result = validator.validate(mock_profile_requirements)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "Insufficient RAM" in result.blocking_issues[0]
        assert result.ram_sufficient is False
    
    def test_validate_insufficient_disk(self, mock_system_info, mock_profile_requirements):
        """Test validation with insufficient disk space."""
        # Create system with low disk space
        low_disk_system = mock_system_info
        low_disk_system.disk_free_gb = 5.0
        
        validator = SystemValidator(low_disk_system)
        result = validator.validate(mock_profile_requirements)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "Insufficient disk space" in result.blocking_issues[0]
        assert result.disk_sufficient is False
    
    def test_validate_insufficient_cpu(self, mock_system_info, mock_profile_requirements):
        """Test validation with insufficient CPU cores."""
        # Create system with low CPU cores
        low_cpu_system = mock_system_info
        low_cpu_system.cpu_cores = 1
        
        validator = SystemValidator(low_cpu_system)
        result = validator.validate(mock_profile_requirements)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "Insufficient CPU cores" in result.blocking_issues[0]
        assert result.cpu_sufficient is False
    
    def test_validate_gpu_required_missing(self, mock_system_info, mock_profile_requirements_gpu):
        """Test validation with GPU required but not available."""
        # Create system without GPU
        no_gpu_system = mock_system_info
        no_gpu_system.gpu_name = None
        no_gpu_system.gpu_vendor = None
        no_gpu_system.cuda_available = False
        no_gpu_system.metal_available = False
        
        validator = SystemValidator(no_gpu_system)
        result = validator.validate(mock_profile_requirements_gpu)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "GPU required but not detected" in result.blocking_issues[0]
        assert result.gpu_sufficient is False
    
    def test_validate_gpu_vendor_mismatch(self, mock_system_info, mock_profile_requirements_gpu):
        """Test validation with wrong GPU vendor."""
        # Create system with wrong GPU vendor
        wrong_gpu_system = mock_system_info
        wrong_gpu_system.gpu_name = "AMD Radeon RX 6800"
        wrong_gpu_system.gpu_vendor = "AMD"
        wrong_gpu_system.cuda_available = False
        wrong_gpu_system.metal_available = False
        
        validator = SystemValidator(wrong_gpu_system)
        result = validator.validate(mock_profile_requirements_gpu)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "Wrong GPU vendor" in result.blocking_issues[0]
        assert result.gpu_sufficient is False
    
    def test_validate_cuda_required_missing(self, mock_system_info, mock_profile_requirements_gpu):
        """Test validation with CUDA required but not available."""
        # Create system with NVIDIA GPU but no CUDA
        no_cuda_system = mock_system_info
        no_cuda_system.gpu_name = "NVIDIA GeForce RTX 3080"
        no_cuda_system.gpu_vendor = "NVIDIA"
        no_cuda_system.cuda_available = False
        no_cuda_system.metal_available = False
        
        validator = SystemValidator(no_cuda_system)
        result = validator.validate(mock_profile_requirements_gpu)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "CUDA required but not available" in result.blocking_issues[0]
        assert result.gpu_sufficient is False
    
    def test_validate_metal_required_missing(self, mock_system_info):
        """Test validation with Metal required but not available."""
        # Create requirements that need Metal
        metal_requirements = ProfileRequirements(
            ram_gb=4.0,
            disk_gb=10.0,
            cpu_cores=2,
            gpu_required=True,
            metal_required=True
        )
        
        # Create system without Metal
        no_metal_system = mock_system_info
        no_metal_system.gpu_name = "Intel UHD Graphics"
        no_metal_system.gpu_vendor = "Intel"
        no_metal_system.cuda_available = False
        no_metal_system.metal_available = False
        
        validator = SystemValidator(no_metal_system)
        result = validator.validate(metal_requirements)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "Metal Performance Shaders required" in result.blocking_issues[0]
        assert result.gpu_sufficient is False
    
    def test_validate_unsupported_architecture(self, mock_system_info, mock_profile_requirements):
        """Test validation with unsupported architecture."""
        # Create requirements with specific architecture
        arch_requirements = ProfileRequirements(
            ram_gb=4.0,
            disk_gb=10.0,
            cpu_cores=2,
            supported_archs=["x86_64"]
        )
        
        # Create system with different architecture
        arm_system = mock_system_info
        arm_system.arch = "arm64"
        
        validator = SystemValidator(arm_system)
        result = validator.validate(arch_requirements)
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) > 0
        assert "Unsupported architecture" in result.blocking_issues[0]
    
    def test_validate_low_available_ram_warning(self, mock_system_info, mock_profile_requirements):
        """Test validation with low available RAM warning."""
        # Create system with low available RAM
        low_available_ram_system = mock_system_info
        low_available_ram_system.ram_available_gb = 1.0  # Less than 50% of required
        
        validator = SystemValidator(low_available_ram_system)
        result = validator.validate(mock_profile_requirements)
        
        assert result.safe_to_install is True  # Still safe to install
        assert len(result.warnings) > 0
        assert "Low available RAM" in result.warnings[0]
    
    def test_validate_low_disk_space_warning(self, mock_system_info, mock_profile_requirements):
        """Test validation with low disk space warning."""
        # Create system with low disk space after installation
        low_disk_system = mock_system_info
        low_disk_system.disk_total_gb = 100.0  # Small total disk
        low_disk_system.disk_free_gb = 15.0  # Just enough for installation
        
        validator = SystemValidator(low_disk_system)
        result = validator.validate(mock_profile_requirements)
        
        assert result.safe_to_install is True  # Still safe to install
        assert len(result.warnings) > 0
        assert "Low disk space after installation" in result.warnings[0]
    
    def test_validate_multiple_profiles(self, mock_system_info, mock_profile_requirements):
        """Test validation of multiple profiles."""
        validator = SystemValidator(mock_system_info)
        
        # Create multiple requirements
        requirements_list = [
            mock_profile_requirements,
            ProfileRequirements(ram_gb=2.0, disk_gb=5.0, cpu_cores=1),
            ProfileRequirements(ram_gb=1.0, disk_gb=2.0, cpu_cores=1)
        ]
        
        results = validator.validate_multiple_profiles(requirements_list)
        
        assert "profile_0" in results
        assert "profile_1" in results
        assert "profile_2" in results
        assert "combined" in results
        
        # Check combined requirements
        combined_result = results["combined"]
        assert combined_result.estimated_download_mb == 7.0  # 5 + 0 + 2
        assert combined_result.disk_space_after_gb == 883.0  # 900 - 17
    
    def test_get_optimization_suggestions(self, mock_system_info):
        """Test optimization suggestions."""
        validator = SystemValidator(mock_system_info)
        suggestions = validator.get_optimization_suggestions()
        
        # Should have suggestions for package managers and development tools
        assert len(suggestions) > 0
        assert any("package manager" in suggestion.lower() for suggestion in suggestions)
    
    def test_estimate_install_time(self, mock_system_info, mock_profile_requirements):
        """Test installation time estimation."""
        validator = SystemValidator(mock_system_info)
        result = validator.validate(mock_profile_requirements)
        
        assert result.estimated_install_time_minutes > 0
        assert isinstance(result.estimated_install_time_minutes, int)
    
    def test_estimate_install_time_gpu(self, mock_system_info, mock_profile_requirements_gpu):
        """Test installation time estimation with GPU requirements."""
        validator = SystemValidator(mock_system_info)
        result = validator.validate(mock_profile_requirements_gpu)
        
        # GPU requirements should add more time
        assert result.estimated_install_time_minutes > 10
        assert isinstance(result.estimated_install_time_minutes, int)


class TestValidationResult:
    """Test ValidationResult dataclass."""
    
    def test_validation_result_creation(self):
        """Test ValidationResult creation."""
        result = ValidationResult(
            safe_to_install=True,
            blocking_issues=[],
            warnings=["Low RAM"],
            recommendations=["Upgrade RAM"],
            ram_sufficient=True,
            disk_sufficient=True,
            cpu_sufficient=True,
            gpu_sufficient=True,
            estimated_download_mb=100.0,
            estimated_install_time_minutes=10,
            disk_space_after_gb=890.0
        )
        
        assert result.safe_to_install is True
        assert len(result.blocking_issues) == 0
        assert len(result.warnings) == 1
        assert len(result.recommendations) == 1
        assert result.ram_sufficient is True
        assert result.disk_sufficient is True
        assert result.cpu_sufficient is True
        assert result.gpu_sufficient is True
        assert result.estimated_download_mb == 100.0
        assert result.estimated_install_time_minutes == 10
        assert result.disk_space_after_gb == 890.0
    
    def test_validation_result_with_issues(self):
        """Test ValidationResult creation with blocking issues."""
        result = ValidationResult(
            safe_to_install=False,
            blocking_issues=["Insufficient RAM", "No GPU"],
            warnings=[],
            recommendations=[],
            ram_sufficient=False,
            disk_sufficient=True,
            cpu_sufficient=True,
            gpu_sufficient=False,
            estimated_download_mb=0.0,
            estimated_install_time_minutes=0,
            disk_space_after_gb=900.0
        )
        
        assert result.safe_to_install is False
        assert len(result.blocking_issues) == 2
        assert "Insufficient RAM" in result.blocking_issues
        assert "No GPU" in result.blocking_issues
        assert result.ram_sufficient is False
        assert result.gpu_sufficient is False
