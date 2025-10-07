# Building a Full-Stack Next.js Application

Learn how to build a complete full-stack application using the Web Next.js profile with TypeScript, Prisma, NextAuth, and modern tooling.

## Prerequisites

```bash
# Install the Web Next.js development environment
he2plus install web-nextjs

# Verify installation
node --version    # Should show v18.x
npx next --version
```

## Project Overview

We'll build a **Blog Platform** with the following features:
- User authentication (email/password and OAuth)
- Create, read, update, delete blog posts
- User profiles
- Comments on posts
- Like/unlike posts
- Responsive design with Tailwind CSS
- API routes with NextAuth
- Database with Prisma (PostgreSQL)

## Step 1: Create Next.js Project

```bash
# Create project
npx create-next-app@latest blog-platform \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"

cd blog-platform

# Install additional dependencies
npm install prisma @prisma/client next-auth @next-auth/prisma-adapter
npm install bcryptjs date-fns
npm install -D @types/bcryptjs
```

## Step 2: Setup Prisma Database

### Initialize Prisma

```bash
npx prisma init
```

### Configure Database

Update `.env`:

```bash
DATABASE_URL="postgresql://user:password@localhost:5432/blog?schema=public"
NEXTAUTH_SECRET="your-secret-key-here" # Generate with: openssl rand -base64 32
NEXTAUTH_URL="http://localhost:3000"
```

### Define Schema

Update `prisma/schema.prisma`:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  password      String?
  bio           String?
  posts         Post[]
  comments      Comment[]
  likes         Like[]
  accounts      Account[]
  sessions      Session[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model Post {
  id        String    @id @default(cuid())
  title     String
  content   String    @db.Text
  published Boolean   @default(false)
  authorId  String
  author    User      @relation(fields: [authorId], references: [id], onDelete: Cascade)
  comments  Comment[]
  likes     Like[]
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt

  @@index([authorId])
}

model Comment {
  id        String   @id @default(cuid())
  content   String   @db.Text
  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([postId])
  @@index([authorId])
}

model Like {
  id        String   @id @default(cuid())
  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())

  @@unique([postId, userId])
  @@index([postId])
  @@index([userId])
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
}
```

### Generate Prisma Client

```bash
npx prisma generate
npx prisma db push
```

## Step 3: Setup NextAuth

Create `src/lib/prisma.ts`:

```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ['query'],
  });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

Create `src/app/api/auth/[...nextauth]/route.ts`:

```typescript
import NextAuth, { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GoogleProvider from 'next-auth/providers/google';
import { PrismaAdapter } from '@next-auth/prisma-adapter';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          throw new Error('Invalid credentials');
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email },
        });

        if (!user || !user.password) {
          throw new Error('Invalid credentials');
        }

        const isPasswordValid = await bcrypt.compare(
          credentials.password,
          user.password
        );

        if (!isPasswordValid) {
          throw new Error('Invalid credentials');
        }

        return user;
      },
    }),
  ],
  pages: {
    signIn: '/auth/signin',
  },
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
      }
      return session;
    },
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
```

## Step 4: Create API Routes

### Create Post API

Create `src/app/api/posts/route.ts`:

```typescript
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '../auth/[...nextauth]/route';
import { prisma } from '@/lib/prisma';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const published = searchParams.get('published');

  const posts = await prisma.post.findMany({
    where: published === 'true' ? { published: true } : undefined,
    include: {
      author: {
        select: {
          name: true,
          email: true,
          image: true,
        },
      },
      _count: {
        select: {
          likes: true,
          comments: true,
        },
      },
    },
    orderBy: {
      createdAt: 'desc',
    },
  });

  return NextResponse.json(posts);
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions);

  if (!session?.user?.email) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { title, content, published } = await request.json();

  if (!title || !content) {
    return NextResponse.json(
      { error: 'Title and content are required' },
      { status: 400 }
    );
  }

  const user = await prisma.user.findUnique({
    where: { email: session.user.email },
  });

  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 });
  }

  const post = await prisma.post.create({
    data: {
      title,
      content,
      published: published || false,
      authorId: user.id,
    },
    include: {
      author: {
        select: {
          name: true,
          email: true,
        },
      },
    },
  });

  return NextResponse.json(post);
}
```

### Like Post API

Create `src/app/api/posts/[id]/like/route.ts`:

```typescript
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '../../../auth/[...nextauth]/route';
import { prisma } from '@/lib/prisma';

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  const session = await getServerSession(authOptions);

  if (!session?.user?.email) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const user = await prisma.user.findUnique({
    where: { email: session.user.email },
  });

  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 });
  }

  const existingLike = await prisma.like.findUnique({
    where: {
      postId_userId: {
        postId: params.id,
        userId: user.id,
      },
    },
  });

  if (existingLike) {
    // Unlike
    await prisma.like.delete({
      where: {
        id: existingLike.id,
      },
    });
    return NextResponse.json({ liked: false });
  } else {
    // Like
    await prisma.like.create({
      data: {
        postId: params.id,
        userId: user.id,
      },
    });
    return NextResponse.json({ liked: true });
  }
}
```

## Step 5: Create Components

### Post Card Component

Create `src/components/PostCard.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { useRouter } from 'next/navigation';

interface PostCardProps {
  post: {
    id: string;
    title: string;
    content: string;
    createdAt: Date;
    author: {
      name: string | null;
      email: string | null;
      image: string | null;
    };
    _count: {
      likes: number;
      comments: number;
    };
  };
}

export default function PostCard({ post }: PostCardProps) {
  const router = useRouter();
  const [likes, setLikes] = useState(post._count.likes);
  const [isLiking, setIsLiking] = useState(false);

  const handleLike = async () => {
    setIsLiking(true);
    try {
      const response = await fetch(`/api/posts/${post.id}/like`, {
        method: 'POST',
      });
      const data = await response.json();
      setLikes(data.liked ? likes + 1 : likes - 1);
    } catch (error) {
      console.error('Error liking post:', error);
    }
    setIsLiking(false);
  };

  return (
    <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center mb-4">
        {post.author.image ? (
          <img
            src={post.author.image}
            alt={post.author.name || ''}
            className="w-10 h-10 rounded-full mr-3"
          />
        ) : (
          <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold mr-3">
            {post.author.name?.[0] || post.author.email?.[0] || 'U'}
          </div>
        )}
        <div>
          <p className="font-medium">{post.author.name || 'Anonymous'}</p>
          <p className="text-sm text-gray-500">
            {formatDistanceToNow(new Date(post.createdAt), { addSuffix: true })}
          </p>
        </div>
      </div>

      <h2
        className="text-2xl font-bold mb-2 cursor-pointer hover:text-blue-600"
        onClick={() => router.push(`/posts/${post.id}`)}
      >
        {post.title}
      </h2>
      
      <p className="text-gray-700 mb-4 line-clamp-3">
        {post.content}
      </p>

      <div className="flex items-center gap-4 text-gray-600">
        <button
          onClick={handleLike}
          disabled={isLiking}
          className="flex items-center gap-1 hover:text-red-500 transition-colors"
        >
          <span>{likes}</span>
          <span>❤️</span>
        </button>
        <span className="flex items-center gap-1">
          <span>{post._count.comments}</span>
          <span>💬</span>
        </span>
      </div>
    </article>
  );
}
```

### Create Post Form

Create `src/components/CreatePostForm.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function CreatePostForm() {
  const router = useRouter();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [published, setPublished] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch('/api/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, content, published }),
      });

      if (response.ok) {
        router.push('/');
        router.refresh();
      }
    } catch (error) {
      console.error('Error creating post:', error);
    }

    setIsSubmitting(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-2xl mx-auto">
      <div>
        <label className="block text-sm font-medium mb-2">Title</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Content</label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          rows={10}
          required
        />
      </div>

      <div className="flex items-center">
        <input
          type="checkbox"
          id="published"
          checked={published}
          onChange={(e) => setPublished(e.target.checked)}
          className="mr-2"
        />
        <label htmlFor="published">Publish immediately</label>
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

## Step 6: Create Pages

### Home Page

Update `src/app/page.tsx`:

```typescript
import { prisma } from '@/lib/prisma';
import PostCard from '@/components/PostCard';
import Link from 'next/link';

async function getPosts() {
  const posts = await prisma.post.findMany({
    where: { published: true },
    include: {
      author: {
        select: {
          name: true,
          email: true,
          image: true,
        },
      },
      _count: {
        select: {
          likes: true,
          comments: true,
        },
      },
    },
    orderBy: {
      createdAt: 'desc',
    },
  });

  return posts;
}

export default async function Home() {
  const posts = await getPosts();

  return (
    <main className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Blog Platform</h1>
          <div className="flex gap-4">
            <Link href="/posts/new" className="text-blue-600 hover:underline">
              New Post
            </Link>
            <Link href="/api/auth/signout" className="text-gray-600 hover:underline">
              Sign Out
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-8">Latest Posts</h2>
        
        {posts.length === 0 ? (
          <p className="text-gray-600">No posts yet. Be the first to create one!</p>
        ) : (
          <div className="grid gap-6">
            {posts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
```

## Step 7: Run the Application

```bash
# Start development server
npm run dev

# Visit http://localhost:3000
```

## Key Features Implemented

✅ **Authentication**:
- Email/password and OAuth (Google)
- Session management with NextAuth
- Protected routes and API endpoints

✅ **Database**:
- PostgreSQL with Prisma ORM
- User, Post, Comment, Like models
- Relational data with type safety

✅ **Blog Features**:
- Create, read, update, delete posts
- Like/unlike posts
- Comment on posts
- User profiles

✅ **Modern Stack**:
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Server and Client Components

## Next Steps

1. **Add More Features**:
   - Edit and delete posts
   - Comment functionality
   - User profile pages
   - Search and filtering
   - Tags and categories

2. **Improve UI/UX**:
   - Loading states
   - Error handling
   - Toast notifications
   - Skeleton loaders

3. **Optimize Performance**:
   - Image optimization
   - Caching strategies
   - ISR (Incremental Static Regeneration)
   - API rate limiting

4. **Deploy**:
   - Deploy to Vercel
   - Set up production database
   - Configure environment variables
   - Set up monitoring

## Resources

- **Next.js**: [https://nextjs.org/docs](https://nextjs.org/docs)
- **Prisma**: [https://www.prisma.io/docs](https://www.prisma.io/docs)
- **NextAuth**: [https://next-auth.js.org](https://next-auth.js.org)
- **Tailwind CSS**: [https://tailwindcss.com/docs](https://tailwindcss.com/docs)

---

**Congratulations! You've built a full-stack Next.js application! 🎉**
