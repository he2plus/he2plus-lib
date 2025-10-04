#!/usr/bin/env python3
"""
Basic usage example for he2plus library
"""

import sys
import os

# Add the parent directory to the path so we can import he2plus
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import he2plus


def main():
    """Main function demonstrating basic he2plus usage"""
    
    print("🚀 he2plus Basic Usage Example")
    print("=" * 40)
    
    # Initialize he2plus
    print("\n1. Initializing he2plus...")
    hp = he2plus.init()
    print("✅ he2plus initialized successfully!")
    
    # Get system information
    print("\n2. Getting system information...")
    system_info = hp.get_system_info()
    print(f"   Platform: {system_info.get('platform', 'Unknown')}")
    print(f"   Architecture: {system_info.get('architecture', 'Unknown')}")
    print(f"   Python Version: {system_info.get('python_version', 'Unknown')}")
    
    # Check dependencies
    print("\n3. Checking dependencies...")
    dependencies = hp.check_dependencies()
    print("   Available dependencies:")
    for dep, available in dependencies.items():
        status = "✅" if available else "❌"
        print(f"   {status} {dep}")
    
    # Get status
    print("\n4. Getting system status...")
    status = hp.get_status()
    print(f"   Version: {status['version']}")
    print(f"   Config loaded: {status['config_loaded']}")
    print(f"   Logger active: {status['logger_active']}")
    
    # Example: Install a package (commented out to avoid actual installation)
    print("\n5. Package installation example (commented out):")
    print("   # hp.install_package('requests', 'pip')")
    print("   # This would install the 'requests' package using pip")
    
    # Example: Setup development environment (commented out to avoid actual setup)
    print("\n6. Development environment setup example (commented out):")
    print("   # hp.setup_dev_environment('default')")
    print("   # This would set up a default development environment")
    
    print("\n🎉 Basic usage example completed!")
    print("\nNext steps:")
    print("   - Try: hp.setup_dev_environment()")
    print("   - Try: hp.install_package('package_name')")
    print("   - Check CLI: he2plus --help")


if __name__ == "__main__":
    main()
