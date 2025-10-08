#!/bin/bash
# Master test runner for he2plus Docker validation
# Runs comprehensive tests across multiple environments

set -e

echo "════════════════════════════════════════════════════════════════"
echo "🚀 HE2PLUS DOCKER VALIDATION SUITE"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "This will test he2plus installation and functionality across:"
echo "  • Ubuntu 22.04 LTS"
echo "  • Ubuntu 20.04 LTS"
echo "  • Debian 12 (Bookworm)"
echo ""
echo "Testing local code from: $(pwd)/../.."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Make test script executable
chmod +x test_comprehensive.sh

# Clean up any previous containers
echo "🧹 Cleaning up previous test containers..."
docker-compose down -v 2>/dev/null || true
echo ""

# Build and run tests
echo "🔨 Building Docker images..."
docker-compose build --no-cache

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🧪 RUNNING TESTS ON UBUNTU 22.04"
echo "════════════════════════════════════════════════════════════════"
docker-compose run --rm ubuntu22-test

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🧪 RUNNING TESTS ON UBUNTU 20.04"
echo "════════════════════════════════════════════════════════════════"
docker-compose run --rm ubuntu20-test

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🧪 RUNNING TESTS ON DEBIAN 12"
echo "════════════════════════════════════════════════════════════════"
docker-compose run --rm debian-test

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ ALL ENVIRONMENT TESTS COMPLETED!"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Clean up
docker-compose down -v

echo "🎉 Validation complete!"

