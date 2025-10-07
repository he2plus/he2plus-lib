# Test Docker image for Mobile React Native Profile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    git \
    curl \
    build-essential \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

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
echo "Testing Mobile React Native Profile"\n\
echo "================================="\n\
\n\
echo "\n1. Checking he2plus installation..."\n\
he2plus --version || exit 1\n\
\n\
echo "\n2. Getting profile info..."\n\
he2plus info mobile-react-native || exit 1\n\
\n\
echo "\n3. Checking Node.js..."\n\
node --version || exit 1\n\
\n\
echo "\n4. Checking npm..."\n\
npm --version || exit 1\n\
\n\
echo "\n5. Checking Java..."\n\
java -version || exit 1\n\
\n\
echo "\n6. Installing React Native CLI..."\n\
npm install -g react-native-cli || exit 1\n\
\n\
echo "\n7. Creating React Native project..."\n\
cd /tmp\n\
npx react-native@latest init TestApp --skip-install || exit 1\n\
\n\
echo "\n8. Installing dependencies..."\n\
cd TestApp\n\
npm install || exit 1\n\
\n\
echo "\n9. Checking TypeScript..."\n\
npx tsc --version || exit 1\n\
\n\
echo "\n10. Installing additional packages..."\n\
npm install @react-navigation/native react-native-reanimated react-native-gesture-handler || exit 1\n\
\n\
echo "\n11. Linting project..."\n\
npm run lint || echo "Lint warnings ignored"\n\
\n\
echo "\n12. Running tests..."\n\
npm test -- --passWithNoTests || exit 1\n\
\n\
echo "\n✅ All Mobile React Native profile tests passed!"\n\
' > /test.sh

RUN chmod +x /test.sh

CMD ["/test.sh"]

