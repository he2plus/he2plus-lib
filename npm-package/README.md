# he2plus (npm package)

**Professional Development Environment Manager - Node.js wrapper**

[![npm version](https://img.shields.io/npm/v/he2plus.svg)](https://www.npmjs.com/package/he2plus)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)

This is the Node.js/npm wrapper for [he2plus](https://github.com/he2plus/he2plus-lib), allowing JavaScript/TypeScript developers to use he2plus via npm.

---

## 🚀 Quick Start

### Installation

```bash
# Global installation (recommended)
npm install -g he2plus

# Or use npx (no installation required)
npx he2plus --help
```

### Usage

```bash
# Check version
he2plus --version

# List available profiles
he2plus list --available

# Get profile information
he2plus info web-nextjs

# Run system diagnostics
he2plus doctor
```

---

## 📋 Requirements

- **Node.js**: 14.0.0 or higher
- **Python**: 3.8 or higher (installed automatically on first use)

The npm package is a wrapper that manages the Python CLI. Python will be checked during installation, and the he2plus Python package will be installed automatically on first use if not present.

---

## ✨ Features

Same as the Python package:

- **12 Development Profiles**: Web, Web3, Mobile, ML stacks
- **Smart System Detection**: Cross-platform compatibility
- **Beautiful CLI**: Rich terminal interface
- **Validated**: End-to-end tested with real applications

---

## 🎯 Available Profiles

- `web-nextjs` - Next.js full-stack development
- `web-mern` - MongoDB + Express + React + Node.js
- `web-angular` - Angular development
- `web-vue` - Vue.js development
- `web3-solidity` - Ethereum smart contract development
- `mobile-react-native` - Cross-platform mobile development
- `ml-python` - Machine learning with TensorFlow, PyTorch
- And more...

---

## 💻 Programmatic Usage

You can also use he2plus programmatically in your Node.js applications:

```javascript
const he2plus = require('he2plus');

// Execute commands programmatically
async function example() {
  try {
    // Run a command
    const result = await he2plus.exec('list --available');
    console.log('Profiles:', result.stdout);
    
    // Check if Python is available
    const pythonCmd = he2plus.checkPython();
    console.log('Python command:', pythonCmd);
    
    // Check if he2plus is installed
    const installed = await he2plus.checkHe2plus(pythonCmd);
    console.log('he2plus installed:', installed);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

example();
```

---

## 🔧 How It Works

This npm package is a lightweight wrapper that:

1. Checks if Python is installed
2. Installs the he2plus Python package (if needed)
3. Provides a convenient CLI interface
4. Manages the underlying Python CLI calls

**Why this approach?**
- Leverages the fully-tested Python implementation
- No code duplication
- Same functionality across Python and Node.js
- Single source of truth

---

## 🐛 Troubleshooting

### Python Not Found

If you get a "Python not found" error:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip
```

**Windows:**
Download from https://www.python.org/downloads/

### he2plus Command Not Found

If installed globally but command not found:

```bash
# Check npm global bin path
npm config get prefix

# Add to PATH if needed (macOS/Linux)
export PATH="$PATH:$(npm config get prefix)/bin"
```

### Permission Errors

If you get permission errors on Linux/macOS:

```bash
# Option 1: Use npx (no installation)
npx he2plus --help

# Option 2: Install without sudo using nvm
# https://github.com/nvm-sh/nvm
```

---

## 📚 Documentation

Full documentation available at:
- **Main Repository**: https://github.com/he2plus/he2plus-lib
- **Python Package**: https://github.com/he2plus/he2plus-lib#readme
- **Test Reports**: https://github.com/he2plus/he2plus-lib/tree/main/tests/e2e-fullstack

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) in the main repository.

---

## 📜 License

MIT License - see [LICENSE](../LICENSE) for details

---

## 🔗 Links

- **npm Package**: https://www.npmjs.com/package/he2plus
- **GitHub**: https://github.com/he2plus/he2plus-lib
- **Issues**: https://github.com/he2plus/he2plus-lib/issues
- **Twitter**: [@he2plus](https://twitter.com/he2plus)

---

## 💡 Examples

### Using with npm scripts

```json
{
  "scripts": {
    "setup": "he2plus info web-nextjs",
    "doctor": "he2plus doctor"
  }
}
```

### Using with CI/CD

```yaml
# .github/workflows/setup.yml
- name: Setup development environment
  run: |
    npm install -g he2plus
    he2plus doctor
```

---

**Built by a developer, for developers** 🚀

*From zero to deploy in one command. No configuration, no frustration, just code.*
