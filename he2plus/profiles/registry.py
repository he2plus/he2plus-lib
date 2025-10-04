"""
Profile registry for he2plus.

This module manages all available profiles and provides search,
filtering, and dependency resolution capabilities.
"""

import importlib
import pkgutil
from typing import Dict, List, Optional, Set, Type
import structlog

from .base import BaseProfile

logger = structlog.get_logger(__name__)


class ProfileRegistry:
    """Registry for all available development profiles."""
    
    def __init__(self):
        self.logger = logger.bind(component="profile_registry")
        self._profiles: Dict[str, BaseProfile] = {}
        self._categories: Dict[str, List[str]] = {}
        self._loaded = False
    
    def load_profiles(self) -> None:
        """Load all available profiles."""
        if self._loaded:
            return
        
        self.logger.info("Loading profiles")
        
        # Load profiles from different categories
        self._load_category_profiles("web3")
        self._load_category_profiles("web")
        self._load_category_profiles("mobile")
        self._load_category_profiles("ml")
        self._load_category_profiles("utils")
        
        self._loaded = True
        self.logger.info("Profiles loaded", count=len(self._profiles))
    
    def _load_category_profiles(self, category: str) -> None:
        """Load profiles from a specific category."""
        try:
            # Import the category module
            module_name = f"he2plus.profiles.{category}"
            module = importlib.import_module(module_name)
            
            # Find all profile classes in the module
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, BaseProfile) and 
                    obj != BaseProfile):
                    
                    try:
                        # Instantiate the profile
                        profile = obj()
                        
                        # Validate the profile
                        issues = profile.validate_components()
                        if issues:
                            self.logger.warning("Profile validation failed", 
                                              profile=profile.id, issues=issues)
                            continue
                        
                        # Register the profile
                        self._profiles[profile.id] = profile
                        
                        # Add to category
                        if category not in self._categories:
                            self._categories[category] = []
                        self._categories[category].append(profile.id)
                        
                        self.logger.debug("Profile loaded", 
                                        profile=profile.id, category=category)
                    
                    except Exception as e:
                        self.logger.error("Failed to load profile", 
                                        profile=name, error=str(e))
        
        except ImportError as e:
            self.logger.debug("Category module not found", category=category, error=str(e))
        except Exception as e:
            self.logger.error("Failed to load category", category=category, error=str(e))
        
        # Also load profiles from submodules
        self._load_submodule_profiles(category)
    
    def _load_submodule_profiles(self, category: str) -> None:
        """Load profiles from submodules within a category."""
        try:
            # Import the category module
            module_name = f"he2plus.profiles.{category}"
            module = importlib.import_module(module_name)
            
            # Find all submodules
            for importer, modname, ispkg in pkgutil.iter_modules(module.__path__, module.__name__ + "."):
                if ispkg:
                    continue
                
                try:
                    # Import the submodule
                    submodule = importlib.import_module(modname)
                    
                    # Find all profile classes in the submodule
                    for name in dir(submodule):
                        obj = getattr(submodule, name)
                        if (isinstance(obj, type) and 
                            issubclass(obj, BaseProfile) and 
                            obj != BaseProfile):
                            
                            try:
                                # Instantiate the profile
                                profile = obj()
                                
                                # Validate the profile
                                issues = profile.validate_components()
                                if issues:
                                    self.logger.warning("Profile validation failed", 
                                                      profile=profile.id, issues=issues)
                                    continue
                                
                                # Register the profile
                                self._profiles[profile.id] = profile
                                
                                # Add to category
                                if category not in self._categories:
                                    self._categories[category] = []
                                self._categories[category].append(profile.id)
                                
                                self.logger.debug("Profile loaded from submodule", 
                                                profile=profile.id, category=category, submodule=modname)
                                
                            except Exception as e:
                                self.logger.error("Failed to load profile from submodule", 
                                                profile=name, submodule=modname, error=str(e))
                
                except ImportError as e:
                    self.logger.debug("Submodule not found", submodule=modname, error=str(e))
                except Exception as e:
                    self.logger.error("Failed to load submodule", 
                                    submodule=modname, error=str(e))
        
        except Exception as e:
            self.logger.error("Failed to load submodule profiles", 
                            category=category, error=str(e))
    
    def get(self, profile_id: str) -> Optional[BaseProfile]:
        """Get a profile by ID."""
        if not self._loaded:
            self.load_profiles()
        
        return self._profiles.get(profile_id)
    
    def get_all(self) -> List[BaseProfile]:
        """Get all available profiles."""
        if not self._loaded:
            self.load_profiles()
        
        return list(self._profiles.values())
    
    def get_by_category(self, category: str) -> List[BaseProfile]:
        """Get all profiles in a category."""
        if not self._loaded:
            self.load_profiles()
        
        profile_ids = self._categories.get(category, [])
        return [self._profiles[pid] for pid in profile_ids if pid in self._profiles]
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        if not self._loaded:
            self.load_profiles()
        
        return list(self._categories.keys())
    
    def search(self, query: str) -> List[BaseProfile]:
        """Search profiles by name, description, or keywords."""
        if not self._loaded:
            self.load_profiles()
        
        query_lower = query.lower()
        results = []
        
        for profile in self._profiles.values():
            # Search in name, description, and category
            if (query_lower in profile.name.lower() or
                query_lower in profile.description.lower() or
                query_lower in profile.category.lower() or
                query_lower in profile.id.lower()):
                results.append(profile)
        
        return results
    
    def get_compatible_profiles(self, profile_ids: List[str]) -> List[BaseProfile]:
        """Get profiles that are compatible with the given profiles."""
        if not self._loaded:
            self.load_profiles()
        
        # Get the specified profiles
        specified_profiles = []
        for pid in profile_ids:
            profile = self._profiles.get(pid)
            if profile:
                specified_profiles.append(profile)
        
        if not specified_profiles:
            return []
        
        # Find compatible profiles
        compatible = []
        for profile in self._profiles.values():
            if profile.id in profile_ids:
                continue  # Skip already specified profiles
            
            # Check compatibility with all specified profiles
            is_compatible = True
            for specified in specified_profiles:
                if not profile.is_compatible_with(specified):
                    is_compatible = False
                    break
            
            if is_compatible:
                compatible.append(profile)
        
        return compatible
    
    def get_dependencies(self, profile_ids: List[str]) -> List[str]:
        """Get all dependencies for the given profiles."""
        if not self._loaded:
            self.load_profiles()
        
        dependencies = set()
        
        for pid in profile_ids:
            profile = self._profiles.get(pid)
            if profile:
                dependencies.update(profile.get_dependencies())
        
        return list(dependencies)
    
    def resolve_dependencies(self, profile_ids: List[str]) -> List[str]:
        """Resolve and order dependencies for installation."""
        if not self._loaded:
            self.load_profiles()
        
        # Build dependency graph
        graph = {}
        for pid in profile_ids:
            profile = self._profiles.get(pid)
            if profile:
                graph[pid] = profile.get_dependencies()
        
        # Topological sort
        visited = set()
        temp_visited = set()
        result = []
        
        def visit(node):
            if node in temp_visited:
                raise ValueError(f"Circular dependency detected: {node}")
            if node in visited:
                return
            
            temp_visited.add(node)
            
            # Visit dependencies first
            for dep in graph.get(node, []):
                if dep in self._profiles:  # Only include if it's a known profile
                    visit(dep)
            
            temp_visited.remove(node)
            visited.add(node)
            result.append(node)
        
        for node in profile_ids:
            if node not in visited:
                visit(node)
        
        return result
    
    def get_installation_plan(self, profile_ids: List[str]) -> Dict[str, any]:
        """Get a complete installation plan for multiple profiles."""
        if not self._loaded:
            self.load_profiles()
        
        # Resolve dependencies
        ordered_profiles = self.resolve_dependencies(profile_ids)
        
        # Get profiles
        profiles = [self._profiles[pid] for pid in ordered_profiles if pid in self._profiles]
        
        # Calculate totals
        total_ram = sum(p.requirements.ram_gb for p in profiles)
        total_disk = sum(p.requirements.disk_gb for p in profiles)
        total_download = sum(p.get_estimated_download_size() for p in profiles)
        total_time = sum(p.get_estimated_install_time() for p in profiles)
        
        # Get all components
        all_components = []
        for profile in profiles:
            all_components.extend(profile.get_components())
        
        # Get all verification steps
        all_verification = []
        for profile in profiles:
            all_verification.extend(profile.get_verification_steps())
        
        return {
            "profiles": [p.to_dict() for p in profiles],
            "ordered_installation": ordered_profiles,
            "totals": {
                "ram_gb": total_ram,
                "disk_gb": total_disk,
                "download_size_mb": total_download,
                "install_time_minutes": total_time,
                "component_count": len(all_components),
                "verification_steps": len(all_verification)
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
                for comp in all_components
            ],
            "verification": [
                {
                    "name": step.name,
                    "command": step.command,
                    "expected_output": step.expected_output,
                    "contains_text": step.contains_text
                }
                for step in all_verification
            ]
        }
    
    def get_recommendations(self, system_info: any) -> List[BaseProfile]:
        """Get profile recommendations based on system capabilities."""
        if not self._loaded:
            self.load_profiles()
        
        recommendations = []
        
        for profile in self._profiles.values():
            # Basic filtering based on system capabilities
            if profile.requirements.ram_gb <= system_info.ram_total_gb:
                if profile.requirements.disk_gb <= system_info.disk_free_gb:
                    if profile.requirements.cpu_cores <= system_info.cpu_cores:
                        recommendations.append(profile)
        
        # Sort by popularity/importance (this could be enhanced with usage data)
        priority_order = [
            "base", "web3-solidity", "web-nextjs", "mobile-react-native",
            "ml-python", "utils-docker", "utils-version-control"
        ]
        
        def sort_key(profile):
            try:
                return priority_order.index(profile.id)
            except ValueError:
                return 999
        
        recommendations.sort(key=sort_key)
        return recommendations
    
    def get_profile_info(self, profile_id: str) -> Optional[Dict[str, any]]:
        """Get detailed information about a profile."""
        profile = self.get(profile_id)
        if not profile:
            return None
        
        return {
            "profile": profile.to_dict(),
            "installation_plan": profile.get_installation_plan(),
            "compatible_profiles": [p.id for p in self.get_compatible_profiles([profile_id])],
            "dependencies": profile.get_dependencies(),
            "conflicts": profile.get_conflicts()
        }
    
    def validate_installation(self, profile_ids: List[str]) -> Dict[str, any]:
        """Validate that profiles can be installed together."""
        if not self._loaded:
            self.load_profiles()
        
        issues = []
        warnings = []
        
        # Check if all profiles exist
        missing_profiles = []
        for pid in profile_ids:
            if pid not in self._profiles:
                missing_profiles.append(pid)
        
        if missing_profiles:
            issues.append(f"Unknown profiles: {', '.join(missing_profiles)}")
        
        # Check for conflicts
        profiles = [self._profiles[pid] for pid in profile_ids if pid in self._profiles]
        
        for i, profile1 in enumerate(profiles):
            for profile2 in profiles[i+1:]:
                if not profile1.is_compatible_with(profile2):
                    issues.append(f"Conflict between {profile1.id} and {profile2.id}")
        
        # Check dependencies
        try:
            self.resolve_dependencies(profile_ids)
        except ValueError as e:
            issues.append(str(e))
        
        # Check resource requirements
        total_ram = sum(p.requirements.ram_gb for p in profiles)
        total_disk = sum(p.requirements.disk_gb for p in profiles)
        
        if total_ram > 32:
            warnings.append(f"High RAM requirement: {total_ram}GB")
        
        if total_disk > 100:
            warnings.append(f"High disk requirement: {total_disk}GB")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "profiles": [p.id for p in profiles],
            "total_ram_gb": total_ram,
            "total_disk_gb": total_disk
        }
    
    def __len__(self) -> int:
        if not self._loaded:
            self.load_profiles()
        return len(self._profiles)
    
    def __contains__(self, profile_id: str) -> bool:
        if not self._loaded:
            self.load_profiles()
        return profile_id in self._profiles
    
    def __iter__(self):
        if not self._loaded:
            self.load_profiles()
        return iter(self._profiles.values())
