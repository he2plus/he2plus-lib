"""
System detection and profiling for he2plus.

This module provides comprehensive system information gathering across
macOS, Windows, and Linux platforms.
"""

import platform
import subprocess
import shutil
import psutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class SystemInfo:
    """Comprehensive system information."""
    
    # Basic system info
    os_name: str
    os_version: str
    arch: str
    platform: str
    
    # Hardware info
    cpu_name: str
    cpu_cores: int
    ram_total_gb: float
    ram_available_gb: float
    disk_total_gb: float
    disk_free_gb: float
    
    # GPU info
    gpu_name: Optional[str] = None
    gpu_vendor: Optional[str] = None
    cuda_available: bool = False
    metal_available: bool = False
    
    # Installed tools
    package_managers: List[str] = None
    languages: Dict[str, str] = None
    
    def __post_init__(self):
        if self.package_managers is None:
            self.package_managers = []
        if self.languages is None:
            self.languages = {}


class SystemProfiler:
    """Cross-platform system profiler for development environment setup."""
    
    def __init__(self):
        self.logger = logger.bind(component="system_profiler")
    
    def profile(self) -> SystemInfo:
        """Get comprehensive system information."""
        self.logger.info("Starting system profiling")
        
        # Basic system info
        os_name, os_version, arch = self._get_basic_info()
        
        # Hardware info
        cpu_name, cpu_cores = self._get_cpu_info()
        ram_total, ram_available = self._get_memory_info()
        disk_total, disk_free = self._get_disk_info()
        
        # GPU info
        gpu_name, gpu_vendor, cuda_available, metal_available = self._get_gpu_info()
        
        # Installed tools
        package_managers = self._detect_package_managers()
        languages = self._detect_languages()
        
        system_info = SystemInfo(
            os_name=os_name,
            os_version=os_version,
            arch=arch,
            platform=platform.platform(),
            cpu_name=cpu_name,
            cpu_cores=cpu_cores,
            ram_total_gb=ram_total,
            ram_available_gb=ram_available,
            disk_total_gb=disk_total,
            disk_free_gb=disk_free,
            gpu_name=gpu_name,
            gpu_vendor=gpu_vendor,
            cuda_available=cuda_available,
            metal_available=metal_available,
            package_managers=package_managers,
            languages=languages
        )
        
        self.logger.info("System profiling completed", 
                        os=os_name, arch=arch, ram_gb=ram_total, 
                        disk_free_gb=disk_free)
        
        return system_info
    
    def _get_basic_info(self) -> Tuple[str, str, str]:
        """Get basic OS information."""
        system = platform.system().lower()
        
        if system == "darwin":
            os_name = "macOS"
            try:
                # Get macOS version
                result = subprocess.run(
                    ["sw_vers", "-productVersion"], 
                    capture_output=True, text=True, check=True
                )
                os_version = result.stdout.strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                os_version = platform.mac_ver()[0]
        elif system == "windows":
            os_name = "Windows"
            os_version = platform.win32_ver()[0]
        elif system == "linux":
            os_name = "Linux"
            try:
                # Try to get distribution info
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            os_version = line.split("=", 1)[1].strip().strip('"')
                            break
                    else:
                        os_version = platform.release()
            except (FileNotFoundError, OSError):
                os_version = platform.release()
        else:
            os_name = system.title()
            os_version = platform.release()
        
        # Get architecture
        arch = platform.machine().lower()
        if arch in ["x86_64", "amd64"]:
            arch = "x86_64"
        elif arch in ["arm64", "aarch64"]:
            arch = "arm64"
        elif arch in ["arm", "armv7l"]:
            arch = "arm"
        
        return os_name, os_version, arch
    
    def _get_cpu_info(self) -> Tuple[str, int]:
        """Get CPU information."""
        try:
            cpu_name = platform.processor()
            if not cpu_name or cpu_name == "unknown":
                # Try alternative methods
                if platform.system() == "Darwin":
                    try:
                        result = subprocess.run(
                            ["sysctl", "-n", "machdep.cpu.brand_string"],
                            capture_output=True, text=True, check=True
                        )
                        cpu_name = result.stdout.strip()
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        cpu_name = "Unknown CPU"
                elif platform.system() == "Linux":
                    try:
                        with open("/proc/cpuinfo", "r") as f:
                            for line in f:
                                if line.startswith("model name"):
                                    cpu_name = line.split(":", 1)[1].strip()
                                    break
                    except (FileNotFoundError, OSError):
                        cpu_name = "Unknown CPU"
                else:
                    cpu_name = "Unknown CPU"
        except Exception:
            cpu_name = "Unknown CPU"
        
        cpu_cores = psutil.cpu_count(logical=True)
        return cpu_name, cpu_cores
    
    def _get_memory_info(self) -> Tuple[float, float]:
        """Get memory information in GB."""
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        return round(total_gb, 1), round(available_gb, 1)
    
    def _get_disk_info(self) -> Tuple[float, float]:
        """Get disk information in GB."""
        try:
            # Get disk usage for the current directory
            disk_usage = psutil.disk_usage(".")
            total_gb = disk_usage.total / (1024**3)
            free_gb = disk_usage.free / (1024**3)
            return round(total_gb, 1), round(free_gb, 1)
        except Exception:
            # Fallback to home directory
            try:
                disk_usage = psutil.disk_usage(str(Path.home()))
                total_gb = disk_usage.total / (1024**3)
                free_gb = disk_usage.free / (1024**3)
                return round(total_gb, 1), round(free_gb, 1)
            except Exception:
                return 0.0, 0.0
    
    def _get_gpu_info(self) -> Tuple[Optional[str], Optional[str], bool, bool]:
        """Get GPU information and capabilities."""
        gpu_name = None
        gpu_vendor = None
        cuda_available = False
        metal_available = False
        
        system = platform.system().lower()
        
        if system == "darwin":
            # macOS - check for Apple Silicon or Intel
            try:
                result = subprocess.run(
                    ["system_profiler", "SPDisplaysDataType", "-json"],
                    capture_output=True, text=True, check=True
                )
                import json
                data = json.loads(result.stdout)
                
                if "SPDisplaysDataType" in data and data["SPDisplaysDataType"]:
                    display = data["SPDisplaysDataType"][0]
                    gpu_name = display.get("_name", "Unknown GPU")
                    gpu_vendor = display.get("sppci_model", "Unknown")
                    
                    # Check for Apple Silicon (Metal support)
                    if "Apple" in gpu_name or "M1" in gpu_name or "M2" in gpu_name:
                        metal_available = True
            except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
                pass
        
        elif system == "linux":
            # Linux - check for NVIDIA, AMD, Intel
            try:
                # Check for NVIDIA
                result = subprocess.run(
                    ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    gpu_name = result.stdout.strip()
                    gpu_vendor = "NVIDIA"
                    cuda_available = True
                else:
                    # Check for AMD
                    result = subprocess.run(
                        ["lspci", "-nn"], capture_output=True, text=True
                    )
                    if "VGA" in result.stdout:
                        if "AMD" in result.stdout:
                            gpu_vendor = "AMD"
                        elif "Intel" in result.stdout:
                            gpu_vendor = "Intel"
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        elif system == "windows":
            # Windows - check for GPU
            try:
                result = subprocess.run(
                    ["wmic", "path", "win32_VideoController", "get", "name"],
                    capture_output=True, text=True, check=True
                )
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip() and "Name" not in line:
                        gpu_name = line.strip()
                        if "NVIDIA" in gpu_name:
                            gpu_vendor = "NVIDIA"
                            cuda_available = True
                        elif "AMD" in gpu_name:
                            gpu_vendor = "AMD"
                        elif "Intel" in gpu_name:
                            gpu_vendor = "Intel"
                        break
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        return gpu_name, gpu_vendor, cuda_available, metal_available
    
    def _detect_package_managers(self) -> List[str]:
        """Detect available package managers."""
        managers = []
        
        # Check for common package managers
        package_managers = {
            "brew": "brew",
            "apt": "apt",
            "yum": "yum", 
            "dnf": "dnf",
            "pacman": "pacman",
            "choco": "choco",
            "winget": "winget",
            "snap": "snap",
            "pip": "pip",
            "npm": "npm",
            "yarn": "yarn",
            "pnpm": "pnpm",
            "cargo": "cargo",
            "go": "go",
            "conda": "conda",
            "poetry": "poetry"
        }
        
        for name, command in package_managers.items():
            if shutil.which(command):
                managers.append(name)
        
        return managers
    
    def _detect_languages(self) -> Dict[str, str]:
        """Detect installed programming languages and versions."""
        languages = {}
        
        # Python
        try:
            result = subprocess.run(
                ["python3", "--version"], capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split()
                if len(parts) >= 2:
                    version = parts[1]
                    languages["python"] = version
        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
            pass
        
        # Node.js
        try:
            result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                languages["node"] = version
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Rust
        try:
            result = subprocess.run(
                ["rustc", "--version"], capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split()
                if len(parts) >= 2:
                    version = parts[1]
                    languages["rust"] = version
        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
            pass
        
        # Go
        try:
            result = subprocess.run(
                ["go", "version"], capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split()
                if len(parts) >= 3:
                    version = parts[2]
                    languages["go"] = version
        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
            pass
        
        # Java
        try:
            result = subprocess.run(
                ["java", "-version"], capture_output=True, text=True
            )
            if result.returncode == 0 and result.stderr.strip():
                lines = result.stderr.strip().split('\n')
                if lines and len(lines[0].split()) >= 3:
                    version = lines[0].split()[2].strip('"')
                    languages["java"] = version
        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
            pass
        
        return languages
    
    def get_install_methods(self) -> Dict[str, List[str]]:
        """Get available installation methods for the current system."""
        methods = {
            "system": [],
            "language_specific": [],
            "containers": []
        }
        
        system = platform.system().lower()
        
        if system == "darwin":
            methods["system"] = ["brew", "macports"]
            if "brew" in self._detect_package_managers():
                methods["system"].insert(0, "brew")
        elif system == "linux":
            methods["system"] = ["apt", "yum", "dnf", "pacman", "snap"]
            # Prioritize based on what's available
            available = self._detect_package_managers()
            methods["system"] = [m for m in methods["system"] if m in available]
        elif system == "windows":
            methods["system"] = ["choco", "winget", "scoop"]
            available = self._detect_package_managers()
            methods["system"] = [m for m in methods["system"] if m in available]
        
        # Language-specific package managers
        available = self._detect_package_managers()
        methods["language_specific"] = [m for m in ["pip", "npm", "yarn", "pnpm", "cargo", "go", "conda", "poetry"] if m in available]
        
        # Container options
        if "docker" in self._detect_package_managers():
            methods["containers"] = ["docker"]
        
        return methods
