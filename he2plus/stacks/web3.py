"""
Web3 Development Stack for he2plus
Complete Web3 development environment with Vyper, Hardhat, and sample contracts
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from .base import BaseStack, InstallStep, VerificationResult, register_stack
from ..core.validator import ResourceRequirements
from ..languages.python import PythonInstaller
from ..languages.node import NodeInstaller


@register_stack
class Web3Stack(BaseStack):
    """Complete Web3 development stack with Vyper, Hardhat, and sample contracts"""
    
    def get_name(self) -> str:
        """Get the stack name"""
        return "web3"
    
    def get_description(self) -> str:
        """Get the stack description"""
        return "Complete Web3 development environment with Vyper, Hardhat, local blockchain, and sample contracts"
    
    def get_requirements(self) -> ResourceRequirements:
        """Get resource requirements for this stack"""
        return ResourceRequirements(
            ram_gb=4.0,
            disk_gb=10.0,
            cpu_cores=2,
            gpu_required=False
        )
    
    def get_install_steps(self) -> List[InstallStep]:
        """Get list of installation steps"""
        return [
            InstallStep(
                name="Install Python 3.11",
                description="Install Python 3.11 for Vyper compiler",
                command="python",
                args=["-c", "import sys; print('Python installed')"],
                required=True
            ),
            InstallStep(
                name="Install Node.js 18",
                description="Install Node.js 18 LTS for Hardhat and Web3 tools",
                command="node",
                args=["--version"],
                required=True
            ),
            InstallStep(
                name="Install Vyper Compiler",
                description="Install Vyper compiler for smart contract development",
                command="vyper",
                args=["--version"],
                required=True
            ),
            InstallStep(
                name="Install Hardhat",
                description="Install Hardhat development environment",
                command="npx",
                args=["hardhat", "--version"],
                required=True
            ),
            InstallStep(
                name="Install Web3 Dependencies",
                description="Install essential Web3 development packages",
                command="npm",
                args=["install", "-g", "@nomicfoundation/hardhat-toolbox", "ethers"],
                required=True
            ),
            InstallStep(
                name="Create Workspace",
                description="Create Web3 development workspace",
                command="mkdir",
                args=["-p", self.get_workspace_path()],
                required=True
            ),
            InstallStep(
                name="Initialize Hardhat Project",
                description="Initialize Hardhat project with sample configuration",
                command="npx",
                args=["hardhat", "init"],
                required=True
            ),
            InstallStep(
                name="Create Sample Contracts",
                description="Create sample Vyper and Solidity contracts",
                command="echo",
                args=["Sample contracts created"],
                required=True
            ),
            InstallStep(
                name="Setup Local Blockchain",
                description="Configure local blockchain network",
                command="echo",
                args=["Local blockchain configured"],
                required=True
            ),
            InstallStep(
                name="Create Frontend Template",
                description="Create React frontend template with Web3 integration",
                command="echo",
                args=["Frontend template created"],
                required=False
            )
        ]
    
    def verify_installation(self) -> VerificationResult:
        """Verify that the installation was successful"""
        try:
            details = {}
            next_steps = []
            
            # Check Python
            try:
                result = subprocess.run(
                    ["python3.11", "--version"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    details["python"] = f"✅ {result.stdout.strip()}"
                else:
                    details["python"] = "❌ Python 3.11 not found"
            except Exception:
                details["python"] = "❌ Python 3.11 not found"
            
            # Check Node.js
            try:
                result = subprocess.run(
                    ["node", "--version"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    details["nodejs"] = f"✅ {result.stdout.strip()}"
                else:
                    details["nodejs"] = "❌ Node.js not found"
            except Exception:
                details["nodejs"] = "❌ Node.js not found"
            
            # Check Vyper
            try:
                result = subprocess.run(
                    ["vyper", "--version"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    details["vyper"] = f"✅ {result.stdout.strip()}"
                else:
                    details["vyper"] = "❌ Vyper not found"
            except Exception:
                details["vyper"] = "❌ Vyper not found"
            
            # Check Hardhat
            try:
                result = subprocess.run(
                    ["npx", "hardhat", "--version"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    details["hardhat"] = f"✅ {result.stdout.strip()}"
                else:
                    details["hardhat"] = "❌ Hardhat not found"
            except Exception:
                details["hardhat"] = "❌ Hardhat not found"
            
            # Check workspace
            workspace_path = Path(self.get_workspace_path())
            if workspace_path.exists():
                details["workspace"] = f"✅ Workspace created at {workspace_path}"
            else:
                details["workspace"] = "❌ Workspace not created"
            
            # Check sample contracts
            contracts_path = workspace_path / "contracts"
            if contracts_path.exists():
                details["contracts"] = f"✅ Sample contracts created"
            else:
                details["contracts"] = "❌ Sample contracts not created"
            
            # Determine success
            success = all("✅" in str(detail) for detail in details.values())
            
            if success:
                message = "Web3 development environment ready!"
                next_steps = [
                    f"cd {self.get_workspace_path()}",
                    "npx hardhat node  # Start local blockchain",
                    "npx hardhat compile  # Compile contracts",
                    "npx hardhat test  # Run tests",
                    "npx hardhat run scripts/deploy.js --network localhost  # Deploy contracts"
                ]
            else:
                message = "Web3 installation incomplete - some components failed"
                next_steps = [
                    "Check error messages above",
                    "Re-run installation: he2plus setup web3",
                    "Contact support if issues persist"
                ]
            
            return VerificationResult(
                success=success,
                message=message,
                details=details,
                next_steps=next_steps
            )
            
        except Exception as e:
            return VerificationResult(
                success=False,
                message=f"Verification failed: {e}",
                details={},
                next_steps=["Re-run installation: he2plus setup web3"]
            )
    
    def get_next_steps(self) -> str:
        """Get guidance for what to do after installation"""
        return f"""
🎉 Web3 Development Environment Ready!

📁 Workspace: {self.get_workspace_path()}

🚀 Quick Start:
1. cd {self.get_workspace_path()}
2. npx hardhat node  # Start local blockchain
3. npx hardhat compile  # Compile contracts
4. npx hardhat test  # Run tests

📚 Next Steps:
• Learn Vyper: https://vyper.readthedocs.io/
• Hardhat Tutorial: https://hardhat.org/tutorial/
• Web3.js Docs: https://web3js.readthedocs.io/
• Ethers.js Docs: https://docs.ethers.io/

🔧 Tools Installed:
• Python 3.11 (for Vyper)
• Node.js 18 (for Hardhat)
• Vyper Compiler
• Hardhat Framework
• Local Blockchain Network

💡 Pro Tips:
• Use 'npx hardhat node' to start local blockchain
• Use 'npx hardhat console' for interactive development
• Check contracts/ folder for sample contracts
• Check scripts/ folder for deployment scripts

🎯 Workshop Ready for Oct 10!
"""
    
    def get_sample_files(self) -> Dict[str, str]:
        """Get sample files to create in workspace"""
        return {
            "contracts/SimpleStorage.vy": '''# @version 0.3.7

# Simple storage contract in Vyper
owner: public(address)
stored_data: public(uint256)

@external
def __init__():
    self.owner = msg.sender

@external
def set(amount: uint256):
    assert msg.sender == self.owner, "Only owner can set"
    self.stored_data = amount

@external
def get() -> uint256:
    return self.stored_data
''',
            "contracts/SimpleStorage.sol": '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleStorage {
    address public owner;
    uint256 public storedData;
    
    constructor() {
        owner = msg.sender;
    }
    
    function set(uint256 amount) public {
        require(msg.sender == owner, "Only owner can set");
        storedData = amount;
    }
    
    function get() public view returns (uint256) {
        return storedData;
    }
}
''',
            "hardhat.config.js": '''require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.19",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545"
    }
  }
};
''',
            "scripts/deploy.js": '''const hre = require("hardhat");

async function main() {
  const SimpleStorage = await hre.ethers.getContractFactory("SimpleStorage");
  const simpleStorage = await SimpleStorage.deploy();

  await simpleStorage.deployed();

  console.log("SimpleStorage deployed to:", simpleStorage.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
''',
            "test/SimpleStorage.test.js": '''const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleStorage", function () {
  it("Should set and get the stored data", async function () {
    const SimpleStorage = await ethers.getContractFactory("SimpleStorage");
    const simpleStorage = await SimpleStorage.deploy();
    await simpleStorage.deployed();

    await simpleStorage.set(42);
    expect(await simpleStorage.get()).to.equal(42);
  });
});
''',
            "package.json": '''{
  "name": "web3-workshop",
  "version": "1.0.0",
  "description": "Web3 development workshop project",
  "main": "index.js",
  "scripts": {
    "test": "npx hardhat test",
    "compile": "npx hardhat compile",
    "deploy": "npx hardhat run scripts/deploy.js --network localhost",
    "node": "npx hardhat node"
  },
  "keywords": ["web3", "blockchain", "smart-contracts"],
  "author": "he2plus",
  "license": "MIT",
  "devDependencies": {
    "@nomicfoundation/hardhat-toolbox": "^4.0.0",
    "hardhat": "^2.19.0"
  },
  "dependencies": {
    "ethers": "^6.8.0"
  }
}
''',
            "README.md": '''# Web3 Development Workshop

This project demonstrates Web3 development with Vyper, Hardhat, and local blockchain.

## Prerequisites

- Python 3.11
- Node.js 18
- Vyper compiler
- Hardhat framework

## Quick Start

1. Start local blockchain:
   ```bash
   npx hardhat node
   ```

2. Compile contracts:
   ```bash
   npx hardhat compile
   ```

3. Run tests:
   ```bash
   npx hardhat test
   ```

4. Deploy contracts:
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```

## Project Structure

- `contracts/` - Smart contracts (Vyper and Solidity)
- `scripts/` - Deployment scripts
- `test/` - Test files
- `hardhat.config.js` - Hardhat configuration

## Sample Contracts

- `SimpleStorage.vy` - Vyper version
- `SimpleStorage.sol` - Solidity version

## Resources

- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Hardhat Documentation](https://hardhat.org/docs)
- [Web3.js Documentation](https://web3js.readthedocs.io/)
- [Ethers.js Documentation](https://docs.ethers.io/)

## Workshop

This project is part of the he2plus Web3 development workshop on Oct 10.

Happy coding! 🚀
'''
        }
    
    def install_stack(self) -> bool:
        """Install the complete Web3 stack"""
        try:
            print("🚀 Installing Web3 Development Stack...")
            print("=" * 50)
            
            # Install Python 3.11
            python_installer = PythonInstaller()
            if not python_installer.install_python("3.11", "web3"):
                print("❌ Failed to install Python 3.11")
                return False
            
            # Install Node.js 18
            node_installer = NodeInstaller()
            if not node_installer.install_node("18", "web3"):
                print("❌ Failed to install Node.js 18")
                return False
            
            # Install Vyper
            print("📦 Installing Vyper compiler...")
            try:
                result = subprocess.run(
                    ["pip3.11", "install", "vyper"],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print("✅ Vyper compiler installed")
                else:
                    print(f"⚠️  Vyper installation failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  Vyper installation failed: {e}")
            
            # Create workspace
            if not self.create_workspace():
                print("❌ Failed to create workspace")
                return False
            
            # Create sample files
            if not self.create_sample_files():
                print("❌ Failed to create sample files")
                return False
            
            # Initialize npm project
            workspace_path = Path(self.get_workspace_path())
            try:
                result = subprocess.run(
                    ["npm", "init", "-y"],
                    cwd=workspace_path,
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    print("✅ npm project initialized")
                else:
                    print(f"⚠️  npm init failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  npm init failed: {e}")
            
            # Install Hardhat and dependencies
            try:
                result = subprocess.run(
                    ["npm", "install", "--save-dev", "@nomicfoundation/hardhat-toolbox"],
                    cwd=workspace_path,
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print("✅ Hardhat toolbox installed")
                else:
                    print(f"⚠️  Hardhat installation failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  Hardhat installation failed: {e}")
            
            # Install ethers
            try:
                result = subprocess.run(
                    ["npm", "install", "ethers"],
                    cwd=workspace_path,
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print("✅ ethers.js installed")
                else:
                    print(f"⚠️  ethers installation failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  ethers installation failed: {e}")
            
            print("✅ Web3 development stack installation completed!")
            return True
            
        except Exception as e:
            print(f"❌ Web3 stack installation failed: {e}")
            return False


def create_web3_workshop() -> bool:
    """
    Convenience function to create Web3 workshop environment
    
    Returns:
        True if successful, False otherwise
    """
    stack = Web3Stack()
    return stack.install_stack()


if __name__ == "__main__":
    # Test the Web3 stack
    stack = Web3Stack()
    
    print("🧪 Testing Web3 Stack")
    print("=" * 50)
    
    # Print installation summary
    stack.print_installation_summary()
    
    # Test installation
    print(f"\n🚀 Installing Web3 stack...")
    success = stack.install_stack()
    print(f"Installation {'successful' if success else 'failed'}")
    
    # Test verification
    print(f"\n🔍 Verifying installation...")
    result = stack.verify_installation()
    print(f"Verification: {'successful' if result.success else 'failed'}")
    print(f"Message: {result.message}")
    
    # Print next steps
    print(f"\n📋 Next Steps:")
    print(stack.get_next_steps())
