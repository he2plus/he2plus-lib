"""
Web3 Solidity development profile for he2plus.

This profile sets up a complete Ethereum smart contract development
environment with Hardhat, Foundry, and all necessary tools.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import structlog

from ..base import BaseProfile, Component, VerificationStep, SampleProject, ProfileRequirements

logger = structlog.get_logger(__name__)


class SolidityProfile(BaseProfile):
    """Solidity smart contract development environment."""
    
    def _initialize_profile(self):
        """Initialize the Solidity development profile."""
        self.id = "web3-solidity"
        self.name = "Solidity Development"
        self.description = "Ethereum smart contract development with Hardhat and Foundry"
        self.category = "web3"
        self.version = "1.0.0"
        
        # Set requirements
        self.requirements = ProfileRequirements(
            ram_gb=4.0,
            disk_gb=10.0,
            cpu_cores=2,
            gpu_required=False,
            internet_required=True,
            download_size_mb=500.0,
            supported_archs=["x86_64", "arm64"]
        )
        
        # Define components
        self.components = [
            # Core language
            Component(
                id="language.node.18",
                name="Node.js 18 LTS",
                description="JavaScript runtime for Hardhat and development tools",
                category="language",
                version="18.19.0",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["nvm", "brew", "apt", "choco", "official"],
                verify_command="node --version",
                verify_expected_output="v18"
            ),
            
            # Package manager
            Component(
                id="tool.npm",
                name="npm",
                description="Node.js package manager",
                category="tool",
                version="10.2.3",
                download_size_mb=0.0,
                install_time_minutes=1,
                depends_on=["language.node.18"],
                install_methods=["included"],
                verify_command="npm --version",
                verify_expected_output="10."
            ),
            
            # Git
            Component(
                id="tool.git",
                name="Git",
                description="Version control system",
                category="tool",
                version="2.39.0",
                download_size_mb=20.0,
                install_time_minutes=3,
                install_methods=["brew", "apt", "choco", "official"],
                verify_command="git --version",
                verify_expected_output="git version"
            ),
            
            # Hardhat
            Component(
                id="framework.hardhat",
                name="Hardhat",
                description="Ethereum development environment",
                category="framework",
                version="2.19.4",
                download_size_mb=100.0,
                install_time_minutes=5,
                depends_on=["language.node.18", "tool.npm"],
                install_methods=["npm"],
                verify_command="npx hardhat --version",
                verify_expected_output="2."
            ),
            
            # Foundry
            Component(
                id="tool.foundry",
                name="Foundry",
                description="Fast, portable and modular toolkit for Ethereum application development",
                category="tool",
                version="0.2.0",
                download_size_mb=200.0,
                install_time_minutes=10,
                install_methods=["foundryup", "brew", "official"],
                verify_command="forge --version",
                verify_expected_output="forge"
            ),
            
            # Solidity compiler
            Component(
                id="tool.solc",
                name="Solidity Compiler",
                description="Solidity compiler for smart contracts",
                category="tool",
                version="0.8.22",
                download_size_mb=50.0,
                install_time_minutes=3,
                depends_on=["framework.hardhat"],
                install_methods=["npm", "brew", "apt"],
                verify_command="npx solc --version",
                verify_expected_output="0.8."
            ),
            
            # OpenZeppelin Contracts
            Component(
                id="package.openzeppelin",
                name="OpenZeppelin Contracts",
                description="Secure smart contract library",
                category="package",
                version="5.0.0",
                download_size_mb=10.0,
                install_time_minutes=2,
                depends_on=["framework.hardhat"],
                install_methods=["npm"],
                verify_command="npm list @openzeppelin/contracts",
                verify_expected_output="@openzeppelin/contracts"
            ),
            
            # ethers.js
            Component(
                id="package.ethers",
                name="ethers.js",
                description="JavaScript library for Ethereum",
                category="package",
                version="6.9.0",
                download_size_mb=5.0,
                install_time_minutes=1,
                depends_on=["framework.hardhat"],
                install_methods=["npm"],
                verify_command="npm list ethers",
                verify_expected_output="ethers"
            ),
            
            # viem (alternative to ethers.js)
            Component(
                id="package.viem",
                name="viem",
                description="TypeScript interface for Ethereum",
                category="package",
                version="1.19.0",
                download_size_mb=3.0,
                install_time_minutes=1,
                depends_on=["framework.hardhat"],
                install_methods=["npm"],
                verify_command="npm list viem",
                verify_expected_output="viem"
            ),
            
            # Alchemy SDK (optional)
            Component(
                id="package.alchemy",
                name="Alchemy SDK",
                description="Web3 development platform SDK",
                category="package",
                version="3.0.0",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=["framework.hardhat"],
                install_methods=["npm"],
                verify_command="npm list alchemy-sdk",
                verify_expected_output="alchemy-sdk"
            ),
            
            # The Graph CLI (optional)
            Component(
                id="tool.graph",
                name="The Graph CLI",
                description="Command line interface for The Graph protocol",
                category="tool",
                version="0.58.0",
                download_size_mb=20.0,
                install_time_minutes=3,
                depends_on=["language.node.18"],
                install_methods=["npm"],
                verify_command="graph --version",
                verify_expected_output="0.58."
            )
        ]
        
        # Define verification steps
        self.verification_steps = [
            VerificationStep(
                name="Node.js Version",
                command="node --version",
                expected_output="v18",
                timeout_seconds=10
            ),
            VerificationStep(
                name="npm Version",
                command="npm --version",
                contains_text="10.",
                timeout_seconds=10
            ),
            VerificationStep(
                name="Git Version",
                command="git --version",
                contains_text="git version",
                timeout_seconds=10
            ),
            VerificationStep(
                name="Hardhat Installation",
                command="npx hardhat --version",
                contains_text="2.",
                timeout_seconds=30
            ),
            VerificationStep(
                name="Foundry Installation",
                command="forge --version",
                contains_text="forge",
                timeout_seconds=30
            ),
            VerificationStep(
                name="Solidity Compiler",
                command="npx solc --version",
                contains_text="0.8.",
                timeout_seconds=30
            ),
            VerificationStep(
                name="OpenZeppelin Contracts",
                command="npm list @openzeppelin/contracts",
                contains_text="@openzeppelin/contracts",
                timeout_seconds=30
            ),
            VerificationStep(
                name="ethers.js",
                command="npm list ethers",
                contains_text="ethers",
                timeout_seconds=30
            ),
            VerificationStep(
                name="viem",
                command="npm list viem",
                contains_text="viem",
                timeout_seconds=30
            ),
            VerificationStep(
                name="Alchemy SDK",
                command="npm list alchemy-sdk",
                contains_text="alchemy-sdk",
                timeout_seconds=30
            ),
            VerificationStep(
                name="The Graph CLI",
                command="graph --version",
                contains_text="0.58.",
                timeout_seconds=30
            )
        ]
        
        # Define sample project
        self.sample_project = SampleProject(
            name="Hardhat Starter Kit",
            description="A complete Hardhat project with sample contracts and tests",
            type="git_clone",
            source="https://github.com/he2plus/hardhat-starter-kit.git",
            directory="~/solidity-project",
            setup_commands=[
                "cd ~/solidity-project",
                "npm install",
                "npx hardhat compile",
                "npx hardhat test"
            ],
            next_steps=[
                "Start local blockchain: npx hardhat node",
                "Deploy contracts: npx hardhat run scripts/deploy.js --network localhost",
                "Run tests: npx hardhat test",
                "Compile contracts: npx hardhat compile"
            ]
        )
        
        # Define next steps
        self.next_steps = [
            "🎉 Solidity development environment ready!",
            "",
            "Next steps:",
            "  1. Create new Hardhat project:",
            "     npx hardhat init",
            "",
            "  2. Or use our starter template:",
            "     git clone https://github.com/he2plus/hardhat-starter-kit",
            "     cd hardhat-starter-kit",
            "     npm install",
            "",
            "  3. Compile contracts:",
            "     npx hardhat compile",
            "",
            "  4. Run tests:",
            "     npx hardhat test",
            "",
            "  5. Start local blockchain:",
            "     npx hardhat node",
            "",
            "  6. Deploy to local network:",
            "     npx hardhat run scripts/deploy.js --network localhost",
            "",
            "  7. Use Foundry for advanced development:",
            "     forge init my-project",
            "     cd my-project",
            "     forge build",
            "     forge test",
            "",
            "📖 Documentation: https://he2plus.dev/docs/profiles/web3-solidity",
            "💬 Get help: https://discord.gg/he2plus",
            "🌟 Star us on GitHub: https://github.com/prakhar/he2plus"
        ]
    
    def get_installation_plan(self) -> Dict[str, Any]:
        """Get detailed installation plan for Solidity development."""
        plan = super().get_installation_plan()
        
        # Add Web3-specific information
        plan["web3_specific"] = {
            "blockchain_networks": [
                "Hardhat Network (local)",
                "Ethereum Mainnet",
                "Ethereum Sepolia (testnet)",
                "Polygon Mumbai (testnet)",
                "Arbitrum Goerli (testnet)"
            ],
            "development_tools": [
                "Hardhat (development environment)",
                "Foundry (testing and deployment)",
                "Remix IDE (browser-based development)",
                "VS Code (with Solidity extension)",
                "Truffle (alternative framework)"
            ],
            "testing_frameworks": [
                "Hardhat Test (JavaScript/TypeScript)",
                "Foundry Test (Solidity)",
                "Waffle (alternative testing framework)"
            ],
            "deployment_options": [
                "Local development (Hardhat Network)",
                "Testnets (Sepolia, Mumbai, Goerli)",
                "Mainnet (Ethereum, Polygon, Arbitrum)"
            ],
            "popular_contracts": [
                "ERC-20 (fungible tokens)",
                "ERC-721 (NFTs)",
                "ERC-1155 (multi-token standard)",
                "OpenZeppelin contracts (security)",
                "Uniswap V2/V3 (DEX)",
                "Compound (lending protocol)"
            ]
        }
        
        return plan
    
    def get_development_workflow(self) -> List[str]:
        """Get recommended development workflow."""
        return [
            "1. Set up project structure",
            "   npx hardhat init",
            "   cd my-project",
            "",
            "2. Install dependencies",
            "   npm install @openzeppelin/contracts",
            "   npm install ethers",
            "",
            "3. Write smart contracts",
            "   contracts/MyContract.sol",
            "",
            "4. Write tests",
            "   test/MyContract.test.js",
            "",
            "5. Compile contracts",
            "   npx hardhat compile",
            "",
            "6. Run tests",
            "   npx hardhat test",
            "",
            "7. Start local blockchain",
            "   npx hardhat node",
            "",
            "8. Deploy contracts",
            "   npx hardhat run scripts/deploy.js --network localhost",
            "",
            "9. Interact with contracts",
            "   npx hardhat console --network localhost",
            "",
            "10. Deploy to testnet",
            "    npx hardhat run scripts/deploy.js --network sepolia"
        ]
    
    def get_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Get troubleshooting guide for common issues."""
        return {
            "Installation Issues": [
                "Node.js version mismatch: Use Node.js 18 LTS",
                "Permission denied: Use sudo (Linux) or run as administrator (Windows)",
                "Network timeout: Check internet connection and try again",
                "Disk space: Ensure at least 10GB free space"
            ],
            "Compilation Issues": [
                "Solidity version mismatch: Check pragma version in contracts",
                "Import errors: Install missing dependencies with npm",
                "Memory issues: Increase Node.js memory limit with --max-old-space-size=4096"
            ],
            "Testing Issues": [
                "Test failures: Check contract logic and test expectations",
                "Timeout errors: Increase test timeout in hardhat.config.js",
                "Network errors: Ensure local blockchain is running"
            ],
            "Deployment Issues": [
                "Gas estimation failed: Check contract constructor parameters",
                "Network not found: Verify network configuration in hardhat.config.js",
                "Private key issues: Ensure private key is properly configured"
            ]
        }
    
    def get_recommended_extensions(self) -> List[str]:
        """Get recommended VS Code extensions."""
        return [
            "hardhat",
            "solidity",
            "prettier-solidity",
            "gitlens",
            "bracket-pair-colorizer",
            "indent-rainbow",
            "auto-rename-tag",
            "path-intellisense",
            "solidity-solhint",
            "solidity-visual-auditor"
        ]
    
    def get_useful_commands(self) -> Dict[str, List[str]]:
        """Get useful commands for Solidity development."""
        return {
            "Hardhat Commands": [
                "npx hardhat init - Initialize new project",
                "npx hardhat compile - Compile contracts",
                "npx hardhat test - Run tests",
                "npx hardhat node - Start local blockchain",
                "npx hardhat run scripts/deploy.js - Deploy contracts",
                "npx hardhat console - Interactive console",
                "npx hardhat clean - Clean build artifacts",
                "npx hardhat coverage - Run coverage analysis"
            ],
            "Foundry Commands": [
                "forge init - Initialize new project",
                "forge build - Build contracts",
                "forge test - Run tests",
                "forge script - Run deployment scripts",
                "forge create - Deploy contract",
                "forge verify - Verify contract on Etherscan",
                "cast call - Call contract function",
                "cast send - Send transaction"
            ],
            "Git Commands": [
                "git init - Initialize repository",
                "git add . - Stage all changes",
                "git commit -m 'message' - Commit changes",
                "git push - Push to remote",
                "git pull - Pull from remote",
                "git branch - List branches",
                "git checkout -b feature - Create new branch",
                "git merge feature - Merge branch"
            ],
            "npm Commands": [
                "npm init - Initialize package.json",
                "npm install - Install dependencies",
                "npm install package - Install specific package",
                "npm run script - Run npm script",
                "npm update - Update dependencies",
                "npm audit - Security audit",
                "npm list - List installed packages",
                "npm outdated - Check outdated packages"
            ]
        }
