---
name: git-workflow
description: Token-efficient Git workflows with quick status checks, fast staging, concise commits, branch management, and automation scripts.
domain: git
type: workflow
frequency: daily
commands: [git, push-to-github.sh]
tools: [~/Tools/push-to-github.sh]
---

# Git Workflow Skill

This skill optimizes Git workflows for minimal token usage and maximum clarity. It's designed for developers using Claude Code and command-line Git who need quick, efficient operations without verbose output that wastes context.

## Overview

Provide token-efficient Git workflows with quick status checks, fast staging, concise commits, branch management, and automation scripts to reduce repeated queries and context overhead.

## When to Use

Use this skill when:
- Working with Claude Code on command line
- Need quick Git status without verbose output
- Staging multiple files efficiently
- Checking changes before commits
- Managing author/coauthor information
- Automating repeated Git queries

## Quick Start

### Python Helper Script

Use `scripts/git_helper.py` for deterministic, concise operations:

```bash
python git_helper.py status       # Summary: modified/staged/untracked counts
python git_helper.py add-all      # Stage everything + show status
python git_helper.py last         # Last commit (hash | author | message)
python git_helper.py diff         # Show unstaged changes
python git_helper.py diff-staged  # Show staged changes
python git_helper.py branch       # Current branch + tracking info
```

### Bash Quick Status Script

Use `scripts/git_status.sh` for fast terminal output:
```bash
bash git_status.sh                # Shows all changes categorized
```

## Common Workflows

### Check Before Commit
```bash
python git_helper.py status       # See what's changed
python git_helper.py diff         # Review changes
```

### Stage and Verify
```bash
python git_helper.py add-all      # Stages all + shows summary
python git_helper.py diff-staged  # Review what will commit
git commit -m "feature: description"
```

### Check Recent Work
```bash
python git_helper.py last         # One-line summary
python git_helper.py branch       # Current branch tracking
```

## Token-Efficient Patterns

Always reference `references/git_commands.md` for command details instead of re-explaining. Use these flags to minimize output:
- `--name-only` instead of full diffs
- `--short` for status summaries
- `--oneline` for log history
- Script repeated operations using `git_helper.py`

## Author/Coauthor Management

Reference `references/git_commands.md` for adding coauthors in commit messages:
```
Commit message

Co-authored-by: Name <email@example.com>
```

For automation, coauthor info can be added via git hooks or scripts.

## Push to GitHub Script

Use `scripts/push-to-github.sh` to quickly push any project to GitHub:

```bash
bash push-to-github.sh
```

This script:
- Installs GitHub CLI if missing
- Handles authentication automatically
- Detects WordPress plugins and adds `wp-` prefix to repo name
- Creates `.gitignore` if missing
- Initializes git, commits, and creates private GitHub repo
- Skips if remote already configured
