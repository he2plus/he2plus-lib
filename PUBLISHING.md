# Publishing he2plus to PyPI

This guide explains how to publish the he2plus library to PyPI so users can install it with `pip install he2plus`.

## Prerequisites

1. **PyPI Account**: Create an account at [pypi.org](https://pypi.org)
2. **TestPyPI Account**: Create an account at [test.pypi.org](https://test.pypi.org) for testing
3. **API Token**: Generate an API token from your PyPI account settings

## Step 1: Prepare for Publishing

### 1.1 Update Version
Update the version in `pyproject.toml`:
```toml
version = "0.1.0"  # Change this for new releases
```

### 1.2 Update README
Ensure README.md is comprehensive and up-to-date.

### 1.3 Run Tests
```bash
cd /Volumes/T7/Projects/Github/he2plus
source venv/bin/activate
python -m pytest tests/ -v
```

### 1.4 Check Package
```bash
python -m build
python -m twine check dist/*
```

## Step 2: Test on TestPyPI

### 2.1 Build Package
```bash
python -m build
```

### 2.2 Upload to TestPyPI
```bash
python -m twine upload --repository testpypi dist/*
```

### 2.3 Test Installation
```bash
pip install --index-url https://test.pypi.org/simple/ he2plus
```

## Step 3: Publish to PyPI

### 3.1 Upload to PyPI
```bash
python -m twine upload dist/*
```

### 3.2 Verify Installation
```bash
pip install he2plus
he2plus --help
```

## Step 4: Automated Publishing with GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/publish.yml`) that automatically publishes to PyPI when you create a release.

### 4.1 Set up Secrets
In your GitHub repository settings, add these secrets:
- `PYPI_API_TOKEN`: Your PyPI API token

### 4.2 Create a Release
1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag the version (e.g., `v0.1.0`)
4. Add release notes
5. Publish the release

The GitHub Action will automatically build and publish to PyPI.

## Step 5: Post-Publication

### 5.1 Update Documentation
- Update the README with installation instructions
- Add usage examples
- Update the changelog

### 5.2 Announce
- Tweet about the release
- Share in relevant communities
- Update your portfolio

## Installation Experience

When users install he2plus, they'll get:

1. **Welcome Message**: Personalized message from Prakhar Tripathi
2. **Interactive Setup**: Guided onboarding process
3. **Use Case Detection**: ML/Cloud/Web3/Web/Mobile/Desktop/DevOps options
4. **System Capacity Check**: RAM, storage, CPU analysis
5. **Installation Plan**: Tailored package recommendations
6. **Shell Commands Guide**: Comprehensive reference
7. **Permission Confirmation**: User approval before installation

## Commands Available After Installation

```bash
he2plus --help          # Show all commands
he2plus welcome         # Interactive setup
he2plus status          # System status
he2plus check           # Dependency check
he2plus info            # System information
he2plus commands        # Shell commands reference
he2plus setup           # Development environment setup
he2plus install <pkg>   # Install a package
```

## Version Management

### Semantic Versioning
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Process
1. Update version in `pyproject.toml`
2. Update changelog in README.md
3. Create GitHub release
4. GitHub Action publishes to PyPI
5. Announce the release

## Troubleshooting

### Common Issues

1. **Build Errors**: Check `pyproject.toml` syntax
2. **Upload Errors**: Verify API token permissions
3. **Installation Errors**: Test on TestPyPI first
4. **Import Errors**: Check package structure

### Getting Help

- Check the [PyPI documentation](https://packaging.python.org/)
- Review [setuptools documentation](https://setuptools.pypa.io/)
- Open an issue on GitHub

## Success Metrics

After publishing, track:
- Download counts on PyPI
- GitHub stars and forks
- User feedback and issues
- Community contributions

## Next Steps

1. **Monitor Usage**: Track downloads and user feedback
2. **Iterate**: Improve based on user needs
3. **Expand**: Add more features and use cases
4. **Community**: Build a community around the library

---

**Remember**: This library was built by a dev frustrated by dependency issues. Let's make the development experience amazing for everyone! 🚀
