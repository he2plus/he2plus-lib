"""Pytest configuration and fixtures for he2plus tests."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import os

from he2plus.core.system import SystemInfo
from he2plus.core.validator import ProfileRequirements
from he2plus.profiles.base import Component, VerificationStep, SampleProject
from he2plus.profiles.web3.solidity import SolidityProfile

# Test directories
TEST_TEMP_DIR = Path("/Volumes/T7/Projects/Github/he2plus/tests/temp")
TEST_FIXTURES_DIR = Path("/Volumes/T7/Projects/Github/he2plus/tests/fixtures")

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment with T7 storage."""
    # Ensure test directories exist
    TEST_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    TEST_FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Set environment variables for testing
    os.environ["HE2PLUS_TEST_MODE"] = "true"
    os.environ["HE2PLUS_TEMP_DIR"] = str(TEST_TEMP_DIR)
    
    yield
    
    # Cleanup after all tests
    if TEST_TEMP_DIR.exists():
        shutil.rmtree(TEST_TEMP_DIR)
        TEST_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Remove test environment variables
    os.environ.pop("HE2PLUS_TEST_MODE", None)
    os.environ.pop("HE2PLUS_TEMP_DIR", None)

@pytest.fixture
def mock_system_info():
    """Mock system information for testing."""
    return SystemInfo(
        os_name="macOS",
        os_version="15.7.1",
        arch="arm64",
        platform="macOS-15.7.1-arm64-arm-64bit",
        cpu_name="Apple M4",
        cpu_cores=10,
        ram_total_gb=16.0,
        ram_available_gb=8.0,
        disk_total_gb=1000.0,
        disk_free_gb=900.0,
        gpu_name="Apple M4",
        gpu_vendor="Apple",
        cuda_available=False,
        metal_available=True,
        package_managers=["brew", "pip", "npm"],
        languages={"python": "3.13.7", "node": "v24.9.0"}
    )

@pytest.fixture
def mock_system_info_linux():
    """Mock Linux system information for testing."""
    return SystemInfo(
        os_name="Linux",
        os_version="Ubuntu 22.04",
        arch="x86_64",
        platform="Linux-5.15.0-x86_64-with-glibc2.35",
        cpu_name="Intel Core i7-12700K",
        cpu_cores=12,
        ram_total_gb=32.0,
        ram_available_gb=16.0,
        disk_total_gb=2000.0,
        disk_free_gb=1800.0,
        gpu_name="NVIDIA GeForce RTX 3080",
        gpu_vendor="NVIDIA",
        cuda_available=True,
        metal_available=False,
        package_managers=["apt", "pip", "npm"],
        languages={"python": "3.10.12", "node": "v18.19.0"}
    )

@pytest.fixture
def mock_system_info_windows():
    """Mock Windows system information for testing."""
    return SystemInfo(
        os_name="Windows",
        os_version="11",
        arch="x86_64",
        platform="Windows-11-10.0.22621-SP0",
        cpu_name="Intel Core i9-12900K",
        cpu_cores=16,
        ram_total_gb=64.0,
        ram_available_gb=32.0,
        disk_total_gb=4000.0,
        disk_free_gb=3500.0,
        gpu_name="NVIDIA GeForce RTX 4090",
        gpu_vendor="NVIDIA",
        cuda_available=True,
        metal_available=False,
        package_managers=["choco", "winget", "pip", "npm"],
        languages={"python": "3.11.8", "node": "v20.10.0"}
    )

@pytest.fixture
def mock_profile_requirements():
    """Mock profile requirements for testing."""
    return ProfileRequirements(
        ram_gb=4.0,
        disk_gb=10.0,
        cpu_cores=2,
        gpu_required=False,
        internet_required=True,
        download_size_mb=500.0
    )

@pytest.fixture
def mock_profile_requirements_gpu():
    """Mock GPU-required profile requirements for testing."""
    return ProfileRequirements(
        ram_gb=8.0,
        disk_gb=20.0,
        cpu_cores=4,
        gpu_required=True,
        gpu_vendor="NVIDIA",
        cuda_required=True,
        internet_required=True,
        download_size_mb=2000.0
    )

@pytest.fixture
def mock_component():
    """Mock component for testing."""
    return Component(
        id="test.component",
        name="Test Component",
        description="A test component",
        category="tool",
        version="1.0.0",
        download_size_mb=10.0,
        install_time_minutes=5,
        install_methods=["test"],
        verify_command="test --version",
        verify_expected_output="1.0.0"
    )

@pytest.fixture
def mock_verification_step():
    """Mock verification step for testing."""
    return VerificationStep(
        name="Test Verification",
        command="test --version",
        expected_output="1.0.0",
        timeout_seconds=30
    )

@pytest.fixture
def mock_sample_project():
    """Mock sample project for testing."""
    return SampleProject(
        name="Test Project",
        description="A test project",
        type="git_clone",
        source="https://github.com/test/test-project.git",
        directory="~/test-project",
        setup_commands=["cd ~/test-project", "npm install"],
        next_steps=["Run tests", "Deploy"]
    )

@pytest.fixture
def solidity_profile():
    """Solidity profile for testing."""
    return SolidityProfile()

@pytest.fixture
def temp_dir():
    """Temporary directory for testing (on T7)."""
    temp_path = TEST_TEMP_DIR / "test_temp"
    temp_path.mkdir(parents=True, exist_ok=True)
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)

@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing."""
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def mock_shutil():
    """Mock shutil for testing."""
    with patch('shutil.which') as mock_which:
        yield mock_which

@pytest.fixture
def mock_platform():
    """Mock platform for testing."""
    with patch('platform.system') as mock_system, \
         patch('platform.machine') as mock_machine, \
         patch('platform.platform') as mock_platform_func:
        
        mock_system.return_value = "Darwin"
        mock_machine.return_value = "arm64"
        mock_platform_func.return_value = "macOS-15.7.1-arm64-arm-64bit"
        
        yield {
            'system': mock_system,
            'machine': mock_machine,
            'platform': mock_platform_func
        }

@pytest.fixture
def mock_psutil():
    """Mock psutil for testing."""
    with patch('psutil.virtual_memory') as mock_memory, \
         patch('psutil.disk_usage') as mock_disk, \
         patch('psutil.cpu_count') as mock_cpu:
        
        # Mock memory
        mock_memory.return_value.total = 16 * 1024**3  # 16 GB
        mock_memory.return_value.available = 8 * 1024**3  # 8 GB
        
        # Mock disk
        mock_disk.return_value.total = 1000 * 1024**3  # 1000 GB
        mock_disk.return_value.free = 900 * 1024**3  # 900 GB
        
        # Mock CPU
        mock_cpu.return_value = 10
        
        yield {
            'memory': mock_memory,
            'disk': mock_disk,
            'cpu': mock_cpu
        }
