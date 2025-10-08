# 🚀 he2plus - Professional Development Environment Manager

**"From zero to deploy in one command. No configuration, no frustration, just code."**

he2plus is a professional-grade, modular development environment manager that eliminates setup friction. Install any stack, switch between technologies effortlessly, and start building immediately.

## 🎯 Vision

he2plus solves the universal problem of development environment setup and dependency management. Built by a developer who experienced firsthand the frustration of spending hours configuring development environments instead of focusing on actual coding.

## ✨ Features

- **🎯 Modular Profiles**: Install complete development stacks with one command
- **🔍 Smart System Detection**: Cross-platform compatibility (macOS, Windows, Linux)
- **⚡ Fast Installation**: Optimized for speed with progress tracking
- **🛡️ Resource Validation**: Check system requirements before installation
- **🔧 Component Management**: Individual tool and language installers
- **📊 Beautiful CLI**: Rich terminal interface with progress bars and colors
- **🌐 Web3 Ready**: Complete blockchain development environments
- **🤖 AI-Powered**: Smart troubleshooting and recommendations (coming soon)

## 🚀 Installation

```bash
pip install he2plus
```

**Note**: The package is now available on PyPI! You can install it directly using the command above.

## 🎯 Quick Start

### Install a Development Profile

```bash
# Install Web3 Solidity development environment
he2plus install web3-solidity

# Install modern web development stack
he2plus install web-nextjs

# Install mobile development environment
he2plus install mobile-react-native

# Install machine learning environment
he2plus install ml-python

# Install multiple profiles
he2plus install web-nextjs mobile-react-native

# List available profiles
he2plus list --available

# Search for profiles
he2plus search react
he2plus search python

# Get detailed profile information
he2plus info web-nextjs
```

### System Diagnostics

```bash
# Check system health and capabilities
he2plus doctor

# Show system information
he2plus info

# Search for profiles
he2plus search "web3"
```

### Profile Management

```bash
# List installed profiles
he2plus list

# Remove profiles (coming soon)
he2plus remove web3-solidity

# Update profiles (coming soon)
he2plus update --all
```

### Python API

```python
import he2plus

# Get system information
system_profiler = he2plus.SystemProfiler()
system_info = system_profiler.profile()

# Validate system requirements
validator = he2plus.SystemValidator(system_info)
validation = validator.validate(requirements)

# Load profiles
registry = he2plus.ProfileRegistry()
profile = registry.get("web3-solidity")

# Get installation plan
plan = registry.get_installation_plan(["web3-solidity"])
```

## 📚 Available Profiles

### 🌐 Web3 Development
- **`web3-solidity`** - Ethereum smart contract development with Hardhat and Foundry
- **`web3-vyper`** - Pythonic smart contracts for Ethereum (coming soon)
- **`web3-rust`** - Solana/NEAR development with Rust (coming soon)
- **`web3-move`** - Move language for Aptos and Sui (coming soon)

### 💻 Web Development
- **`web-nextjs`** - Next.js full-stack development with TypeScript, Tailwind CSS, and modern tooling
- **`web-mern`** - MongoDB, Express, React, Node.js (coming soon)
- **`web-django`** - Django full-stack development (coming soon)
- **`web-angular`** - Angular development (coming soon)
- **`web-vue`** - Vue.js development (coming soon)

### 📱 Mobile Development
- **`mobile-react-native`** - Cross-platform mobile development with React Native, TypeScript, and modern tooling
- **`mobile-flutter`** - Google's UI toolkit (coming soon)
- **`mobile-swift`** - iOS development with Swift (coming soon)
- **`mobile-kotlin`** - Android development with Kotlin (coming soon)

### 🤖 Machine Learning
- **`ml-python`** - Complete Python ML environment with TensorFlow, PyTorch, scikit-learn, and modern tooling
- **`ml-gpu`** - GPU-accelerated deep learning (coming soon)

### 🛠️ Utilities
- **`utils-docker`** - Docker containerization (coming soon)
- **`utils-version-control`** - Git and GitHub CLI setup (coming soon)
- **`utils-databases`** - Database tools (PostgreSQL, MySQL, MongoDB) (coming soon)

## 🏗️ Architecture

he2plus uses a modular profile system where each development environment is defined as a profile containing:

- **Components**: Individual tools, languages, and frameworks
- **Requirements**: System resource requirements (RAM, disk, CPU, GPU)
- **Dependencies**: Component dependencies and conflicts
- **Verification**: Post-installation verification steps
- **Sample Projects**: Ready-to-use project templates

## 📖 Documentation

- [Project Context](PROJECT_CONTEXT.md) - Complete project vision and strategy
- [Contributing](CONTRIBUTING.md) - How to contribute to he2plus
- [Strategic Directions](STRATEGIC_DIRECTIONS.md) - Future roadmap

## License

MIT License

## 🎯 Example: Web3 Solidity Development

```bash
# Install complete Web3 development environment
he2plus install web3-solidity

# Output:
# 🔍 Analyzing system...
#    ✓ macOS 15.7.1 (arm64)
#    ✓ 16.0 GB RAM (5.9 GB available)
#    ✓ 900.5 GB disk free
#
# 📋 Installation Plan: web3-solidity
# Will install:
#    📦 Node.js 18.19.0 (ARM64)         ~50 MB
#    📦 npm 10.2.3                       (included)
#    📦 Hardhat 2.19.4                   ~100 MB
#    📦 Foundry (forge, cast, anvil)     ~200 MB
#    📦 Solidity compiler 0.8.22         ~50 MB
#    📦 OpenZeppelin Contracts           ~10 MB
#    📦 ethers.js 6.9.0                  ~5 MB
#
# ⏱️  Estimated time: 8-12 minutes
# 💾 Total download: ~415 MB
# 💽 Disk space after install: ~890 GB free
#
# Continue? [Y/n] y
#
# 📦 Installing web3-solidity...
# [1/11] Node.js 18.19.0 ████████████████████ 100% ✓ (2m 34s)
# [2/11] npm             ████████████████████ 100% ✓ (0m 05s)
# [3/11] Git             ████████████████████ 100% ✓ (1m 12s)
# [4/11] Hardhat         ████████████████████ 100% ✓ (3m 45s)
# [5/11] Foundry         ████████████████████ 100% ✓ (2m 23s)
# [6/11] Solidity        ████████████████████ 100% ✓ (0m 23s)
# [7/11] OpenZeppelin    ████████████████████ 100% ✓ (0m 15s)
# [8/11] ethers.js       ████████████████████ 100% ✓ (0m 08s)
# [9/11] viem            ████████████████████ 100% ✓ (0m 05s)
# [10/11] Alchemy SDK    ████████████████████ 100% ✓ (0m 03s)
# [11/11] The Graph CLI  ████████████████████ 100% ✓ (0m 12s)
#
# ✅ web3-solidity installed successfully! (8m 22s)
#
# 🎯 Next steps:
#    1. Create new project:  npx hardhat init
#    2. Or use starter:      git clone https://github.com/he2plus/hardhat-starter
#    3. Compile contracts:   npx hardhat compile
#    4. Run tests:           npx hardhat test
#    5. Start local node:    npx hardhat node
```
---

## 🌟 Why he2plus?

**Built by a developer, for developers.** This library was created by Prakhar Tripathi after experiencing firsthand the frustration of spending hours configuring development environments instead of focusing on actual coding.

**"This library was built by a dev frustrated by dependency issues and hence he cared for you - Prakhar Tripathi"**

### Key Benefits:
- **⚡ Speed**: Get from zero to coding in minutes, not hours
- **🛡️ Reliability**: Tested across multiple platforms and scenarios
- **🎯 Focus**: Spend time on code, not configuration
- **📚 Learning**: Understand what's being installed and why
- **🔄 Flexibility**: Mix and match profiles for your needs

### Community:
- **Twitter**: [@he2plus](https://twitter.com/he2plus) for updates and community
- **GitHub**: Open source development and contributions
- **Discord**: Community support and discussions (coming soon)

**Let's make the development experience amazing for everyone! 🎉**
