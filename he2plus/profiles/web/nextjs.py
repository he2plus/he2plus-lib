"""
Next.js development profile for he2plus.

This profile sets up a complete Next.js development environment
with TypeScript, Tailwind CSS, and modern tooling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..base import BaseProfile, Component, VerificationStep, SampleProject


class NextJSProfile(BaseProfile):
    """Next.js development environment for modern web applications."""

    def _initialize_profile(self) -> None:
        self.id = "web-nextjs"
        self.name = "Next.js Development"
        self.description = "Modern React framework with TypeScript, Tailwind CSS, and full-stack capabilities"
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
                description="JavaScript runtime for Next.js development",
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
            
            Component(
                id="tool.pnpm",
                name="pnpm",
                description="Fast, disk space efficient package manager",
                category="tool",
                download_size_mb=3.0,
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
                description="Code editor with excellent TypeScript and React support",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["package_manager", "official"]
            ),
            
            # Next.js and React ecosystem
            Component(
                id="framework.nextjs",
                name="Next.js",
                description="The React Framework for Production",
                category="framework",
                download_size_mb=20.0,
                install_time_minutes=3,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.react",
                name="React",
                description="A JavaScript library for building user interfaces",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.react-dom",
                name="React DOM",
                description="React package for working with the DOM",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # TypeScript support
            Component(
                id="language.typescript",
                name="TypeScript",
                description="Typed JavaScript at scale",
                category="language",
                download_size_mb=15.0,
                install_time_minutes=2,
                install_methods=["npm", "package_manager"]
            ),
            
            # Styling
            Component(
                id="library.tailwindcss",
                name="Tailwind CSS",
                description="Utility-first CSS framework",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.styled-components",
                name="Styled Components",
                description="CSS-in-JS library for styled React components",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # State management
            Component(
                id="library.zustand",
                name="Zustand",
                description="Small, fast and scalable state management solution",
                category="library",
                download_size_mb=0.5,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.redux-toolkit",
                name="Redux Toolkit",
                description="The official, opinionated, batteries-included toolset for efficient Redux development",
                category="library",
                download_size_mb=3.0,
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
                id="tool.cypress",
                name="Cypress",
                description="End-to-end testing framework",
                category="tool",
                download_size_mb=50.0,
                install_time_minutes=3,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.playwright",
                name="Playwright",
                description="End-to-end testing for modern web apps",
                category="tool",
                download_size_mb=30.0,
                install_time_minutes=3,
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
            
            # Database and ORM
            Component(
                id="library.prisma",
                name="Prisma",
                description="Next-generation ORM for Node.js and TypeScript",
                category="library",
                download_size_mb=8.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.drizzle",
                name="Drizzle ORM",
                description="TypeScript ORM for SQL databases",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Authentication
            Component(
                id="library.next-auth",
                name="NextAuth.js",
                description="Authentication for Next.js",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.clerk",
                name="Clerk",
                description="Complete user management for modern applications",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Deployment
            Component(
                id="tool.vercel-cli",
                name="Vercel CLI",
                description="Command-line interface for Vercel",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.netlify-cli",
                name="Netlify CLI",
                description="Command-line interface for Netlify",
                category="tool",
                download_size_mb=3.0,
                install_time_minutes=2,
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
                name="Next.js CLI",
                command="npx next --version",
                contains_text="Next.js"
            ),
            VerificationStep(
                name="TypeScript",
                command="npx tsc --version",
                contains_text="Version"
            ),
            VerificationStep(
                name="Tailwind CSS",
                command="npx tailwindcss --version",
                contains_text="tailwindcss"
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
            VerificationStep(
                name="Vercel CLI",
                command="npx vercel --version",
                contains_text="."
            ),
        ]

        # Sample project
        self.sample_project = SampleProject(
            name="Next.js Starter Kit",
            description="A complete Next.js project with TypeScript, Tailwind CSS, and modern tooling",
            type="create_app",
            source="npx create-next-app@latest my-nextjs-app --typescript --tailwind --eslint --app --src-dir --import-alias '@/*'",
            directory="~/my-nextjs-app",
            setup_commands=[
                "cd ~/my-nextjs-app",
                "npm install",
                "npm run dev"
            ],
            next_steps=[
                "Open http://localhost:3000 in your browser",
                "Start editing pages in the app directory",
                "Add components in the components directory",
                "Configure Tailwind CSS in tailwind.config.js"
            ]
        )

        # Next steps
        self.next_steps = [
            "🎉 Next.js development environment ready!",
            "",
            "📚 Quick Start:",
            "  • Create new project: npx create-next-app@latest my-app --typescript --tailwind",
            "  • Start development server: npm run dev",
            "  • Build for production: npm run build",
            "  • Deploy to Vercel: npx vercel",
            "",
            "🛠️  Development Tools:",
            "  • VS Code with TypeScript and React extensions",
            "  • ESLint for code linting",
            "  • Prettier for code formatting",
            "  • Jest for unit testing",
            "  • Cypress/Playwright for E2E testing",
            "",
            "📦 Key Libraries:",
            "  • React 18 with Server Components",
            "  • TypeScript for type safety",
            "  • Tailwind CSS for styling",
            "  • NextAuth.js for authentication",
            "  • Prisma for database management",
            "",
            "🚀 Deployment Options:",
            "  • Vercel (recommended for Next.js)",
            "  • Netlify",
            "  • AWS Amplify",
            "  • Railway",
            "  • DigitalOcean App Platform",
            "",
            "📖 Resources:",
            "  • Next.js Documentation: https://nextjs.org/docs",
            "  • React Documentation: https://react.dev",
            "  • TypeScript Handbook: https://www.typescriptlang.org/docs",
            "  • Tailwind CSS Docs: https://tailwindcss.com/docs",
            "  • Vercel Deployment Guide: https://vercel.com/docs",
            "",
            "💡 Pro Tips:",
            "  • Use Server Components for better performance",
            "  • Leverage App Router for modern routing",
            "  • Implement proper error boundaries",
            "  • Use TypeScript strict mode",
            "  • Set up proper SEO with metadata API",
            "",
            "🔗 Community:",
            "  • Next.js Discord: https://discord.gg/nextjs",
            "  • React Community: https://react.dev/community",
            "  • TypeScript Community: https://discord.gg/typescript",
            "",
            "📞 Support:",
            "  • GitHub Issues: https://github.com/vercel/next.js/issues",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/next.js",
            "  • Reddit: https://reddit.com/r/nextjs"
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
            "web_specific": {
                "frameworks": ["Next.js", "React"],
                "languages": ["JavaScript", "TypeScript"],
                "styling": ["Tailwind CSS", "Styled Components", "CSS Modules"],
                "state_management": ["Zustand", "Redux Toolkit", "React Context"],
                "testing": ["Jest", "Cypress", "Playwright", "React Testing Library"],
                "deployment": ["Vercel", "Netlify", "AWS Amplify", "Railway"],
                "databases": ["PostgreSQL", "MySQL", "SQLite", "MongoDB"],
                "authentication": ["NextAuth.js", "Clerk", "Auth0", "Firebase Auth"],
                "popular_libraries": [
                    "React Query", "SWR", "Framer Motion", "React Hook Form",
                    "Zod", "React Router", "React Helmet", "React Icons"
                ]
            }
        }

    def get_development_workflow(self) -> List[str]:
        """Get typical development workflow for Next.js projects."""
        return [
            "1. Create new Next.js project: npx create-next-app@latest my-app --typescript --tailwind",
            "2. Navigate to project: cd my-app",
            "3. Install dependencies: npm install",
            "4. Start development server: npm run dev",
            "5. Open browser: http://localhost:3000",
            "6. Edit pages in app/ directory",
            "7. Add components in components/ directory",
            "8. Style with Tailwind CSS classes",
            "9. Add TypeScript types for better development experience",
            "10. Write tests with Jest and React Testing Library",
            "11. Run tests: npm test",
            "12. Build for production: npm run build",
            "13. Deploy to Vercel: npx vercel",
            "14. Set up CI/CD with GitHub Actions",
            "15. Monitor with Vercel Analytics"
        ]

    def get_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Get troubleshooting guide for common Next.js issues."""
        return {
            "Installation Issues": [
                "Node.js version compatibility - ensure Node.js 18+ is installed",
                "npm cache issues - run 'npm cache clean --force'",
                "Permission errors - use 'sudo' on Linux/macOS or run as administrator on Windows",
                "Network issues - check internet connection and proxy settings",
                "Disk space - ensure at least 5GB free space available"
            ],
            "Development Issues": [
                "Hot reload not working - restart development server",
                "TypeScript errors - check tsconfig.json configuration",
                "Tailwind CSS not working - verify tailwind.config.js setup",
                "Import errors - check import paths and file extensions",
                "Build errors - run 'npm run build' to see detailed error messages"
            ],
            "Performance Issues": [
                "Slow development server - increase Node.js memory limit",
                "Large bundle size - use dynamic imports and code splitting",
                "Slow builds - enable SWC compiler in next.config.js",
                "Memory leaks - check for proper cleanup in useEffect hooks",
                "Slow page loads - optimize images and use Next.js Image component"
            ],
            "Deployment Issues": [
                "Build failures - check environment variables and dependencies",
                "Vercel deployment errors - check vercel.json configuration",
                "Environment variables - ensure all required env vars are set",
                "Static export issues - configure next.config.js for static export",
                "API routes not working - check serverless function limits"
            ]
        }

    def get_recommended_extensions(self) -> List[str]:
        """Get recommended VS Code extensions for Next.js development."""
        return [
            "ms-vscode.vscode-typescript-next",
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
            "ms-vscode.vscode-cypress",
            "ms-vscode.vscode-playwright",
            "ms-vscode.vscode-prisma",
            "ms-vscode.vscode-tailwindcss"
        ]

    def get_useful_commands(self) -> Dict[str, List[str]]:
        """Get useful commands for Next.js development."""
        return {
            "Next.js Commands": [
                "npx create-next-app@latest my-app --typescript --tailwind",
                "npm run dev - Start development server",
                "npm run build - Build for production",
                "npm run start - Start production server",
                "npm run lint - Run ESLint",
                "npm run test - Run tests",
                "npx next --version - Check Next.js version"
            ],
            "Package Management": [
                "npm install - Install dependencies",
                "npm install package-name - Install package",
                "npm install -D package-name - Install dev dependency",
                "npm uninstall package-name - Remove package",
                "npm update - Update all packages",
                "npm audit - Check for vulnerabilities",
                "npm audit fix - Fix vulnerabilities"
            ],
            "Git Commands": [
                "git init - Initialize repository",
                "git add . - Stage all changes",
                "git commit -m 'message' - Commit changes",
                "git push - Push to remote",
                "git pull - Pull from remote",
                "git status - Check status",
                "git log --oneline - View commit history"
            ],
            "Development Tools": [
                "npx tsc --noEmit - Check TypeScript without emitting",
                "npx eslint . --ext .ts,.tsx - Lint TypeScript files",
                "npx prettier --write . - Format all files",
                "npx jest --watch - Run tests in watch mode",
                "npx cypress open - Open Cypress test runner",
                "npx playwright test - Run Playwright tests"
            ],
            "Deployment Commands": [
                "npx vercel - Deploy to Vercel",
                "npx vercel --prod - Deploy to production",
                "npx netlify deploy - Deploy to Netlify",
                "npx netlify deploy --prod - Deploy to production",
                "npm run build && npm run start - Local production build"
            ]
        }
