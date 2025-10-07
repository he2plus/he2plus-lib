# Docker Profile Tests

Automated testing suite for validating all he2plus development profiles in isolated Docker containers.

## Overview

This test suite validates that each profile's documentation matches reality by:
1. Installing he2plus from source
2. Setting up the profile environment
3. Creating a test project
4. Running basic validation tests

Each profile is tested in a separate Docker container to ensure isolation and reproducibility.

## Profiles Tested

- ✅ **Web3 Solidity** - Hardhat, Foundry, OpenZeppelin, smart contracts
- ✅ **Web Next.js** - Next.js 14, React 18, TypeScript, Tailwind CSS
- ✅ **ML Python** - TensorFlow, PyTorch, scikit-learn, NumPy, Pandas
- ✅ **Mobile React Native** - React Native, TypeScript, React Navigation

## Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)
- At least 10GB free disk space
- Stable internet connection

## Quick Start

### Run All Tests

```bash
cd tests/docker
chmod +x run-all-tests.sh
./run-all-tests.sh
```

This will:
1. Build Docker images for each profile
2. Run tests in separate containers
3. Display results summary
4. Clean up resources

### Run Individual Profile Test

```bash
cd tests/docker

# Test Web3 Solidity
docker-compose -f docker-compose.test.yml run --rm test-web3-solidity

# Test Web Next.js
docker-compose -f docker-compose.test.yml run --rm test-web-nextjs

# Test ML Python
docker-compose -f docker-compose.test.yml run --rm test-ml-python

# Test Mobile React Native
docker-compose -f docker-compose.test.yml run --rm test-mobile-react-native
```

## What Each Test Does

### Web3 Solidity Test

1. Verifies he2plus installation
2. Checks Node.js and npm
3. Installs Hardhat
4. Installs Foundry (forge, cast, anvil)
5. Creates test Hardhat project
6. Installs OpenZeppelin contracts
7. Compiles smart contracts
8. Runs contract tests

### Web Next.js Test

1. Verifies he2plus installation
2. Checks Node.js and npm
3. Creates Next.js project with TypeScript and Tailwind
4. Installs dependencies
5. Installs additional packages (TanStack Query, Zustand, Framer Motion)
6. Runs linting
7. Builds production bundle

### ML Python Test

1. Verifies he2plus installation
2. Checks Python version
3. Creates virtual environment
4. Installs core ML libraries (NumPy, Pandas, scikit-learn)
5. Installs TensorFlow (CPU version)
6. Installs PyTorch (CPU version)
7. Tests all imports
8. Runs scikit-learn classification test
9. Runs PyTorch neural network test

### Mobile React Native Test

1. Verifies he2plus installation
2. Checks Node.js and npm
3. Checks Java JDK
4. Installs React Native CLI
5. Creates React Native project
6. Installs dependencies
7. Installs navigation and animation packages
8. Runs linting
9. Runs tests

## Expected Duration

| Profile | Build Time | Test Time | Total |
|---------|-----------|-----------|-------|
| Web3 Solidity | 2-3 min | 3-5 min | ~5-8 min |
| Web Next.js | 1-2 min | 2-3 min | ~3-5 min |
| ML Python | 2-3 min | 5-10 min | ~7-13 min |
| Mobile React Native | 2-3 min | 3-5 min | ~5-8 min |
| **Total (all)** | **~8 min** | **~15 min** | **~23 min** |

Note: Times may vary based on internet speed and system performance.

## Troubleshooting

### Docker Build Fails

```bash
# Clean Docker cache and rebuild
docker system prune -a
cd tests/docker
./run-all-tests.sh
```

### Test Fails

Check the test logs for specific error messages:

```bash
# View logs for a specific test
docker-compose -f docker-compose.test.yml logs test-web3-solidity
```

### Out of Disk Space

```bash
# Remove unused Docker images
docker system prune -a

# Check disk usage
docker system df
```

### Network Issues

If downloads fail, check your internet connection and try again. Some packages are large:
- ML Python: ~2GB of dependencies
- Web3 Solidity: ~500MB
- Web Next.js: ~300MB
- Mobile React Native: ~400MB

## CI/CD Integration

These tests can be integrated into GitHub Actions:

```yaml
name: Profile Tests

on: [push, pull_request]

jobs:
  test-profiles:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        profile: [web3-solidity, web-nextjs, ml-python, mobile-react-native]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Test ${{ matrix.profile }}
        run: |
          cd tests/docker
          docker-compose -f docker-compose.test.yml run --rm test-${{ matrix.profile }}
```

## Manual Testing

If you prefer to test manually:

```bash
# 1. Build the image
docker build -f tests/docker/test-web3-solidity.dockerfile -t he2plus-test-web3 .

# 2. Run the container
docker run --rm he2plus-test-web3

# 3. Or run interactively
docker run --rm -it he2plus-test-web3 /bin/bash
```

## Cleanup

Remove all test containers and images:

```bash
cd tests/docker
docker-compose -f docker-compose.test.yml down --rmi all --volumes
```

## Contributing

When adding new profiles or updating existing ones:

1. Create a new Dockerfile in `tests/docker/`
2. Add the service to `docker-compose.test.yml`
3. Update `run-all-tests.sh` to include the new profile
4. Test locally before committing
5. Update this README

## Notes

- Tests use Ubuntu 22.04 as the base image
- Python 3.11 is used for all tests
- Node.js 18 LTS is used for JavaScript/TypeScript profiles
- ML tests use CPU versions of TensorFlow/PyTorch for speed
- Tests are designed to be deterministic and reproducible

## Support

If tests fail or you encounter issues:
1. Check the logs for specific errors
2. Verify your Docker installation is up to date
3. Ensure you have sufficient disk space
4. Check internet connectivity
5. Open an issue on GitHub with test logs

---

**Testing ensures documentation accuracy and profile reliability! 🚀**

