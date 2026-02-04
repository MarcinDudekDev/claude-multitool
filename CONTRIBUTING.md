# Contributing to Claude Multitool

Thanks for your interest in contributing! This toolkit grew from real daily usage patterns, and we welcome improvements from the community.

## Quick Start

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/claude-multitool.git
cd claude-multitool

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes, test locally
./scripts/test.sh

# Commit and push
git commit -m "Add: brief description of change"
git push origin feature/your-feature-name

# Open a PR
```

## Project Structure

```
claude-multitool/
├── packages/
│   ├── layer-0/        # Standalone tools (no dependencies)
│   ├── layer-1/        # Requires Layer 0
│   ├── layer-2/        # Full orchestration
│   ├── memory/         # Graph-vector memory
│   └── utilities/      # Standalone utilities
├── skills/             # Claude Code skills
├── workflows/          # Complex multi-agent workflows
└── scripts/            # Installation & testing
```

## Code Guidelines

### General

- **Test before submitting** - All tools should work with `--help`
- **No hardcoded paths** - Use environment variables with defaults
- **Document changes** - Update README files in affected packages

### Bash Scripts

```bash
#!/usr/bin/env bash
set -e  # Exit on error

# Use functions for organization
main() {
    # Entry point
}

main "$@"
```

### Python Scripts

```python
#!/usr/bin/env python3
"""Brief description of what this tool does."""

import argparse
import os
from pathlib import Path

def main():
    """Entry point."""
    pass

if __name__ == "__main__":
    main()
```

### Environment Variables

Tools should auto-detect paths but allow override:

```python
# Good: auto-detect with override
tool_path = os.environ.get("MY_TOOL_PATH") or find_tool("mytool")

# Bad: hardcoded path
tool_path = "/Users/someone/tools/mytool"
```

## Adding a New Tool

1. **Choose the right layer:**
   - Layer 0: No dependencies on other tools
   - Layer 1: Depends on Layer 0 tools
   - Layer 2: Full orchestration features

2. **Create the directory structure:**
   ```bash
   mkdir -p packages/layer-X/your-tool
   ```

3. **Add the tool script:**
   - Must support `--help` flag
   - Must work without configuration
   - Add sensible defaults

4. **Add a README:**
   ```markdown
   # your-tool

   Brief description.

   ## Installation
   ## Usage
   ## Configuration
   ```

5. **Update main README** if significant

## Adding a Skill

1. Create `skills/your-skill/SKILL.md`:
   ```yaml
   ---
   name: your-skill
   description: What this skill does
   domain: area (web, data, etc.)
   type: knowledge|tool|workflow
   commands: [optional-commands]
   ---

   # Your Skill

   Skill documentation...
   ```

2. Add any supporting modules in `skills/your-skill/modules/`

## Testing

```bash
# Run all tests
./scripts/test.sh

# Test specific tool
packages/layer-0/your-tool/your-tool --help
```

## Commit Messages

Use prefixes:

- `Add:` New feature
- `Fix:` Bug fix
- `Update:` Enhancement to existing feature
- `Docs:` Documentation only
- `Refactor:` Code restructure without behavior change

## Pull Request Process

1. Ensure tests pass
2. Update documentation
3. Fill out the PR template
4. Wait for review

## Questions?

Open an issue with the `question` label.

---

Thank you for contributing!
