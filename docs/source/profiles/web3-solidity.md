# Web3 Solidity Profile

**Status:** ✅ Production Ready  
**Profile ID:** `web3-solidity`  
**Category:** Web3 Development  
**Version:** 1.0.0

## Overview

Complete Ethereum smart contract development environment with Hardhat, Foundry, and all necessary tools for building, testing, and deploying decentralized applications (dApps) on the Ethereum blockchain and EVM-compatible chains.

## What's Included

### Core Development Tools

#### Language Runtime
- **Node.js 18.19.0 LTS** - JavaScript runtime for Hardhat and development tools
- **npm 10.2.3** - Node.js package manager

#### Version Control
- **Git 2.39.0** - Version control system for smart contract projects

### Smart Contract Development

#### Development Frameworks
- **Hardhat 2.19.4** - Ethereum development environment with built-in local blockchain
- **Foundry 0.2.0** - Fast, portable toolkit for Ethereum development
  - forge - Build, test, and deploy contracts
  - cast - Interact with smart contracts from CLI
  - anvil - Local Ethereum node
  - chisel - Solidity REPL

#### Compilers & Languages
- **Solidity Compiler 0.8.22** - Latest Solidity compiler for smart contracts
- **Vyper (optional)** - Pythonic smart contract language

### Libraries & Frameworks

#### Smart Contract Libraries
- **OpenZeppelin Contracts 5.0.0** - Secure, battle-tested smart contract library
  - ERC20, ERC721, ERC1155 token standards
  - Access control and security utilities
  - Governance contracts
  - Proxy patterns for upgradeable contracts
- **OpenZeppelin Contracts Upgradeable** - Upgradeable contract patterns
- **Solmate** - Gas-optimized Solidity contracts
- **ds-test** - Testing framework for Foundry

#### JavaScript/TypeScript Libraries
- **ethers.js 6.9.0** - Complete Ethereum library for JavaScript/TypeScript
- **viem 1.19.0** - TypeScript interface for Ethereum with modern patterns
- **web3.js (optional)** - Original Ethereum JavaScript API

### Development Infrastructure

#### Node Management & Testing
- **Hardhat Network** - Built-in local Ethereum network for testing
- **Ganache** - Personal blockchain for Ethereum development
- **Anvil** - Foundry's local Ethereum node (Rust-based, ultra-fast)

#### Testing & Security
- **Hardhat Test Runner** - Mocha-based testing framework
- **Forge Test** - Foundry's testing framework (Solidity-based tests)
- **Chai** - Assertion library for JavaScript tests
- **Hardhat Gas Reporter** - Gas usage metrics for smart contracts
- **Solhint** - Linter for Solidity code
- **Slither** - Static analysis framework for smart contracts
- **Mythril** - Security analysis tool for EVM bytecode

### Deployment & Infrastructure

#### Deployment Tools
- **Hardhat Deploy** - Deployment plugin for Hardhat
- **Hardhat Ignition** - Declarative deployment system
- **Forge Script** - Solidity-based deployment scripting

#### Node Providers & APIs
- **Alchemy SDK 3.0.0** - Web3 development platform SDK
- **Infura** - Ethereum node infrastructure
- **QuickNode** - Multi-chain node infrastructure

#### Blockchain Data
- **The Graph CLI 0.58.0** - Indexing protocol for blockchain data
- **Subgraph Studio** - GraphQL API for blockchain data
- **Etherscan API** - Blockchain explorer API integration

### Frontend Integration

#### Web3 Connection Libraries
- **RainbowKit** - Beautiful wallet connection UI
- **wagmi** - React hooks for Ethereum
- **ConnectKit** - Wallet connection library
- **Web3Modal** - Multi-wallet connection library

#### DApp Frameworks
- **Scaffold-ETH 2** - Full-stack Ethereum development template
- **thirdweb SDK** - Complete web3 development platform
- **Moralis SDK** - Backend infrastructure for web3 apps

### Development Tools

#### IDE Support
- **Visual Studio Code** - Code editor with excellent Solidity support
- **Solidity Extension** - VS Code extension for Solidity development
- **Hardhat for VS Code** - Hardhat integration for VS Code

#### Testing & Debugging
- **Hardhat Console** - Interactive JavaScript console
- **Hardhat Tracer** - Transaction tracing and debugging
- **Tenderly** - Smart contract monitoring and debugging
- **OpenZeppelin Defender** - Secure operations platform

#### Code Quality
- **Prettier Solidity** - Code formatter for Solidity
- **ESLint** - JavaScript/TypeScript linting
- **TypeScript 5.x** - Type safety for JavaScript code
- **Husky** - Git hooks for pre-commit checks

### Additional Tools

#### Utilities
- **dotenv** - Environment variable management
- **ts-node** - TypeScript execution for scripts
- **hardhat-shorthand** - Run Hardhat with `hh` instead of `npx hardhat`

#### Documentation
- **Solidity DocGen** - Documentation generator from NatSpec comments
- **Hardhat Docgen** - Generate documentation for contracts

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| **RAM** | 8 GB | 16 GB |
| **Disk Space** | 15 GB | 30 GB |
| **CPU** | 4 cores | 8 cores |
| **Internet** | Required | High-speed |
| **Download Size** | ~1.2 GB | - |
| **Installation Time** | 10-15 min | - |

## Quick Install

```bash
# Install complete Web3 Solidity environment
he2plus install web3-solidity

# Verify installation
he2plus info web3-solidity
```

## Getting Started

### 1. Create a New Hardhat Project

```bash
# Create project directory
mkdir my-defi-project
cd my-defi-project

# Initialize Hardhat project
npx hardhat init

# Choose: Create a TypeScript project
# Install dependencies
npm install

# Project structure created:
# contracts/     - Solidity smart contracts
# scripts/       - Deployment scripts
# test/          - Contract tests
# hardhat.config.ts - Hardhat configuration
```

### 2. Create a New Foundry Project

```bash
# Initialize Foundry project
forge init my-nft-project
cd my-nft-project

# Project structure:
# src/           - Solidity contracts
# test/          - Solidity tests
# script/        - Deployment scripts
# foundry.toml   - Foundry configuration
```

### 3. Write Your First Smart Contract

```solidity
// contracts/SimpleToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SimpleToken is ERC20, Ownable {
    constructor(uint256 initialSupply) 
        ERC20("SimpleToken", "STK") 
        Ownable(msg.sender) 
    {
        _mint(msg.sender, initialSupply);
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```

### 4. Write Tests

**Hardhat Test (TypeScript/JavaScript):**

```typescript
// test/SimpleToken.test.ts
import { expect } from "chai";
import { ethers } from "hardhat";

describe("SimpleToken", function () {
  it("Should mint initial supply to owner", async function () {
    const [owner] = await ethers.getSigners();
    
    const SimpleToken = await ethers.getContractFactory("SimpleToken");
    const token = await SimpleToken.deploy(ethers.parseEther("1000000"));
    
    const balance = await token.balanceOf(owner.address);
    expect(balance).to.equal(ethers.parseEther("1000000"));
  });

  it("Should allow owner to mint new tokens", async function () {
    const [owner, addr1] = await ethers.getSigners();
    
    const SimpleToken = await ethers.getContractFactory("SimpleToken");
    const token = await SimpleToken.deploy(0);
    
    await token.mint(addr1.address, ethers.parseEther("100"));
    
    const balance = await token.balanceOf(addr1.address);
    expect(balance).to.equal(ethers.parseEther("100"));
  });
});
```

**Foundry Test (Solidity):**

```solidity
// test/SimpleToken.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import "../src/SimpleToken.sol";

contract SimpleTokenTest is Test {
    SimpleToken token;
    address owner = address(1);
    address user = address(2);

    function setUp() public {
        vm.prank(owner);
        token = new SimpleToken(1000000 ether);
    }

    function testInitialSupply() public {
        assertEq(token.balanceOf(owner), 1000000 ether);
    }

    function testMinting() public {
        vm.prank(owner);
        token.mint(user, 100 ether);
        assertEq(token.balanceOf(user), 100 ether);
    }

    function testFailUnauthorizedMint() public {
        vm.prank(user);
        token.mint(user, 100 ether); // Should fail
    }
}
```

### 5. Compile Contracts

```bash
# Hardhat
npx hardhat compile

# Foundry
forge build
```

### 6. Run Tests

```bash
# Hardhat
npx hardhat test

# Hardhat with gas reporting
REPORT_GAS=true npx hardhat test

# Foundry
forge test

# Foundry with verbosity
forge test -vvv

# Foundry with gas reporting
forge test --gas-report
```

### 7. Deploy to Network

**Hardhat Deployment Script:**

```typescript
// scripts/deploy.ts
import { ethers } from "hardhat";

async function main() {
  const initialSupply = ethers.parseEther("1000000");

  const SimpleToken = await ethers.getContractFactory("SimpleToken");
  const token = await SimpleToken.deploy(initialSupply);

  await token.waitForDeployment();

  console.log(`SimpleToken deployed to ${await token.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

```bash
# Deploy to local network
npx hardhat node  # In one terminal
npx hardhat run scripts/deploy.ts --network localhost  # In another

# Deploy to testnet
npx hardhat run scripts/deploy.ts --network sepolia

# Verify on Etherscan
npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

**Foundry Deployment Script:**

```solidity
// script/Deploy.s.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Script.sol";
import "../src/SimpleToken.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        
        vm.startBroadcast(deployerPrivateKey);
        
        SimpleToken token = new SimpleToken(1000000 ether);
        
        vm.stopBroadcast();
        
        console.log("SimpleToken deployed to:", address(token));
    }
}
```

```bash
# Deploy with Foundry
forge script script/Deploy.s.sol:DeployScript --rpc-url sepolia --broadcast --verify
```

## Development Workflow

### 1. Project Initialization
```bash
# Hardhat approach
npx hardhat init

# Foundry approach
forge init my-project

# Or use Scaffold-ETH 2 for full-stack
npx create-eth@latest
```

### 2. Smart Contract Development
- Write contracts in Solidity (or Vyper)
- Use OpenZeppelin for security best practices
- Implement proper access control
- Follow Solidity style guide

### 3. Testing Strategy
- Write comprehensive unit tests
- Use Foundry for fast Solidity-based tests
- Use Hardhat for integration tests with JavaScript
- Aim for >90% code coverage
- Test edge cases and failure scenarios

### 4. Security Auditing
```bash
# Static analysis with Slither
slither .

# Security scan with Mythril
myth analyze contracts/MyContract.sol

# Run Hardhat security plugins
npx hardhat check
```

### 5. Gas Optimization
```bash
# Analyze gas usage
REPORT_GAS=true npx hardhat test

# Foundry gas reporting
forge test --gas-report

# Use forge snapshot for gas baselines
forge snapshot
```

### 6. Deployment Process
- Test on local network (Hardhat Network or Anvil)
- Deploy to testnet (Sepolia, Goerli)
- Verify contracts on Etherscan
- Deploy to mainnet with multisig
- Set up monitoring with Tenderly

### 7. Maintenance
- Monitor contract events
- Set up alerts with OpenZeppelin Defender
- Prepare upgrade paths for upgradeable contracts
- Maintain off-chain indexing with The Graph

## Configuration Examples

### Hardhat Configuration

```typescript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "hardhat-gas-reporter";
import "solidity-coverage";

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.22",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 1337,
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
    mainnet: {
      url: process.env.MAINNET_RPC_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
  gasReporter: {
    enabled: process.env.REPORT_GAS === "true",
    currency: "USD",
    coinmarketcap: process.env.COINMARKETCAP_API_KEY,
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
};

export default config;
```

### Foundry Configuration

```toml
# foundry.toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc_version = "0.8.22"
optimizer = true
optimizer_runs = 200
verbosity = 2

[profile.default.fuzz]
runs = 256

[rpc_endpoints]
sepolia = "${SEPOLIA_RPC_URL}"
mainnet = "${MAINNET_RPC_URL}"

[etherscan]
sepolia = { key = "${ETHERSCAN_API_KEY}" }
mainnet = { key = "${ETHERSCAN_API_KEY}" }
```

## Example Projects

### 1. ERC20 Token with Staking

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract StakingToken is ERC20, ReentrancyGuard {
    mapping(address => uint256) public stakedBalance;
    mapping(address => uint256) public stakingTimestamp;
    
    uint256 public constant REWARD_RATE = 10; // 10% APY
    
    constructor() ERC20("StakingToken", "STK") {
        _mint(msg.sender, 1000000 * 10**decimals());
    }
    
    function stake(uint256 amount) external nonReentrant {
        require(amount > 0, "Cannot stake 0");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");
        
        if (stakedBalance[msg.sender] > 0) {
            claimRewards();
        }
        
        _transfer(msg.sender, address(this), amount);
        stakedBalance[msg.sender] += amount;
        stakingTimestamp[msg.sender] = block.timestamp;
    }
    
    function unstake(uint256 amount) external nonReentrant {
        require(stakedBalance[msg.sender] >= amount, "Insufficient staked");
        
        claimRewards();
        
        stakedBalance[msg.sender] -= amount;
        _transfer(address(this), msg.sender, amount);
    }
    
    function claimRewards() public {
        uint256 rewards = calculateRewards(msg.sender);
        if (rewards > 0) {
            _mint(msg.sender, rewards);
            stakingTimestamp[msg.sender] = block.timestamp;
        }
    }
    
    function calculateRewards(address account) public view returns (uint256) {
        uint256 stakedTime = block.timestamp - stakingTimestamp[account];
        return (stakedBalance[account] * REWARD_RATE * stakedTime) / 
               (365 days * 100);
    }
}
```

### 2. NFT Marketplace

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFTMarketplace is ReentrancyGuard, Ownable {
    struct Listing {
        address seller;
        uint256 price;
        bool active;
    }
    
    mapping(address => mapping(uint256 => Listing)) public listings;
    
    uint256 public feePercent = 250; // 2.5%
    
    event Listed(address indexed nft, uint256 indexed tokenId, uint256 price);
    event Sold(address indexed nft, uint256 indexed tokenId, address buyer);
    event Cancelled(address indexed nft, uint256 indexed tokenId);
    
    constructor() Ownable(msg.sender) {}
    
    function list(address nft, uint256 tokenId, uint256 price) 
        external 
        nonReentrant 
    {
        require(price > 0, "Price must be > 0");
        
        IERC721(nft).transferFrom(msg.sender, address(this), tokenId);
        
        listings[nft][tokenId] = Listing({
            seller: msg.sender,
            price: price,
            active: true
        });
        
        emit Listed(nft, tokenId, price);
    }
    
    function buy(address nft, uint256 tokenId) 
        external 
        payable 
        nonReentrant 
    {
        Listing memory listing = listings[nft][tokenId];
        require(listing.active, "Not listed");
        require(msg.value >= listing.price, "Insufficient payment");
        
        listings[nft][tokenId].active = false;
        
        uint256 fee = (listing.price * feePercent) / 10000;
        uint256 sellerProceeds = listing.price - fee;
        
        payable(listing.seller).transfer(sellerProceeds);
        IERC721(nft).transferFrom(address(this), msg.sender, tokenId);
        
        emit Sold(nft, tokenId, msg.sender);
    }
    
    function cancel(address nft, uint256 tokenId) external nonReentrant {
        Listing memory listing = listings[nft][tokenId];
        require(listing.seller == msg.sender, "Not seller");
        require(listing.active, "Not active");
        
        listings[nft][tokenId].active = false;
        IERC721(nft).transferFrom(address(this), msg.sender, tokenId);
        
        emit Cancelled(nft, tokenId);
    }
    
    function withdrawFees() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

### 3. DeFi Lending Protocol (Simplified)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SimpleLending is ReentrancyGuard {
    IERC20 public immutable token;
    
    uint256 public totalDeposits;
    uint256 public totalBorrows;
    
    mapping(address => uint256) public deposits;
    mapping(address => uint256) public borrows;
    
    uint256 public constant INTEREST_RATE = 5; // 5% APY
    uint256 public constant COLLATERAL_RATIO = 150; // 150%
    
    constructor(address _token) {
        token = IERC20(_token);
    }
    
    function deposit(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        
        token.transferFrom(msg.sender, address(this), amount);
        deposits[msg.sender] += amount;
        totalDeposits += amount;
    }
    
    function withdraw(uint256 amount) external nonReentrant {
        require(deposits[msg.sender] >= amount, "Insufficient deposits");
        require(
            deposits[msg.sender] - amount >= 
            (borrows[msg.sender] * COLLATERAL_RATIO) / 100,
            "Would under-collateralize"
        );
        
        deposits[msg.sender] -= amount;
        totalDeposits -= amount;
        token.transfer(msg.sender, amount);
    }
    
    function borrow(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        require(
            deposits[msg.sender] >= 
            ((borrows[msg.sender] + amount) * COLLATERAL_RATIO) / 100,
            "Insufficient collateral"
        );
        
        borrows[msg.sender] += amount;
        totalBorrows += amount;
        token.transfer(msg.sender, amount);
    }
    
    function repay(uint256 amount) external nonReentrant {
        require(borrows[msg.sender] >= amount, "Repay exceeds borrow");
        
        token.transferFrom(msg.sender, address(this), amount);
        borrows[msg.sender] -= amount;
        totalBorrows -= amount;
    }
    
    function getMaxBorrow(address account) public view returns (uint256) {
        uint256 maxBorrow = (deposits[account] * 100) / COLLATERAL_RATIO;
        return maxBorrow > borrows[account] ? maxBorrow - borrows[account] : 0;
    }
}
```

## Troubleshooting Guide

### Common Issues

#### 1. Installation Issues
- **Node.js version mismatch**: Ensure Node.js 18+ is installed
- **npm permission errors**: Use nvm for Node.js management
- **Foundry installation fails**: Run `curl -L https://foundry.paradigm.xyz | bash` then `foundryup`
- **Git not found**: Install Git from official website or package manager

#### 2. Compilation Errors
- **Solidity version mismatch**: Check pragma statement matches config
- **Import not found**: Ensure dependencies are installed with `npm install`
- **Out of memory**: Increase Node.js memory: `NODE_OPTIONS="--max-old-space-size=4096"`
- **Forge build fails**: Update Foundry with `foundryup`

#### 3. Testing Issues
- **Tests fail with gas errors**: Increase gas limit in Hardhat config
- **Hardhat network errors**: Clear cache with `npx hardhat clean`
- **Foundry tests timeout**: Increase timeout in foundry.toml
- **Fork testing fails**: Check RPC URL and API key

#### 4. Deployment Issues
- **Insufficient funds**: Ensure wallet has enough ETH for gas
- **Nonce too low**: Clear pending transactions or wait
- **Gas estimation failed**: Check contract logic for reverts
- **Verification fails**: Ensure exact compiler settings match

#### 5. Development Environment
- **VS Code not recognizing Solidity**: Install Solidity extension
- **IntelliSense not working**: Generate TypeScript types with `npx hardhat typechain`
- **Hardhat console issues**: Clear cache and reinstall: `rm -rf artifacts cache node_modules && npm install`

## VS Code Extensions

### Essential
- **solidity** - Juan Blanco's Solidity extension
- **hardhat-solidity** - Hardhat plugin for VS Code
- **prettier-solidity** - Solidity formatting

### Recommended
- **ESLint** - JavaScript/TypeScript linting
- **Prettier** - Code formatting
- **GitLens** - Enhanced Git integration
- **Error Lens** - Inline error display

## Useful Commands Reference

### Hardhat Commands

```bash
# Project initialization
npx hardhat init

# Compilation
npx hardhat compile
npx hardhat clean  # Clear artifacts

# Testing
npx hardhat test
npx hardhat test --grep "pattern"  # Run specific tests
REPORT_GAS=true npx hardhat test  # With gas reporting
npx hardhat coverage  # Code coverage

# Local blockchain
npx hardhat node  # Start local node
npx hardhat console --network localhost  # Interactive console

# Deployment
npx hardhat run scripts/deploy.ts --network sepolia
npx hardhat verify --network sepolia <address> <constructor-args>

# Utilities
npx hardhat accounts  # List accounts
npx hardhat compile --force  # Force recompile
npx hardhat flatten contracts/MyContract.sol  # Flatten for verification
```

### Foundry Commands

```bash
# Project initialization
forge init my-project
forge install <github-repo>  # Install dependencies

# Compilation
forge build
forge build --force  # Force rebuild
forge clean  # Clear artifacts

# Testing
forge test
forge test -vvv  # Verbose output
forge test --match-contract ContractName  # Test specific contract
forge test --match-test testFunction  # Test specific function
forge test --gas-report  # Gas usage
forge snapshot  # Save gas snapshot
forge coverage  # Code coverage

# Deployment & Interaction
forge create src/MyContract.sol:MyContract --rpc-url <url> --private-key <key>
forge script script/Deploy.s.sol --rpc-url sepolia --broadcast
cast call <address> "balanceOf(address)" <address> --rpc-url <url>
cast send <address> "transfer(address,uint256)" <to> <amount> --rpc-url <url> --private-key <key>

# Blockchain interaction
cast block-number --rpc-url <url>
cast balance <address> --rpc-url <url>
cast code <address> --rpc-url <url>
cast storage <address> <slot> --rpc-url <url>

# Utilities
forge fmt  # Format code
forge inspect <contract> abi  # Get ABI
forge tree  # Show dependency tree
anvil  # Start local node
```

### Other Tools

```bash
# Slither (Security)
slither .
slither contracts/MyContract.sol

# Mythril (Security)
myth analyze contracts/MyContract.sol

# The Graph
graph init --studio <subgraph-name>
graph codegen
graph build
graph deploy --studio <subgraph-name>

# OpenZeppelin
npx oz-wizard  # Contract wizard
```

## Resources & Documentation

### Official Documentation
- **Solidity**: https://docs.soliditylang.org
- **Hardhat**: https://hardhat.org/docs
- **Foundry**: https://book.getfoundry.sh
- **OpenZeppelin**: https://docs.openzeppelin.com
- **ethers.js**: https://docs.ethers.org
- **viem**: https://viem.sh

### Learning Resources
- **Solidity by Example**: https://solidity-by-example.org
- **Ethereum.org**: https://ethereum.org/developers
- **CryptoZombies**: https://cryptozombies.io
- **Alchemy University**: https://university.alchemy.com
- **Cyfrin Updraft**: https://updraft.cyfrin.io

### Security
- **Consensys Smart Contract Best Practices**: https://consensys.github.io/smart-contract-best-practices
- **OpenZeppelin Security**: https://www.openzeppelin.com/security-audits
- **Immunefi**: https://immunefi.com (Bug bounties)

### Tools & Services
- **Etherscan**: https://etherscan.io
- **Tenderly**: https://tenderly.co
- **OpenZeppelin Defender**: https://defender.openzeppelin.com
- **The Graph**: https://thegraph.com
- **Alchemy**: https://www.alchemy.com
- **Infura**: https://www.infura.io

### Community
- **Ethereum Stack Exchange**: https://ethereum.stackexchange.com
- **Hardhat Discord**: https://discord.gg/hardhat
- **Foundry Telegram**: https://t.me/foundry_rs
- **r/ethdev**: https://reddit.com/r/ethdev

## Pro Tips

### Development Best Practices
1. **Always use OpenZeppelin** for standard implementations (ERC20, ERC721, etc.)
2. **Write tests first** - Test-driven development catches bugs early
3. **Use Foundry for unit tests** - Much faster than JavaScript tests
4. **Enable optimizer** - But test with it enabled
5. **Follow CEI pattern** - Checks, Effects, Interactions to prevent reentrancy
6. **Use SafeMath** - Or Solidity 0.8+ which has built-in overflow protection
7. **Implement access control** - Use OpenZeppelin's Ownable or AccessControl

### Security Best Practices
1. **Never trust user input** - Always validate and sanitize
2. **Use ReentrancyGuard** - Protect against reentrancy attacks
3. **Be careful with delegatecall** - Can be dangerous if misused
4. **Limit gas consumption** - Avoid unbounded loops
5. **Use pull over push** - For payments (withdrawals vs sends)
6. **Test edge cases** - Zero values, max values, overflows
7. **Get audited** - Professional audits for production contracts

### Gas Optimization
1. **Pack storage variables** - Use appropriate sizes (uint128, uint64)
2. **Use calldata for arrays** - Instead of memory in external functions
3. **Cache storage reads** - Read once, use many times
4. **Use events** - Instead of storing data when possible
5. **Minimize storage writes** - Most expensive operation
6. **Use unchecked** - When you know overflow won't occur
7. **Optimize loops** - Cache length, use ++i instead of i++

### Testing Tips
1. **Aim for 100% coverage** - Every line should be tested
2. **Test failure cases** - Not just success paths
3. **Use fuzz testing** - Foundry's built-in fuzzing is excellent
4. **Test gas usage** - Optimize expensive operations
5. **Test events** - Ensure events are emitted correctly
6. **Fork testing** - Test against mainnet state
7. **Test upgrades** - If using proxy patterns

### Deployment Checklist
- [ ] All tests passing with 100% coverage
- [ ] Security audit completed (for production)
- [ ] Gas optimization reviewed
- [ ] Documentation complete (NatSpec comments)
- [ ] Deployment script tested on testnet
- [ ] Constructor parameters verified
- [ ] Post-deployment verification planned
- [ ] Monitoring and alerts configured
- [ ] Emergency pause mechanism (if applicable)
- [ ] Upgrade path documented (if upgradeable)

## Next Steps

After installing the Web3 Solidity profile:

1. **📚 Learn Solidity** - Complete [CryptoZombies](https://cryptozombies.io)
2. **🔨 Build Projects** - Start with simple contracts and progressively build complexity
3. **🧪 Master Testing** - Learn both Hardhat and Foundry testing patterns
4. **🔒 Study Security** - Read [Consensys Best Practices](https://consensys.github.io/smart-contract-best-practices)
5. **🚀 Deploy** - Start on testnets, graduate to mainnet
6. **🎓 Join Community** - Engage with Ethereum developer communities
7. **📖 Stay Updated** - Follow Ethereum Improvement Proposals (EIPs)

---

**Ready to build the decentralized future? Start coding! 🚀**

