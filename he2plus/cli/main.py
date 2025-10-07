"""
Main CLI interface for he2plus.

This module provides the command-line interface for the he2plus
development environment manager.
"""

import click
import sys
import subprocess
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm, Prompt
import structlog

from ..core.system import SystemProfiler
from ..core.validator import SystemValidator
from ..core.installer import InstallationEngine
from ..profiles.registry import ProfileRegistry
from ..components.languages.python import PythonInstaller
from ..components.languages.node import NodeInstaller
from ..components.tools.git import GitInstaller

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

console = Console()
logger = structlog.get_logger(__name__)


@click.group()
@click.version_option(version="0.3.0")
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Quiet output')
@click.pass_context
def cli(ctx, verbose, quiet):
    """he2plus - Professional Development Environment Manager
    
    From zero to deploy in one command. No configuration, no frustration, just code.
    
    Install complete development stacks with one command.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    
    # Set logging level
    if verbose:
        structlog.configure(processors=[structlog.dev.ConsoleRenderer()])
    elif quiet:
        structlog.configure(processors=[])


@cli.command()
@click.argument('profiles', nargs=-1, required=True)
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def install(ctx, profiles, yes, verbose):
    """Install one or more development profiles.
    
    Examples:
      he2plus install web3-solidity
      he2plus install web-nextjs mobile-react-native
    """
    
    console.print("\n🔍 Analyzing system...", style="cyan")
    
    # Detect system
    system_profiler = SystemProfiler()
    system = system_profiler.profile()
    
    console.print(f"   ✓ {system.os_name} {system.os_version} ({system.arch})")
    console.print(f"   ✓ {system.ram_total_gb} GB RAM ({system.ram_available_gb} GB available)")
    console.print(f"   ✓ {system.disk_free_gb} GB disk free\n")
    
    # Load profiles
    registry = ProfileRegistry()
    profile_objects = []
    
    for profile_name in profiles:
        profile = registry.get(profile_name)
        if not profile:
            console.print(f"❌ Profile not found: {profile_name}", style="red")
            console.print(f"   Run 'he2plus list --available' to see all profiles")
            return
        profile_objects.append(profile)
    
    # Validate resources
    validator = SystemValidator(system)
    
    for profile in profile_objects:
        validation = validator.validate(profile.get_requirements())
        
        if not validation.safe_to_install:
            console.print(f"\n❌ Cannot install {profile.name}:", style="red")
            for issue in validation.blocking_issues:
                console.print(f"   • {issue}", style="red")
            return
        
        if validation.warnings:
            console.print(f"\n⚠️  Warnings for {profile.name}:", style="yellow")
            for warning in validation.warnings:
                console.print(f"   • {warning}", style="yellow")
    
    # Show installation plan
    console.print("\n📋 Installation Plan:\n", style="cyan bold")
    
    total_download_mb = 0
    total_disk_gb = 0
    total_time_minutes = 0
    
    for profile in profile_objects:
        console.print(f"[bold]{profile.name}[/bold]")
        console.print(f"  {profile.description}")
        
        components = profile.get_components()
        console.print(f"  Components: {len(components)}")
        
        # Calculate sizes
        download_mb = profile.get_estimated_download_size()
        disk_gb = profile.get_requirements().disk_gb
        time_minutes = profile.get_estimated_install_time()
        
        total_download_mb += download_mb
        total_disk_gb += disk_gb
        total_time_minutes += time_minutes
        
        console.print(f"  Download: ~{download_mb} MB")
        console.print(f"  Disk space: ~{disk_gb} GB")
        console.print(f"  Time: ~{time_minutes} minutes\n")
    
    console.print(f"⏱️  Estimated time: {total_time_minutes} minutes")
    console.print(f"💾 Total download: ~{total_download_mb} MB")
    console.print(f"💽 Disk space after: ~{system.disk_free_gb - total_disk_gb:.1f} GB free\n")
    
    # Confirm
    if not yes:
        if not Confirm.ask("Continue with installation?"):
            console.print("Installation cancelled.")
            return
    
    # Install
    console.print("\n📦 Installing...\n", style="cyan bold")
    
    # Initialize installation engine
    installer = InstallationEngine(system)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        for profile in profile_objects:
            task = progress.add_task(
                f"[cyan]Installing {profile.name}...", 
                total=len(profile.get_components())
            )
            
            # Install each component
            for component in profile.get_components():
                progress.update(task, description=f"[cyan]{component.name}")
                
                # Use the new installation engine
                result = installer.install_component(component, progress, task)
                
                if not result.success:
                    console.print(f"❌ Failed to install {component.name}: {result.error}", style="red")
                    if result.warnings:
                        for warning in result.warnings:
                            console.print(f"   ⚠️  {warning}", style="yellow")
        
        if result.warnings:
            for warning in result.warnings:
                console.print(f"   ⚠️  {warning}", style="yellow")
        
        progress.update(task, advance=1)
    
    # Verify
    console.print("\n🔍 Verifying installation...\n", style="cyan")
    
    all_verified = True
    for profile in profile_objects:
        verified = verify_profile(profile, installer)
        if verified:
            console.print(f"✓ {profile.name} verified", style="green")
        else:
            console.print(f"❌ {profile.name} verification failed", style="red")
            all_verified = False
    
    if all_verified:
        console.print("\n✅ All profiles installed successfully!\n", style="green bold")
        
        # Show next steps
        for profile in profile_objects:
            console.print(Panel(
                "\n".join(profile.get_next_steps()),
                title=f"🎉 {profile.name} Ready!",
                border_style="green"
            ))
    else:
        console.print("\n⚠️  Some installations failed verification", style="yellow")
        console.print("   Run 'he2plus doctor' for diagnostics\n")


@cli.command()
@click.option('--available', '-a', is_flag=True, help='Show all available profiles')
@click.option('--category', '-c', help='Filter by category')
def list(available, category):
    """List installed or available profiles."""
    
    registry = ProfileRegistry()
    
    if available:
        console.print("\n📦 Available Profiles:\n", style="cyan bold")
        
        categories = registry.get_categories()
        
        for cat in categories:
            if category and cat != category:
                continue
                
            console.print(f"\n[bold]{cat.upper()}[/bold]")
            profiles = registry.get_by_category(cat)
            
            for profile in profiles:
                console.print(f"  • [cyan]{profile.id}[/cyan] - {profile.description}")
        
        console.print(f"\n💡 Install with: he2plus install <profile-id>\n")
    else:
        console.print("\n📦 Installed Profiles:\n", style="cyan bold")
        # Show installed profiles
        console.print("  (none installed yet)\n")


@cli.command()
@click.option('--profile', '-p', help='Check specific profile')
@click.option('--fix', '-f', is_flag=True, help='Attempt to fix issues')
def doctor(profile, fix):
    """Run system diagnostics."""
    
    console.print("\n🏥 System Health Check\n", style="cyan bold")
    
    # System detection
    system_profiler = SystemProfiler()
    system = system_profiler.profile()
    
    # Create system info table
    table = Table(title="System Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("OS", f"{system.os_name} {system.os_version}")
    table.add_row("Architecture", system.arch)
    table.add_row("CPU", f"{system.cpu_name} ({system.cpu_cores} cores)")
    table.add_row("RAM", f"{system.ram_total_gb} GB ({system.ram_available_gb} GB available)")
    table.add_row("Disk", f"{system.disk_free_gb} GB free")
    
    if system.gpu_name:
        table.add_row("GPU", system.gpu_name)
    
    console.print(table)
    
    # Check development tools
    console.print("\n🛠️  Development Tools:", style="bold")
    
    tools_table = Table()
    tools_table.add_column("Tool", style="cyan")
    tools_table.add_column("Status", style="green")
    tools_table.add_column("Version", style="yellow")
    
    # Check common tools
    tools = ['git', 'python3', 'node', 'docker']
    for tool in tools:
        installed = check_tool_installed(tool)
        if installed:
            tools_table.add_row(tool, "✓ Installed", installed['version'])
        else:
            tools_table.add_row(tool, "❌ Not installed", "N/A")
    
    console.print(tools_table)
    
    # Check package managers
    console.print("\n📦 Package Managers:", style="bold")
    
    pm_table = Table()
    pm_table.add_column("Package Manager", style="cyan")
    pm_table.add_column("Status", style="green")
    
    for pm in system.package_managers:
        pm_table.add_row(pm, "✓ Available")
    
    if not system.package_managers:
        pm_table.add_row("None", "❌ No package managers found")
    
    console.print(pm_table)
    
    # Check specific profile if requested
    if profile:
        console.print(f"\n🔍 Checking profile: {profile}", style="bold")
        registry = ProfileRegistry()
        profile_obj = registry.get(profile)
        if profile_obj:
            validator = SystemValidator(system)
            validation = validator.validate(profile_obj.get_requirements())
            
            if validation.safe_to_install:
                console.print("✓ Profile can be installed", style="green")
            else:
                console.print("❌ Profile cannot be installed:", style="red")
                for issue in validation.blocking_issues:
                    console.print(f"   • {issue}", style="red")
        else:
            console.print(f"❌ Profile not found: {profile}", style="red")
    
    console.print("\n")


@cli.command()
@click.argument('profile', required=False)
@click.option('--json', '-j', is_flag=True, help='Output as JSON')
def info(profile, json):
    """Show system or profile information."""
    
    if profile:
        # Show profile info
        registry = ProfileRegistry()
        profile_obj = registry.get(profile)
        
        if not profile_obj:
            console.print(f"❌ Profile not found: {profile}", style="red")
            return
        
        if json:
            import json
            console.print(json.dumps(profile_obj.to_dict(), indent=2))
            return
        
        console.print(f"\n📦 {profile_obj.name}\n", style="cyan bold")
        console.print(f"{profile_obj.description}\n")
        console.print(f"Category: {profile_obj.category}")
        console.print(f"Version: {profile_obj.version}")
        
        # Requirements
        req = profile_obj.get_requirements()
        console.print(f"\nRequirements:")
        console.print(f"  • RAM: {req.ram_gb} GB")
        console.print(f"  • Disk: {req.disk_gb} GB")
        console.print(f"  • CPU: {req.cpu_cores} cores")
        if req.gpu_required:
            console.print(f"  • GPU: Required")
        
        # Components
        components = profile_obj.get_components()
        console.print(f"\nComponents ({len(components)}):")
        for component in components:
            console.print(f"  • {component.name} ({component.category})")
        
        # Verification steps
        verification = profile_obj.get_verification_steps()
        console.print(f"\nVerification Steps ({len(verification)}):")
        for step in verification:
            console.print(f"  • {step.name}: {step.command}")
        
        # Sample project
        if profile_obj.get_sample_project():
            sample = profile_obj.get_sample_project()
            console.print(f"\nSample Project:")
            console.print(f"  • Name: {sample.name}")
            console.print(f"  • Type: {sample.type}")
            console.print(f"  • Source: {sample.source}")
        
        console.print(f"\n📖 Documentation: https://he2plus.dev/docs/profiles/{profile}\n")
    else:
        # Show system info
        system_profiler = SystemProfiler()
        system = system_profiler.profile()
        
        if json:
            import json
            console.print(json.dumps({
                "os_name": system.os_name,
                "os_version": system.os_version,
                "arch": system.arch,
                "cpu_name": system.cpu_name,
                "cpu_cores": system.cpu_cores,
                "ram_total_gb": system.ram_total_gb,
                "ram_available_gb": system.ram_available_gb,
                "disk_free_gb": system.disk_free_gb,
                "gpu_name": system.gpu_name,
                "package_managers": system.package_managers,
                "languages": system.languages
            }, indent=2))
            return
        
        console.print("\n💻 System Information\n", style="cyan bold")
        console.print(f"OS: {system.os_name} {system.os_version}")
        console.print(f"Architecture: {system.arch}")
        console.print(f"CPU: {system.cpu_name} ({system.cpu_cores} cores)")
        console.print(f"RAM: {system.ram_total_gb} GB")
        console.print(f"Disk: {system.disk_free_gb} GB free")
        if system.gpu_name:
            console.print(f"GPU: {system.gpu_name}")
        console.print(f"Package Managers: {', '.join(system.package_managers)}")
        console.print(f"Languages: {', '.join(f'{k} {v}' for k, v in system.languages.items())}\n")


@cli.command()
@click.argument('query', required=False)
def search(query):
    """Search for profiles by name, description, or keywords."""
    
    if not query:
        console.print("❌ Please provide a search query", style="red")
        console.print("Usage: he2plus search <query>")
        return
    
    registry = ProfileRegistry()
    results = registry.search(query)
    
    if not results:
        console.print(f"No profiles found matching '{query}'", style="yellow")
        return
    
    console.print(f"\n🔍 Search Results for '{query}':\n", style="cyan bold")
    
    for profile in results:
        console.print(f"[bold]{profile.name}[/bold] ([cyan]{profile.id}[/cyan])")
        console.print(f"  {profile.description}")
        console.print(f"  Category: {profile.category}")
        console.print(f"  Requirements: {profile.get_requirements().ram_gb}GB RAM, {profile.get_requirements().disk_gb}GB disk")
        console.print()


@cli.command()
@click.argument('profiles', nargs=-1, required=True)
def remove(profiles):
    """Remove installed profiles."""
    
    console.print("❌ Profile removal not yet implemented", style="red")
    console.print("This feature will be available in a future version.")


@cli.command()
@click.argument('profiles', nargs=-1, required=True)
def update(profiles):
    """Update installed profiles."""
    
    console.print("❌ Profile updates not yet implemented", style="red")
    console.print("This feature will be available in a future version.")


def verify_profile(profile, installer: InstallationEngine) -> bool:
    """Verify that a profile is properly installed."""
    verification_steps = profile.get_verification_steps()
    
    for step in verification_steps:
        result = installer.verify_component(None, step)  # We don't need the component for verification
        if not result.success:
            console.print(f"   ❌ {step.name}: {result.error}", style="red")
            return False
        else:
            console.print(f"   ✓ {step.name}", style="green")
    
    return True


def check_tool_installed(tool: str) -> Optional[dict]:
    """Check if a tool is installed and get its version."""
    try:
        result = subprocess.run(
            [tool, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            return {"version": version}
    except:
        pass
    
    return None


if __name__ == '__main__':
    cli()