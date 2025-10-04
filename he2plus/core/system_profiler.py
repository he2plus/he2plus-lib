"""
System Profiler for he2plus
Detects system resources, installed software, and capabilities
"""

import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import psutil


@dataclass
class SystemInfo:
    """Comprehensive system information"""
    # Basic system info
    os_name: str
    os_version: str
    architecture: str
    
    # Hardware resources
    ram_total_gb: float
    ram_available_gb: float
    disk_total_gb: float
    disk_free_gb: float
    cpu_cores: int
    cpu_name: str
    
    # GPU information
    gpu_name: Optional[str]
    gpu_type: Optional[str]  # nvidia, amd, apple, intel, none
    
    # Installed software
    python_versions: List[str]
    node_versions: List[str]
    package_managers: List[str]
    
    # System paths
    home_dir: str
    temp_dir: str


def get_system_info() -> SystemInfo:
    """
    Get comprehensive system information
    
    Returns:
        SystemInfo: Complete system information
    """
    try:
        # Basic system info
        os_name = platform.system().lower()
        os_version = platform.release()
        architecture = platform.machine().lower()
        
        # Hardware resources
        ram_info = _get_ram_info()
        disk_info = _get_disk_info()
        cpu_info = _get_cpu_info()
        
        # GPU information
        gpu_info = _get_gpu_info()
        
        # Installed software
        python_versions = _find_python_versions()
        node_versions = _find_node_versions()
        package_managers = _find_package_managers()
        
        # System paths
        home_dir = str(Path.home())
        temp_dir = str(Path.home() / ".he2plus" / "temp")
        
        return SystemInfo(
            os_name=os_name,
            os_version=os_version,
            architecture=architecture,
            ram_total_gb=ram_info[0],
            ram_available_gb=ram_info[1],
            disk_total_gb=disk_info[0],
            disk_free_gb=disk_info[1],
            cpu_cores=cpu_info[0],
            cpu_name=cpu_info[1],
            gpu_name=gpu_info[0],
            gpu_type=gpu_info[1],
            python_versions=python_versions,
            node_versions=node_versions,
            package_managers=package_managers,
            home_dir=home_dir,
            temp_dir=temp_dir
        )
        
    except Exception as e:
        # Return minimal info if something fails
        return SystemInfo(
            os_name=platform.system().lower(),
            os_version=platform.release(),
            architecture=platform.machine().lower(),
            ram_total_gb=0.0,
            ram_available_gb=0.0,
            disk_total_gb=0.0,
            disk_free_gb=0.0,
            cpu_cores=1,
            cpu_name="Unknown",
            gpu_name=None,
            gpu_type=None,
            python_versions=[],
            node_versions=[],
            package_managers=[],
            home_dir=str(Path.home()),
            temp_dir=str(Path.home() / ".he2plus" / "temp")
        )


def _get_ram_info() -> Tuple[float, float]:
    """Get RAM information in GB"""
    try:
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        return round(total_gb, 2), round(available_gb, 2)
    except Exception:
        return 0.0, 0.0


def _get_disk_info() -> Tuple[float, float]:
    """Get disk information for home directory in GB"""
    try:
        home_path = Path.home()
        disk_usage = psutil.disk_usage(str(home_path))
        total_gb = disk_usage.total / (1024**3)
        free_gb = disk_usage.free / (1024**3)
        return round(total_gb, 2), round(free_gb, 2)
    except Exception:
        return 0.0, 0.0


def _get_cpu_info() -> Tuple[int, str]:
    """Get CPU information"""
    try:
        cpu_count = psutil.cpu_count()
        cpu_name = "Unknown"
        
        # Try to get CPU name
        try:
            if platform.system().lower() == "darwin":  # macOS
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    cpu_name = result.stdout.strip()
            elif platform.system().lower() == "linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if line.startswith("model name"):
                            cpu_name = line.split(":")[1].strip()
                            break
            elif platform.system().lower() == "windows":
                result = subprocess.run(
                    ["wmic", "cpu", "get", "name", "/value"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    for line in result.stdout.split("\n"):
                        if line.startswith("Name="):
                            cpu_name = line.split("=", 1)[1].strip()
                            break
        except Exception:
            pass
        
        return cpu_count or 1, cpu_name
        
    except Exception:
        return 1, "Unknown"


def _get_gpu_info() -> Tuple[Optional[str], Optional[str]]:
    """Detect GPU information"""
    try:
        if platform.system().lower() == "darwin":  # macOS
            return _detect_gpu_macos()
        elif platform.system().lower() == "linux":
            return _detect_gpu_linux()
        elif platform.system().lower() == "windows":
            return _detect_gpu_windows()
        else:
            return None, None
    except Exception:
        return None, None


def _detect_gpu_macos() -> Tuple[Optional[str], Optional[str]]:
    """Detect GPU on macOS"""
    try:
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            output = result.stdout.lower()
            if "nvidia" in output:
                return "NVIDIA GPU", "nvidia"
            elif "amd" in output or "radeon" in output:
                return "AMD GPU", "amd"
            elif "apple" in output or "m1" in output or "m2" in output or "m3" in output:
                return "Apple GPU", "apple"
            elif "intel" in output:
                return "Intel GPU", "intel"
        return None, None
    except Exception:
        return None, None


def _detect_gpu_linux() -> Tuple[Optional[str], Optional[str]]:
    """Detect GPU on Linux"""
    try:
        # Try nvidia-smi first
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            gpu_name = result.stdout.strip()
            return gpu_name, "nvidia"
        
        # Try lspci
        result = subprocess.run(
            ["lspci"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            output = result.stdout.lower()
            if "nvidia" in output:
                return "NVIDIA GPU", "nvidia"
            elif "amd" in output or "radeon" in output:
                return "AMD GPU", "amd"
            elif "intel" in output:
                return "Intel GPU", "intel"
        
        return None, None
    except Exception:
        return None, None


def _detect_gpu_windows() -> Tuple[Optional[str], Optional[str]]:
    """Detect GPU on Windows"""
    try:
        result = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "name", "/value"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            output = result.stdout.lower()
            if "nvidia" in output:
                return "NVIDIA GPU", "nvidia"
            elif "amd" in output or "radeon" in output:
                return "AMD GPU", "amd"
            elif "intel" in output:
                return "Intel GPU", "intel"
        return None, None
    except Exception:
        return None, None


def _find_python_versions() -> List[str]:
    """Find installed Python versions"""
    versions = []
    
    try:
        # Check current Python
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        versions.append(current_version)
        
        # Check PATH for other Python versions
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        for path_dir in path_dirs:
            try:
                for item in os.listdir(path_dir):
                    if item.startswith("python") and item[6:].replace(".", "").isdigit():
                        version = item[6:]  # Remove "python" prefix
                        if version not in versions:
                            versions.append(version)
            except (OSError, PermissionError):
                continue
        
        # Check common installation locations
        common_paths = [
            "/usr/bin/python*",
            "/usr/local/bin/python*",
            "/opt/homebrew/bin/python*",
            "C:\\Python*",
            "C:\\Program Files\\Python*",
            "C:\\Users\\*\\AppData\\Local\\Programs\\Python\\Python*"
        ]
        
        # This is a simplified check - in practice, you'd use glob patterns
        # For now, we'll rely on PATH detection
        
    except Exception:
        pass
    
    return sorted(list(set(versions)))


def _find_node_versions() -> List[str]:
    """Find installed Node.js versions"""
    versions = []
    
    try:
        # Check if node is in PATH
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().lstrip("v")
            versions.append(version)
        
        # Check for nvm installations
        nvm_path = Path.home() / ".nvm"
        if nvm_path.exists():
            try:
                for item in nvm_path.iterdir():
                    if item.is_dir() and item.name.startswith("v"):
                        version = item.name[1:]  # Remove "v" prefix
                        if version not in versions:
                            versions.append(version)
            except (OSError, PermissionError):
                pass
        
        # Check for fnm installations
        fnm_path = Path.home() / ".fnm"
        if fnm_path.exists():
            try:
                for item in fnm_path.iterdir():
                    if item.is_dir() and item.name.startswith("v"):
                        version = item.name[1:]  # Remove "v" prefix
                        if version not in versions:
                            versions.append(version)
            except (OSError, PermissionError):
                pass
        
    except Exception:
        pass
    
    return sorted(list(set(versions)))


def _find_package_managers() -> List[str]:
    """Find available package managers"""
    managers = []
    
    # List of package managers to check
    package_managers = [
        ("brew", "Homebrew"),
        ("apt", "APT"),
        ("yum", "YUM"),
        ("dnf", "DNF"),
        ("pacman", "Pacman"),
        ("choco", "Chocolatey"),
        ("winget", "Winget"),
        ("snap", "Snap"),
        ("flatpak", "Flatpak"),
        ("port", "MacPorts")
    ]
    
    for command, name in package_managers:
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0:
                managers.append(name)
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue
    
    return managers


def print_system_info() -> None:
    """Print system information in a formatted way"""
    info = get_system_info()
    
    print("🖥️  System Information")
    print("=" * 50)
    print(f"OS: {info.os_name.title()} {info.os_version}")
    print(f"Architecture: {info.architecture}")
    print(f"CPU: {info.cpu_name} ({info.cpu_cores} cores)")
    print(f"RAM: {info.ram_total_gb} GB total, {info.ram_available_gb} GB available")
    print(f"Disk: {info.disk_total_gb} GB total, {info.disk_free_gb} GB free")
    
    if info.gpu_name:
        print(f"GPU: {info.gpu_name} ({info.gpu_type})")
    else:
        print("GPU: Not detected")
    
    print(f"\n🐍 Python Versions: {', '.join(info.python_versions) if info.python_versions else 'None found'}")
    print(f"📦 Node Versions: {', '.join(info.node_versions) if info.node_versions else 'None found'}")
    print(f"🔧 Package Managers: {', '.join(info.package_managers) if info.package_managers else 'None found'}")


if __name__ == "__main__":
    print_system_info()
