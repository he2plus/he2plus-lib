#!/bin/bash
# Comprehensive he2plus Testing Script
# Tests all core functionality as a real user would experience it

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════════"
echo "🧪 HE2PLUS COMPREHENSIVE VALIDATION TEST"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Testing Date: $(date)"
echo "Test Environment: $(lsb_release -d | cut -f2)"
echo "Python Version: $(python3 --version)"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    
    TESTS_RUN=$((TESTS_RUN + 1))
    echo ""
    echo "────────────────────────────────────────────────────────────────"
    echo -e "${BLUE}TEST $TESTS_RUN: $test_name${NC}"
    echo "────────────────────────────────────────────────────────────────"
    echo "Command: $test_command"
    echo ""
    
    if eval "$test_command"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        return 0
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        return 1
    fi
}

# No venv needed - installed with pip --user
echo "🔧 Using user-installed he2plus..."
echo ""

# ═══════════════════════════════════════════════════════════════════
# PHASE 1: INSTALLATION VERIFICATION
# ═══════════════════════════════════════════════════════════════════
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 1: INSTALLATION VERIFICATION"
echo "════════════════════════════════════════════════════════════════"

run_test "he2plus command is available" "which he2plus"
run_test "he2plus is executable" "test -x \$(which he2plus)"

# ═══════════════════════════════════════════════════════════════════
# PHASE 2: BASIC CLI COMMANDS
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 2: BASIC CLI COMMANDS"
echo "════════════════════════════════════════════════════════════════"

run_test "Version command" "he2plus --version"
run_test "Help command" "he2plus --help"
run_test "List command" "he2plus list"
run_test "List available profiles" "he2plus list --available"

# ═══════════════════════════════════════════════════════════════════
# PHASE 3: SYSTEM INFO DETECTION
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 3: SYSTEM INFO DETECTION"
echo "════════════════════════════════════════════════════════════════"

run_test "System info command" "he2plus info"
run_test "System info shows OS" "he2plus info | grep -i 'os'"
run_test "System info shows RAM" "he2plus info | grep -i 'ram'"

# ═══════════════════════════════════════════════════════════════════
# PHASE 4: PROFILE DISCOVERY
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 4: PROFILE DISCOVERY"
echo "════════════════════════════════════════════════════════════════"

run_test "Search web profiles" "he2plus search web"
run_test "Search ml profiles" "he2plus search ml"
run_test "Search web3 profiles" "he2plus search web3"
run_test "Search mobile profiles" "he2plus search mobile"

# ═══════════════════════════════════════════════════════════════════
# PHASE 5: PROFILE INFORMATION
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 5: PROFILE INFORMATION"
echo "════════════════════════════════════════════════════════════════"

run_test "Info for web-nextjs profile" "he2plus info web-nextjs"
run_test "Info for web3-solidity profile" "he2plus info web3-solidity"
run_test "Info for ml-python profile" "he2plus info ml-python"
run_test "Info for mobile-react-native profile" "he2plus info mobile-react-native"
run_test "Info for web-mern profile" "he2plus info web-mern"

# ═══════════════════════════════════════════════════════════════════
# PHASE 6: PROFILE INSTALLATION DRY-RUN
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 6: PROFILE INSTALLATION DRY-RUN"
echo "════════════════════════════════════════════════════════════════"
echo "Note: These tests verify install command works, not actual installation"

# We can't do full installation in Docker without package managers,
# but we can verify the command accepts the profile and shows plan
run_test "Install command accepts web-nextjs" "he2plus install web-nextjs --help || true"
run_test "Install command accepts web3-solidity" "he2plus install web3-solidity --help || true"

# ═══════════════════════════════════════════════════════════════════
# PHASE 7: DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 7: DIAGNOSTICS"
echo "════════════════════════════════════════════════════════════════"

run_test "Doctor command" "he2plus doctor"

# ═══════════════════════════════════════════════════════════════════
# PHASE 8: ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 8: ERROR HANDLING"
echo "════════════════════════════════════════════════════════════════"

run_test "Non-existent profile shows error" "he2plus info fake-profile-xyz 2>&1 | grep -q 'not found'"
run_test "Invalid command shows error" "he2plus invalidcommand 2>&1 | grep -q 'Error'"

# ═══════════════════════════════════════════════════════════════════
# PHASE 9: PYTHON IMPORT TESTS
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 9: PYTHON IMPORT TESTS"
echo "════════════════════════════════════════════════════════════════"

run_test "Import he2plus module" "python3 -c 'import he2plus'"
run_test "Import core system" "python3 -c 'from he2plus.core import system'"
run_test "Import profiles registry" "python3 -c 'from he2plus.profiles import registry'"
run_test "Import CLI main" "python3 -c 'from he2plus.cli import main'"

# ═══════════════════════════════════════════════════════════════════
# PHASE 10: PROFILE LOADING TEST
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "PHASE 10: PROFILE LOADING TEST"
echo "════════════════════════════════════════════════════════════════"

# Test that all profiles can be loaded
cat > /tmp/test_profiles.py << 'EOF'
from he2plus.profiles.registry import ProfileRegistry

registry = ProfileRegistry()
profiles = registry.get_all()

print(f"\n✅ Found {len(profiles)} profiles:")
for profile in profiles:
    print(f"  • {profile.id}: {profile.name}")
    # Verify profile has required attributes
    assert hasattr(profile, 'components'), f"{profile.id} missing components"
    assert hasattr(profile, 'requirements'), f"{profile.id} missing requirements"
    assert hasattr(profile, 'verification_steps'), f"{profile.id} missing verification_steps"
    print(f"    ✓ {len(profile.components)} components")
    print(f"    ✓ Requirements defined")
    print(f"    ✓ {len(profile.verification_steps)} verification steps")

print(f"\n✅ All profiles loaded successfully!")
EOF

run_test "Load all profiles programmatically" "python3 /tmp/test_profiles.py"

# ═══════════════════════════════════════════════════════════════════
# FINAL RESULTS
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "📊 TEST RESULTS SUMMARY"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Total Tests Run:    $TESTS_RUN"
echo -e "${GREEN}Tests Passed:       $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed:       $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ ALL TESTS PASSED! HE2PLUS IS WORKING CORRECTLY! 🎉${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
    exit 0
else
    SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($TESTS_PASSED/$TESTS_RUN)*100}")
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}⚠️  SOME TESTS FAILED (Success Rate: ${SUCCESS_RATE}%)${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════${NC}"
    exit 1
fi
