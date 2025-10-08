# Version Control Environment

## Overview

Complete Git ecosystem and version control environment with Git, GitHub CLI, GitLab CLI, and comprehensive Git tools for modern development workflows.

## Profile ID
`utils-version-control`

## Category
Utils

## System Requirements

- **RAM**: 4.0 GB
- **Disk Space**: 5.0 GB
- **CPU Cores**: 2
- **GPU**: Not required
- **Internet**: Required

## Components (29 total)

### Core Version Control
- Git 2.42.0
- Git LFS (Large File Storage)
- Git GUI
- Gitk (Repository viewer)

### Platform CLIs
- GitHub CLI (gh)
- GitLab CLI (glab)
- Bitbucket CLI
- Gitea CLI

### Git Tools
- Git Flow
- Git Extras
- Tig (Text-mode interface)
- Lazygit (Terminal UI)
- GitKraken (GUI client)
- Sourcetree (GUI client)

### Commit Tools
- Commitizen (Conventional commits)
- Commitlint (Commit message linting)
- Husky (Git hooks)
- Pre-commit (Git hook manager)
- Lint-staged (Run linters on staged files)

### Merge & Diff Tools
- Meld (Visual diff)
- Beyond Compare
- KDiff3
- P4Merge

### Code Review
- Git Review
- Gerrit CLI
- Review Board CLI

### Git Utilities
- Git Secrets (Prevent secret commits)
- Git Crypt (Transparent encryption)
- BFG Repo-Cleaner
- Git Filter-Repo

## Quick Start

### Basic Git Workflow
```bash
# Initialize repository
git init

# Clone repository
git clone https://github.com/user/repo.git

# Basic commands
git add .
git commit -m "feat: add new feature"
git push origin main

# Branch management
git checkout -b feature/new-feature
git merge feature/new-feature
```

### GitHub CLI
```bash
# Authenticate
gh auth login

# Create repository
gh repo create myproject --public

# Create pull request
gh pr create --title "Add feature" --body "Description"

# View issues
gh issue list

# Create release
gh release create v1.0.0
```

### GitLab CLI
```bash
# Authenticate
glab auth login

# Create merge request
glab mr create

# View pipelines
glab ci status

# Clone project
glab repo clone group/project
```

### Advanced Git Tools
```bash
# Use Lazygit (Terminal UI)
lazygit

# Use Tig (Text interface)
tig

# Use commitizen
cz commit

# Set up pre-commit hooks
pre-commit install
```

## Development Workflow

1. Clone repository
2. Create feature branch
3. Make changes
4. Use commitizen for conventional commits
5. Run pre-commit hooks
6. Push to remote
7. Create pull request with GitHub CLI
8. Code review and merge

## Pro Tips

- Use conventional commits with commitizen
- Set up pre-commit hooks for code quality
- Use GitHub CLI for faster PR creation
- Leverage Git LFS for large files
- Use Lazygit for easier Git management
- Configure Git aliases for common commands
- Use Git hooks with Husky
- Review code with GUI tools like GitKraken

## Git Configuration

```bash
# Set up user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch
git config --global init.defaultBranch main

# Enable helpful features
git config --global color.ui auto
git config --global pull.rebase false

# Set up aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitLab CLI Documentation](https://gitlab.com/gitlab-org/cli)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

## Installation

```bash
he2plus install utils-version-control
```

