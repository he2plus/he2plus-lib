"""Unit tests for profile registry module."""

import pytest
from unittest.mock import patch, Mock

from he2plus.profiles.registry import ProfileRegistry
from he2plus.profiles.web3.solidity import SolidityProfile


class TestProfileRegistry:
    """Test ProfileRegistry class."""
    
    def test_registry_creation(self):
        """Test ProfileRegistry creation."""
        registry = ProfileRegistry()
        
        assert registry._profiles == {}
        assert registry._categories == {}
        assert registry._loaded is False
    
    def test_registry_load_profiles(self):
        """Test ProfileRegistry profile loading."""
        with patch('he2plus.profiles.registry.importlib.import_module') as mock_import:
            # Mock the web3 module
            mock_module = Mock()
            mock_module.SolidityProfile = SolidityProfile
            
            # Mock dir() to return SolidityProfile
            with patch('builtins.dir', return_value=['SolidityProfile']):
                mock_import.return_value = mock_module
                
                registry = ProfileRegistry()
                registry.load_profiles()
                
                assert registry._loaded is True
                assert len(registry._profiles) > 0
                assert "web3-solidity" in registry._profiles
                assert "web3" in registry._categories
    
    def test_registry_get_profile(self):
        """Test ProfileRegistry get profile by ID."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            registry._profiles = {"web3-solidity": Mock()}
            registry._loaded = True
            
            profile = registry.get("web3-solidity")
            assert profile is not None
            
            profile = registry.get("nonexistent")
            assert profile is None
    
    def test_registry_get_all_profiles(self):
        """Test ProfileRegistry get all profiles."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile2 = Mock()
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            profiles = registry.get_all()
            assert len(profiles) == 2
            assert mock_profile1 in profiles
            assert mock_profile2 in profiles
    
    def test_registry_get_by_category(self):
        """Test ProfileRegistry get profiles by category."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile = Mock()
            registry._profiles = {"web3-solidity": mock_profile}
            registry._categories = {"web3": ["web3-solidity"]}
            registry._loaded = True
            
            profiles = registry.get_by_category("web3")
            assert len(profiles) == 1
            assert mock_profile in profiles
            
            profiles = registry.get_by_category("nonexistent")
            assert len(profiles) == 0
    
    def test_registry_get_categories(self):
        """Test ProfileRegistry get categories."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            registry._categories = {"web3": ["web3-solidity"], "web": ["web-nextjs"]}
            registry._loaded = True
            
            categories = registry.get_categories()
            assert len(categories) == 2
            assert "web3" in categories
            assert "web" in categories
    
    def test_registry_search(self):
        """Test ProfileRegistry search profiles."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.name = "Solidity Development"
            mock_profile1.description = "Ethereum smart contract development"
            mock_profile1.category = "web3"
            mock_profile1.id = "web3-solidity"
            
            mock_profile2 = Mock()
            mock_profile2.name = "Next.js Development"
            mock_profile2.description = "React framework development"
            mock_profile2.category = "web"
            mock_profile2.id = "web-nextjs"
            
            registry._profiles = {
                "web3-solidity": mock_profile1,
                "web-nextjs": mock_profile2
            }
            registry._loaded = True
            
            # Search by name
            results = registry.search("Solidity")
            assert len(results) == 1
            assert mock_profile1 in results
            
            # Search by description
            results = registry.search("Ethereum")
            assert len(results) == 1
            assert mock_profile1 in results
            
            # Search by category
            results = registry.search("web3")
            assert len(results) == 1
            assert mock_profile1 in results
            
            # Search by ID
            results = registry.search("web3-solidity")
            assert len(results) == 1
            assert mock_profile1 in results
            
            # Search with no results
            results = registry.search("nonexistent")
            assert len(results) == 0
    
    def test_registry_get_compatible_profiles(self):
        """Test ProfileRegistry get compatible profiles."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.id = "web3-solidity"
            mock_profile1.is_compatible_with.return_value = True
            
            mock_profile2 = Mock()
            mock_profile2.id = "web-nextjs"
            mock_profile2.is_compatible_with.return_value = True
            
            mock_profile3 = Mock()
            mock_profile3.id = "conflicting-profile"
            mock_profile3.is_compatible_with.return_value = False
            
            registry._profiles = {
                "web3-solidity": mock_profile1,
                "web-nextjs": mock_profile2,
                "conflicting-profile": mock_profile3
            }
            registry._loaded = True
            
            compatible = registry.get_compatible_profiles(["web3-solidity"])
            assert len(compatible) == 1
            assert mock_profile2 in compatible
            assert mock_profile3 not in compatible
    
    def test_registry_get_dependencies(self):
        """Test ProfileRegistry get dependencies."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.get_dependencies.return_value = ["dep1", "dep2"]
            
            mock_profile2 = Mock()
            mock_profile2.get_dependencies.return_value = ["dep2", "dep3"]
            
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            dependencies = registry.get_dependencies(["profile1", "profile2"])
            assert len(dependencies) == 3
            assert "dep1" in dependencies
            assert "dep2" in dependencies
            assert "dep3" in dependencies
    
    def test_registry_resolve_dependencies(self):
        """Test ProfileRegistry resolve dependencies."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.get_dependencies.return_value = ["profile2"]
            
            mock_profile2 = Mock()
            mock_profile2.get_dependencies.return_value = []
            
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            resolved = registry.resolve_dependencies(["profile1"])
            assert len(resolved) == 2
            assert resolved[0] == "profile2"  # Dependency first
            assert resolved[1] == "profile1"  # Then the profile
    
    def test_registry_resolve_dependencies_circular(self):
        """Test ProfileRegistry resolve dependencies with circular dependency."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.get_dependencies.return_value = ["profile2"]
            
            mock_profile2 = Mock()
            mock_profile2.get_dependencies.return_value = ["profile1"]
            
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            with pytest.raises(ValueError, match="Circular dependency detected"):
                registry.resolve_dependencies(["profile1"])
    
    def test_registry_get_installation_plan(self):
        """Test ProfileRegistry get installation plan."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile = Mock()
            mock_profile.get_components.return_value = []
            mock_profile.get_verification_steps.return_value = []
            mock_profile.to_dict.return_value = {"id": "test-profile"}
            mock_profile.requirements.ram_gb = 4.0
            mock_profile.requirements.disk_gb = 10.0
            mock_profile.get_estimated_download_size.return_value = 100.0
            mock_profile.get_estimated_install_time.return_value = 30
            
            registry._profiles = {"test-profile": mock_profile}
            registry._loaded = True
            
            # Mock resolve_dependencies
            with patch.object(registry, 'resolve_dependencies', return_value=["test-profile"]):
                plan = registry.get_installation_plan(["test-profile"])
                
                assert "profiles" in plan
                assert "ordered_installation" in plan
                assert "totals" in plan
                assert "components" in plan
                assert "verification" in plan
                
                assert len(plan["profiles"]) == 1
                assert plan["ordered_installation"] == ["test-profile"]
                assert plan["totals"]["ram_gb"] == 4.0
                assert plan["totals"]["disk_gb"] == 10.0
                assert plan["totals"]["download_size_mb"] == 100.0
                assert plan["totals"]["install_time_minutes"] == 30
    
    def test_registry_get_recommendations(self, mock_system_info):
        """Test ProfileRegistry get recommendations."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.requirements.ram_gb = 2.0
            mock_profile1.requirements.disk_gb = 5.0
            mock_profile1.requirements.cpu_cores = 1
            mock_profile1.id = "profile1"
            
            mock_profile2 = Mock()
            mock_profile2.requirements.ram_gb = 20.0  # Too much RAM
            mock_profile2.requirements.disk_gb = 5.0
            mock_profile2.requirements.cpu_cores = 1
            mock_profile2.id = "profile2"
            
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            recommendations = registry.get_recommendations(mock_system_info)
            assert len(recommendations) == 1
            assert mock_profile1 in recommendations
            assert mock_profile2 not in recommendations
    
    def test_registry_get_profile_info(self):
        """Test ProfileRegistry get profile info."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile = Mock()
            mock_profile.to_dict.return_value = {"id": "test-profile"}
            mock_profile.get_installation_plan.return_value = {"plan": "test"}
            mock_profile.get_dependencies.return_value = ["dep1"]
            mock_profile.get_conflicts.return_value = ["conflict1"]
            
            registry._profiles = {"test-profile": mock_profile}
            registry._loaded = True
            
            # Mock get_compatible_profiles
            with patch.object(registry, 'get_compatible_profiles', return_value=[]):
                info = registry.get_profile_info("test-profile")
                
                assert "profile" in info
                assert "installation_plan" in info
                assert "compatible_profiles" in info
                assert "dependencies" in info
                assert "conflicts" in info
                
                assert info["profile"]["id"] == "test-profile"
                assert info["dependencies"] == ["dep1"]
                assert info["conflicts"] == ["conflict1"]
    
    def test_registry_validate_installation(self):
        """Test ProfileRegistry validate installation."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.id = "profile1"
            mock_profile1.is_compatible_with.return_value = True
            mock_profile1.requirements.ram_gb = 4.0
            mock_profile1.requirements.disk_gb = 10.0
            
            mock_profile2 = Mock()
            mock_profile2.id = "profile2"
            mock_profile2.is_compatible_with.return_value = True
            mock_profile2.requirements.ram_gb = 2.0
            mock_profile2.requirements.disk_gb = 5.0
            
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            # Mock resolve_dependencies
            with patch.object(registry, 'resolve_dependencies', return_value=["profile1", "profile2"]):
                validation = registry.validate_installation(["profile1", "profile2"])
                
                assert "valid" in validation
                assert "issues" in validation
                assert "warnings" in validation
                assert "profiles" in validation
                assert "total_ram_gb" in validation
                assert "total_disk_gb" in validation
                
                assert validation["valid"] is True
                assert len(validation["issues"]) == 0
                assert validation["total_ram_gb"] == 6.0
                assert validation["total_disk_gb"] == 15.0
    
    def test_registry_validate_installation_missing_profile(self):
        """Test ProfileRegistry validate installation with missing profile."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            registry._profiles = {}
            registry._loaded = True
            
            validation = registry.validate_installation(["nonexistent"])
            
            assert validation["valid"] is False
            assert len(validation["issues"]) > 0
            assert "Unknown profiles" in validation["issues"][0]
    
    def test_registry_validate_installation_conflicts(self):
        """Test ProfileRegistry validate installation with conflicts."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile1.id = "profile1"
            mock_profile1.is_compatible_with.return_value = False
            mock_profile1.requirements.ram_gb = 4.0
            mock_profile1.requirements.disk_gb = 10.0
            
            mock_profile2 = Mock()
            mock_profile2.id = "profile2"
            mock_profile2.is_compatible_with.return_value = False
            mock_profile2.requirements.ram_gb = 2.0
            mock_profile2.requirements.disk_gb = 5.0
            
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            validation = registry.validate_installation(["profile1", "profile2"])
            
            assert validation["valid"] is False
            assert len(validation["issues"]) > 0
            assert "Conflict between" in validation["issues"][0]
    
    def test_registry_validate_installation_high_resources(self):
        """Test ProfileRegistry validate installation with high resource requirements."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile = Mock()
            mock_profile.id = "profile1"
            mock_profile.is_compatible_with.return_value = True
            mock_profile.requirements.ram_gb = 50.0  # High RAM
            mock_profile.requirements.disk_gb = 200.0  # High disk
            
            registry._profiles = {"profile1": mock_profile}
            registry._loaded = True
            
            # Mock resolve_dependencies
            with patch.object(registry, 'resolve_dependencies', return_value=["profile1"]):
                validation = registry.validate_installation(["profile1"])
                
                assert validation["valid"] is True
                assert len(validation["warnings"]) > 0
                assert any("High RAM requirement" in warning for warning in validation["warnings"])
                assert any("High disk requirement" in warning for warning in validation["warnings"])
    
    def test_registry_len(self):
        """Test ProfileRegistry __len__ method."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            registry._profiles = {"profile1": Mock(), "profile2": Mock()}
            registry._loaded = True
            
            assert len(registry) == 2
    
    def test_registry_contains(self):
        """Test ProfileRegistry __contains__ method."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            registry._profiles = {"profile1": Mock()}
            registry._loaded = True
            
            assert "profile1" in registry
            assert "nonexistent" not in registry
    
    def test_registry_iter(self):
        """Test ProfileRegistry __iter__ method."""
        registry = ProfileRegistry()
        
        # Mock the profile loading
        with patch.object(registry, 'load_profiles'):
            mock_profile1 = Mock()
            mock_profile2 = Mock()
            registry._profiles = {
                "profile1": mock_profile1,
                "profile2": mock_profile2
            }
            registry._loaded = True
            
            profiles = list(registry)
            assert len(profiles) == 2
            assert mock_profile1 in profiles
            assert mock_profile2 in profiles
