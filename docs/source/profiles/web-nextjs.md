# Web Next.js Profile

**Status:** ✅ Production Ready  
**Profile ID:** `web-nextjs`  
**Category:** Web Development
**Version:** 1.0.0

## Overview

Complete Next.js development environment with TypeScript, Tailwind CSS, and modern full-stack tooling. Build production-ready web applications with Server Components, App Router, and the latest React features.

## What's Included

### Core Development Environment

#### Language Runtime & Package Managers
- **Node.js 18.19.0 LTS** - JavaScript runtime for Next.js development
- **npm 10.2.3** - Node Package Manager (included with Node.js)
- **Yarn 1.22+** - Fast, reliable dependency management
- **pnpm 8.x** - Fast, disk space efficient package manager

#### Version Control
- **Git 2.39+** - Distributed version control system

#### Development Tools
- **Visual Studio Code** - Code editor with excellent TypeScript and React support

### Framework & Core Libraries

#### Next.js Ecosystem
- **Next.js 14+** - The React Framework for Production with App Router
- **React 18+** - JavaScript library for building user interfaces
- **React DOM** - React package for working with the DOM
- **TypeScript 5.x** - Typed JavaScript at scale for better developer experience

### Styling Solutions

#### CSS Frameworks & Tools
- **Tailwind CSS 3.x** - Utility-first CSS framework
- **PostCSS** - CSS transformation tool
- **Autoprefixer** - PostCSS plugin for vendor prefixes
- **Styled Components** - CSS-in-JS library for styled React components
- **Emotion** - CSS-in-JS library with powerful composition

### State Management

#### State Libraries
- **Zustand** - Small, fast and scalable state management solution
- **Redux Toolkit** - Official, opinionated, batteries-included toolset for Redux
- **Jotai** - Primitive and flexible state management
- **React Context** - Built-in React state management (no installation needed)

### UI Component Libraries

#### Design Systems & Component Libraries
- **shadcn/ui** - Beautifully designed components with Radix UI and Tailwind
- **Radix UI** - Low-level UI primitives for React
- **Headless UI** - Unstyled, accessible UI components for React
- **Lucide React** - Beautiful & consistent icon toolkit
- **React Icons** - Popular icon library for React
- **Heroicons** - Beautiful hand-crafted SVG icons

### Animation & Motion

#### Animation Libraries
- **Framer Motion** - Production-ready motion library for React
- **React Spring** - Spring-physics based animation library
- **Auto Animate** - Zero-config, drop-in animations

### Forms & Validation

#### Form Management
- **React Hook Form** - Performant, flexible forms with easy validation
- **Zod** - TypeScript-first schema validation
- **Yup** - Schema validation library
- **Formik** - Popular form library for React

### Data Fetching & Caching

#### Data Management Libraries
- **TanStack Query** (React Query) - Powerful data synchronization for React
- **SWR** - React Hooks for data fetching with caching and revalidation
- **Axios** - Promise-based HTTP client
- **React Query Devtools** - Developer tools for TanStack Query

### Database & Backend

#### ORMs & Database Tools
- **Prisma** - Next-generation ORM for Node.js and TypeScript
- **Drizzle ORM** - TypeScript ORM for SQL databases
- **Mongoose** - MongoDB object modeling
- **SQL.js** - SQLite compiled to JavaScript

#### Authentication
- **NextAuth.js** - Authentication for Next.js applications
- **Clerk** - Complete user management for modern applications
- **Auth0** - Authentication and authorization platform
- **Supabase Auth** - Open-source Firebase alternative

### Testing

#### Testing Frameworks & Tools
- **Jest** - JavaScript testing framework with focus on simplicity
- **React Testing Library** - Testing utilities for React components
- **Cypress** - End-to-end testing framework
- **Playwright** - End-to-end testing for modern web apps
- **Vitest** - Fast unit testing framework powered by Vite
- **Testing Library User Event** - User interaction simulation

### Code Quality & Linting

#### Linters & Formatters
- **ESLint** - JavaScript and TypeScript linter
- **Prettier** - Opinionated code formatter
- **Husky** - Git hooks made easy
- **lint-staged** - Run linters on staged git files
- **commitlint** - Lint commit messages

### Build & Bundle Tools

#### Build Tools
- **Turbopack** - Incremental bundler optimized for JavaScript/TypeScript
- **SWC** - Super-fast TypeScript/JavaScript compiler (built into Next.js)
- **Webpack** - Module bundler (used by Next.js internally)

### Development & Debugging

#### Developer Experience
- **React DevTools** - Browser extension for debugging React
- **Redux DevTools** - Browser extension for Redux debugging  
- **Next.js DevTools** - Built-in development tools
- **Storybook** - Tool for building UI components in isolation
- **Chromatic** - Visual testing for Storybook

### Deployment & Hosting

#### Deployment Tools & CLIs
- **Vercel CLI** - Command-line interface for Vercel (recommended)
- **Netlify CLI** - Command-line interface for Netlify
- **Railway CLI** - Command-line interface for Railway deployment
- **Docker** - Containerization platform for consistent deployments

### Monitoring & Analytics

#### Error Tracking & Performance
- **Sentry Next.js SDK** - Error monitoring and performance tracking
- **Sentry CLI** - Command-line interface for Sentry
- **Vercel Analytics** - Built-in web analytics
- **Google Analytics** - Web analytics service
- **PostHog** - Open-source product analytics

### Advanced Features

#### Progressive Web Apps
- **next-pwa** - Zero-config PWA plugin for Next.js
- **Workbox** - Service worker libraries

#### SEO & Metadata
- **Next SEO** - SEO plugin for Next.js
- **next-sitemap** - Sitemap generator for Next.js
- **Schema.org types** - Structured data for SEO

#### Theming
- **next-themes** - Perfect dark mode in 2 lines of code
- **Theme UI** - Build consistent, themeable React apps

#### Internationalization
- **next-intl** - Internationalization for Next.js
- **react-i18next** - Internationalization framework

### Additional Utilities

#### Utility Libraries
- **date-fns** - Modern JavaScript date utility library
- **lodash** - Modern JavaScript utility library
- **clsx** - Utility for constructing className strings
- **class-variance-authority** - CSS class variance utility

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| **RAM** | 8 GB | 16 GB |
| **Disk Space** | 10 GB | 20 GB |
| **CPU** | 4 cores | 8 cores |
| **Internet** | Required | High-speed |
| **Download Size** | ~800 MB | - |
| **Installation Time** | 10-15 min | - |

## Quick Install

```bash
# Install complete Next.js development environment
he2plus install web-nextjs

# Verify installation
he2plus info web-nextjs
```

## Getting Started

### 1. Create a New Next.js Project

```bash
# Create new project with TypeScript and Tailwind CSS
npx create-next-app@latest my-nextjs-app \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"

# Navigate to project
cd my-nextjs-app

# Start development server
npm run dev
```

Visit `http://localhost:3000` to see your app!

### 2. Project Structure

```
my-nextjs-app/
├── src/
│   ├── app/              # App Router pages and layouts
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Home page
│   │   └── api/          # API routes
│   ├── components/       # React components
│   ├── lib/             # Utility functions
│   └── styles/          # Global styles
├── public/              # Static assets
├── next.config.js       # Next.js configuration
├── tailwind.config.js   # Tailwind configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies
```

### 3. Create Your First Component

```typescript
// src/components/Hero.tsx
'use client';

import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 to-purple-600"
    >
      <h1 className="text-6xl font-bold text-white mb-4">
        Welcome to Next.js
      </h1>
      <p className="text-xl text-white/80 mb-8">
        Build amazing web applications with React
      </p>
      <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
        Get Started
      </button>
    </motion.div>
  );
}
```

### 4. Using App Router (Next.js 14)

```typescript
// src/app/page.tsx
import Hero from '@/components/Hero';
import Features from '@/components/Features';

export default function Home() {
  return (
    <main>
      <Hero />
      <Features />
    </main>
  );
}
```

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'My Next.js App',
  description: 'Built with Next.js 14',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

### 5. Server Components & API Routes

```typescript
// src/app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const users = [
    { id: 1, name: 'John Doe' },
    { id: 2, name: 'Jane Smith' },
  ];
  
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  // Process the data
  return NextResponse.json({ success: true, data: body });
}
```

### 6. Data Fetching with TanStack Query

```typescript
// src/app/users/page.tsx
'use client';

import { useQuery } from '@tanstack/react-query';

async function fetchUsers() {
  const res = await fetch('/api/users');
  return res.json();
}

export default function UsersPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading users</div>;

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {data.map((user: any) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### 7. Form Handling with React Hook Form + Zod

```typescript
// src/components/ContactForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
});

type FormData = z.infer<typeof schema>;

export default function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <input
          {...register('name')}
          placeholder="Name"
          className="w-full px-4 py-2 border rounded"
        />
        {errors.name && (
          <p className="text-red-500 text-sm">{errors.name.message}</p>
        )}
      </div>

      <div>
        <input
          {...register('email')}
          type="email"
          placeholder="Email"
          className="w-full px-4 py-2 border rounded"
        />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}
      </div>

      <div>
        <textarea
          {...register('message')}
          placeholder="Message"
          rows={4}
          className="w-full px-4 py-2 border rounded"
        />
        {errors.message && (
          <p className="text-red-500 text-sm">{errors.message.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  );
}
```

### 8. State Management with Zustand

```typescript
// src/lib/store.ts
import { create } from 'zustand';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
  total: () => number;
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],
  
  addItem: (item) =>
    set((state) => ({
      items: [...state.items, item],
    })),
  
  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),
  
  clearCart: () => set({ items: [] }),
  
  total: () =>
    get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),
}));
```

```typescript
// Using the store in a component
'use client';

import { useCartStore } from '@/lib/store';

export default function Cart() {
  const { items, removeItem, total } = useCartStore();

  return (
    <div>
      <h2>Shopping Cart</h2>
      {items.map((item) => (
        <div key={item.id}>
          <span>{item.name} - ${item.price}</span>
          <button onClick={() => removeItem(item.id)}>Remove</button>
        </div>
      ))}
      <div>Total: ${total()}</div>
    </div>
  );
}
```

### 9. Database with Prisma

```bash
# Install Prisma
npm install prisma @prisma/client

# Initialize Prisma
npx prisma init
```

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
}
```

```typescript
// src/lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ['query'],
  });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

```typescript
// src/app/api/posts/route.ts
import { prisma } from '@/lib/prisma';
import { NextResponse } from 'next/server';

export async function GET() {
  const posts = await prisma.post.findMany({
    include: { author: true },
  });
  return NextResponse.json(posts);
}
```

### 10. Authentication with NextAuth.js

```bash
npm install next-auth
```

```typescript
// src/app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';

const handler = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  pages: {
    signIn: '/auth/signin',
  },
});

export { handler as GET, handler as POST };
```

## Development Workflow

### 1. Project Setup
```bash
# Create project
npx create-next-app@latest my-app --typescript --tailwind

# Install additional dependencies
npm install @tanstack/react-query zustand framer-motion

# Start development
npm run dev
```

### 2. Development Process
- Use App Router for modern routing patterns
- Leverage Server Components for better performance
- Implement proper TypeScript types
- Use Tailwind CSS for rapid styling
- Add Framer Motion for smooth animations

### 3. Testing Strategy
```bash
# Install testing dependencies
npm install -D jest @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# E2E testing with Cypress
npm install -D cypress
npx cypress open
```

### 4. Code Quality
```bash
# Run linter
npm run lint

# Format code
npx prettier --write .

# Type checking
npx tsc --noEmit
```

### 5. Build & Deploy
```bash
# Build for production
npm run build

# Test production build locally
npm run start

# Deploy to Vercel
npx vercel

# Deploy to production
npx vercel --prod
```

## Configuration Examples

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['example.com'],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    serverActions: true,
    typedRoutes: true,
  },
  // Enable SWC minification
  swcMinify: true,
  
  // Environment variables
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
  
  // Rewrites for API proxy
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.example.com/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
```

### tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

## Troubleshooting Guide

### Common Issues

#### 1. Installation Problems
- **Node.js version**: Ensure Node.js 18+ is installed
- **npm cache**: Clear with `npm cache clean --force`
- **Port conflicts**: Change port with `PORT=3001 npm run dev`

#### 2. Build Errors
- **TypeScript errors**: Run `npx tsc --noEmit` to check types
- **Module not found**: Delete `node_modules` and `.next`, reinstall
- **Memory issues**: Increase Node.js memory: `NODE_OPTIONS='--max-old-space-size=4096'`

#### 3. Development Issues
- **Hot reload not working**: Restart dev server
- **Tailwind not applying**: Check `tailwind.config.js` paths
- **Imports not working**: Verify `tsconfig.json` paths

#### 4. Deployment Issues
- **Build failures**: Check environment variables
- **Vercel timeout**: Optimize build, use Edge Functions
- **Image optimization**: Configure `next.config.js` properly

## VS Code Extensions

### Essential
- **ES7+ React/Redux/React-Native snippets** - Code snippets
- **Tailwind CSS IntelliSense** - Autocomplete for Tailwind
- **Prettier** - Code formatter
- **ESLint** - JavaScript linter

### Recommended
- **Auto Rename Tag** - Rename paired HTML/JSX tags
- **Path Intellisense** - Autocomplete filenames
- **GitLens** - Enhanced Git integration
- **Thunder Client** - API testing

## Useful Commands

### Next.js Commands
```bash
npx create-next-app@latest    # Create new project
npm run dev                    # Start development server
npm run build                  # Build for production
npm run start                  # Start production server
npm run lint                   # Run ESLint
```

### Package Management
```bash
npm install <package>          # Install package
npm install -D <package>       # Install dev dependency
npm update                     # Update packages
npm audit fix                  # Fix vulnerabilities
```

### Development Tools
```bash
npx tsc --noEmit              # Type check
npx eslint . --ext .ts,.tsx   # Lint files
npx prettier --write .        # Format code
npx jest --watch              # Run tests in watch mode
```

## Resources & Documentation

### Official Documentation
- **Next.js**: https://nextjs.org/docs
- **React**: https://react.dev
- **TypeScript**: https://www.typescriptlang.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

### Learning Resources
- **Next.js Learn**: https://nextjs.org/learn
- **React Tutorial**: https://react.dev/learn
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook

### Community
- **Next.js Discord**: https://discord.gg/nextjs
- **React Community**: https://react.dev/community
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/next.js

## Pro Tips

### Performance
1. Use Server Components by default
2. Implement proper code splitting
3. Optimize images with `next/image`
4. Use `next/font` for font optimization
5. Enable SWC minification

### SEO
1. Use `next-seo` for metadata
2. Implement proper heading hierarchy
3. Add structured data (JSON-LD)
4. Generate sitemap with `next-sitemap`
5. Optimize Core Web Vitals

### Development
1. Use TypeScript strict mode
2. Implement proper error boundaries
3. Use React Hook Form for forms
4. Implement proper loading states
5. Use environment variables properly

### Security
1. Validate all user inputs
2. Use environment variables for secrets
3. Implement proper authentication
4. Use HTTPS in production
5. Set proper CORS policies

---

**Ready to build amazing web applications? Start creating! 🚀**
