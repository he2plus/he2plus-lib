"""Unit tests for system detection module."""

import pytest
from unittest.mock import patch, Mock
import platform

from he2plus.core.system import SystemProfiler, SystemInfo


class TestSystemProfiler:
    """Test SystemProfiler class."""
    
    def test_profile_basic_info_macos(self, mock_platform, mock_psutil):
        """Test basic system info detection on macOS."""
        with patch('subprocess.run') as mock_run:
            # Mock sw_vers command
            mock_run.return_value.stdout = "15.7.1\n"
            mock_run.return_value.returncode = 0
            
            profiler = SystemProfiler()
            system_info = profiler.profile()
            
            assert system_info.os_name == "macOS"
            assert system_info.os_version == "15.7.1"
            assert system_info.arch == "arm64"
    
    def test_profile_basic_info_linux(self, mock_psutil):
        """Test basic system info detection on Linux."""
        with patch('platform.system') as mock_system, \
             patch('platform.machine') as mock_machine, \
             patch('platform.platform') as mock_platform_func, \
             patch('builtins.open', create=True) as mock_open:
            
            mock_system.return_value = "Linux"
            mock_machine.return_value = "x86_64"
            mock_platform_func.return_value = "Linux-5.15.0-x86_64"
            
            # Mock /etc/os-release
            mock_open.return_value.__enter__.return_value = [
                'PRETTY_NAME="Ubuntu 22.04 LTS"\n'
            ]
            
            profiler = SystemProfiler()
            system_info = profiler.profile()
            
            assert system_info.os_name == "Linux"
            assert system_info.os_version == "Ubuntu 22.04 LTS"
            assert system_info.arch == "x86_64"
    
    def test_profile_basic_info_windows(self, mock_psutil):
        """Test basic system info detection on Windows."""
        with patch('platform.system') as mock_system, \
             patch('platform.machine') as mock_machine, \
             patch('platform.platform') as mock_platform_func, \
             patch('platform.win32_ver') as mock_win32_ver:
            
            mock_system.return_value = "Windows"
            mock_machine.return_value = "AMD64"
            mock_platform_func.return_value = "Windows-11-10.0.22621"
            mock_win32_ver.return_value = ("11", "10.0.22621", "SP0", "")
            
            profiler = SystemProfiler()
            system_info = profiler.profile()
            
            assert system_info.os_name == "Windows"
            assert system_info.os_version == "11"
            assert system_info.arch == "x86_64"
    
    def test_get_cpu_info_macos(self, mock_psutil):
        """Test CPU info detection on macOS."""
        with patch('platform.system') as mock_system, \
             patch('platform.processor') as mock_processor, \
             patch('subprocess.run') as mock_run:
            
            mock_system.return_value = "Darwin"
            mock_processor.return_value = "unknown"
            mock_run.return_value.stdout = "Apple M4\n"
            mock_run.return_value.returncode = 0
            
            profiler = SystemProfiler()
            cpu_name, cpu_cores = profiler._get_cpu_info()
            
            assert cpu_name == "Apple M4"
            assert cpu_cores == 10  # From mock_psutil fixture
    
    def test_get_cpu_info_linux(self, mock_psutil):
        """Test CPU info detection on Linux."""
        with patch('platform.system') as mock_system, \
             patch('platform.processor') as mock_processor, \
             patch('builtins.open', create=True) as mock_open:
            
            mock_system.return_value = "Linux"
            mock_processor.return_value = "unknown"
            
            # Mock /proc/cpuinfo
            mock_open.return_value.__enter__.return_value = [
                'model name\t: Intel Core i7-12700K\n'
            ]
            
            profiler = SystemProfiler()
            cpu_name, cpu_cores = profiler._get_cpu_info()
            
            assert cpu_name == "Intel Core i7-12700K"
            assert cpu_cores == 10  # From mock_psutil fixture
    
    def test_get_memory_info(self, mock_psutil):
        """Test memory info detection."""
        profiler = SystemProfiler()
        total_gb, available_gb = profiler._get_memory_info()
        
        assert total_gb == 16.0
        assert available_gb == 8.0
    
    def test_get_disk_info(self, mock_psutil):
        """Test disk info detection."""
        profiler = SystemProfiler()
        total_gb, free_gb = profiler._get_disk_info()
        
        assert total_gb == 1000.0
        assert free_gb == 900.0
    
    def test_get_gpu_info_macos(self, mock_psutil):
        """Test GPU info detection on macOS."""
        with patch('platform.system') as mock_system, \
             patch('subprocess.run') as mock_run:
            
            mock_system.return_value = "darwin"
            
            # Mock system_profiler output
            mock_run.return_value.stdout = '{"SPDisplaysDataType": [{"_name": "Apple M4", "sppci_model": "Apple"}]}'
            mock_run.return_value.returncode = 0
            
            profiler = SystemProfiler()
            gpu_name, gpu_vendor, cuda_available, metal_available = profiler._get_gpu_info()
            
            assert gpu_name == "Apple M4"
            assert gpu_vendor == "Apple"
            assert cuda_available is False
            assert metal_available is True
    
    def test_get_gpu_info_linux_nvidia(self, mock_psutil):
        """Test GPU info detection on Linux with NVIDIA."""
        with patch('platform.system') as mock_system, \
             patch('subprocess.run') as mock_run:
            
            mock_system.return_value = "linux"
            
            # Mock nvidia-smi output
            mock_run.return_value.stdout = "NVIDIA GeForce RTX 3080\n"
            mock_run.return_value.returncode = 0
            
            profiler = SystemProfiler()
            gpu_name, gpu_vendor, cuda_available, metal_available = profiler._get_gpu_info()
            
            assert gpu_name == "NVIDIA GeForce RTX 3080"
            assert gpu_vendor == "NVIDIA"
            assert cuda_available is True
            assert metal_available is False
    
    def test_detect_package_managers(self, mock_shutil):
        """Test package manager detection."""
        # Mock shutil.which to return True for some package managers
        def mock_which(cmd):
            return cmd if cmd in ["brew", "pip", "npm"] else None
        
        mock_shutil.side_effect = mock_which
        
        profiler = SystemProfiler()
        managers = profiler._detect_package_managers()
        
        assert "brew" in managers
        assert "pip" in managers
        assert "npm" in managers
        assert "unknown_manager" not in managers
    
    def test_detect_languages(self, mock_subprocess):
        """Test language detection."""
        # Mock subprocess.run for different languages
        def mock_run(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            
            if "python3" in cmd:
                mock_result.stdout = "Python 3.13.7\n"
            elif "node" in cmd:
                mock_result.stdout = "v24.9.0\n"
            elif "rustc" in cmd:
                mock_result.stdout = "rustc 1.75.0\n"
            elif "go" in cmd:
                mock_result.stdout = "go version go1.21.0\n"
            elif "java" in cmd:
                mock_result.stderr = 'java version "17.0.1"\n'
            else:
                mock_result.returncode = 1
            
            return mock_result
        
        mock_subprocess.side_effect = mock_run
        
        profiler = SystemProfiler()
        languages = profiler._detect_languages()
        
        assert "python" in languages
        assert languages["python"] == "3.13.7"
        assert "node" in languages
        assert languages["node"] == "v24.9.0"
    
    def test_get_install_methods_macos(self, mock_shutil):
        """Test installation methods detection on macOS."""
        def mock_which(cmd):
            return cmd if cmd in ["brew", "pip", "npm", "docker"] else None
        
        mock_shutil.side_effect = mock_which
        
        with patch('platform.system') as mock_system:
            mock_system.return_value = "darwin"
            
            profiler = SystemProfiler()
            methods = profiler.get_install_methods()
            
            assert "brew" in methods["system"]
            assert "pip" in methods["language_specific"]
            assert "npm" in methods["language_specific"]
            assert "docker" in methods["containers"]
    
    def test_get_install_methods_linux(self, mock_shutil):
        """Test installation methods detection on Linux."""
        def mock_which(cmd):
            return cmd if cmd in ["apt", "pip", "npm", "docker"] else None
        
        mock_shutil.side_effect = mock_which
        
        with patch('platform.system') as mock_system:
            mock_system.return_value = "linux"
            
            profiler = SystemProfiler()
            methods = profiler.get_install_methods()
            
            assert "apt" in methods["system"]
            assert "pip" in methods["language_specific"]
            assert "npm" in methods["language_specific"]
            assert "docker" in methods["containers"]
    
    def test_get_install_methods_windows(self, mock_shutil):
        """Test installation methods detection on Windows."""
        def mock_which(cmd):
            return cmd if cmd in ["choco", "winget", "pip", "npm", "docker"] else None
        
        mock_shutil.side_effect = mock_which
        
        with patch('platform.system') as mock_system:
            mock_system.return_value = "windows"
            
            profiler = SystemProfiler()
            methods = profiler.get_install_methods()
            
            assert "choco" in methods["system"]
            assert "winget" in methods["system"]
            assert "pip" in methods["language_specific"]
            assert "npm" in methods["language_specific"]
            assert "docker" in methods["containers"]


class TestSystemInfo:
    """Test SystemInfo dataclass."""
    
    def test_system_info_creation(self):
        """Test SystemInfo creation with default values."""
        system_info = SystemInfo(
            os_name="macOS",
            os_version="15.7.1",
            arch="arm64",
            platform="macOS-15.7.1-arm64",
            cpu_name="Apple M4",
            cpu_cores=10,
            ram_total_gb=16.0,
            ram_available_gb=8.0,
            disk_total_gb=1000.0,
            disk_free_gb=900.0
        )
        
        assert system_info.os_name == "macOS"
        assert system_info.os_version == "15.7.1"
        assert system_info.arch == "arm64"
        assert system_info.cpu_name == "Apple M4"
        assert system_info.cpu_cores == 10
        assert system_info.ram_total_gb == 16.0
        assert system_info.ram_available_gb == 8.0
        assert system_info.disk_total_gb == 1000.0
        assert system_info.disk_free_gb == 900.0
        assert system_info.package_managers == []
        assert system_info.languages == {}
    
    def test_system_info_with_gpu(self):
        """Test SystemInfo creation with GPU information."""
        system_info = SystemInfo(
            os_name="macOS",
            os_version="15.7.1",
            arch="arm64",
            platform="macOS-15.7.1-arm64",
            cpu_name="Apple M4",
            cpu_cores=10,
            ram_total_gb=16.0,
            ram_available_gb=8.0,
            disk_total_gb=1000.0,
            disk_free_gb=900.0,
            gpu_name="Apple M4",
            gpu_vendor="Apple",
            cuda_available=False,
            metal_available=True
        )
        
        assert system_info.gpu_name == "Apple M4"
        assert system_info.gpu_vendor == "Apple"
        assert system_info.cuda_available is False
        assert system_info.metal_available is True
    
    def test_system_info_with_package_managers(self):
        """Test SystemInfo creation with package managers."""
        system_info = SystemInfo(
            os_name="macOS",
            os_version="15.7.1",
            arch="arm64",
            platform="macOS-15.7.1-arm64",
            cpu_name="Apple M4",
            cpu_cores=10,
            ram_total_gb=16.0,
            ram_available_gb=8.0,
            disk_total_gb=1000.0,
            disk_free_gb=900.0,
            package_managers=["brew", "pip", "npm"],
            languages={"python": "3.13.7", "node": "v24.9.0"}
        )
        
        assert system_info.package_managers == ["brew", "pip", "npm"]
        assert system_info.languages == {"python": "3.13.7", "node": "v24.9.0"}
