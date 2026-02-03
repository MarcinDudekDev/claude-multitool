#!/bin/bash
# Fast git status - shows changed files without verbosity
# Usage: ./git_status.sh

echo "=== Modified Files ==="
git diff --name-only

echo ""
echo "=== Staged Files ==="
git diff --cached --name-only

echo ""
echo "=== Untracked Files ==="
git ls-files --others --exclude-standard

echo ""
echo "=== Summary ==="
git status --short
