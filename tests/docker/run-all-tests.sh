#!/bin/bash

# Run all profile tests in Docker containers
# This script tests each profile in isolation to verify documentation accuracy

set -e

echo "=========================================="
echo "he2plus Profile Testing Suite"
echo "=========================================="
echo ""
echo "This will test all 4 profiles:"
echo "  1. Web3 Solidity"
echo "  2. Web Next.js"
echo "  3. ML Python"
echo "  4. Mobile React Native"
echo ""
echo "Each profile will be tested in a separate Docker container."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to run a single test
run_test() {
    local profile=$1
    local service=$2
    
    echo ""
    echo "=========================================="
    echo "Testing: $profile"
    echo "=========================================="
    echo ""
    
    # Build the image
    echo "Building Docker image for $profile..."
    docker-compose -f docker-compose.test.yml build "$service" 2>&1 | grep -v "WARNING" || true
    
    # Run the test
    echo ""
    echo "Running tests for $profile..."
    if docker-compose -f docker-compose.test.yml run --rm "$service"; then
        echo ""
        echo -e "${GREEN}✅ $profile tests PASSED${NC}"
        return 0
    else
        echo ""
        echo -e "${RED}❌ $profile tests FAILED${NC}"
        return 1
    fi
}

# Track results
declare -a RESULTS
declare -a PROFILES

# Test each profile
PROFILES=(
    "Web3 Solidity:test-web3-solidity"
    "Web Next.js:test-web-nextjs"
    "ML Python:test-ml-python"
    "Mobile React Native:test-mobile-react-native"
)

SUCCESS_COUNT=0
FAIL_COUNT=0

for profile_service in "${PROFILES[@]}"; do
    IFS=':' read -r profile service <<< "$profile_service"
    
    if run_test "$profile" "$service"; then
        RESULTS+=("✅ $profile")
        ((SUCCESS_COUNT++))
    else
        RESULTS+=("❌ $profile")
        ((FAIL_COUNT++))
    fi
done

# Print summary
echo ""
echo "=========================================="
echo "Test Results Summary"
echo "=========================================="
echo ""

for result in "${RESULTS[@]}"; do
    echo "  $result"
done

echo ""
echo "Total: ${SUCCESS_COUNT} passed, ${FAIL_COUNT} failed"
echo ""

# Cleanup
echo "Cleaning up Docker resources..."
docker-compose -f docker-compose.test.yml down 2>/dev/null || true

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}=========================================="
    echo "All tests passed! 🎉"
    echo -e "==========================================${NC}"
    exit 0
else
    echo -e "${RED}=========================================="
    echo "Some tests failed. Please check the logs."
    echo -e "==========================================${NC}"
    exit 1
fi

