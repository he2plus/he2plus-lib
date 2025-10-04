"""Unit tests for profile system."""

import pytest

from he2plus.profiles.base import BaseProfile, Component, VerificationStep, SampleProject, ProfileRequirements
from he2plus.profiles.web3.solidity import SolidityProfile


class TestComponent:
    """Test Component dataclass."""
    
    def test_component_creation(self):
        """Test Component creation."""
        component = Component(
            id="test.component",
            name="Test Component",
            description="A test component",
            category="tool",
            version="1.0.0",
            download_size_mb=10.0,
            install_time_minutes=5,
            depends_on=["other.component"],
            conflicts_with=["conflicting.component"],
            supported_platforms=["macos", "linux"],
            supported_archs=["x86_64", "arm64"],
            install_methods=["brew", "apt"],
            verify_command="test --version",
            verify_expected_output="1.0.0"
        )
        
        assert component.id == "test.component"
        assert component.name == "Test Component"
        assert component.description == "A test component"
        assert component.category == "tool"
        assert component.version == "1.0.0"
        assert component.download_size_mb == 10.0
        assert component.install_time_minutes == 5
        assert component.depends_on == ["other.component"]
        assert component.conflicts_with == ["conflicting.component"]
        assert component.supported_platforms == ["macos", "linux"]
        assert component.supported_archs == ["x86_64", "arm64"]
        assert component.install_methods == ["brew", "apt"]
        assert component.verify_command == "test --version"
        assert component.verify_expected_output == "1.0.0"
    
    def test_component_default_install_methods(self):
        """Test Component with default install methods based on category."""
        # Language component
        lang_component = Component(
            id="lang.python",
            name="Python",
            description="Python language",
            category="language"
        )
        assert "official" in lang_component.install_methods
        assert "package_manager" in lang_component.install_methods
        
        # Tool component
        tool_component = Component(
            id="tool.git",
            name="Git",
            description="Git version control",
            category="tool"
        )
        assert "package_manager" in tool_component.install_methods
        assert "official" in tool_component.install_methods
        
        # Framework component
        framework_component = Component(
            id="framework.hardhat",
            name="Hardhat",
            description="Hardhat framework",
            category="framework"
        )
        assert "package_manager" in framework_component.install_methods
        assert "pip" in framework_component.install_methods
        assert "npm" in framework_component.install_methods
        
        # Package component
        package_component = Component(
            id="package.ethers",
            name="ethers.js",
            description="ethers.js package",
            category="package"
        )
        assert "pip" in package_component.install_methods
        assert "npm" in package_component.install_methods
        assert "cargo" in package_component.install_methods


class TestVerificationStep:
    """Test VerificationStep dataclass."""
    
    def test_verification_step_creation(self):
        """Test VerificationStep creation."""
        step = VerificationStep(
            name="Test Verification",
            command="test --version",
            expected_output="1.0.0",
            contains_text="1.0",
            timeout_seconds=30
        )
        
        assert step.name == "Test Verification"
        assert step.command == "test --version"
        assert step.expected_output == "1.0.0"
        assert step.contains_text == "1.0"
        assert step.timeout_seconds == 30
    
    def test_verification_step_verify_expected_output(self):
        """Test VerificationStep verification with expected output."""
        step = VerificationStep(
            name="Test Verification",
            command="test --version",
            expected_output="1.0.0"
        )
        
        assert step.verify("1.0.0") is True
        assert step.verify("1.0.1") is False
        assert step.verify("2.0.0") is False
    
    def test_verification_step_verify_contains_text(self):
        """Test VerificationStep verification with contains text."""
        step = VerificationStep(
            name="Test Verification",
            command="test --version",
            contains_text="1.0"
        )
        
        assert step.verify("1.0.0") is True
        assert step.verify("1.0.1") is True
        assert step.verify("2.0.0") is False
    
    def test_verification_step_verify_default(self):
        """Test VerificationStep verification with no specific output."""
        step = VerificationStep(
            name="Test Verification",
            command="test --version"
        )
        
        # Should always return True when no specific output is expected
        assert step.verify("any output") is True
        assert step.verify("") is True


class TestSampleProject:
    """Test SampleProject dataclass."""
    
    def test_sample_project_creation(self):
        """Test SampleProject creation."""
        project = SampleProject(
            name="Test Project",
            description="A test project",
            type="git_clone",
            source="https://github.com/test/test-project.git",
            directory="~/test-project",
            setup_commands=["cd ~/test-project", "npm install"],
            next_steps=["Run tests", "Deploy"]
        )
        
        assert project.name == "Test Project"
        assert project.description == "A test project"
        assert project.type == "git_clone"
        assert project.source == "https://github.com/test/test-project.git"
        assert project.directory == "~/test-project"
        assert project.setup_commands == ["cd ~/test-project", "npm install"]
        assert project.next_steps == ["Run tests", "Deploy"]


class TestBaseProfile:
    """Test BaseProfile abstract class."""
    
    def test_base_profile_creation(self):
        """Test BaseProfile creation."""
        # Create a concrete implementation for testing
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
        assert profile.version == "1.0.0"
        assert isinstance(profile.requirements, ProfileRequirements)
        assert profile.components == []
        assert profile.verification_steps == []
        assert profile.sample_project is None
        assert profile.next_steps == []
    
    def test_base_profile_with_components(self):
        """Test BaseProfile with components."""
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
                
                # Add components
                self.components = [
                    Component(
                        id="test.component1",
                        name="Component 1",
                        description="First component",
                        category="tool"
                    ),
                    Component(
                        id="test.component2",
                        name="Component 2",
                        description="Second component",
                        category="package"
                    )
                ]
        
        profile = TestProfile()
        
        assert len(profile.get_components()) == 2
        assert profile.get_component_ids() == ["test.component1", "test.component2"]
        
        # Test getting component by ID
        component1 = profile.get_component_by_id("test.component1")
        assert component1 is not None
        assert component1.name == "Component 1"
        
        component3 = profile.get_component_by_id("test.component3")
        assert component3 is None
    
    def test_base_profile_dependencies(self):
        """Test BaseProfile dependency management."""
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
                
                # Add components with dependencies
                self.components = [
                    Component(
                        id="test.component1",
                        name="Component 1",
                        description="First component",
                        category="tool",
                        depends_on=["test.component2"]
                    ),
                    Component(
                        id="test.component2",
                        name="Component 2",
                        description="Second component",
                        category="package",
                        conflicts_with=["test.component3"]
                    ),
                    Component(
                        id="test.component3",
                        name="Component 3",
                        description="Third component",
                        category="tool"
                    )
                ]
        
        profile = TestProfile()
        
        dependencies = profile.get_dependencies()
        assert "test.component2" in dependencies
        
        conflicts = profile.get_conflicts()
        assert "test.component3" in conflicts
    
    def test_base_profile_compatibility(self):
        """Test BaseProfile compatibility checking."""
        class TestProfile1(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile-1"
                self.name = "Test Profile 1"
                self.description = "A test profile"
                self.category = "test"
                
                self.components = [
                    Component(
                        id="test.component1",
                        name="Component 1",
                        description="First component",
                        category="tool"
                    )
                ]
        
        class TestProfile2(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile-2"
                self.name = "Test Profile 2"
                self.description = "A test profile"
                self.category = "test"
                
                self.components = [
                    Component(
                        id="test.component2",
                        name="Component 2",
                        description="Second component",
                        category="package"
                    )
                ]
        
        class TestProfile3(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile-3"
                self.name = "Test Profile 3"
                self.description = "A test profile"
                self.category = "test"
                
                self.components = [
                    Component(
                        id="test.component1",
                        name="Component 1",
                        description="First component",
                        category="tool",
                        conflicts_with=["test.component2"]
                    )
                ]
        
        profile1 = TestProfile1()
        profile2 = TestProfile2()
        profile3 = TestProfile3()
        
        # Compatible profiles
        assert profile1.is_compatible_with(profile2) is True
        assert profile2.is_compatible_with(profile1) is True
        
        # Incompatible profiles (conflicting components)
        assert profile1.is_compatible_with(profile3) is False
        assert profile3.is_compatible_with(profile1) is False
    
    def test_base_profile_validation(self):
        """Test BaseProfile validation."""
        class ValidProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "valid-profile"
                self.name = "Valid Profile"
                self.description = "A valid profile"
                self.category = "test"
                
                self.components = [
                    Component(
                        id="test.component",
                        name="Test Component",
                        description="A test component",
                        category="tool"
                    )
                ]
        
        class InvalidProfile(BaseProfile):
            def _initialize_profile(self):
                # Missing required fields
                self.id = ""
                self.name = ""
                self.description = ""
                self.category = ""
                
                self.components = [
                    Component(
                        id="",  # Missing ID
                        name="",  # Missing name
                        description="",  # Missing description
                        category="tool"
                    )
                ]
        
        valid_profile = ValidProfile()
        invalid_profile = InvalidProfile()
        
        valid_issues = valid_profile.validate_components()
        invalid_issues = invalid_profile.validate_components()
        
        assert len(valid_issues) == 0
        assert len(invalid_issues) > 0
        assert "Profile ID is required" in invalid_issues
        assert "Profile name is required" in invalid_issues
        assert "Component ID is required" in invalid_issues
    
    def test_base_profile_estimates(self):
        """Test BaseProfile size and time estimates."""
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
                
                self.components = [
                    Component(
                        id="test.component1",
                        name="Component 1",
                        description="First component",
                        category="tool",
                        download_size_mb=100.0,
                        install_time_minutes=10
                    ),
                    Component(
                        id="test.component2",
                        name="Component 2",
                        description="Second component",
                        category="package",
                        download_size_mb=50.0,
                        install_time_minutes=5
                    )
                ]
        
        profile = TestProfile()
        
        assert profile.get_estimated_download_size() == 150.0
        assert profile.get_estimated_install_time() == 15
    
    def test_base_profile_to_dict(self):
        """Test BaseProfile to_dict conversion."""
        class TestProfile(BaseProfile):
            def _initialize_profile(self):
                self.id = "test-profile"
                self.name = "Test Profile"
                self.description = "A test profile"
                self.category = "test"
                
                self.components = [
                    Component(
                        id="test.component",
                        name="Test Component",
                        description="A test component",
                        category="tool"
                    )
                ]
                
                self.verification_steps = [
                    VerificationStep(
                        name="Test Verification",
                        command="test --version",
                        expected_output="1.0.0"
                    )
                ]
                
                self.sample_project = SampleProject(
                    name="Test Project",
                    description="A test project",
                    type="git_clone",
                    source="https://github.com/test/test-project.git",
                    directory="~/test-project"
                )
                
                self.next_steps = ["Step 1", "Step 2"]
        
        profile = TestProfile()
        profile_dict = profile.to_dict()
        
        assert profile_dict["id"] == "test-profile"
        assert profile_dict["name"] == "Test Profile"
        assert profile_dict["description"] == "A test profile"
        assert profile_dict["category"] == "test"
        assert len(profile_dict["components"]) == 1
        assert len(profile_dict["verification_steps"]) == 1
        assert profile_dict["sample_project"]["name"] == "Test Project"
        assert len(profile_dict["next_steps"]) == 2


class TestSolidityProfile:
    """Test SolidityProfile class."""
    
    def test_solidity_profile_creation(self, solidity_profile):
        """Test SolidityProfile creation."""
        assert solidity_profile.id == "web3-solidity"
        assert solidity_profile.name == "Solidity Development"
        assert solidity_profile.description == "Ethereum smart contract development with Hardhat and Foundry"
        assert solidity_profile.category == "web3"
        assert solidity_profile.version == "1.0.0"
    
    def test_solidity_profile_requirements(self, solidity_profile):
        """Test SolidityProfile requirements."""
        requirements = solidity_profile.get_requirements()
        
        assert requirements.ram_gb == 4.0
        assert requirements.disk_gb == 10.0
        assert requirements.cpu_cores == 2
        assert requirements.gpu_required is False
        assert requirements.internet_required is True
        assert requirements.download_size_mb == 500.0
        assert "x86_64" in requirements.supported_archs
        assert "arm64" in requirements.supported_archs
    
    def test_solidity_profile_components(self, solidity_profile):
        """Test SolidityProfile components."""
        components = solidity_profile.get_components()
        
        assert len(components) == 11
        
        # Check for key components
        component_ids = [comp.id for comp in components]
        assert "language.node.18" in component_ids
        assert "tool.npm" in component_ids
        assert "tool.git" in component_ids
        assert "framework.hardhat" in component_ids
        assert "tool.foundry" in component_ids
        assert "tool.solc" in component_ids
        assert "package.openzeppelin" in component_ids
        assert "package.ethers" in component_ids
        assert "package.viem" in component_ids
        assert "package.alchemy" in component_ids
        assert "tool.graph" in component_ids
    
    def test_solidity_profile_verification_steps(self, solidity_profile):
        """Test SolidityProfile verification steps."""
        verification_steps = solidity_profile.get_verification_steps()
        
        assert len(verification_steps) == 11
        
        # Check for key verification steps
        step_names = [step.name for step in verification_steps]
        assert "Node.js Version" in step_names
        assert "npm Version" in step_names
        assert "Git Version" in step_names
        assert "Hardhat Installation" in step_names
        assert "Foundry Installation" in step_names
        assert "Solidity Compiler" in step_names
        assert "OpenZeppelin Contracts" in step_names
        assert "ethers.js" in step_names
        assert "viem" in step_names
        assert "Alchemy SDK" in step_names
        assert "The Graph CLI" in step_names
    
    def test_solidity_profile_sample_project(self, solidity_profile):
        """Test SolidityProfile sample project."""
        sample_project = solidity_profile.get_sample_project()
        
        assert sample_project is not None
        assert sample_project.name == "Hardhat Starter Kit"
        assert sample_project.description == "A complete Hardhat project with sample contracts and tests"
        assert sample_project.type == "git_clone"
        assert sample_project.source == "https://github.com/he2plus/hardhat-starter-kit.git"
        assert sample_project.directory == "~/solidity-project"
        assert len(sample_project.setup_commands) == 4
        assert len(sample_project.next_steps) == 4
    
    def test_solidity_profile_next_steps(self, solidity_profile):
        """Test SolidityProfile next steps."""
        next_steps = solidity_profile.get_next_steps()
        
        assert len(next_steps) > 0
        assert "🎉 Solidity development environment ready!" in next_steps
        assert "npx hardhat init" in " ".join(next_steps)
        assert "npx hardhat compile" in " ".join(next_steps)
        assert "npx hardhat test" in " ".join(next_steps)
        assert "npx hardhat node" in " ".join(next_steps)
    
    def test_solidity_profile_estimates(self, solidity_profile):
        """Test SolidityProfile size and time estimates."""
        download_size = solidity_profile.get_estimated_download_size()
        install_time = solidity_profile.get_estimated_install_time()
        
        assert download_size > 0
        assert install_time > 0
        assert isinstance(download_size, float)
        assert isinstance(install_time, int)
    
    def test_solidity_profile_installation_plan(self, solidity_profile):
        """Test SolidityProfile installation plan."""
        plan = solidity_profile.get_installation_plan()
        
        assert "profile" in plan
        assert "requirements" in plan
        assert "components" in plan
        assert "verification" in plan
        assert "sample_project" in plan
        assert "next_steps" in plan
        assert "estimated_total_time_minutes" in plan
        
        assert plan["profile"]["id"] == "web3-solidity"
        assert plan["profile"]["name"] == "Solidity Development"
        assert len(plan["components"]) == 11
        assert len(plan["verification"]) == 11
        assert plan["estimated_total_time_minutes"] > 0
    
    def test_solidity_profile_web3_specific(self, solidity_profile):
        """Test SolidityProfile Web3-specific information."""
        plan = solidity_profile.get_installation_plan()
        
        assert "web3_specific" in plan
        web3_info = plan["web3_specific"]
        
        assert "blockchain_networks" in web3_info
        assert "development_tools" in web3_info
        assert "testing_frameworks" in web3_info
        assert "deployment_options" in web3_info
        assert "popular_contracts" in web3_info
        
        assert "Hardhat Network (local)" in web3_info["blockchain_networks"]
        assert "Hardhat (development environment)" in web3_info["development_tools"]
        assert "Hardhat Test (JavaScript/TypeScript)" in web3_info["testing_frameworks"]
        assert "Local development (Hardhat Network)" in web3_info["deployment_options"]
        assert "ERC-20 (fungible tokens)" in web3_info["popular_contracts"]
    
    def test_solidity_profile_development_workflow(self, solidity_profile):
        """Test SolidityProfile development workflow."""
        workflow = solidity_profile.get_development_workflow()
        
        assert len(workflow) > 0
        assert "npx hardhat init" in " ".join(workflow)
        assert "npx hardhat compile" in " ".join(workflow)
        assert "npx hardhat test" in " ".join(workflow)
        assert "npx hardhat node" in " ".join(workflow)
    
    def test_solidity_profile_troubleshooting_guide(self, solidity_profile):
        """Test SolidityProfile troubleshooting guide."""
        guide = solidity_profile.get_troubleshooting_guide()
        
        assert "Installation Issues" in guide
        assert "Compilation Issues" in guide
        assert "Testing Issues" in guide
        assert "Deployment Issues" in guide
        
        assert len(guide["Installation Issues"]) > 0
        assert len(guide["Compilation Issues"]) > 0
        assert len(guide["Testing Issues"]) > 0
        assert len(guide["Deployment Issues"]) > 0
    
    def test_solidity_profile_recommended_extensions(self, solidity_profile):
        """Test SolidityProfile recommended VS Code extensions."""
        extensions = solidity_profile.get_recommended_extensions()
        
        assert "hardhat" in extensions
        assert "solidity" in extensions
        assert "prettier-solidity" in extensions
        assert "gitlens" in extensions
        assert len(extensions) > 0
    
    def test_solidity_profile_useful_commands(self, solidity_profile):
        """Test SolidityProfile useful commands."""
        commands = solidity_profile.get_useful_commands()
        
        assert "Hardhat Commands" in commands
        assert "Foundry Commands" in commands
        assert "Git Commands" in commands
        assert "npm Commands" in commands
        
        assert len(commands["Hardhat Commands"]) > 0
        assert len(commands["Foundry Commands"]) > 0
        assert len(commands["Git Commands"]) > 0
        assert len(commands["npm Commands"]) > 0
        
        assert "npx hardhat init" in commands["Hardhat Commands"]
        assert "forge init" in commands["Foundry Commands"]
        assert "git init" in commands["Git Commands"]
        assert "npm install" in commands["npm Commands"]
