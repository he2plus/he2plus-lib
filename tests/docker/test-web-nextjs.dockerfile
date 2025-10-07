# Test Docker image for Web Next.js Profile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy he2plus library
WORKDIR /app
COPY . /app

# Install he2plus
RUN pip3 install -e .

# Test script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "================================="\n\
echo "Testing Web Next.js Profile"\n\
echo "================================="\n\
\n\
echo "\n1. Checking he2plus installation..."\n\
he2plus --version || exit 1\n\
\n\
echo "\n2. Getting profile info..."\n\
he2plus info web-nextjs || exit 1\n\
\n\
echo "\n3. Checking Node.js..."\n\
node --version || exit 1\n\
\n\
echo "\n4. Checking npm..."\n\
npm --version || exit 1\n\
\n\
echo "\n5. Creating Next.js project..."\n\
cd /tmp\n\
npx create-next-app@latest test-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --yes || exit 1\n\
\n\
echo "\n6. Installing dependencies..."\n\
cd test-app\n\
npm install || exit 1\n\
\n\
echo "\n7. Checking TypeScript..."\n\
npx tsc --version || exit 1\n\
\n\
echo "\n8. Installing additional packages..."\n\
npm install @tanstack/react-query zustand framer-motion || exit 1\n\
\n\
echo "\n9. Linting project..."\n\
npm run lint || exit 1\n\
\n\
echo "\n10. Building project..."\n\
npm run build || exit 1\n\
\n\
echo "\n✅ All Web Next.js profile tests passed!"\n\
' > /test.sh

RUN chmod +x /test.sh

CMD ["/test.sh"]

