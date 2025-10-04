"""
Vue.js development profile for he2plus.

This profile sets up a complete Vue.js development environment with modern tooling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..base import BaseProfile, Component, VerificationStep, SampleProject


class VueProfile(BaseProfile):
    """Vue.js development environment for modern web applications."""

    def _initialize_profile(self) -> None:
        self.id = "web-vue"
        self.name = "Vue.js Development"
        self.description = "Progressive JavaScript framework for building user interfaces"
        self.category = "web"
        self.version = "1.0.0"

        # Requirements
        self.requirements.ram_gb = 4.0
        self.requirements.disk_gb = 5.0
        self.requirements.cpu_cores = 2
        self.requirements.gpu_required = False
        self.requirements.internet_required = True
        self.requirements.download_size_mb = 200.0
        self.requirements.supported_archs = ["x86_64", "arm64", "arm"]

        # Components
        self.components = [
            # Core runtime
            Component(
                id="language.node.18",
                name="Node.js 18 LTS",
                description="JavaScript runtime for Vue.js development",
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
                description="Code editor with excellent Vue.js support",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["package_manager", "official"]
            ),
            
            # Vue.js core
            Component(
                id="framework.vue",
                name="Vue.js",
                description="Progressive JavaScript framework",
                category="framework",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.vue-router",
                name="Vue Router",
                description="Official router for Vue.js",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.vuex",
                name="Vuex",
                description="State management pattern and library for Vue.js applications",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.pinia",
                name="Pinia",
                description="The Vue Store that you will enjoy using",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Build tools
            Component(
                id="tool.vite",
                name="Vite",
                description="Next generation frontend tooling",
                category="tool",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.vue-cli",
                name="Vue CLI",
                description="Standard tooling for Vue.js development",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Styling
            Component(
                id="library.vuetify",
                name="Vuetify",
                description="Material Design component framework for Vue.js",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.quasar",
                name="Quasar",
                description="Build high-performance Vue.js user interfaces",
                category="library",
                download_size_mb=8.0,
                install_time_minutes=3,
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
            
            # HTTP client
            Component(
                id="library.axios",
                name="Axios",
                description="Promise-based HTTP client",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Testing
            Component(
                id="tool.vitest",
                name="Vitest",
                description="Blazing fast unit test framework powered by Vite",
                category="tool",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.vue-test-utils",
                name="Vue Test Utils",
                description="Official testing utilities for Vue.js",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.cypress",
                name="Cypress",
                description="End-to-end testing framework",
                category="library",
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
            
            # TypeScript support
            Component(
                id="language.typescript",
                name="TypeScript",
                description="Typed superset of JavaScript",
                category="language",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Development tools
            Component(
                id="tool.vue-devtools",
                name="Vue DevTools",
                description="Browser extension for debugging Vue.js applications",
                category="tool",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["browser_extension"]
            ),
            
            # Deployment
            Component(
                id="tool.netlify-cli",
                name="Netlify CLI",
                description="Command line interface for Netlify",
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
                name="Vue CLI",
                command="vue --version",
                contains_text="@vue/cli"
            ),
            VerificationStep(
                name="Vite",
                command="npx vite --version",
                contains_text="v"
            ),
            VerificationStep(
                name="Vue.js",
                command="npm list vue",
                contains_text="vue"
            ),
            VerificationStep(
                name="Vue Router",
                command="npm list vue-router",
                contains_text="vue-router"
            ),
            VerificationStep(
                name="TypeScript",
                command="npx tsc --version",
                contains_text="Version"
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
            name="Vue.js Starter Kit",
            description="A modern Vue.js application with TypeScript, Vite, and best practices",
            type="create_app",
            source="npm create vue@latest my-vue-app",
            directory="~/my-vue-app",
            setup_commands=[
                "cd ~/my-vue-app",
                "npm install",
                "npm run dev"
            ],
            next_steps=[
                "Open http://localhost:5173 in your browser",
                "Start building your Vue.js application",
                "Check the README for detailed setup instructions"
            ]
        )

        # Next steps
        self.next_steps = [
            "🎉 Vue.js development environment ready!",
            "",
            "📚 Quick Start:",
            "  • Create new project: npm create vue@latest my-vue-app",
            "  • Or use Vue CLI: vue create my-vue-app",
            "  • Start development: npm run dev",
            "  • Build for production: npm run build",
            "",
            "🛠️  Development Tools:",
            "  • VS Code with Vue.js extensions",
            "  • Vue DevTools browser extension",
            "  • Vite for fast development and building",
            "  • ESLint and Prettier for code quality",
            "  • Vitest for unit testing",
            "",
            "📦 Key Technologies:",
            "  • Vue.js 3 for reactive UI components",
            "  • Vue Router for client-side routing",
            "  • Pinia for state management",
            "  • Vite for build tooling",
            "  • TypeScript for type safety",
            "  • Tailwind CSS for styling",
            "",
            "🚀 Deployment Options:",
            "  • Netlify for static site deployment",
            "  • Vercel for serverless deployment",
            "  • GitHub Pages for free hosting",
            "  • AWS S3 + CloudFront for scalable hosting",
            "  • Docker for containerized deployment",
            "",
            "📖 Resources:",
            "  • Vue.js Documentation: https://vuejs.org",
            "  • Vue Router Documentation: https://router.vuejs.org",
            "  • Pinia Documentation: https://pinia.vuejs.org",
            "  • Vite Documentation: https://vitejs.dev",
            "  • Vue.js Style Guide: https://vuejs.org/style-guide",
            "",
            "💡 Pro Tips:",
            "  • Use Composition API for better code organization",
            "  • Implement proper error handling",
            "  • Use TypeScript for better development experience",
            "  • Set up proper testing with Vitest",
            "  • Use Vue DevTools for debugging",
            "  • Follow Vue.js style guide for consistency",
            "",
            "🔗 Community:",
            "  • Vue.js Community: https://vuejs.org/community",
            "  • Vue.js Discord: https://discord.gg/vue",
            "  • Vue.js Forum: https://forum.vuejs.org",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/vue.js",
            "",
            "📞 Support:",
            "  • GitHub Issues: https://github.com/vuejs/core/issues",
            "  • Vue.js Discord: https://discord.gg/vue",
            "  • Vue.js Forum: https://forum.vuejs.org"
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
            "vue_specific": {
                "core": ["Vue.js", "Vue Router", "Pinia", "Vuex"],
                "build_tools": ["Vite", "Vue CLI", "Webpack"],
                "styling": ["Vuetify", "Quasar", "Tailwind CSS", "Bootstrap Vue"],
                "testing": ["Vitest", "Vue Test Utils", "Cypress", "Jest"],
                "deployment": ["Netlify", "Vercel", "GitHub Pages", "AWS S3"],
                "development_tools": ["Vue DevTools", "ESLint", "Prettier", "TypeScript"],
                "popular_libraries": [
                    "Vue.js", "Vue Router", "Pinia", "Vite", "TypeScript",
                    "Tailwind CSS", "Vuetify", "Axios", "Vitest", "ESLint"
                ]
            }
        }

    def get_development_workflow(self) -> List[str]:
        """Get typical development workflow for Vue.js projects."""
        return [
            "1. Create Vue.js project: npm create vue@latest my-vue-app",
            "2. Choose TypeScript, Router, Pinia, and testing options",
            "3. Install dependencies: npm install",
            "4. Set up project structure and components",
            "5. Configure Vue Router for navigation",
            "6. Set up Pinia stores for state management",
            "7. Create reusable components and composables",
            "8. Implement API integration with Axios",
            "9. Add styling with Tailwind CSS or Vuetify",
            "10. Write unit tests with Vitest",
            "11. Set up ESLint and Prettier for code quality",
            "12. Configure build and deployment settings",
            "13. Test the application thoroughly",
            "14. Deploy to Netlify, Vercel, or other platforms"
        ]

    def get_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Get troubleshooting guide for common Vue.js issues."""
        return {
            "Installation Issues": [
                "Node.js version compatibility - ensure Node.js 18+ is installed",
                "npm cache issues - clear cache with 'npm cache clean --force'",
                "Permission errors - use 'sudo' on Linux/macOS or run as administrator on Windows",
                "Network issues - check firewall and proxy settings",
                "Disk space - ensure at least 5GB free space available",
                "Vue CLI not found - install globally with 'npm install -g @vue/cli'"
            ],
            "Development Issues": [
                "Hot reload not working - check Vite configuration and file watchers",
                "Component not rendering - check template syntax and component registration",
                "Router navigation issues - verify route definitions and component imports",
                "State management issues - check Pinia store setup and component usage",
                "TypeScript errors - verify type definitions and tsconfig.json",
                "Build errors - check for syntax errors and missing dependencies"
            ],
            "Build Issues": [
                "Build failures - check for TypeScript errors and missing imports",
                "Bundle size too large - use code splitting and lazy loading",
                "Static assets not loading - check public folder and asset paths",
                "Environment variables not working - check .env file location and syntax",
                "CSS not applying - check Tailwind CSS configuration and imports",
                "Memory leaks - check for proper cleanup in onUnmounted hooks"
            ],
            "Deployment Issues": [
                "Netlify deployment failures - check build command and output directory",
                "Vercel deployment issues - check vercel.json configuration",
                "GitHub Pages not working - check base path and build settings",
                "API endpoints not working - check CORS and proxy configuration",
                "Environment variables in production - set them in deployment platform",
                "Static file serving - configure proper static file paths"
            ]
        }

    def get_recommended_extensions(self) -> List[str]:
        """Get recommended VS Code extensions for Vue.js development."""
        return [
            "Vue.volar",
            "Vue.vscode-typescript-vue-plugin",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode",
            "ms-vscode.vscode-eslint",
            "ms-vscode.vscode-typescript-next",
            "ms-vscode.vscode-javascript",
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
        """Get useful commands for Vue.js development."""
        return {
            "Project Setup": [
                "npm create vue@latest my-vue-app - Create Vue.js project",
                "vue create my-vue-app - Create project with Vue CLI",
                "npm install - Install dependencies",
                "npm run dev - Start development server",
                "npm run build - Build for production"
            ],
            "Development": [
                "npm run dev - Start development server",
                "npm run build - Build for production",
                "npm run preview - Preview production build",
                "npm run test - Run tests",
                "npm run test:ui - Run tests with UI"
            ],
            "Code Quality": [
                "npm run lint - Run ESLint",
                "npm run format - Format code with Prettier",
                "npm run type-check - Check TypeScript types",
                "npm run test:coverage - Run tests with coverage",
                "npm run test:watch - Run tests in watch mode"
            ],
            "Vue CLI": [
                "vue create my-app - Create new project",
                "vue add router - Add Vue Router",
                "vue add vuex - Add Vuex state management",
                "vue add typescript - Add TypeScript support",
                "vue add eslint - Add ESLint configuration"
            ],
            "Deployment": [
                "npm run build - Build for production",
                "netlify deploy - Deploy to Netlify",
                "vercel deploy - Deploy to Vercel",
                "npm run build && npm run preview - Test production build locally",
                "docker build -t my-vue-app . - Build Docker image"
            ]
        }
