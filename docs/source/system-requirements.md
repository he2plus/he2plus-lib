# System Requirements

## Overview

he2plus profiles have different system requirements based on the tools they install.

## General Requirements

### All Profiles
- **Python**: 3.8 or higher
- **Internet**: Broadband connection for downloads
- **Disk**: At least 5GB free space

## Profile-Specific Requirements

### Web3 Solidity
- **RAM**: 8 GB minimum, 16 GB recommended
- **Disk**: 1.2 GB download + 3 GB installed
- **CPU**: Dual-core minimum, quad-core recommended
- **Platform**: macOS, Windows, Linux

### Web Next.js
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk**: 500 MB download + 2 GB installed
- **CPU**: Dual-core minimum
- **Platform**: macOS, Windows, Linux

### Mobile React Native
- **RAM**: 8 GB minimum, 16 GB recommended
- **Disk**: 2 GB download + 10 GB installed (with Android Studio/Xcode)
- **CPU**: Quad-core recommended
- **Platform**: macOS (for iOS), Windows/Linux (for Android only)

### ML Python
- **RAM**: 16 GB minimum, 32 GB recommended
- **Disk**: 5 GB download + 15 GB installed
- **CPU**: Quad-core minimum, 8-core recommended
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended for deep learning)
- **Platform**: macOS, Windows, Linux

## Operating System Support

### macOS
- **Minimum**: macOS 10.14 (Mojave)
- **Recommended**: macOS 12+ (Monterey or newer)
- **Native Support**: Apple Silicon (M1/M2/M3) and Intel

### Windows
- **Minimum**: Windows 10
- **Recommended**: Windows 11
- **Package Manager**: Chocolatey or winget recommended

### Linux
- **Supported Distributions**:
  - Ubuntu 18.04+ (LTS recommended)
  - Debian 10+
  - Fedora 32+
  - CentOS 8+
  - Arch Linux

## Network Requirements

- **Bandwidth**: 10 Mbps minimum for reasonable download speeds
- **Stability**: Stable connection required (installations can be resumed)
- **Firewall**: May need to allow package manager connections

## Disk Space Breakdown

### By Profile
- **web3-solidity**: ~4 GB total
- **web-nextjs**: ~2.5 GB total
- **web-mern**: ~3 GB total
- **mobile-react-native**: ~12 GB total (with SDKs)
- **ml-python**: ~20 GB total
- **utils-docker**: ~5 GB total

### Recommendations
- Keep at least 20 GB free for comfortable development
- Use SSD for better performance
- Consider external storage for large projects

## Performance Considerations

### Compilation Speed
- **SSD vs HDD**: 3-5x faster on SSD
- **RAM**: More RAM = faster compilation
- **CPU**: More cores = faster parallel builds

### Network Speed
Installation times vary by connection:
- **Fast (100+ Mbps)**: 5-10 minutes per profile
- **Medium (25-100 Mbps)**: 10-20 minutes per profile
- **Slow (<25 Mbps)**: 20-40 minutes per profile

## GPU Requirements (ML/AI)

### For Machine Learning
- **NVIDIA GPU**: GTX 1060 or better
- **VRAM**: 6 GB minimum, 8 GB+ recommended
- **CUDA**: Version 11.8 or 12.x
- **cuDNN**: Latest version
- **Drivers**: Up-to-date NVIDIA drivers

### For Deep Learning
- **NVIDIA GPU**: RTX 3070 or better
- **VRAM**: 12 GB minimum, 24 GB+ for large models
- **Multi-GPU**: Supported for distributed training

## Checking Your System

Use the built-in doctor command:

```bash
he2plus doctor
```

This checks:
- ✓ Operating system compatibility
- ✓ Available RAM
- ✓ Free disk space
- ✓ Python version
- ✓ Package managers
- ✓ Network connectivity
