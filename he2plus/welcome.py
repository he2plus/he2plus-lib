"""
Welcome system for he2plus library
"""

import os
import sys
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
import inquirer
from .utils import Logger
from .system import SystemManager


class WelcomeSystem:
    """Interactive welcome and onboarding system"""
    
    def __init__(self, logger: Logger, system_manager: SystemManager):
        """
        Initialize welcome system
        
        Args:
            logger: Logger instance
            system_manager: SystemManager instance
        """
        self.logger = logger
        self.system = system_manager
        self.console = Console()
        
    def show_welcome(self) -> None:
        """Show welcome message and author information"""
        welcome_text = Text()
        welcome_text.append("🚀 Welcome to he2plus!\n\n", style="bold blue")
        welcome_text.append("Happy coding! This was built by a dev frustrated by dependency issues\n", style="green")
        welcome_text.append("and hence he cared for you.\n\n", style="green")
        welcome_text.append("Prakhar Tripathi - @https://twitter.com/he2plus\n", style="bold yellow")
        welcome_text.append("\nLet's make your development experience amazing! 🎉", style="bold green")
        
        panel = Panel(
            welcome_text,
            title="[bold blue]he2plus - Developer Productivity Library[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def get_use_case(self) -> str:
        """
        Get user's intended use case
        
        Returns:
            Selected use case
        """
        self.console.print("[bold cyan]What's your primary development focus?[/bold cyan]")
        
        questions = [
            inquirer.List(
                'use_case',
                message="Select your use case",
                choices=[
                    ('Machine Learning & AI', 'ml'),
                    ('Cloud Development', 'cloud'),
                    ('Web3 & Blockchain', 'web3'),
                    ('Web Development', 'web'),
                    ('Mobile Development', 'mobile'),
                    ('Desktop Applications', 'desktop'),
                    ('DevOps & Infrastructure', 'devops'),
                    ('General Development', 'general'),
                    ('I\'m not sure yet', 'unsure')
                ]
            )
        ]
        
        answers = inquirer.prompt(questions)
        return answers['use_case'] if answers else 'general'
    
    def show_system_capacity(self) -> Dict[str, Any]:
        """
        Show system capacity information
        
        Returns:
            System capacity information
        """
        system_info = self.system.get_system_info()
        
        # Calculate storage info
        import shutil
        total, used, free = shutil.disk_usage("/")
        total_gb = total // (1024**3)
        used_gb = used // (1024**3)
        free_gb = free // (1024**3)
        
        # Get memory info
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total // (1024**3)
        memory_used_gb = memory.used // (1024**3)
        memory_free_gb = memory.available // (1024**3)
        
        capacity_info = {
            'storage': {
                'total': total_gb,
                'used': used_gb,
                'free': free_gb,
                'percent_used': (used_gb / total_gb) * 100
            },
            'memory': {
                'total': memory_gb,
                'used': memory_used_gb,
                'free': memory_free_gb,
                'percent_used': memory.percent
            },
            'cpu_cores': system_info.get('cpu_count', 1),
            'platform': system_info.get('platform', 'unknown')
        }
        
        # Display system capacity
        table = Table(title="🖥️  Your System Capacity")
        table.add_column("Resource", style="cyan")
        table.add_column("Total", style="green")
        table.add_column("Used", style="yellow")
        table.add_column("Free", style="blue")
        table.add_column("Status", style="magenta")
        
        # Storage row
        storage_status = "✅ Good" if capacity_info['storage']['free'] > 10 else "⚠️  Low"
        table.add_row(
            "Storage",
            f"{capacity_info['storage']['total']} GB",
            f"{capacity_info['storage']['used']} GB",
            f"{capacity_info['storage']['free']} GB",
            storage_status
        )
        
        # Memory row
        memory_status = "✅ Good" if capacity_info['memory']['free'] > 2 else "⚠️  Low"
        table.add_row(
            "Memory",
            f"{capacity_info['memory']['total']} GB",
            f"{capacity_info['memory']['used']} GB",
            f"{capacity_info['memory']['free']} GB",
            memory_status
        )
        
        # CPU row
        cpu_status = "✅ Good" if capacity_info['cpu_cores'] >= 4 else "⚠️  Limited"
        table.add_row(
            "CPU Cores",
            f"{capacity_info['cpu_cores']}",
            "-",
            "-",
            cpu_status
        )
        
        self.console.print(table)
        self.console.print()
        
        return capacity_info
    
    def get_installation_plan(self, use_case: str, capacity_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get installation plan based on use case and system capacity
        
        Args:
            use_case: User's selected use case
            capacity_info: System capacity information
            
        Returns:
            Installation plan
        """
        plans = {
            'ml': {
                'name': 'Machine Learning & AI',
                'packages': ['python', 'pip', 'git', 'jupyter', 'numpy', 'pandas', 'scikit-learn'],
                'optional': ['tensorflow', 'torch', 'conda'],
                'storage_required': 8,  # GB
                'memory_required': 8,   # GB
                'description': 'Python, Jupyter, NumPy, Pandas, Scikit-learn, TensorFlow, PyTorch'
            },
            'cloud': {
                'name': 'Cloud Development',
                'packages': ['python', 'pip', 'git', 'docker', 'kubectl', 'aws-cli'],
                'optional': ['azure-cli', 'gcloud', 'terraform'],
                'storage_required': 5,  # GB
                'memory_required': 4,   # GB
                'description': 'Docker, Kubernetes, AWS CLI, Azure CLI, Google Cloud SDK'
            },
            'web3': {
                'name': 'Web3 & Blockchain',
                'packages': ['python', 'pip', 'git', 'nodejs', 'hardhat', 'brownie'],
                'optional': ['solana', 'foundry', 'truffle'],
                'storage_required': 3,  # GB
                'memory_required': 4,   # GB
                'description': 'Node.js, Hardhat, Brownie, Solana CLI, Foundry'
            },
            'web': {
                'name': 'Web Development',
                'packages': ['python', 'pip', 'git', 'nodejs', 'npm', 'yarn'],
                'optional': ['docker', 'nginx', 'redis'],
                'storage_required': 2,  # GB
                'memory_required': 2,   # GB
                'description': 'Node.js, npm, yarn, Docker, nginx, Redis'
            },
            'mobile': {
                'name': 'Mobile Development',
                'packages': ['python', 'pip', 'git', 'nodejs', 'react-native'],
                'optional': ['flutter', 'android-studio', 'xcode'],
                'storage_required': 10, # GB
                'memory_required': 8,   # GB
                'description': 'React Native, Flutter, Android Studio, Xcode'
            },
            'desktop': {
                'name': 'Desktop Applications',
                'packages': ['python', 'pip', 'git', 'tkinter', 'pyqt'],
                'optional': ['electron', 'tauri'],
                'storage_required': 2,  # GB
                'memory_required': 2,   # GB
                'description': 'Tkinter, PyQt, Electron, Tauri'
            },
            'devops': {
                'name': 'DevOps & Infrastructure',
                'packages': ['python', 'pip', 'git', 'docker', 'kubectl', 'terraform'],
                'optional': ['ansible', 'vagrant', 'packer'],
                'storage_required': 6,  # GB
                'memory_required': 4,   # GB
                'description': 'Docker, Kubernetes, Terraform, Ansible, Vagrant'
            },
            'general': {
                'name': 'General Development',
                'packages': ['python', 'pip', 'git', 'curl', 'wget'],
                'optional': ['docker', 'nodejs'],
                'storage_required': 1,  # GB
                'memory_required': 1,   # GB
                'description': 'Python, pip, git, curl, wget, Docker, Node.js'
            }
        }
        
        plan = plans.get(use_case, plans['general'])
        
        # Check if system can handle the requirements
        storage_ok = capacity_info['storage']['free'] >= plan['storage_required']
        memory_ok = capacity_info['memory']['free'] >= plan['memory_required']
        
        # Display installation plan
        self.console.print(f"[bold cyan]📋 Installation Plan for {plan['name']}[/bold cyan]")
        self.console.print(f"[green]Description:[/green] {plan['description']}")
        self.console.print(f"[yellow]Storage Required:[/yellow] {plan['storage_required']} GB")
        self.console.print(f"[yellow]Memory Required:[/yellow] {plan['memory_required']} GB")
        
        # System compatibility check
        if storage_ok and memory_ok:
            self.console.print("[green]✅ Your system can handle this installation![/green]")
        else:
            self.console.print("[red]⚠️  Warning: Your system might struggle with this installation[/red]")
            if not storage_ok:
                self.console.print(f"[red]   - Need {plan['storage_required']} GB storage, have {capacity_info['storage']['free']} GB[/red]")
            if not memory_ok:
                self.console.print(f"[red]   - Need {plan['memory_required']} GB memory, have {capacity_info['memory']['free']} GB[/red]")
        
        self.console.print()
        
        return plan
    
    def confirm_installation(self, plan: Dict[str, Any]) -> bool:
        """
        Confirm installation with user
        
        Args:
            plan: Installation plan
            
        Returns:
            True if user confirms, False otherwise
        """
        self.console.print("[bold yellow]⚠️  Installation Confirmation[/bold yellow]")
        self.console.print("This will install the following packages:")
        
        for package in plan['packages']:
            self.console.print(f"  • {package}")
        
        if plan['optional']:
            self.console.print("\nOptional packages (will be installed if available):")
            for package in plan['optional']:
                self.console.print(f"  • {package}")
        
        self.console.print()
        
        return Confirm.ask("Do you want to proceed with the installation?", default=True)
    
    def show_shell_commands_guide(self) -> None:
        """Show shell commands reference guide"""
        self.console.print("[bold cyan]📚 Shell Commands Reference[/bold cyan]")
        
        commands_table = Table(title="Essential Shell Commands")
        commands_table.add_column("Command", style="cyan")
        commands_table.add_column("Description", style="green")
        commands_table.add_column("Example", style="yellow")
        
        commands = [
            ("ls", "List directory contents", "ls -la"),
            ("cd", "Change directory", "cd /path/to/directory"),
            ("pwd", "Print working directory", "pwd"),
            ("mkdir", "Create directory", "mkdir new_folder"),
            ("rm", "Remove files/directories", "rm -rf old_folder"),
            ("cp", "Copy files", "cp file.txt backup.txt"),
            ("mv", "Move/rename files", "mv old_name.txt new_name.txt"),
            ("cat", "Display file contents", "cat file.txt"),
            ("grep", "Search in files", "grep 'pattern' file.txt"),
            ("find", "Find files", "find . -name '*.py'"),
            ("chmod", "Change permissions", "chmod +x script.sh"),
            ("sudo", "Run as administrator", "sudo apt update"),
            ("ps", "Show running processes", "ps aux"),
            ("kill", "Terminate process", "kill -9 PID"),
            ("top", "Show system processes", "top"),
            ("df", "Show disk usage", "df -h"),
            ("free", "Show memory usage", "free -h"),
            ("curl", "Download from URL", "curl -O https://example.com/file"),
            ("wget", "Download files", "wget https://example.com/file"),
            ("tar", "Archive files", "tar -czf archive.tar.gz folder/"),
            ("unzip", "Extract zip files", "unzip file.zip"),
            ("ssh", "Connect to remote server", "ssh user@server.com"),
            ("scp", "Copy files over SSH", "scp file.txt user@server.com:/path/"),
            ("git", "Version control", "git clone https://github.com/user/repo"),
            ("docker", "Container management", "docker run -it ubuntu"),
            ("kubectl", "Kubernetes management", "kubectl get pods"),
            ("npm", "Node.js package manager", "npm install package"),
            ("pip", "Python package manager", "pip install package"),
            ("conda", "Conda package manager", "conda install package"),
            ("brew", "Homebrew package manager", "brew install package"),
        ]
        
        for command, description, example in commands:
            commands_table.add_row(command, description, example)
        
        self.console.print(commands_table)
        self.console.print()
        
        # Save to file
        try:
            with open(os.path.expanduser("~/.he2plus/shell_commands.txt"), "w") as f:
                f.write("he2plus Shell Commands Reference\n")
                f.write("=" * 40 + "\n\n")
                for command, description, example in commands:
                    f.write(f"{command:<12} - {description}\n")
                    f.write(f"{'':<12}   Example: {example}\n\n")
            
            self.console.print(f"[green]📄 Commands reference saved to ~/.he2plus/shell_commands.txt[/green]")
        except Exception as e:
            self.logger.warning(f"Could not save commands reference: {e}")
    
    def run_onboarding(self) -> Dict[str, Any]:
        """
        Run complete onboarding process
        
        Returns:
            Onboarding results
        """
        try:
            # Show welcome
            self.show_welcome()
            
            # Get use case
            use_case = self.get_use_case()
            
            # Show system capacity
            capacity_info = self.show_system_capacity()
            
            # Get installation plan
            plan = self.get_installation_plan(use_case, capacity_info)
            
            # Confirm installation
            confirmed = self.confirm_installation(plan)
            
            # Show shell commands guide
            if Confirm.ask("Would you like to see the shell commands reference?", default=True):
                self.show_shell_commands_guide()
            
            return {
                'use_case': use_case,
                'plan': plan,
                'confirmed': confirmed,
                'capacity_info': capacity_info
            }
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Installation cancelled by user[/yellow]")
            return {'confirmed': False}
        except Exception as e:
            self.logger.error(f"Error during onboarding: {e}")
            self.console.print(f"[red]Error during onboarding: {e}[/red]")
            return {'confirmed': False}
