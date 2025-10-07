# Testing Guide for he2plus Profiles

## 🧪 How to Test All Profiles

This guide shows you how to install and test he2plus profiles both locally and with Docker.

## Installation Methods

### Method 1: Install from Source (For Development & Testing)

```bash
# Clone the repository
git clone https://github.com/he2plus/he2plus-lib.git
cd he2plus-lib

# Install in editable/development mode
pip install -e .

# Verify installation
he2plus --version
he2plus list --available
```

**Benefits:**
- Changes to code are immediately reflected
- Can modify and test profiles easily
- Best for development and testing

### Method 2: Install from GitHub Directly

```bash
# Install directly from GitHub
pip install git+https://github.com/he2plus/he2plus-lib.git

# Or install a specific branch
pip install git+https://github.com/he2plus/he2plus-lib.git@main
```

### Method 3: Install from PyPI (When Published)

```bash
# Will be available when published to PyPI
pip install he2plus
```

## Manual Testing

### Test Web3 Solidity Profile

```bash
# 1. Check if profile exists
he2plus info web3-solidity

# 2. Install Node.js 18 (if not already installed)
# macOS: brew install node@18
# Linux: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs

# 3. Verify Node.js
node --version  # Should show v18.x

# 4. Test Hardhat
npx hardhat init
npm install @openzeppelin/contracts
npx hardhat compile
npx hardhat test

# 5. Test Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup
forge --version
cast --version
anvil --version
```

### Test Web Next.js Profile

```bash
# 1. Check profile
he2plus info web-nextjs

# 2. Create test project
npx create-next-app@latest my-test-app --typescript --tailwind --eslint --app

# 3. Install and test
cd my-test-app
npm install
npm run lint
npm run build
npm run dev  # Visit http://localhost:3000
```

### Test ML Python Profile

```bash
# 1. Check profile
he2plus info ml-python

# 2. Create virtual environment
python -m venv ml-test
source ml-test/bin/activate  # On Windows: ml-test\Scripts\activate

# 3. Install core libraries
pip install numpy pandas matplotlib seaborn scikit-learn

# 4. Install deep learning frameworks
pip install tensorflow torch torchvision

# 5. Test imports
python -c "import numpy, pandas, sklearn, tensorflow, torch; print('All imports successful!')"

# 6. Run simple test
python << EOF
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Model accuracy: {accuracy:.2%}")
EOF
```

### Test Mobile React Native Profile

```bash
# 1. Check profile
he2plus info mobile-react-native

# 2. Install prerequisites
# - Node.js 18
# - Java JDK 11 (for Android)
# - Xcode (for iOS, macOS only)
# - Android Studio (for Android)

# 3. Create test project
npx react-native@latest init MyTestApp

# 4. Install and test
cd MyTestApp
npm install

# Android
npm run android

# iOS (macOS only)
npm run ios
```

## Automated Docker Testing

For comprehensive automated testing in isolated environments, use the Docker test suite:

### Prerequisites

```bash
# Install Docker Desktop from: https://www.docker.com/products/docker-desktop/
# Verify installation:
docker --version
docker-compose --version
```

### Run All Profile Tests

```bash
# Navigate to test directory
cd /path/to/he2plus-lib/tests/docker

# Run all tests (takes ~20-30 minutes)
./run-all-tests.sh
```

This will test all 4 profiles in separate Docker containers:
- ✅ Web3 Solidity (~5-8 minutes)
- ✅ Web Next.js (~3-5 minutes)
- ✅ ML Python (~7-13 minutes)
- ✅ Mobile React Native (~5-8 minutes)

### Run Individual Profile Test

```bash
cd tests/docker

# Test a specific profile
docker-compose -f docker-compose.test.yml run --rm test-web3-solidity
docker-compose -f docker-compose.test.yml run --rm test-web-nextjs
docker-compose -f docker-compose.test.yml run --rm test-ml-python
docker-compose -f docker-compose.test.yml run --rm test-mobile-react-native
```

### What the Docker Tests Validate

Each Docker test:
1. ✅ Installs he2plus from source
2. ✅ Sets up the profile environment
3. ✅ Installs all required tools
4. ✅ Creates a test project
5. ✅ Compiles/builds the project
6. ✅ Runs tests
7. ✅ Validates all components work together

See `tests/docker/README.md` for detailed information about Docker testing.

## Quick Validation Tests

### Verify he2plus Installation

```bash
# Check version
he2plus --version

# List available profiles
he2plus list --available

# Get profile details
he2plus info web3-solidity
he2plus info web-nextjs
he2plus info ml-python
he2plus info mobile-react-native

# Check system
he2plus doctor
```

### Verify Documentation

```bash
# Check if documentation builds
cd docs/source
sphinx-build -b html . ../build/html

# Or use Python directly
python3 -m sphinx -b html . ../build/html
```

## Testing Checklist

Before considering a profile "tested":

- [ ] Profile info command works (`he2plus info <profile>`)
- [ ] All core tools install successfully
- [ ] Can create a new project
- [ ] Project compiles/builds without errors
- [ ] Basic examples run successfully
- [ ] Documentation matches reality
- [ ] All commands in docs work as described

## Common Issues

### Node.js Version Issues

```bash
# Use nvm to manage Node.js versions
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### Python Version Issues

```bash
# Use pyenv to manage Python versions
curl https://pyenv.run | bash
pyenv install 3.11
pyenv global 3.11
```

### Docker Issues

```bash
# Clean Docker cache
docker system prune -a

# Check disk space
docker system df

# Reset Docker Desktop (if needed)
# Docker Desktop -> Preferences -> Reset
```

## Testing in CI/CD

Example GitHub Actions workflow:

```yaml
name: Test Profiles

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        profile: [web3-solidity, web-nextjs, ml-python, mobile-react-native]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker
        uses: docker/setup-buildx-action@v2
      
      - name: Test ${{ matrix.profile }}
        run: |
          cd tests/docker
          docker-compose -f docker-compose.test.yml run --rm test-${{ matrix.profile }}
```

## Continuous Testing

To ensure profiles stay up to date:

1. **Weekly**: Run Docker tests on all profiles
2. **On PR**: Run tests for affected profiles
3. **Before Release**: Full test suite on all platforms
4. **After Docs Update**: Validate examples still work

## Reporting Issues

If tests fail:

1. Note which profile failed
2. Copy the error message
3. Note your system (OS, versions)
4. Check if issue is already reported
5. Open GitHub issue with details

## Contributing Tests

When adding new profiles:

1. Create Dockerfile in `tests/docker/`
2. Add service to `docker-compose.test.yml`
3. Update `run-all-tests.sh`
4. Test locally
5. Update this guide
6. Submit PR with tests

---

## Summary

| Method | Best For | Time | Reliability |
|--------|----------|------|-------------|
| **Manual Testing** | Quick checks | 5-10 min | Good |
| **Docker Testing** | Comprehensive validation | 20-30 min | Excellent |
| **CI/CD Testing** | Automated verification | 20-30 min | Excellent |

**Recommendation**: Use **Manual Testing** for quick validation, **Docker Testing** for thorough verification before releases.

---

**Testing ensures quality and documentation accuracy! 🧪**

