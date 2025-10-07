# Test Docker image for Web3 Solidity Profile
FROM ubuntu:22.04

# Prevent interactive prompts
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

# Install he2plus in development mode
RUN pip3 install -e .

# Test script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "================================="\n\
echo "Testing Web3 Solidity Profile"\n\
echo "================================="\n\
\n\
echo "\n1. Checking he2plus installation..."\n\
he2plus --version || exit 1\n\
\n\
echo "\n2. Listing available profiles..."\n\
he2plus list --available || exit 1\n\
\n\
echo "\n3. Getting profile info..."\n\
he2plus info web3-solidity || exit 1\n\
\n\
echo "\n4. Checking Node.js..."\n\
node --version || exit 1\n\
\n\
echo "\n5. Checking npm..."\n\
npm --version || exit 1\n\
\n\
echo "\n6. Installing Hardhat..."\n\
npm install -g hardhat || exit 1\n\
\n\
echo "\n7. Checking Hardhat installation..."\n\
npx hardhat --version || exit 1\n\
\n\
echo "\n8. Installing Foundry..."\n\
curl -L https://foundry.paradigm.xyz | bash || exit 1\n\
export PATH="$HOME/.foundry/bin:$PATH"\n\
foundryup || exit 1\n\
\n\
echo "\n9. Checking Foundry installation..."\n\
forge --version || exit 1\n\
cast --version || exit 1\n\
anvil --version || exit 1\n\
\n\
echo "\n10. Creating test Hardhat project..."\n\
mkdir -p /tmp/test-hardhat && cd /tmp/test-hardhat\n\
npx hardhat init --yes || exit 1\n\
\n\
echo "\n11. Installing OpenZeppelin..."\n\
npm install @openzeppelin/contracts || exit 1\n\
\n\
echo "\n12. Compiling contracts..."\n\
npx hardhat compile || exit 1\n\
\n\
echo "\n13. Running tests..."\n\
npx hardhat test || exit 1\n\
\n\
echo "\n✅ All Web3 Solidity profile tests passed!"\n\
' > /test.sh

RUN chmod +x /test.sh

CMD ["/test.sh"]

