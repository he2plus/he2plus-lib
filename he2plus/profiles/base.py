"""
Base profile system for he2plus.

This module defines the base classes and interfaces for all development profiles.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import structlog

from ..core.validator import ProfileRequirements

logger = structlog.get_logger(__name__)


@dataclass
class Component:
    """Represents a component that can be installed."""
    
    id: str
    name: str
    description: str
    category: str  # "language", "tool", "framework", "package"
    
    # Installation info
    version: Optional[str] = None
    download_size_mb: float = 0.0
    install_time_minutes: int = 5
    
    # Dependencies
    depends_on: List[str] = field(default_factory=list)
    conflicts_with: List[str] = field(default_factory=list)
    
    # Platform support
    supported_platforms: List[str] = field(default_factory=lambda: ["macos", "linux", "windows"])
    supported_archs: List[str] = field(default_factory=lambda: ["x86_64", "arm64", "arm"])
    
    # Installation methods
    install_methods: List[str] = field(default_factory=list)  # ["brew", "apt", "pip", "npm", etc.]
    
    # Verification
    verify_command: Optional[str] = None
    verify_expected_output: Optional[str] = None
    
    def __post_init__(self):
        if not self.install_methods:
            # Default installation methods based on category
            if self.category == "language":
                self.install_methods = ["official", "package_manager"]
            elif self.category == "tool":
                self.install_methods = ["package_manager", "official"]
            elif self.category == "framework":
                self.install_methods = ["package_manager", "pip", "npm"]
            elif self.category == "package":
                self.install_methods = ["pip", "npm", "cargo"]


@dataclass
class VerificationStep:
    """A step to verify installation."""
    
    name: str
    command: str
    expected_output: Optional[str] = None
    contains_text: Optional[str] = None
    timeout_seconds: int = 30
    
    def verify(self, output: str) -> bool:
        """Verify the command output."""
        if self.expected_output:
            return self.expected_output in output
        elif self.contains_text:
            return self.contains_text in output
        return True


@dataclass
class SampleProject:
    """A sample project to create after installation."""
    
    name: str
    description: str
    type: str  # "git_clone", "template", "scaffold"
    source: str  # URL or template name
    directory: str
    setup_commands: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)


class BaseProfile(ABC):
    """Base class for all development profiles."""
    
    def __init__(self):
        # Profile metadata
        self.id = ""
        self.name = ""
        self.description = ""
        self.category = ""
        self.version = "1.0.0"
        
        # Requirements
        self.requirements = ProfileRequirements()
        
        # Components
        self.components = []
        
        # Verification
        self.verification_steps = []
        
        # Sample project
        self.sample_project = None
        
        # Next steps
        self.next_steps = []
        
        self.logger = logger.bind(profile=self.id)
        self._initialize_profile()
    
    @abstractmethod
    def _initialize_profile(self) -> None:
        """Initialize the profile with components and requirements."""
        pass
    
    def get_components(self) -> List[Component]:
        """Get all components for this profile."""
        return self.components
    
    def get_component_ids(self) -> List[str]:
        """Get component IDs for dependency resolution."""
        return [comp.id for comp in self.components]
    
    def get_requirements(self) -> ProfileRequirements:
        """Get profile requirements."""
        return self.requirements
    
    def get_verification_steps(self) -> List[VerificationStep]:
        """Get verification steps."""
        return self.verification_steps
    
    def get_sample_project(self) -> Optional[SampleProject]:
        """Get sample project."""
        return self.sample_project
    
    def get_next_steps(self) -> List[str]:
        """Get next steps after installation."""
        return self.next_steps
    
    def get_estimated_download_size(self) -> float:
        """Get estimated download size in MB."""
        return sum(comp.download_size_mb for comp in self.components)
    
    def get_estimated_install_time(self) -> int:
        """Get estimated installation time in minutes."""
        return sum(comp.install_time_minutes for comp in self.components)
    
    def get_component_by_id(self, component_id: str) -> Optional[Component]:
        """Get a component by its ID."""
        for comp in self.components:
            if comp.id == component_id:
                return comp
        return None
    
    def get_dependencies(self) -> List[str]:
        """Get all dependencies for this profile."""
        deps = set()
        for comp in self.components:
            deps.update(comp.depends_on)
        return list(deps)
    
    def get_conflicts(self) -> List[str]:
        """Get all conflicts for this profile."""
        conflicts = set()
        for comp in self.components:
            conflicts.update(comp.conflicts_with)
        return list(conflicts)
    
    def is_compatible_with(self, other_profile: 'BaseProfile') -> bool:
        """Check if this profile is compatible with another."""
        our_conflicts = set(self.get_conflicts())
        their_components = set(other_profile.get_component_ids())
        
        # Check if any of our conflicts are in their components
        if our_conflicts.intersection(their_components):
            return False
        
        their_conflicts = set(other_profile.get_conflicts())
        our_components = set(self.get_component_ids())
        
        # Check if any of their conflicts are in our components
        if their_conflicts.intersection(our_components):
            return False
        
        return True
    
    def get_installation_plan(self) -> Dict[str, Any]:
        """Get a detailed installation plan."""
        return {
            "profile": {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "category": self.category,
                "version": self.version
            },
            "requirements": {
                "ram_gb": self.requirements.ram_gb,
                "disk_gb": self.requirements.disk_gb,
                "cpu_cores": self.requirements.cpu_cores,
                "gpu_required": self.requirements.gpu_required,
                "download_size_mb": self.get_estimated_download_size()
            },
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "description": comp.description,
                    "category": comp.category,
                    "version": comp.version,
                    "download_size_mb": comp.download_size_mb,
                    "install_time_minutes": comp.install_time_minutes,
                    "depends_on": comp.depends_on,
                    "install_methods": comp.install_methods
                }
                for comp in self.components
            ],
            "verification": [
                {
                    "name": step.name,
                    "command": step.command,
                    "expected_output": step.expected_output,
                    "contains_text": step.contains_text
                }
                for step in self.verification_steps
            ],
            "sample_project": {
                "name": self.sample_project.name,
                "description": self.sample_project.description,
                "type": self.sample_project.type,
                "source": self.sample_project.source,
                "directory": self.sample_project.directory
            } if self.sample_project else None,
            "next_steps": self.next_steps,
            "estimated_total_time_minutes": self.get_estimated_install_time()
        }
    
    def validate_components(self) -> List[str]:
        """Validate that all components are properly configured."""
        issues = []
        
        if not self.id:
            issues.append("Profile ID is required")
        
        if not self.name:
            issues.append("Profile name is required")
        
        if not self.description:
            issues.append("Profile description is required")
        
        if not self.components:
            issues.append("Profile must have at least one component")
        
        # Validate components
        component_ids = set()
        for comp in self.components:
            if not comp.id:
                issues.append("Component ID is required")
            elif comp.id in component_ids:
                issues.append(f"Duplicate component ID: {comp.id}")
            else:
                component_ids.add(comp.id)
            
            if not comp.name:
                issues.append(f"Component {comp.id} name is required")
            
            if not comp.description:
                issues.append(f"Component {comp.id} description is required")
        
        # Check dependencies
        for comp in self.components:
            for dep in comp.depends_on:
                if dep not in component_ids:
                    issues.append(f"Component {comp.id} depends on unknown component: {dep}")
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "requirements": {
                "ram_gb": self.requirements.ram_gb,
                "disk_gb": self.requirements.disk_gb,
                "cpu_cores": self.requirements.cpu_cores,
                "gpu_required": self.requirements.gpu_required,
                "gpu_vendor": self.requirements.gpu_vendor,
                "cuda_required": self.requirements.cuda_required,
                "metal_required": self.requirements.metal_required,
                "min_os_version": self.requirements.min_os_version,
                "supported_archs": self.requirements.supported_archs,
                "internet_required": self.requirements.internet_required,
                "download_size_mb": self.requirements.download_size_mb
            },
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "description": comp.description,
                    "category": comp.category,
                    "version": comp.version,
                    "download_size_mb": comp.download_size_mb,
                    "install_time_minutes": comp.install_time_minutes,
                    "depends_on": comp.depends_on,
                    "conflicts_with": comp.conflicts_with,
                    "supported_platforms": comp.supported_platforms,
                    "supported_archs": comp.supported_archs,
                    "install_methods": comp.install_methods,
                    "verify_command": comp.verify_command,
                    "verify_expected_output": comp.verify_expected_output
                }
                for comp in self.components
            ],
            "verification_steps": [
                {
                    "name": step.name,
                    "command": step.command,
                    "expected_output": step.expected_output,
                    "contains_text": step.contains_text,
                    "timeout_seconds": step.timeout_seconds
                }
                for step in self.verification_steps
            ],
            "sample_project": {
                "name": self.sample_project.name,
                "description": self.sample_project.description,
                "type": self.sample_project.type,
                "source": self.sample_project.source,
                "directory": self.sample_project.directory,
                "setup_commands": self.sample_project.setup_commands,
                "next_steps": self.sample_project.next_steps
            } if self.sample_project else None,
            "next_steps": self.next_steps
        }
    
    def __str__(self) -> str:
        return f"{self.name} ({self.id})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self.id}', name='{self.name}')>"
