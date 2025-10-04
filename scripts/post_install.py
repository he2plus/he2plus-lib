#!/usr/bin/env python3
"""
Post-installation script for he2plus
This script runs automatically after pip install he2plus
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Main post-installation function"""
    print("🚀 he2plus installation completed!")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print("✅ Detected virtual environment - good practice!")
    else:
        print("⚠️  Not in a virtual environment. Consider using one for better dependency management.")
    
    # Show next steps
    print("\n📋 Next Steps:")
    print("1. Run 'he2plus welcome' to start the interactive setup")
    print("2. Run 'he2plus status' to check your system")
    print("3. Run 'he2plus commands' to see shell commands reference")
    print("4. Run 'he2plus --help' to see all available commands")
    
    print("\n🎯 Quick Start:")
    print("   he2plus welcome  # Interactive setup")
    print("   he2plus status   # System check")
    
    print("\n📚 Documentation:")
    print("   GitHub: https://github.com/he2plus/he2plus")
    print("   Twitter: https://twitter.com/he2plus")
    
    print("\n💡 Pro Tip:")
    print("   This library was built by a dev frustrated by dependency issues.")
    print("   Let's make your development experience amazing! 🎉")
    
    # Try to run welcome automatically (optional)
    try:
        response = input("\n🤔 Would you like to run the welcome setup now? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            print("\n🚀 Starting welcome setup...")
            subprocess.run([sys.executable, '-m', 'he2plus', 'welcome'], check=False)
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled. Run 'he2plus welcome' anytime to start!")
    except Exception as e:
        print(f"\n⚠️  Could not start welcome setup: {e}")
        print("   You can run 'he2plus welcome' manually anytime.")


if __name__ == "__main__":
    main()
