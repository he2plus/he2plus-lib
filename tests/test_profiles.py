"""
Tests for he2plus profiles.

This module tests all profile functionality including profile loading,
validation, and component management.
"""

import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from he2plus.profiles.registry import ProfileRegistry
from he2plus.profiles.base import BaseProfile, Component, VerificationStep, SampleProject
from he2plus.profiles.web3.solidity import SolidityProfile
from he2plus.profiles.web.nextjs import NextJSProfile
from he2plus.profiles.mobile.react_native import ReactNativeProfile
from he2plus.profiles.ml.python import PythonMLProfile


class TestSolidityProfile:
    """Test Solidity profile functionality."""
    
    def test_profile_initialization(self):
        """Test SolidityProfile initialization."""
        profile = SolidityProfile()
        
        assert profile.id == "web3-solidity"
        assert profile.name == "Solidity Development"
        assert profile.description == "Ethereum smart contract development with Hardhat and Foundry"
        assert profile.category == "web3"
        assert profile.version == "1.0.0"
    
    def test_requirements(self):
        """Test profile requirements."""
        profile = SolidityProfile()
        requirements = profile.get_requirements()
        
        assert requirements.ram_gb == 4.0
        assert requirements.disk_gb == 10.0
        assert requirements.cpu_cores == 2
        assert requirements.gpu_required is False
        assert requirements.internet_required is True
        assert requirements.download_size_mb == 500.0
        assert "x86_64" in requirements.supported_archs
        assert "arm64" in requirements.supported_archs
    
    def test_components(self):
        """Test profile components."""
        profile = SolidityProfile()
        components = profile.get_components()
        
        assert len(components) > 0
        
        # Check for key components
        component_ids = [comp.id for comp in components]
        assert "language.node.18" in component_ids
        assert "tool.npm" in component_ids
        assert "tool.git" in component_ids
        assert "framework.hardhat" in component_ids
        assert "tool.foundry" in component_ids
        assert "tool.solc" in component_ids
    
    def test_verification_steps(self):
        """Test verification steps."""
        profile = SolidityProfile()
        steps = profile.get_verification_steps()
        
        assert len(steps) > 0
        
        # Check for key verification steps
        step_names = [step.name for step in steps]
        assert "Node.js Version" in step_names
        assert "npm Version" in step_names
        assert "Git Version" in step_names
        assert "Hardhat Installation" in step_names
        assert "Foundry Installation" in step_names
    
    def test_sample_project(self):
        """Test sample project."""
        profile = SolidityProfile()
        sample_project = profile.get_sample_project()
        
        assert sample_project is not None
        assert sample_project.name == "Hardhat Starter Kit"
        assert sample_project.type == "git_clone"
        assert "hardhat-starter-kit" in sample_project.source
    
    def test_next_steps(self):
        """Test next steps."""
        profile = SolidityProfile()
        next_steps = profile.get_next_steps()
        
        assert len(next_steps) > 0
        assert any("Hardhat" in step for step in next_steps)
        assert any("Foundry" in step for step in next_steps)


class TestNextJSProfile:
    """Test Next.js profile functionality."""
    
    def test_profile_initialization(self):
        """Test NextJSProfile initialization."""
        profile = NextJSProfile()
        
        assert profile.id == "web-nextjs"
        assert profile.name == "Next.js Development"
        assert "React framework" in profile.description
        assert profile.category == "web"
        assert profile.version == "1.0.0"
    
    def test_requirements(self):
        """Test profile requirements."""
        profile = NextJSProfile()
        requirements = profile.get_requirements()
        
        assert requirements.ram_gb == 4.0
        assert requirements.disk_gb == 5.0
        assert requirements.cpu_cores == 2
        assert requirements.gpu_required is False
        assert requirements.internet_required is True
        assert requirements.download_size_mb == 200.0
    
    def test_components(self):
        """Test profile components."""
        profile = NextJSProfile()
        components = profile.get_components()
        
        assert len(components) > 0
        
        # Check for key components
        component_ids = [comp.id for comp in components]
        assert "language.node.18" in component_ids
        assert "tool.npm" in component_ids
        assert "tool.yarn" in component_ids
        assert "tool.pnpm" in component_ids
        assert "tool.git" in component_ids
        assert "framework.nextjs" in component_ids
        assert "library.react" in component_ids
        assert "language.typescript" in component_ids
        assert "library.tailwindcss" in component_ids
    
    def test_verification_steps(self):
        """Test verification steps."""
        profile = NextJSProfile()
        steps = profile.get_verification_steps()
        
        assert len(steps) > 0
        
        # Check for key verification steps
        step_names = [step.name for step in steps]
        assert "Node.js Version" in step_names
        assert "npm Version" in step_names
        assert "Next.js CLI" in step_names
        assert "TypeScript" in step_names
        assert "Tailwind CSS" in step_names
    
    def test_sample_project(self):
        """Test sample project."""
        profile = NextJSProfile()
        sample_project = profile.get_sample_project()
        
        assert sample_project is not None
        assert sample_project.name == "Next.js Starter Kit"
        assert sample_project.type == "create_app"
        assert "create-next-app" in sample_project.source
    
    def test_installation_plan(self):
        """Test installation plan."""
        profile = NextJSProfile()
        plan = profile.get_installation_plan()
        
        assert plan is not None
        assert "profile" in plan
        assert "requirements" in plan
        assert "components" in plan
        assert "verification" in plan
        assert "sample_project" in plan
        assert "next_steps" in plan
        assert "web_specific" in plan
        
        assert plan["profile"]["id"] == "web-nextjs"
        assert plan["requirements"]["ram_gb"] == 4.0
        assert len(plan["components"]) > 0


class TestReactNativeProfile:
    """Test React Native profile functionality."""
    
    def test_profile_initialization(self):
        """Test ReactNativeProfile initialization."""
        profile = ReactNativeProfile()
        
        assert profile.id == "mobile-react-native"
        assert profile.name == "React Native Development"
        assert "Cross-platform mobile" in profile.description
        assert profile.category == "mobile"
        assert profile.version == "1.0.0"
    
    def test_requirements(self):
        """Test profile requirements."""
        profile = ReactNativeProfile()
        requirements = profile.get_requirements()
        
        assert requirements.ram_gb == 8.0
        assert requirements.disk_gb == 15.0
        assert requirements.cpu_cores == 4
        assert requirements.gpu_required is False
        assert requirements.internet_required is True
        assert requirements.download_size_mb == 2000.0
    
    def test_components(self):
        """Test profile components."""
        profile = ReactNativeProfile()
        components = profile.get_components()
        
        assert len(components) > 0
        
        # Check for key components
        component_ids = [comp.id for comp in components]
        assert "language.node.18" in component_ids
        assert "tool.npm" in component_ids
        assert "tool.yarn" in component_ids
        assert "tool.git" in component_ids
        assert "tool.react-native-cli" in component_ids
        assert "tool.expo-cli" in component_ids
        assert "language.typescript" in component_ids
        assert "framework.react-native" in component_ids
        assert "library.react" in component_ids
    
    def test_verification_steps(self):
        """Test verification steps."""
        profile = ReactNativeProfile()
        steps = profile.get_verification_steps()
        
        assert len(steps) > 0
        
        # Check for key verification steps
        step_names = [step.name for step in steps]
        assert "Node.js Version" in step_names
        assert "npm Version" in step_names
        assert "React Native CLI" in step_names
        assert "TypeScript" in step_names
    
    def test_sample_project(self):
        """Test sample project."""
        profile = ReactNativeProfile()
        sample_project = profile.get_sample_project()
        
        assert sample_project is not None
        assert sample_project.name == "React Native Starter App"
        assert sample_project.type == "create_app"
        assert "react-native" in sample_project.source
    
    def test_development_workflow(self):
        """Test development workflow."""
        profile = ReactNativeProfile()
        workflow = profile.get_development_workflow()
        
        assert len(workflow) > 0
        assert any("react-native" in step for step in workflow)
        assert any("typescript" in step.lower() for step in workflow)
    
    def test_troubleshooting_guide(self):
        """Test troubleshooting guide."""
        profile = ReactNativeProfile()
        guide = profile.get_troubleshooting_guide()
        
        assert "Installation Issues" in guide
        assert "Development Issues" in guide
        assert "Build Issues" in guide
        assert "Performance Issues" in guide
        
        assert len(guide["Installation Issues"]) > 0
        assert len(guide["Development Issues"]) > 0


class TestPythonMLProfile:
    """Test Python ML profile functionality."""
    
    def test_profile_initialization(self):
        """Test PythonMLProfile initialization."""
        profile = PythonMLProfile()
        
        assert profile.id == "ml-python"
        assert profile.name == "Python Machine Learning"
        assert "TensorFlow" in profile.description
        assert profile.category == "ml"
        assert profile.version == "1.0.0"
    
    def test_requirements(self):
        """Test profile requirements."""
        profile = PythonMLProfile()
        requirements = profile.get_requirements()
        
        assert requirements.ram_gb == 8.0
        assert requirements.disk_gb == 20.0
        assert requirements.cpu_cores == 4
        assert requirements.gpu_required is True
        assert requirements.gpu_vendor == "NVIDIA"
        assert requirements.cuda_required is True
        assert requirements.internet_required is True
        assert requirements.download_size_mb == 3000.0
    
    def test_components(self):
        """Test profile components."""
        profile = PythonMLProfile()
        components = profile.get_components()
        
        assert len(components) > 0
        
        # Check for key components
        component_ids = [comp.id for comp in components]
        assert "language.python.3.11" in component_ids
        assert "tool.pip" in component_ids
        assert "tool.conda" in component_ids
        assert "tool.mamba" in component_ids
        assert "tool.poetry" in component_ids
        assert "tool.git" in component_ids
        assert "tool.jupyter" in component_ids
        assert "library.tensorflow" in component_ids
        assert "library.pytorch" in component_ids
        assert "library.scikit-learn" in component_ids
        assert "library.pandas" in component_ids
        assert "library.numpy" in component_ids
    
    def test_verification_steps(self):
        """Test verification steps."""
        profile = PythonMLProfile()
        steps = profile.get_verification_steps()
        
        assert len(steps) > 0
        
        # Check for key verification steps
        step_names = [step.name for step in steps]
        assert "Python Version" in step_names
        assert "pip Version" in step_names
        assert "Jupyter Lab" in step_names
        assert "TensorFlow" in step_names
        assert "PyTorch" in step_names
        assert "CUDA Support" in step_names
    
    def test_sample_project(self):
        """Test sample project."""
        profile = PythonMLProfile()
        sample_project = profile.get_sample_project()
        
        assert sample_project is not None
        assert sample_project.name == "ML Starter Project"
        assert sample_project.type == "create_app"
        assert "ml-starter-kit" in sample_project.source
    
    def test_development_workflow(self):
        """Test development workflow."""
        profile = PythonMLProfile()
        workflow = profile.get_development_workflow()
        
        assert len(workflow) > 0
        assert any("python" in step for step in workflow)
        assert any("jupyter" in step for step in workflow)
        assert any("tensorflow" in step.lower() for step in workflow)
    
    def test_recommended_extensions(self):
        """Test recommended VS Code extensions."""
        profile = PythonMLProfile()
        extensions = profile.get_recommended_extensions()
        
        assert len(extensions) > 0
        assert "ms-python.python" in extensions
        assert "ms-toolsai.jupyter" in extensions
        assert "ms-python.vscode-pylance" in extensions
    
    def test_useful_commands(self):
        """Test useful commands."""
        profile = PythonMLProfile()
        commands = profile.get_useful_commands()
        
        assert "Environment Management" in commands
        assert "Jupyter Commands" in commands
        assert "Data Science" in commands
        assert "Model Training" in commands
        assert "Testing and Quality" in commands
        assert "Deployment" in commands
        
        assert len(commands["Environment Management"]) > 0
        assert len(commands["Jupyter Commands"]) > 0


class TestProfileRegistry:
    """Test profile registry with all profiles."""
    
    def test_all_profiles_loaded(self):
        """Test that all profiles are loaded correctly."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        # Check that all expected profiles are loaded
        profile_ids = list(registry._profiles.keys())
        
        assert "web3-solidity" in profile_ids
        assert "web-nextjs" in profile_ids
        assert "mobile-react-native" in profile_ids
        assert "ml-python" in profile_ids
    
    def test_profile_categories(self):
        """Test profile categories."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        categories = registry.get_categories()
        
        assert "web3" in categories
        assert "web" in categories
        assert "mobile" in categories
        assert "ml" in categories
    
    def test_profile_search(self):
        """Test profile search functionality."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        # Test searching for React profiles
        react_results = registry.search("react")
        assert len(react_results) > 0
        
        # Test searching for Python profiles
        python_results = registry.search("python")
        assert len(python_results) > 0
        
        # Test searching for web3 profiles
        web3_results = registry.search("solidity")
        assert len(web3_results) > 0
    
    def test_profile_validation(self):
        """Test profile validation."""
        registry = ProfileRegistry()
        registry.load_profiles()
        
        # Test that all profiles are valid
        for profile_id, profile in registry._profiles.items():
            assert profile.id == profile_id
            assert profile.name is not None
            assert profile.description is not None
            assert profile.category is not None
            assert len(profile.get_components()) > 0
            assert len(profile.get_verification_steps()) > 0


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
