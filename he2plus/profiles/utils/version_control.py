"""
Utils-Version-Control Profile

Complete Git ecosystem and version control environment with Git, GitHub CLI, GitLab CLI,
and comprehensive Git tools for professional development workflows.
"""

from ..base import BaseProfile, Component, ProfileRequirements, VerificationStep, SampleProject


class VersionControlProfile(BaseProfile):
    """Complete Git ecosystem and version control environment."""
    
    def __init__(self):
        super().__init__()
        
        self.id = "utils-version-control"
        self.name = "Version Control Environment"
        self.description = "Complete Git ecosystem and version control environment with Git, GitHub CLI, GitLab CLI, and comprehensive Git tools"
        self.category = "utils"
        self.version = "1.0.0"
    
    def _initialize_profile(self) -> None:
        """Initialize the version control profile."""
        
        # Git tools have minimal requirements
        self.requirements = ProfileRequirements(
            ram_gb=4.0,  # Git tools are lightweight
            disk_gb=5.0,  # Minimal disk usage
            cpu_cores=2,  # Basic requirements
            gpu_required=False,
            gpu_vendor=None,
            cuda_required=False,
            metal_required=False,
            min_os_version=None,
            supported_archs=['x86_64', 'arm64', 'arm'],
            internet_required=True,
            download_size_mb=500.0  # Git tools are relatively small
        )
        
        self.components = [
            # Core Git Tools
            Component(
                id="tool.git",
                name="Git",
                description="Distributed version control system",
                category="tool",
                version="2.51.0",
                download_size_mb=20.0,
                install_time_minutes=3,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git --version",
                verify_expected_output="git version"
            ),
            
            Component(
                id="tool.git-lfs",
                name="Git LFS",
                description="Git Large File Storage for handling large files",
                category="tool",
                version="3.4.1",
                download_size_mb=10.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git lfs version",
                verify_expected_output="git-lfs/"
            ),
            
            # Platform CLIs
            Component(
                id="tool.github-cli",
                name="GitHub CLI",
                description="Official GitHub command line interface",
                category="tool",
                version="2.40.1",
                download_size_mb=25.0,
                install_time_minutes=3,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="gh --version",
                verify_expected_output="gh version"
            ),
            
            Component(
                id="tool.gitlab-cli",
                name="GitLab CLI",
                description="GitLab command line interface",
                category="tool",
                version="1.36.0",
                download_size_mb=20.0,
                install_time_minutes=3,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="glab --version",
                verify_expected_output="glab version"
            ),
            
            Component(
                id="tool.bitbucket-cli",
                name="Bitbucket CLI",
                description="Atlassian Bitbucket command line interface",
                category="tool",
                version="1.0.0",
                download_size_mb=15.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="bitbucket --version",
                verify_expected_output="bitbucket"
            ),
            
            # Git Workflow Tools
            Component(
                id="tool.git-flow",
                name="Git Flow",
                description="Git extensions for branching workflow",
                category="tool",
                version="1.12.3",
                download_size_mb=5.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git flow version",
                verify_expected_output="git-flow"
            ),
            
            Component(
                id="tool.git-hooks",
                name="Git Hooks Manager",
                description="Git hooks management and templates",
                category="tool",
                version="1.0.0",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco'],
                verify_command="git hooks --version",
                verify_expected_output="git-hooks"
            ),
            
            # Git GUI Tools
            Component(
                id="tool.lazygit",
                name="LazyGit",
                description="Simple terminal UI for Git commands",
                category="tool",
                version="0.40.2",
                download_size_mb=10.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="lazygit --version",
                verify_expected_output="lazygit"
            ),
            
            Component(
                id="tool.tig",
                name="Tig",
                description="Text-mode interface for Git",
                category="tool",
                version="2.5.8",
                download_size_mb=5.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="tig --version",
                verify_expected_output="tig"
            ),
            
            Component(
                id="tool.gitui",
                name="GitUI",
                description="Blazing fast terminal-ui for Git",
                category="tool",
                version="0.24.3",
                download_size_mb=8.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="gitui --version",
                verify_expected_output="gitui"
            ),
            
            # Git Enhancement Tools
            Component(
                id="tool.delta",
                name="Delta",
                description="Syntax-highlighting pager for Git",
                category="tool",
                version="0.16.5",
                download_size_mb=5.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="delta --version",
                verify_expected_output="delta"
            ),
            
            Component(
                id="tool.bat",
                name="Bat",
                description="Cat clone with syntax highlighting and Git integration",
                category="tool",
                version="0.24.0",
                download_size_mb=3.0,
                install_time_minutes=1,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="bat --version",
                verify_expected_output="bat"
            ),
            
            Component(
                id="tool.fd",
                name="fd",
                description="Simple, fast and user-friendly alternative to find",
                category="tool",
                version="8.7.1",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="fd --version",
                verify_expected_output="fd"
            ),
            
            Component(
                id="tool.ripgrep",
                name="ripgrep",
                description="Line-oriented search tool that recursively searches directories",
                category="tool",
                version="14.0.3",
                download_size_mb=3.0,
                install_time_minutes=1,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="rg --version",
                verify_expected_output="ripgrep"
            ),
            
            # Git Security Tools
            Component(
                id="tool.git-crypt",
                name="Git Crypt",
                description="Transparent file encryption in Git repositories",
                category="tool",
                version="0.7.0",
                download_size_mb=5.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git-crypt --version",
                verify_expected_output="git-crypt"
            ),
            
            Component(
                id="tool.git-secrets",
                name="Git Secrets",
                description="Prevents you from committing secrets and passwords",
                category="tool",
                version="1.3.0",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git-secrets --version",
                verify_expected_output="git-secrets"
            ),
            
            # Git Automation Tools
            Component(
                id="tool.husky",
                name="Husky",
                description="Git hooks made easy",
                category="tool",
                version="8.0.3",
                download_size_mb=5.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['npm'],
                verify_command="npx husky --version",
                verify_expected_output="husky"
            ),
            
            Component(
                id="tool.lint-staged",
                name="Lint Staged",
                description="Run linters on staged files",
                category="tool",
                version="15.2.0",
                download_size_mb=3.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['npm'],
                verify_command="npx lint-staged --version",
                verify_expected_output="lint-staged"
            ),
            
            Component(
                id="tool.commitizen",
                name="Commitizen",
                description="Conventional commit messages",
                category="tool",
                version="4.3.0",
                download_size_mb=5.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['npm'],
                verify_command="npx commitizen --version",
                verify_expected_output="commitizen"
            ),
            
            Component(
                id="tool.semantic-release",
                name="Semantic Release",
                description="Fully automated version management and package publishing",
                category="tool",
                version="22.0.8",
                download_size_mb=10.0,
                install_time_minutes=3,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['npm'],
                verify_command="npx semantic-release --version",
                verify_expected_output="semantic-release"
            ),
            
            # Git Analysis Tools
            Component(
                id="tool.git-quick-stats",
                name="Git Quick Stats",
                description="Simple and efficient way to access various Git statistics",
                category="tool",
                version="2.5.7",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git-quick-stats --version",
                verify_expected_output="git-quick-stats"
            ),
            
            Component(
                id="tool.git-fame",
                name="Git Fame",
                description="Pretty-print Git repository statistics",
                category="tool",
                version="1.16.0",
                download_size_mb=3.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git-fame --version",
                verify_expected_output="git-fame"
            ),
            
            Component(
                id="tool.git-standup",
                name="Git Standup",
                description="Recall what you did on the last working day",
                category="tool",
                version="2.5.4",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git-standup --version",
                verify_expected_output="git-standup"
            ),
            
            # Git Backup and Sync Tools
            Component(
                id="tool.git-annex",
                name="Git Annex",
                description="Manage files with Git, without checking them into Git",
                category="tool",
                version="10.20231009",
                download_size_mb=20.0,
                install_time_minutes=5,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git-annex version",
                verify_expected_output="git-annex"
            ),
            
            Component(
                id="tool.git-bundle",
                name="Git Bundle",
                description="Package repositories for offline transfer",
                category="tool",
                version="2.51.0",
                download_size_mb=1.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['included'],
                verify_command="git bundle --help",
                verify_expected_output="git-bundle"
            ),
            
            # Git Configuration and Templates
            Component(
                id="tool.gitignore-templates",
                name="Git Ignore Templates",
                description="Collection of .gitignore templates",
                category="tool",
                version="1.0.0",
                download_size_mb=5.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="gitignore --version",
                verify_expected_output="gitignore"
            ),
            
            Component(
                id="tool.gitconfig-templates",
                name="Git Config Templates",
                description="Professional Git configuration templates",
                category="tool",
                version="1.0.0",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git config --global --list",
                verify_expected_output="user.name"
            ),
            
            # Git Learning and Documentation Tools
            Component(
                id="tool.git-extras",
                name="Git Extras",
                description="GIT utilities -- repo summary, repl, changelog population, author commit percentages and more",
                category="tool",
                version="7.0.0",
                download_size_mb=5.0,
                install_time_minutes=2,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git extras --version",
                verify_expected_output="git-extras"
            ),
            
            Component(
                id="tool.git-tips",
                name="Git Tips",
                description="Collection of useful Git tips and tricks",
                category="tool",
                version="1.0.0",
                download_size_mb=2.0,
                install_time_minutes=1,
                depends_on=['tool.git'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="git-tips --help",
                verify_expected_output="git-tips"
            )
        ]
        
        # Verification steps for all installed components
        self.verification_steps = [
            VerificationStep(
                name="Git Core",
                command="git --version",
                expected_output=None,
                contains_text="git version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git LFS",
                command="git lfs version",
                expected_output=None,
                contains_text="git-lfs/",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="GitHub CLI",
                command="gh --version",
                expected_output=None,
                contains_text="gh version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="GitLab CLI",
                command="glab --version",
                expected_output=None,
                contains_text="glab version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git Flow",
                command="git flow version",
                expected_output=None,
                contains_text="git-flow",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="LazyGit",
                command="lazygit --version",
                expected_output=None,
                contains_text="lazygit",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Tig",
                command="tig --version",
                expected_output=None,
                contains_text="tig",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="GitUI",
                command="gitui --version",
                expected_output=None,
                contains_text="gitui",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Delta",
                command="delta --version",
                expected_output=None,
                contains_text="delta",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Bat",
                command="bat --version",
                expected_output=None,
                contains_text="bat",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="fd",
                command="fd --version",
                expected_output=None,
                contains_text="fd",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="ripgrep",
                command="rg --version",
                expected_output=None,
                contains_text="ripgrep",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git Crypt",
                command="git-crypt --version",
                expected_output=None,
                contains_text="git-crypt",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git Secrets",
                command="git-secrets --version",
                expected_output=None,
                contains_text="git-secrets",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Husky",
                command="npx husky --version",
                expected_output=None,
                contains_text="husky",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Lint Staged",
                command="npx lint-staged --version",
                expected_output=None,
                contains_text="lint-staged",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Commitizen",
                command="npx commitizen --version",
                expected_output=None,
                contains_text="commitizen",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Semantic Release",
                command="npx semantic-release --version",
                expected_output=None,
                contains_text="semantic-release",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git Quick Stats",
                command="git-quick-stats --version",
                expected_output=None,
                contains_text="git-quick-stats",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git Fame",
                command="git-fame --version",
                expected_output=None,
                contains_text="git-fame",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git Standup",
                command="git-standup --version",
                expected_output=None,
                contains_text="git-standup",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Git Annex",
                command="git-annex version",
                expected_output=None,
                contains_text="git-annex",
                timeout_seconds=10
            )
        ]
        
        # Sample project for version control
        self.sample_project = SampleProject(
            name="Git Workflow Starter Kit",
            description="Complete Git workflow setup with hooks, templates, and best practices",
            type="git_clone",
            source="https://github.com/he2plus/git-workflow-kit.git",
            directory="~/git-project",
            setup_commands=[
                "cd ~/git-project",
                "git init",
                "npx husky install",
                "npx husky add .husky/pre-commit 'npx lint-staged'",
                "npx husky add .husky/commit-msg 'npx commitizen --hook'",
                "git add .",
                "git commit -m 'feat: initial commit with Git workflow setup'"
            ],
            next_steps=[
                "Configure Git user: git config --global user.name 'Your Name'",
                "Configure Git email: git config --global user.email 'your.email@example.com'",
                "Set up SSH keys: ssh-keygen -t ed25519 -C 'your.email@example.com'",
                "Authenticate GitHub: gh auth login",
                "Authenticate GitLab: glab auth login",
                "Try LazyGit: lazygit",
                "Try GitUI: gitui",
                "Set up Git hooks: npx husky install"
            ]
        )
        
        # Comprehensive next steps for version control
        self.next_steps = [
            "🎉 Complete Git ecosystem and version control environment ready!",
            "",
            "🔧 Core Git Tools Installed:",
            "   ✅ Git 2.51.0 (Distributed version control)",
            "   ✅ Git LFS 3.4.1 (Large file storage)",
            "   ✅ GitHub CLI 2.40.1 (GitHub integration)",
            "   ✅ GitLab CLI 1.36.0 (GitLab integration)",
            "   ✅ Bitbucket CLI 1.0.0 (Bitbucket integration)",
            "",
            "🔄 Git Workflow Tools:",
            "   ✅ Git Flow 1.12.3 (Branching workflow)",
            "   ✅ Git Hooks Manager (Hooks management)",
            "   ✅ Husky 8.0.3 (Git hooks made easy)",
            "   ✅ Lint Staged 15.2.0 (Staged file linting)",
            "   ✅ Commitizen 4.3.0 (Conventional commits)",
            "   ✅ Semantic Release 22.0.8 (Automated releases)",
            "",
            "🖥️ Git GUI Tools:",
            "   ✅ LazyGit 0.40.2 (Terminal Git UI)",
            "   ✅ Tig 2.5.8 (Text-mode Git interface)",
            "   ✅ GitUI 0.24.3 (Fast terminal Git UI)",
            "",
            "🎨 Git Enhancement Tools:",
            "   ✅ Delta 0.16.5 (Syntax-highlighting pager)",
            "   ✅ Bat 0.24.0 (Cat clone with syntax highlighting)",
            "   ✅ fd 8.7.1 (User-friendly find alternative)",
            "   ✅ ripgrep 14.0.3 (Line-oriented search tool)",
            "",
            "🔒 Git Security Tools:",
            "   ✅ Git Crypt 0.7.0 (File encryption in Git)",
            "   ✅ Git Secrets 1.3.0 (Prevent secret commits)",
            "",
            "📊 Git Analysis Tools:",
            "   ✅ Git Quick Stats 2.5.7 (Git statistics)",
            "   ✅ Git Fame 1.16.0 (Repository statistics)",
            "   ✅ Git Standup 2.5.4 (Daily work summary)",
            "",
            "💾 Git Backup & Sync:",
            "   ✅ Git Annex 10.20231009 (Large file management)",
            "   ✅ Git Bundle (Offline repository transfer)",
            "",
            "📚 Git Learning & Documentation:",
            "   ✅ Git Extras 7.0.0 (Additional Git utilities)",
            "   ✅ Git Tips (Useful Git tips and tricks)",
            "   ✅ Git Ignore Templates (.gitignore templates)",
            "   ✅ Git Config Templates (Professional configurations)",
            "",
            "🚀 Quick Start Options:",
            "  1. Basic Git Setup:",
            "     git config --global user.name 'Your Name'",
            "     git config --global user.email 'your.email@example.com'",
            "     ssh-keygen -t ed25519 -C 'your.email@example.com'",
            "",
            "  2. Platform Authentication:",
            "     gh auth login  # GitHub",
            "     glab auth login  # GitLab",
            "     bitbucket auth login  # Bitbucket",
            "",
            "  3. GUI Tools:",
            "     lazygit  # Terminal Git UI",
            "     gitui  # Fast terminal Git UI",
            "     tig  # Text-mode Git interface",
            "",
            "  4. Workflow Setup:",
            "     npx husky install",
            "     npx husky add .husky/pre-commit 'npx lint-staged'",
            "     npx husky add .husky/commit-msg 'npx commitizen --hook'",
            "",
            "  5. Git Flow Workflow:",
            "     git flow init",
            "     git flow feature start my-feature",
            "     git flow feature finish my-feature",
            "",
            "📋 Common Git Commands:",
            "  • Clone: git clone <repository-url>",
            "  • Status: git status",
            "  • Add: git add <file>",
            "  • Commit: git commit -m 'message'",
            "  • Push: git push origin <branch>",
            "  • Pull: git pull origin <branch>",
            "  • Branch: git branch <branch-name>",
            "  • Checkout: git checkout <branch>",
            "  • Merge: git merge <branch>",
            "  • Log: git log --oneline",
            "",
            "🔧 Advanced Git Features:",
            "  • Interactive Rebase: git rebase -i HEAD~3",
            "  • Cherry Pick: git cherry-pick <commit-hash>",
            "  • Stash: git stash push -m 'message'",
            "  • Reset: git reset --hard HEAD~1",
            "  • Revert: git revert <commit-hash>",
            "  • Blame: git blame <file>",
            "  • Bisect: git bisect start",
            "",
            "📖 Resources:",
            "  • Git Documentation: https://git-scm.com/doc",
            "  • GitHub Docs: https://docs.github.com/",
            "  • GitLab Docs: https://docs.gitlab.com/",
            "  • Bitbucket Docs: https://support.atlassian.com/bitbucket-cloud/",
            "  • Conventional Commits: https://conventionalcommits.org/",
            "  • Semantic Versioning: https://semver.org/",
            "",
            "💡 Pro Tips:",
            "  • Use LazyGit for interactive Git operations",
            "  • Set up Git hooks with Husky for code quality",
            "  • Use conventional commits for better changelogs",
            "  • Leverage Git LFS for large files",
            "  • Use Git Flow for structured branching",
            "  • Enable Delta for beautiful diffs",
            "  • Use ripgrep for fast code searching",
            "  • Set up semantic release for automated versioning",
            "",
            "🔗 Community:",
            "  • Git Community: https://git-scm.com/community",
            "  • GitHub Community: https://github.community/",
            "  • GitLab Community: https://forum.gitlab.com/",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/git",
            "",
            "📞 Support:",
            "  • Git-specific documentation and tutorials",
            "  • Platform-specific authentication guides",
            "  • he2plus Community: https://discord.gg/he2plus"
        ]
