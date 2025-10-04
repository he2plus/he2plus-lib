"""
Resource validation and requirement checking for he2plus.

This module validates system resources against profile requirements
and provides clear feedback on what's needed.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import structlog

from .system import SystemInfo

logger = structlog.get_logger(__name__)


@dataclass
class ProfileRequirements:
    """Requirements for a development profile."""
    
    # Resource requirements
    ram_gb: float = 4.0
    disk_gb: float = 10.0
    cpu_cores: int = 2
    
    # Optional requirements
    gpu_required: bool = False
    gpu_vendor: Optional[str] = None  # "NVIDIA", "AMD", "Apple", "Intel"
    cuda_required: bool = False
    metal_required: bool = False
    
    # Platform requirements
    min_os_version: Optional[str] = None
    supported_archs: List[str] = None
    
    # Network requirements
    internet_required: bool = True
    download_size_mb: float = 0.0
    
    def __post_init__(self):
        if self.supported_archs is None:
            self.supported_archs = ["x86_64", "arm64", "arm"]


@dataclass
class ValidationResult:
    """Result of system validation against profile requirements."""
    
    safe_to_install: bool
    blocking_issues: List[str]
    warnings: List[str]
    recommendations: List[str]
    
    # Resource analysis
    ram_sufficient: bool
    disk_sufficient: bool
    cpu_sufficient: bool
    gpu_sufficient: bool
    
    # Estimated impact
    estimated_download_mb: float
    estimated_install_time_minutes: int
    disk_space_after_gb: float


class SystemValidator:
    """Validates system resources against profile requirements."""
    
    def __init__(self, system_info: SystemInfo):
        self.system = system_info
        self.logger = logger.bind(component="system_validator")
    
    def validate(self, requirements: ProfileRequirements) -> ValidationResult:
        """Validate system against profile requirements."""
        self.logger.info("Validating system against requirements", 
                        ram_gb=requirements.ram_gb, 
                        disk_gb=requirements.disk_gb)
        
        blocking_issues = []
        warnings = []
        recommendations = []
        
        # Check RAM
        ram_sufficient = self._check_ram(requirements, blocking_issues, warnings)
        
        # Check disk space
        disk_sufficient = self._check_disk(requirements, blocking_issues, warnings)
        
        # Check CPU
        cpu_sufficient = self._check_cpu(requirements, blocking_issues, warnings)
        
        # Check GPU
        gpu_sufficient = self._check_gpu(requirements, blocking_issues, warnings)
        
        # Check platform compatibility
        self._check_platform(requirements, blocking_issues, warnings)
        
        # Generate recommendations
        self._generate_recommendations(requirements, recommendations)
        
        # Calculate estimates
        estimated_download_mb = requirements.download_size_mb
        estimated_install_time = self._estimate_install_time(requirements)
        disk_space_after = self.system.disk_free_gb - requirements.disk_gb
        
        safe_to_install = (
            ram_sufficient and 
            disk_sufficient and 
            cpu_sufficient and 
            gpu_sufficient and
            len(blocking_issues) == 0
        )
        
        result = ValidationResult(
            safe_to_install=safe_to_install,
            blocking_issues=blocking_issues,
            warnings=warnings,
            recommendations=recommendations,
            ram_sufficient=ram_sufficient,
            disk_sufficient=disk_sufficient,
            cpu_sufficient=cpu_sufficient,
            gpu_sufficient=gpu_sufficient,
            estimated_download_mb=estimated_download_mb,
            estimated_install_time_minutes=estimated_install_time,
            disk_space_after_gb=disk_space_after
        )
        
        self.logger.info("Validation completed", 
                        safe_to_install=safe_to_install,
                        blocking_issues=len(blocking_issues),
                        warnings=len(warnings))
        
        return result
    
    def _check_ram(self, requirements: ProfileRequirements, 
                   blocking_issues: List[str], warnings: List[str]) -> bool:
        """Check RAM requirements."""
        if self.system.ram_total_gb < requirements.ram_gb:
            blocking_issues.append(
                f"Insufficient RAM: {self.system.ram_total_gb}GB available, "
                f"{requirements.ram_gb}GB required"
            )
            return False
        
        if self.system.ram_available_gb < requirements.ram_gb * 0.5:
            warnings.append(
                f"Low available RAM: {self.system.ram_available_gb}GB available, "
                f"consider closing other applications"
            )
        
        return True
    
    def _check_disk(self, requirements: ProfileRequirements,
                    blocking_issues: List[str], warnings: List[str]) -> bool:
        """Check disk space requirements."""
        if self.system.disk_free_gb < requirements.disk_gb:
            blocking_issues.append(
                f"Insufficient disk space: {self.system.disk_free_gb}GB available, "
                f"{requirements.disk_gb}GB required"
            )
            return False
        
        # Warn if less than 20% free space after installation
        space_after = self.system.disk_free_gb - requirements.disk_gb
        if space_after < self.system.disk_total_gb * 0.2:
            warnings.append(
                f"Low disk space after installation: {space_after:.1f}GB will remain "
                f"({(space_after/self.system.disk_total_gb)*100:.1f}% of total disk)"
            )
        
        return True
    
    def _check_cpu(self, requirements: ProfileRequirements,
                   blocking_issues: List[str], warnings: List[str]) -> bool:
        """Check CPU requirements."""
        if self.system.cpu_cores < requirements.cpu_cores:
            blocking_issues.append(
                f"Insufficient CPU cores: {self.system.cpu_cores} available, "
                f"{requirements.cpu_cores} required"
            )
            return False
        
        return True
    
    def _check_gpu(self, requirements: ProfileRequirements,
                   blocking_issues: List[str], warnings: List[str]) -> bool:
        """Check GPU requirements."""
        if not requirements.gpu_required:
            return True
        
        if not self.system.gpu_name:
            blocking_issues.append("GPU required but not detected")
            return False
        
        # Check specific GPU vendor requirements
        if requirements.gpu_vendor:
            if self.system.gpu_vendor != requirements.gpu_vendor:
                blocking_issues.append(
                    f"Wrong GPU vendor: {self.system.gpu_vendor} detected, "
                    f"{requirements.gpu_vendor} required"
                )
                return False
        
        # Check CUDA requirements
        if requirements.cuda_required and not self.system.cuda_available:
            blocking_issues.append("CUDA required but not available")
            return False
        
        # Check Metal requirements
        if requirements.metal_required and not self.system.metal_available:
            blocking_issues.append("Metal Performance Shaders required but not available")
            return False
        
        return True
    
    def _check_platform(self, requirements: ProfileRequirements,
                        blocking_issues: List[str], warnings: List[str]) -> None:
        """Check platform compatibility."""
        # Check architecture support
        if requirements.supported_archs:
            if self.system.arch not in requirements.supported_archs:
                blocking_issues.append(
                    f"Unsupported architecture: {self.system.arch}, "
                    f"supported: {', '.join(requirements.supported_archs)}"
                )
        
        # Check OS version (basic check)
        if requirements.min_os_version:
            # This is a simplified check - in practice, you'd want more sophisticated version comparison
            if self.system.os_name == "macOS":
                try:
                    current_version = tuple(map(int, self.system.os_version.split('.')))
                    min_version = tuple(map(int, requirements.min_os_version.split('.')))
                    if current_version < min_version:
                        blocking_issues.append(
                            f"OS version too old: {self.system.os_version}, "
                            f"minimum: {requirements.min_os_version}"
                        )
                except (ValueError, AttributeError):
                    warnings.append("Could not parse OS version for comparison")
    
    def _generate_recommendations(self, requirements: ProfileRequirements,
                                 recommendations: List[str]) -> None:
        """Generate recommendations for optimal setup."""
        
        # RAM recommendations
        if self.system.ram_total_gb < requirements.ram_gb * 1.5:
            recommendations.append(
                f"Consider upgrading to {requirements.ram_gb * 2}GB RAM for better performance"
            )
        
        # Disk recommendations
        if self.system.disk_free_gb < requirements.disk_gb * 2:
            recommendations.append(
                "Consider freeing up disk space or using external storage"
            )
        
        # GPU recommendations
        if requirements.gpu_required and not self.system.gpu_name:
            recommendations.append("Consider adding a dedicated GPU for better performance")
        
        # Package manager recommendations
        if not self.system.package_managers:
            recommendations.append("Install a package manager (brew, apt, choco) for easier setup")
        
        # Network recommendations
        if requirements.internet_required and requirements.download_size_mb > 1000:
            recommendations.append("Ensure stable internet connection for large downloads")
    
    def _estimate_install_time(self, requirements: ProfileRequirements) -> int:
        """Estimate installation time in minutes."""
        base_time = 5  # Base time for any installation
        
        # Add time based on download size
        if requirements.download_size_mb > 0:
            # Assume 10 MB/s download speed
            download_time = requirements.download_size_mb / 10 / 60
            base_time += download_time
        
        # Add time based on disk space (compilation, extraction)
        if requirements.disk_gb > 5:
            base_time += requirements.disk_gb * 0.5
        
        # Add time for GPU drivers if needed
        if requirements.cuda_required or requirements.metal_required:
            base_time += 10
        
        return int(base_time)
    
    def validate_multiple_profiles(self, requirements_list: List[ProfileRequirements]) -> Dict[str, ValidationResult]:
        """Validate system against multiple profiles."""
        results = {}
        
        total_ram = sum(req.ram_gb for req in requirements_list)
        total_disk = sum(req.disk_gb for req in requirements_list)
        total_download = sum(req.download_size_mb for req in requirements_list)
        
        # Create combined requirements
        combined_requirements = ProfileRequirements(
            ram_gb=total_ram,
            disk_gb=total_disk,
            download_size_mb=total_download,
            gpu_required=any(req.gpu_required for req in requirements_list),
            cuda_required=any(req.cuda_required for req in requirements_list),
            metal_required=any(req.metal_required for req in requirements_list)
        )
        
        # Validate each profile individually
        for i, requirements in enumerate(requirements_list):
            result = self.validate(requirements)
            results[f"profile_{i}"] = result
        
        # Validate combined requirements
        combined_result = self.validate(combined_requirements)
        results["combined"] = combined_result
        
        return results
    
    def get_optimization_suggestions(self) -> List[str]:
        """Get suggestions for optimizing the system for development."""
        suggestions = []
        
        # RAM optimization
        if self.system.ram_total_gb < 8:
            suggestions.append("Consider upgrading to 16GB+ RAM for better development experience")
        
        # Storage optimization
        if self.system.disk_free_gb < 50:
            suggestions.append("Free up disk space or add external storage for development projects")
        
        # Package manager optimization
        if not self.system.package_managers:
            if self.system.os_name == "macOS":
                suggestions.append("Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            elif self.system.os_name == "Linux":
                suggestions.append("Install a package manager (apt, yum, dnf, or pacman)")
            elif self.system.os_name == "Windows":
                suggestions.append("Install Chocolatey or winget for easier package management")
        
        # Development tools
        if "git" not in self.system.languages:
            suggestions.append("Install Git for version control")
        
        if "python" not in self.system.languages:
            suggestions.append("Install Python 3.8+ for development")
        
        return suggestions