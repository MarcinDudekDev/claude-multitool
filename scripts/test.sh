#!/usr/bin/env bash
#
# Test suite for Claude Multitool
# Run: ./scripts/test.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

passed=0
failed=0
skipped=0

# Test a tool's --help flag
test_help() {
    local name="$1"
    local path="$2"

    if [ ! -f "$path" ]; then
        echo -e "  ${YELLOW}SKIP${NC} $name (not found)"
        skipped=$((skipped + 1))
        return
    fi

    if [ ! -x "$path" ]; then
        chmod +x "$path"
    fi

    if "$path" --help >/dev/null 2>&1; then
        echo -e "  ${GREEN}PASS${NC} $name --help"
        passed=$((passed + 1))
    else
        echo -e "  ${RED}FAIL${NC} $name --help"
        failed=$((failed + 1))
    fi
}

# Test Python syntax
test_python_syntax() {
    local name="$1"
    local path="$2"

    if [ ! -f "$path" ]; then
        return
    fi

    if python3 -m py_compile "$path" 2>/dev/null; then
        echo -e "  ${GREEN}PASS${NC} $name syntax"
        passed=$((passed + 1))
    else
        echo -e "  ${RED}FAIL${NC} $name syntax"
        failed=$((failed + 1))
    fi
}

# Test bash syntax
test_bash_syntax() {
    local name="$1"
    local path="$2"

    if [ ! -f "$path" ]; then
        return
    fi

    if bash -n "$path" 2>/dev/null; then
        echo -e "  ${GREEN}PASS${NC} $name syntax"
        passed=$((passed + 1))
    else
        echo -e "  ${RED}FAIL${NC} $name syntax"
        failed=$((failed + 1))
    fi
}

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              Claude Multitool Test Suite                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Layer 0 tests
echo "Layer 0 (Standalone):"
test_help "pane-status" "$ROOT_DIR/packages/layer-0/pane-status/pane-status"
test_bash_syntax "pane-status" "$ROOT_DIR/packages/layer-0/pane-status/pane-status"
test_help "p" "$ROOT_DIR/packages/layer-0/p/p"
test_python_syntax "p" "$ROOT_DIR/packages/layer-0/p/p"
echo ""

# Layer 1 tests
echo "Layer 1 (Messaging):"
test_help "msg" "$ROOT_DIR/packages/layer-1/msg/msg"
test_bash_syntax "msg" "$ROOT_DIR/packages/layer-1/msg/msg"
test_help "inbox-daemon" "$ROOT_DIR/packages/layer-1/inbox-daemon/inbox-daemon"
test_bash_syntax "inbox-daemon" "$ROOT_DIR/packages/layer-1/inbox-daemon/inbox-daemon"
echo ""

# Layer 2 tests
echo "Layer 2 (Orchestration):"
test_help "op" "$ROOT_DIR/packages/layer-2/op/op"
test_python_syntax "op" "$ROOT_DIR/packages/layer-2/op/op"
echo ""

# Memory tests
echo "Memory System:"
test_help "memory" "$ROOT_DIR/packages/memory/helix-memory/memory"
test_help "memorize" "$ROOT_DIR/packages/memory/memorize/memorize"
echo ""

# Utility tests
echo "Utilities:"
test_help "t" "$ROOT_DIR/packages/utilities/t/t"
test_help "img-optimize" "$ROOT_DIR/packages/utilities/img-optimize/img-optimize"
echo ""

# Installer test
echo "Installer:"
test_bash_syntax "install.sh" "$ROOT_DIR/install.sh"
if bash "$ROOT_DIR/install.sh" --help >/dev/null 2>&1; then
    echo -e "  ${GREEN}PASS${NC} install.sh --help"
    passed=$((passed + 1))
else
    echo -e "  ${RED}FAIL${NC} install.sh --help"
    failed=$((failed + 1))
fi
echo ""

# Skills structure test
echo "Skills:"
for skill_dir in "$ROOT_DIR/skills/"*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
        echo -e "  ${GREEN}PASS${NC} $skill_name has SKILL.md"
        passed=$((passed + 1))
    else
        echo -e "  ${RED}FAIL${NC} $skill_name missing SKILL.md"
        failed=$((failed + 1))
    fi
done
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════"
total=$((passed + failed + skipped))
echo -e "Results: ${GREEN}$passed passed${NC}, ${RED}$failed failed${NC}, ${YELLOW}$skipped skipped${NC} (total: $total)"

if [ $failed -gt 0 ]; then
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
