"""
Angular development profile for he2plus.

This profile sets up a complete Angular development environment with modern tooling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..base import BaseProfile, Component, VerificationStep, SampleProject


class AngularProfile(BaseProfile):
    """Angular development environment for enterprise web applications."""

    def _initialize_profile(self) -> None:
        self.id = "web-angular"
        self.name = "Angular Development"
        self.description = "Platform for building mobile and desktop web applications"
        self.category = "web"
        self.version = "1.0.0"

        # Requirements
        self.requirements.ram_gb = 6.0
        self.requirements.disk_gb = 8.0
        self.requirements.cpu_cores = 2
        self.requirements.gpu_required = False
        self.requirements.internet_required = True
        self.requirements.download_size_mb = 500.0
        self.requirements.supported_archs = ["x86_64", "arm64", "arm"]

        # Components
        self.components = [
            # Core runtime
            Component(
                id="language.node.18",
                name="Node.js 18 LTS",
                description="JavaScript runtime for Angular development",
                category="language",
                version="18",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["package_manager", "nvm", "volta", "official"]
            ),
            
            # Package managers
            Component(
                id="tool.npm",
                name="npm",
                description="Node Package Manager (comes with Node.js)",
                category="tool",
                download_size_mb=0.0,
                install_time_minutes=0,
                install_methods=["package_manager"]
            ),
            
            Component(
                id="tool.yarn",
                name="Yarn",
                description="Fast, reliable, and secure dependency management",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm", "package_manager"]
            ),
            
            # Version control
            Component(
                id="tool.git",
                name="Git",
                description="Version control system",
                category="tool",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["package_manager", "official"]
            ),
            
            # Development tools
            Component(
                id="tool.vscode",
                name="Visual Studio Code",
                description="Code editor with excellent Angular support",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["package_manager", "official"]
            ),
            
            # Angular core
            Component(
                id="framework.angular",
                name="Angular",
                description="Platform for building mobile and desktop web applications",
                category="framework",
                download_size_mb=10.0,
                install_time_minutes=3,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.angular-cli",
                name="Angular CLI",
                description="Command line interface for Angular",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # TypeScript
            Component(
                id="language.typescript",
                name="TypeScript",
                description="Typed superset of JavaScript",
                category="language",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Angular modules
            Component(
                id="library.angular-router",
                name="Angular Router",
                description="Navigation library for Angular applications",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.angular-forms",
                name="Angular Forms",
                description="Form handling and validation",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.angular-http",
                name="Angular HTTP Client",
                description="HTTP client for Angular applications",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # State management
            Component(
                id="library.ngrx",
                name="NgRx",
                description="Reactive state management for Angular",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.akita",
                name="Akita",
                description="State management library for Angular",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # UI libraries
            Component(
                id="library.angular-material",
                name="Angular Material",
                description="Material Design components for Angular",
                category="library",
                download_size_mb=8.0,
                install_time_minutes=3,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.primeng",
                name="PrimeNG",
                description="UI component library for Angular",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.ng-bootstrap",
                name="ng-bootstrap",
                description="Bootstrap components for Angular",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Styling
            Component(
                id="library.bootstrap",
                name="Bootstrap",
                description="CSS framework for responsive web design",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.tailwindcss",
                name="Tailwind CSS",
                description="Utility-first CSS framework",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Testing
            Component(
                id="tool.jest",
                name="Jest",
                description="JavaScript testing framework",
                category="tool",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.jasmine",
                name="Jasmine",
                description="Behavior-driven development framework",
                category="tool",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.karma",
                name="Karma",
                description="Test runner for JavaScript",
                category="tool",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.protractor",
                name="Protractor",
                description="End-to-end testing framework for Angular",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.cypress",
                name="Cypress",
                description="End-to-end testing framework",
                category="tool",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["npm"]
            ),
            
            # Code quality
            Component(
                id="tool.eslint",
                name="ESLint",
                description="JavaScript and TypeScript linter",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.prettier",
                name="Prettier",
                description="Code formatter",
                category="tool",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.husky",
                name="Husky",
                description="Git hooks made easy",
                category="tool",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Development tools
            Component(
                id="tool.angular-devkit",
                name="Angular DevKit",
                description="Development tools for Angular",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.webpack",
                name="Webpack",
                description="Module bundler for JavaScript",
                category="tool",
                download_size_mb=8.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Deployment
            Component(
                id="tool.firebase-cli",
                name="Firebase CLI",
                description="Command line interface for Firebase",
                category="tool",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.vercel-cli",
                name="Vercel CLI",
                description="Command line interface for Vercel",
                category="tool",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
        ]

        # Verification steps
        self.verification_steps = [
            VerificationStep(
                name="Node.js Version",
                command="node --version",
                contains_text="v18"
            ),
            VerificationStep(
                name="npm Version",
                command="npm --version"
            ),
            VerificationStep(
                name="Git Version",
                command="git --version",
                contains_text="git version"
            ),
            VerificationStep(
                name="Angular CLI",
                command="ng version",
                contains_text="Angular CLI"
            ),
            VerificationStep(
                name="TypeScript",
                command="npx tsc --version",
                contains_text="Version"
            ),
            VerificationStep(
                name="Angular",
                command="npm list @angular/core",
                contains_text="@angular/core"
            ),
            VerificationStep(
                name="Angular Material",
                command="npm list @angular/material",
                contains_text="@angular/material"
            ),
            VerificationStep(
                name="Jest",
                command="npx jest --version",
                contains_text="."
            ),
            VerificationStep(
                name="ESLint",
                command="npx eslint --version",
                contains_text="v"
            ),
            VerificationStep(
                name="Prettier",
                command="npx prettier --version",
                contains_text="."
            ),
        ]

        # Sample project
        self.sample_project = SampleProject(
            name="Angular Starter Kit",
            description="A complete Angular application with TypeScript, Material Design, and best practices",
            type="create_app",
            source="ng new my-angular-app --routing --style=scss --package-manager=npm",
            directory="~/my-angular-app",
            setup_commands=[
                "cd ~/my-angular-app",
                "ng add @angular/material",
                "npm install",
                "ng serve"
            ],
            next_steps=[
                "Open http://localhost:4200 in your browser",
                "Start building your Angular application",
                "Check the README for detailed setup instructions"
            ]
        )

        # Next steps
        self.next_steps = [
            "🎉 Angular development environment ready!",
            "",
            "📚 Quick Start:",
            "  • Create new project: ng new my-angular-app --routing --style=scss",
            "  • Add Angular Material: ng add @angular/material",
            "  • Start development: ng serve",
            "  • Build for production: ng build --prod",
            "",
            "🛠️  Development Tools:",
            "  • VS Code with Angular extensions",
            "  • Angular CLI for project management",
            "  • Angular DevTools for debugging",
            "  • ESLint and Prettier for code quality",
            "  • Jest and Karma for testing",
            "",
            "📦 Key Technologies:",
            "  • Angular 17+ for enterprise web applications",
            "  • TypeScript for type safety",
            "  • Angular Material for UI components",
            "  • NgRx for state management",
            "  • Angular Router for navigation",
            "  • Angular HTTP Client for API calls",
            "",
            "🚀 Deployment Options:",
            "  • Firebase Hosting for static hosting",
            "  • Vercel for serverless deployment",
            "  • AWS S3 + CloudFront for scalable hosting",
            "  • Docker for containerized deployment",
            "  • Azure Static Web Apps for enterprise hosting",
            "",
            "📖 Resources:",
            "  • Angular Documentation: https://angular.io",
            "  • Angular Material Documentation: https://material.angular.io",
            "  • NgRx Documentation: https://ngrx.io",
            "  • TypeScript Documentation: https://www.typescriptlang.org",
            "  • Angular Style Guide: https://angular.io/guide/styleguide",
            "",
            "💡 Pro Tips:",
            "  • Use Angular CLI for all project operations",
            "  • Implement proper error handling",
            "  • Use TypeScript for better development experience",
            "  • Set up proper testing with Jest and Karma",
            "  • Use Angular DevTools for debugging",
            "  • Follow Angular style guide for consistency",
            "",
            "🔗 Community:",
            "  • Angular Community: https://angular.io/community",
            "  • Angular Discord: https://discord.gg/angular",
            "  • Angular Forum: https://forum.angular.io",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/angular",
            "",
            "📞 Support:",
            "  • GitHub Issues: https://github.com/angular/angular/issues",
            "  • Angular Discord: https://discord.gg/angular",
            "  • Angular Forum: https://forum.angular.io"
        ]

    def get_installation_plan(self) -> Dict[str, any]:
        """Get detailed installation plan for this profile."""
        return {
            "profile": {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "category": self.category,
                "version": self.version
            },
            "requirements": {
                "ram_gb": self.requirements.ram_gb,
                "disk_gb": self.requirements.disk_gb,
                "cpu_cores": self.requirements.cpu_cores,
                "gpu_required": self.requirements.gpu_required,
                "internet_required": self.requirements.internet_required,
                "download_size_mb": self.requirements.download_size_mb,
                "supported_archs": self.requirements.supported_archs
            },
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "description": comp.description,
                    "category": comp.category,
                    "version": comp.version,
                    "download_size_mb": comp.download_size_mb,
                    "install_time_minutes": comp.install_time_minutes,
                    "install_methods": comp.install_methods
                }
                for comp in self.components
            ],
            "verification": [
                {
                    "name": step.name,
                    "command": step.command,
                    "expected_output": step.expected_output,
                    "contains_text": step.contains_text,
                    "timeout_seconds": step.timeout_seconds
                }
                for step in self.verification_steps
            ],
            "sample_project": {
                "name": self.sample_project.name,
                "description": self.sample_project.description,
                "type": self.sample_project.type,
                "source": self.sample_project.source,
                "directory": self.sample_project.directory,
                "setup_commands": self.sample_project.setup_commands,
                "next_steps": self.sample_project.next_steps
            },
            "next_steps": self.next_steps,
            "estimated_total_time_minutes": sum(comp.install_time_minutes for comp in self.components),
            "estimated_download_size_mb": sum(comp.download_size_mb for comp in self.components),
            "angular_specific": {
                "core": ["Angular", "TypeScript", "Angular CLI", "Angular DevKit"],
                "ui_libraries": ["Angular Material", "PrimeNG", "ng-bootstrap"],
                "state_management": ["NgRx", "Akita", "Angular Services"],
                "testing": ["Jest", "Jasmine", "Karma", "Cypress", "Protractor"],
                "deployment": ["Firebase Hosting", "Vercel", "AWS S3", "Azure Static Web Apps"],
                "development_tools": ["Angular CLI", "Angular DevTools", "ESLint", "Prettier"],
                "popular_libraries": [
                    "Angular", "TypeScript", "Angular Material", "NgRx", "Angular Router",
                    "Angular HTTP Client", "Jest", "Cypress", "ESLint", "Prettier"
                ]
            }
        }

    def get_development_workflow(self) -> List[str]:
        """Get typical development workflow for Angular projects."""
        return [
            "1. Create Angular project: ng new my-angular-app --routing --style=scss",
            "2. Add Angular Material: ng add @angular/material",
            "3. Set up project structure and modules",
            "4. Configure Angular Router for navigation",
            "5. Set up NgRx stores for state management",
            "6. Create components and services",
            "7. Implement HTTP client for API calls",
            "8. Add form handling and validation",
            "9. Set up testing with Jest and Karma",
            "10. Configure ESLint and Prettier",
            "11. Set up build and deployment configuration",
            "12. Test the application thoroughly",
            "13. Deploy to Firebase, Vercel, or other platforms"
        ]

    def get_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Get troubleshooting guide for common Angular issues."""
        return {
            "Installation Issues": [
                "Node.js version compatibility - ensure Node.js 18+ is installed",
                "Angular CLI not found - install globally with 'npm install -g @angular/cli'",
                "npm cache issues - clear cache with 'npm cache clean --force'",
                "Permission errors - use 'sudo' on Linux/macOS or run as administrator on Windows",
                "Network issues - check firewall and proxy settings",
                "Disk space - ensure at least 8GB free space available"
            ],
            "Development Issues": [
                "Hot reload not working - check Angular CLI configuration and file watchers",
                "Component not rendering - check module declarations and component imports",
                "Router navigation issues - verify route definitions and component imports",
                "State management issues - check NgRx store setup and component usage",
                "TypeScript errors - verify type definitions and tsconfig.json",
                "Build errors - check for syntax errors and missing dependencies"
            ],
            "Build Issues": [
                "Build failures - check for TypeScript errors and missing imports",
                "Bundle size too large - use lazy loading and code splitting",
                "Static assets not loading - check assets folder and build configuration",
                "Environment variables not working - check environment files and build settings",
                "CSS not applying - check Angular Material theme and global styles",
                "Memory leaks - check for proper cleanup in ngOnDestroy"
            ],
            "Deployment Issues": [
                "Firebase deployment failures - check firebase.json and build settings",
                "Vercel deployment issues - check vercel.json configuration",
                "AWS S3 deployment problems - check bucket policies and CloudFront settings",
                "API endpoints not working - check CORS and proxy configuration",
                "Environment variables in production - set them in deployment platform",
                "Static file serving - configure proper static file paths"
            ]
        }

    def get_recommended_extensions(self) -> List[str]:
        """Get recommended VS Code extensions for Angular development."""
        return [
            "angular.ng-template",
            "ms-vscode.vscode-typescript-next",
            "ms-vscode.vscode-javascript",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode",
            "ms-vscode.vscode-eslint",
            "ms-vscode.vscode-json",
            "formulahendry.auto-rename-tag",
            "christian-kohler.path-intellisense",
            "ms-vscode.vscode-html-css-support",
            "ms-vscode.vscode-css-peek",
            "ms-vscode.vscode-emmet",
            "ms-vscode.vscode-git",
            "ms-vscode.vscode-git-graph",
            "ms-vscode.vscode-gitlens",
            "ms-vscode.vscode-thunder-client",
            "ms-vscode.vscode-restclient",
            "ms-vscode.vscode-jest",
            "ms-vscode.vscode-node-debug2",
            "ms-vscode.vscode-npm-scripts"
        ]

    def get_useful_commands(self) -> Dict[str, List[str]]:
        """Get useful commands for Angular development."""
        return {
            "Project Setup": [
                "ng new my-angular-app - Create new Angular project",
                "ng add @angular/material - Add Angular Material",
                "ng add @angular/pwa - Add Progressive Web App features",
                "ng add @ngrx/store - Add NgRx state management",
                "npm install - Install dependencies"
            ],
            "Development": [
                "ng serve - Start development server",
                "ng build - Build for production",
                "ng test - Run unit tests",
                "ng e2e - Run end-to-end tests",
                "ng lint - Run linting"
            ],
            "Code Generation": [
                "ng generate component my-component - Generate component",
                "ng generate service my-service - Generate service",
                "ng generate module my-module - Generate module",
                "ng generate guard my-guard - Generate guard",
                "ng generate interceptor my-interceptor - Generate interceptor"
            ],
            "Code Quality": [
                "ng lint - Run ESLint",
                "ng format - Format code with Prettier",
                "ng test --watch - Run tests in watch mode",
                "ng test --coverage - Run tests with coverage",
                "ng build --stats-json - Build with bundle analysis"
            ],
            "Deployment": [
                "ng build --prod - Build for production",
                "firebase deploy - Deploy to Firebase",
                "vercel deploy - Deploy to Vercel",
                "ng build --prod && ng serve --prod - Test production build locally",
                "docker build -t my-angular-app . - Build Docker image"
            ]
        }
