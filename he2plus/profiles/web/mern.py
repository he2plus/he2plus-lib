"""
MERN stack development profile for he2plus.

This profile sets up a complete MERN (MongoDB, Express, React, Node.js) 
development environment with modern tooling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..base import BaseProfile, Component, VerificationStep, SampleProject


class MERNProfile(BaseProfile):
    """MERN stack development environment for full-stack web applications."""

    def _initialize_profile(self) -> None:
        self.id = "web-mern"
        self.name = "MERN Stack Development"
        self.description = "Full-stack web development with MongoDB, Express, React, and Node.js"
        self.category = "web"
        self.version = "1.0.0"

        # Requirements
        self.requirements.ram_gb = 6.0
        self.requirements.disk_gb = 8.0
        self.requirements.cpu_cores = 2
        self.requirements.gpu_required = False
        self.requirements.internet_required = True
        self.requirements.download_size_mb = 400.0
        self.requirements.supported_archs = ["x86_64", "arm64", "arm"]

        # Components
        self.components = [
            # Core runtime
            Component(
                id="language.node.18",
                name="Node.js 18 LTS",
                description="JavaScript runtime for MERN development",
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
                description="Code editor with excellent JavaScript and React support",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["package_manager", "official"]
            ),
            
            # Backend - Express.js
            Component(
                id="framework.express",
                name="Express.js",
                description="Fast, unopinionated, minimalist web framework for Node.js",
                category="framework",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.cors",
                name="CORS",
                description="Cross-Origin Resource Sharing middleware",
                category="library",
                download_size_mb=0.5,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.helmet",
                name="Helmet",
                description="Security middleware for Express",
                category="library",
                download_size_mb=0.5,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.morgan",
                name="Morgan",
                description="HTTP request logger middleware",
                category="library",
                download_size_mb=0.5,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.dotenv",
                name="dotenv",
                description="Environment variable loader",
                category="library",
                download_size_mb=0.5,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Database - MongoDB
            Component(
                id="database.mongodb",
                name="MongoDB",
                description="NoSQL document database",
                category="database",
                download_size_mb=200.0,
                install_time_minutes=15,
                install_methods=["package_manager", "official"]
            ),
            
            Component(
                id="library.mongoose",
                name="Mongoose",
                description="MongoDB object modeling for Node.js",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.mongodb-compass",
                name="MongoDB Compass",
                description="GUI for MongoDB",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["official"]
            ),
            
            # Frontend - React
            Component(
                id="library.react",
                name="React",
                description="A JavaScript library for building user interfaces",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=2,
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
            
            Component(
                id="library.react-router-dom",
                name="React Router DOM",
                description="Declarative routing for React web applications",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.axios",
                name="Axios",
                description="Promise-based HTTP client",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # State management
            Component(
                id="library.redux",
                name="Redux",
                description="Predictable state container for JavaScript apps",
                category="library",
                download_size_mb=2.0,
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
            
            Component(
                id="library.react-redux",
                name="React Redux",
                description="Official React bindings for Redux",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Styling
            Component(
                id="library.styled-components",
                name="Styled Components",
                description="CSS-in-JS library for styled React components",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.material-ui",
                name="Material-UI",
                description="React components implementing Google's Material Design",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Authentication
            Component(
                id="library.jsonwebtoken",
                name="JSON Web Token",
                description="JSON Web Token implementation",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.bcryptjs",
                name="bcryptjs",
                description="Optimized bcrypt for JavaScript",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Development tools
            Component(
                id="tool.nodemon",
                name="Nodemon",
                description="Tool that helps develop Node.js applications",
                category="tool",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.concurrently",
                name="Concurrently",
                description="Run multiple commands concurrently",
                category="tool",
                download_size_mb=1.0,
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
                id="library.supertest",
                name="Supertest",
                description="HTTP assertion library",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.react-testing-library",
                name="React Testing Library",
                description="Simple and complete testing utilities for React",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
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
            
            # Deployment
            Component(
                id="tool.pm2",
                name="PM2",
                description="Process manager for Node.js applications",
                category="tool",
                download_size_mb=3.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.nginx",
                name="Nginx",
                description="Web server and reverse proxy",
                category="tool",
                download_size_mb=2.0,
                install_time_minutes=3,
                install_methods=["package_manager"]
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
                name="MongoDB Version",
                command="mongod --version",
                contains_text="db version"
            ),
            VerificationStep(
                name="Express.js",
                command="npm list express",
                contains_text="express"
            ),
            VerificationStep(
                name="React",
                command="npm list react",
                contains_text="react"
            ),
            VerificationStep(
                name="Mongoose",
                command="npm list mongoose",
                contains_text="mongoose"
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
            name="MERN Starter Kit",
            description="A complete MERN stack application with authentication, CRUD operations, and modern tooling",
            type="git_clone",
            source="git clone https://github.com/he2plus/mern-starter-kit.git",
            directory="~/mern-starter-kit",
            setup_commands=[
                "cd ~/mern-starter-kit",
                "npm install",
                "npm run dev"
            ],
            next_steps=[
                "Open http://localhost:3000 in your browser",
                "Open http://localhost:5000 for API documentation",
                "Start building your MERN application",
                "Check the README for detailed setup instructions"
            ]
        )

        # Next steps
        self.next_steps = [
            "🎉 MERN stack development environment ready!",
            "",
            "📚 Quick Start:",
            "  • Create new project: npx create-react-app my-mern-app",
            "  • Set up Express server: mkdir server && cd server && npm init -y",
            "  • Install dependencies: npm install express mongoose cors helmet morgan dotenv",
            "  • Start development: npm run dev (runs both frontend and backend)",
            "",
            "🛠️  Development Tools:",
            "  • VS Code with JavaScript and React extensions",
            "  • MongoDB Compass for database management",
            "  • Postman for API testing",
            "  • Redux DevTools for state management",
            "  • React Developer Tools for debugging",
            "",
            "📦 Key Technologies:",
            "  • MongoDB for NoSQL database",
            "  • Express.js for backend API",
            "  • React for frontend UI",
            "  • Node.js for JavaScript runtime",
            "  • Redux for state management",
            "  • JWT for authentication",
            "",
            "🚀 Deployment Options:",
            "  • Heroku for full-stack deployment",
            "  • Netlify for frontend deployment",
            "  • MongoDB Atlas for cloud database",
            "  • AWS/GCP for production deployment",
            "  • Docker for containerization",
            "",
            "📖 Resources:",
            "  • Express.js Documentation: https://expressjs.com",
            "  • React Documentation: https://react.dev",
            "  • MongoDB Documentation: https://docs.mongodb.com",
            "  • Redux Documentation: https://redux.js.org",
            "  • Mongoose Documentation: https://mongoosejs.com",
            "",
            "💡 Pro Tips:",
            "  • Use environment variables for configuration",
            "  • Implement proper error handling",
            "  • Use middleware for common functionality",
            "  • Set up proper CORS configuration",
            "  • Use JWT for secure authentication",
            "  • Implement input validation and sanitization",
            "",
            "🔗 Community:",
            "  • Express.js Community: https://expressjs.com/en/resources/community.html",
            "  • React Community: https://react.dev/community",
            "  • MongoDB Community: https://community.mongodb.com",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/mern",
            "",
            "📞 Support:",
            "  • GitHub Issues: https://github.com/expressjs/express/issues",
            "  • React Issues: https://github.com/facebook/react/issues",
            "  • MongoDB Support: https://support.mongodb.com"
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
            "mern_specific": {
                "backend": ["Node.js", "Express.js", "MongoDB", "Mongoose"],
                "frontend": ["React", "Redux", "React Router", "Axios"],
                "database": ["MongoDB", "MongoDB Compass", "MongoDB Atlas"],
                "authentication": ["JWT", "bcryptjs", "Passport.js"],
                "styling": ["Styled Components", "Material-UI", "CSS Modules"],
                "testing": ["Jest", "Supertest", "React Testing Library"],
                "deployment": ["Heroku", "Netlify", "AWS", "Docker"],
                "development_tools": ["Nodemon", "Concurrently", "ESLint", "Prettier"],
                "popular_libraries": [
                    "Express.js", "React", "MongoDB", "Mongoose", "Redux",
                    "React Router", "Axios", "JWT", "bcryptjs", "Helmet"
                ]
            }
        }

    def get_development_workflow(self) -> List[str]:
        """Get typical development workflow for MERN projects."""
        return [
            "1. Create React app: npx create-react-app my-mern-app",
            "2. Set up Express server: mkdir server && cd server && npm init -y",
            "3. Install backend dependencies: npm install express mongoose cors helmet morgan dotenv",
            "4. Install frontend dependencies: cd .. && npm install axios react-router-dom redux react-redux",
            "5. Set up MongoDB connection in server/index.js",
            "6. Create Express routes and middleware",
            "7. Set up Redux store and actions",
            "8. Create React components and pages",
            "9. Implement authentication with JWT",
            "10. Add form validation and error handling",
            "11. Set up testing with Jest and React Testing Library",
            "12. Configure ESLint and Prettier",
            "13. Set up environment variables",
            "14. Test the full-stack application",
            "15. Deploy to Heroku or other platforms"
        ]

    def get_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Get troubleshooting guide for common MERN issues."""
        return {
            "Installation Issues": [
                "Node.js version compatibility - ensure Node.js 18+ is installed",
                "MongoDB connection issues - check if MongoDB service is running",
                "Port conflicts - ensure ports 3000 and 5000 are available",
                "Permission errors - use 'sudo' on Linux/macOS or run as administrator on Windows",
                "Network issues - check firewall and proxy settings",
                "Disk space - ensure at least 8GB free space available"
            ],
            "Development Issues": [
                "CORS errors - configure CORS middleware properly",
                "MongoDB connection errors - check connection string and database name",
                "React build errors - check for syntax errors and missing dependencies",
                "Redux state issues - check action creators and reducers",
                "API route not working - check Express middleware and route definitions",
                "Authentication failures - verify JWT secret and token expiration"
            ],
            "Build Issues": [
                "Build failures - check for TypeScript errors and missing imports",
                "Bundle size too large - use code splitting and lazy loading",
                "Environment variables not loading - check .env file location and syntax",
                "Static files not serving - configure Express static middleware",
                "Database connection in production - use connection pooling",
                "Memory leaks - check for proper cleanup in useEffect hooks"
            ],
            "Deployment Issues": [
                "Heroku deployment failures - check buildpacks and environment variables",
                "MongoDB Atlas connection - whitelist IP addresses and check credentials",
                "Static file serving - configure proper static file paths",
                "API endpoints not working - check CORS and proxy configuration",
                "Environment variables in production - set them in deployment platform",
                "Database migrations - run migrations before deployment"
            ]
        }

    def get_recommended_extensions(self) -> List[str]:
        """Get recommended VS Code extensions for MERN development."""
        return [
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
            "ms-vscode.vscode-mongodb",
            "ms-vscode.vscode-node-debug2",
            "ms-vscode.vscode-npm-scripts"
        ]

    def get_useful_commands(self) -> Dict[str, List[str]]:
        """Get useful commands for MERN development."""
        return {
            "Project Setup": [
                "npx create-react-app my-mern-app - Create React app",
                "mkdir server && cd server - Create server directory",
                "npm init -y - Initialize Node.js project",
                "npm install express mongoose cors helmet morgan dotenv - Install backend dependencies",
                "npm install axios react-router-dom redux react-redux - Install frontend dependencies"
            ],
            "Backend Commands": [
                "npm start - Start Express server",
                "npm run dev - Start server with nodemon",
                "npm test - Run backend tests",
                "npm run build - Build for production",
                "node server.js - Run production server"
            ],
            "Frontend Commands": [
                "npm start - Start React development server",
                "npm run build - Build React app for production",
                "npm test - Run React tests",
                "npm run eject - Eject from Create React App",
                "npm run deploy - Deploy to GitHub Pages"
            ],
            "Database Commands": [
                "mongod - Start MongoDB daemon",
                "mongo - Connect to MongoDB shell",
                "mongodump - Backup MongoDB database",
                "mongorestore - Restore MongoDB database",
                "mongoexport - Export MongoDB collection"
            ],
            "Development Tools": [
                "npm run dev - Start both frontend and backend",
                "npm run lint - Run ESLint",
                "npm run format - Format code with Prettier",
                "npm run test:watch - Run tests in watch mode",
                "npm run test:coverage - Run tests with coverage"
            ],
            "Deployment Commands": [
                "heroku create my-mern-app - Create Heroku app",
                "git push heroku main - Deploy to Heroku",
                "heroku logs --tail - View Heroku logs",
                "heroku config:set NODE_ENV=production - Set environment variables",
                "heroku addons:create mongolab:sandbox - Add MongoDB to Heroku"
            ]
        }
