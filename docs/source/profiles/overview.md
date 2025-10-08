# Profile Overview

he2plus provides comprehensive development environment profiles for various technology stacks. Each profile includes all necessary tools, libraries, and frameworks to start developing immediately.

**Total Profiles**: 10  
**Total Components**: 580+ across all profiles

## Available Profiles

### Web3 Development (1 profile)
- **[web3-solidity](web3-solidity.md)** - Complete Ethereum smart contract development
  - Status: ✅ Production Ready
  - 26 components including Hardhat, Foundry, Solidity, OpenZeppelin, ethers.js, viem, The Graph
  - Full smart contract development, testing, and deployment environment
  - Comprehensive security tools and best practices
  
### Web Development (4 profiles)
- **[web-nextjs](web-nextjs.md)** - Modern React framework with TypeScript
  - Status: ✅ Production Ready
  - 46 components including Next.js 14+, React 18+, TypeScript, Tailwind CSS, Prisma, NextAuth
  - Full-stack development with App Router, Server Components, and API routes
  - Comprehensive UI libraries, state management, testing, and deployment tools

- **web-angular** - Platform for building mobile and desktop web applications
  - Status: ✅ Production Ready
  - 97 components including Angular, TypeScript, RxJS, Angular Material, NgRx
  - Complete Angular development environment
  - Testing, deployment, and enterprise-ready tools

- **web-mern** - Full-stack web development with MongoDB, Express, React, Node.js
  - Status: ✅ Production Ready
  - 103 components (largest profile!)
  - Complete MERN stack with authentication, GraphQL, WebSocket, payment integration
  - Testing, monitoring, and deployment tools

- **web-vue** - Progressive JavaScript framework for building user interfaces
  - Status: ✅ Production Ready
  - 84 components including Vue 3, TypeScript, Vite, Pinia, Vue Router
  - Complete Vue.js ecosystem with Nuxt.js, Vuetify, testing, and deployment

### Mobile Development (1 profile)
- **[mobile-react-native](mobile-react-native.md)** - Cross-platform mobile apps
  - Status: ✅ Production Ready
  - 60 components including React Native 0.72+, TypeScript, React Navigation, Reanimated
  - Complete iOS and Android development environment
  - UI libraries, state management, Firebase integration, and deployment automation

### Machine Learning (1 profile)
- **[ml-python](ml-python.md)** - Complete ML/AI environment
  - Status: ✅ Production Ready
  - 74 components including TensorFlow, PyTorch, scikit-learn, Hugging Face Transformers
  - Deep learning, computer vision, NLP, time series, and reinforcement learning
  - MLOps tools, experiment tracking, model deployment, and GPU acceleration

### Utilities (3 profiles)
- **[utils-databases](utils-databases.md)** - Database development environment
  - Status: ✅ Production Ready
  - 32 components including PostgreSQL, MySQL, MongoDB, Redis, Neo4j, SQLite
  - Administration tools (pgAdmin, DBeaver, MongoDB Compass)
  - Migration tools, Python drivers, and monitoring tools

- **[utils-docker](utils-docker.md)** - Containerization and orchestration
  - Status: ✅ Production Ready
  - 29 components including Docker, Kubernetes, Helm, Minikube, K9s
  - Container registries, security scanning, monitoring
  - CI/CD integration and DevOps tools

- **[utils-version-control](utils-version-control.md)** - Git ecosystem
  - Status: ✅ Production Ready
  - 29 components including Git, GitHub CLI, GitLab CLI, Git Flow
  - GUI clients (GitKraken, Sourcetree), commit tools, merge tools
  - Code review tools and Git utilities

## Quick Install

```bash
# List all available profiles
he2plus list --available

# Search for profiles
he2plus search web
he2plus search ml
he2plus search docker

# Get profile information
he2plus info web-nextjs

# Install a profile
he2plus install web-nextjs
```

## Profile Categories

| Category | Profiles | Components | Use Case |
|----------|----------|------------|----------|
| **Web3** | 1 | 26 | Blockchain & smart contracts |
| **Web** | 4 | 330 | Web applications |
| **Mobile** | 1 | 60 | Mobile apps |
| **ML** | 1 | 74 | AI & machine learning |
| **Utils** | 3 | 90 | Development tools |
| **TOTAL** | **10** | **580** | All development needs |

## Coming Soon

See [coming-soon](coming-soon.md) for profiles in development.
