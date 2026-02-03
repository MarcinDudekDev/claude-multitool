# memorize

Simple wrapper for storing memories with auto-categorization.

## Features

- Auto-detects project from working directory
- Auto-categorizes content using AI
- Merges project tags with user tags
- Simple interface for quick storage

## Requirements

- helix-memory (memory CLI)

## Installation

```bash
# Add to PATH
ln -s /path/to/memorize ~/.local/bin/memorize

# Set memory CLI location (if not in standard path)
export MEMORY_CLI=~/.local/bin/memory
```

## Usage

```bash
# Auto-categorize (simplest)
memorize "User prefers rsync over scp"

# Explicit category and importance
memorize -t preference -i 10 "Always test before marking complete"

# With tags
memorize -t fact -i 7 -g "api,config" "API key stored in .env"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-t` | Category | auto-detect |
| `-i` | Importance (1-10) | auto |
| `-g` | Tags (comma-sep) | auto (project) |

## Categories

| Category | Use |
|----------|-----|
| `preference` | Workflows, tool choices, "always/never" |
| `decision` | Technical choices made |
| `fact` | Setup, config, paths, credentials |
| `context` | Project background, domain |
| `task` | TODOs, blockers, action items |
| `solution` | Problems solved, fixes |

## Project Detection

Automatically detects project from:
1. `CLAUDE_PROJECT` environment variable
2. Current working directory

Adds project as a tag automatically.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MEMORY_CLI` | Path to memory CLI |
| `CLAUDE_PROJECT` | Override project detection |

## License

MIT
