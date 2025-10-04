"""
Command-line interface for he2plus library
"""

import click
import sys
from .core import He2Plus
from .utils import Logger


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--config', '-c', help='Path to configuration file')
@click.pass_context
def cli(ctx, verbose, config):
    """he2plus - A powerful Python library for developer productivity and automation"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = config


@cli.command()
@click.option('--profile', '-p', default='default', help='Environment profile to use')
@click.pass_context
def setup(ctx, profile):
    """Set up development environment"""
    try:
        he2plus = He2Plus(ctx.obj['config'])
        success = he2plus.setup_dev_environment(profile)
        
        if success:
            click.echo("✅ Development environment setup completed successfully!")
        else:
            click.echo("❌ Development environment setup completed with some issues")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.argument('package')
@click.option('--method', '-m', default='auto', help='Installation method')
@click.pass_context
def install(ctx, package, method):
    """Install a package"""
    try:
        he2plus = He2Plus(ctx.obj['config'])
        success = he2plus.install_package(package, method)
        
        if success:
            click.echo(f"✅ Package '{package}' installed successfully!")
        else:
            click.echo(f"❌ Failed to install package '{package}'")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Show system status"""
    try:
        he2plus = He2Plus(ctx.obj['config'])
        status_info = he2plus.get_status()
        
        click.echo("🔍 System Status:")
        click.echo(f"  Version: {status_info['version']}")
        click.echo(f"  Platform: {status_info['system_info'].get('platform', 'Unknown')}")
        click.echo(f"  Architecture: {status_info['system_info'].get('architecture', 'Unknown')}")
        click.echo(f"  Python Version: {status_info['system_info'].get('python_version', 'Unknown')}")
        
        click.echo("\n📦 Dependencies:")
        for dep, available in status_info['dependencies'].items():
            status_icon = "✅" if available else "❌"
            click.echo(f"  {status_icon} {dep}")
        
        click.echo(f"\n⚙️  Configuration: {'✅ Loaded' if status_info['config_loaded'] else '❌ Not loaded'}")
        click.echo(f"📝 Logger: {'✅ Active' if status_info['logger_active'] else '❌ Inactive'}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def info(ctx):
    """Show system information"""
    try:
        he2plus = He2Plus(ctx.obj['config'])
        system_info = he2plus.get_system_info()
        
        click.echo("💻 System Information:")
        for key, value in system_info.items():
            if key != 'error':
                click.echo(f"  {key}: {value}")
        
        if 'error' in system_info:
            click.echo(f"❌ Error: {system_info['error']}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def check(ctx):
    """Check dependencies"""
    try:
        he2plus = He2Plus(ctx.obj['config'])
        dependencies = he2plus.check_dependencies()
        
        click.echo("🔍 Dependency Check:")
        for dep, available in dependencies.items():
            status_icon = "✅" if available else "❌"
            click.echo(f"  {status_icon} {dep}")
        
        missing = [dep for dep, available in dependencies.items() if not available]
        if missing:
            click.echo(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        else:
            click.echo("\n✅ All dependencies are available!")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def welcome(ctx):
    """Run interactive welcome and onboarding"""
    try:
        he2plus = He2Plus(ctx.obj['config'])
        result = he2plus.run_onboarding()
        
        if result.get('confirmed', False):
            click.echo("🎉 Onboarding completed! You're ready to start coding!")
        else:
            click.echo("👋 Onboarding cancelled. Run 'he2plus welcome' anytime to start again!")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def commands(ctx):
    """Show shell commands reference guide"""
    try:
        he2plus = He2Plus(ctx.obj['config'])
        he2plus.show_shell_commands()
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point for CLI"""
    cli()


if __name__ == '__main__':
    main()
