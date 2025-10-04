"""
Base Stack System for he2plus
Abstract base class for all development stacks
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from ..core.validator import ResourceRequirements, ValidationResult
from ..core.system_profiler import SystemInfo


@dataclass
class InstallStep:
    """Represents a single installation step"""
    name: str
    description: str
    command: str
    args: List[str]
    timeout: int = 300  # 5 minutes default
    retry_count: int = 3
    required: bool = True
    platform_specific: bool = False
    platforms: List[str] = None  # ['macos', 'linux', 'windows']
    
    def __post_init__(self):
        if self.platforms is None:
            self.platforms = ['macos', 'linux', 'windows']


@dataclass
class VerificationResult:
    """Result of installation verification"""
    success: bool
    message: str
    details: Dict[str, Any]
    next_steps: List[str]


class BaseStack(ABC):
    """
    Abstract base class for all development stacks
    
    Each stack defines:
    - Resource requirements
    - Installation steps
    - Verification process
    - Post-installation guidance
    """
    
    def __init__(self):
        """Initialize the stack"""
        self.name = self.get_name()
        self.description = self.get_description()
        self.requirements = self.get_requirements()
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the stack name"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get the stack description"""
        pass
    
    @abstractmethod
    def get_requirements(self) -> ResourceRequirements:
        """Get resource requirements for this stack"""
        pass
    
    @abstractmethod
    def get_install_steps(self) -> List[InstallStep]:
        """
        Get list of installation steps
        
        Returns:
            List of InstallStep objects in execution order
        """
        pass
    
    @abstractmethod
    def verify_installation(self) -> VerificationResult:
        """
        Verify that the installation was successful
        
        Returns:
            VerificationResult with success status and details
        """
        pass
    
    @abstractmethod
    def get_next_steps(self) -> str:
        """
        Get guidance for what to do after installation
        
        Returns:
            String with next steps and guidance
        """
        pass
    
    def get_workspace_path(self) -> str:
        """
        Get the workspace path for this stack
        
        Returns:
            Path where stack files will be created
        """
        from pathlib import Path
        return str(Path.home() / f"workshop-{self.name}")
    
    def create_workspace(self) -> bool:
        """
        Create workspace directory for this stack
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from pathlib import Path
            workspace_path = Path(self.get_workspace_path())
            workspace_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    def get_sample_files(self) -> Dict[str, str]:
        """
        Get sample files to create in workspace
        
        Returns:
            Dictionary mapping file paths to content
        """
        return {}
    
    def create_sample_files(self) -> bool:
        """
        Create sample files in workspace
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from pathlib import Path
            workspace_path = Path(self.get_workspace_path())
            sample_files = self.get_sample_files()
            
            for file_path, content in sample_files.items():
                full_path = workspace_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
            
            return True
        except Exception:
            return False
    
    def get_dependencies(self) -> List[str]:
        """
        Get list of other stacks this stack depends on
        
        Returns:
            List of stack names that must be installed first
        """
        return []
    
    def is_compatible_with(self, system_info: SystemInfo) -> bool:
        """
        Check if this stack is compatible with the system
        
        Args:
            system_info: System information
            
        Returns:
            True if compatible, False otherwise
        """
        # Basic compatibility check
        if system_info.os_name not in ['macos', 'linux', 'windows']:
            return False
        
        # Check architecture compatibility
        if system_info.architecture not in ['x86_64', 'arm64', 'amd64']:
            return False
        
        return True
    
    def get_installation_summary(self) -> Dict[str, Any]:
        """
        Get summary of what will be installed
        
        Returns:
            Dictionary with installation summary
        """
        steps = self.get_install_steps()
        return {
            'name': self.name,
            'description': self.description,
            'total_steps': len(steps),
            'estimated_time': len(steps) * 2,  # 2 minutes per step
            'requirements': {
                'ram_gb': self.requirements.ram_gb,
                'disk_gb': self.requirements.disk_gb,
                'cpu_cores': self.requirements.cpu_cores,
                'gpu_required': self.requirements.gpu_required
            },
            'steps': [
                {
                    'name': step.name,
                    'description': step.description,
                    'required': step.required
                }
                for step in steps
            ]
        }
    
    def print_installation_summary(self) -> None:
        """Print a formatted installation summary"""
        summary = self.get_installation_summary()
        
        print(f"📦 {summary['name'].upper()} Stack Installation Summary")
        print("=" * 50)
        print(f"Description: {summary['description']}")
        print(f"Total Steps: {summary['total_steps']}")
        print(f"Estimated Time: {summary['estimated_time']} minutes")
        
        print(f"\n💻 Requirements:")
        req = summary['requirements']
        print(f"   RAM: {req['ram_gb']} GB")
        print(f"   Disk: {req['disk_gb']} GB")
        print(f"   CPU: {req['cpu_cores']} cores")
        if req['gpu_required']:
            print(f"   GPU: Required")
        
        print(f"\n📋 Installation Steps:")
        for i, step in enumerate(summary['steps'], 1):
            status = "✓" if step['required'] else "○"
            print(f"   {i}. {status} {step['name']}")
            print(f"      {step['description']}")
        
        print(f"\n📁 Workspace: {self.get_workspace_path()}")


class StackRegistry:
    """Registry for managing available stacks"""
    
    def __init__(self):
        """Initialize the registry"""
        self._stacks: Dict[str, BaseStack] = {}
    
    def register(self, stack: BaseStack) -> None:
        """
        Register a stack
        
        Args:
            stack: Stack instance to register
        """
        self._stacks[stack.name] = stack
    
    def get_stack(self, name: str) -> Optional[BaseStack]:
        """
        Get a stack by name
        
        Args:
            name: Stack name
            
        Returns:
            Stack instance or None if not found
        """
        return self._stacks.get(name)
    
    def list_stacks(self) -> List[str]:
        """
        List all registered stack names
        
        Returns:
            List of stack names
        """
        return list(self._stacks.keys())
    
    def get_compatible_stacks(self, system_info: SystemInfo) -> List[BaseStack]:
        """
        Get stacks compatible with the system
        
        Args:
            system_info: System information
            
        Returns:
            List of compatible stack instances
        """
        compatible = []
        for stack in self._stacks.values():
            if stack.is_compatible_with(system_info):
                compatible.append(stack)
        return compatible
    
    def print_available_stacks(self) -> None:
        """Print all available stacks"""
        print("📦 Available Development Stacks")
        print("=" * 50)
        
        for name, stack in self._stacks.items():
            print(f"\n🔧 {name.upper()}")
            print(f"   Description: {stack.description}")
            print(f"   Requirements: {stack.requirements.ram_gb}GB RAM, {stack.requirements.disk_gb}GB disk")
            print(f"   Workspace: {stack.get_workspace_path()}")


# Global registry instance
stack_registry = StackRegistry()


def register_stack(stack_class: type) -> type:
    """
    Decorator to register a stack class
    
    Args:
        stack_class: Stack class to register
        
    Returns:
        The stack class (for chaining)
    """
    instance = stack_class()
    stack_registry.register(instance)
    return stack_class


if __name__ == "__main__":
    # Test the base stack system
    print("🧪 Testing Base Stack System")
    print("=" * 50)
    
    # Create a test stack
    class TestStack(BaseStack):
        def get_name(self) -> str:
            return "test"
        
        def get_description(self) -> str:
            return "Test stack for development"
        
        def get_requirements(self) -> ResourceRequirements:
            return ResourceRequirements(ram_gb=2.0, disk_gb=5.0)
        
        def get_install_steps(self) -> List[InstallStep]:
            return [
                InstallStep(
                    name="Install Test Tool",
                    description="Install a test tool",
                    command="echo",
                    args=["Test installation"]
                )
            ]
        
        def verify_installation(self) -> VerificationResult:
            return VerificationResult(
                success=True,
                message="Test installation verified",
                details={},
                next_steps=["Run test command"]
            )
        
        def get_next_steps(self) -> str:
            return "Test stack installed successfully!"
    
    # Test the stack
    test_stack = TestStack()
    test_stack.print_installation_summary()
    
    # Test registry
    stack_registry.register(test_stack)
    stack_registry.print_available_stacks()
