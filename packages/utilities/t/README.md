# t - Tool Selector

Interactive tool picker using fzf for quick access to CLI tools.

## Features

- Fuzzy search across all tools
- Auto-extracts descriptions from docstrings/comments
- Caches tool list for fast startup
- Passes arguments through to selected tool

## Requirements

- Python 3.8+
- fzf (`brew install fzf`)

## Installation

```bash
# Add to PATH
ln -s /path/to/t ~/.local/bin/t

# Optional: set custom tools directory
export TOOLS_DIR=~/my-tools
```

## Usage

```bash
t              # Interactive picker
t browser      # Pre-filter with query
t --list       # Plain list of all tools
t --refresh    # Rebuild cache
t --path NAME  # Output tool path (for scripts)

# Pass arguments to selected tool
t browser -- --url http://localhost
```

## How It Works

1. Scans `TOOLS_DIR` for executable files
2. Extracts descriptions from:
   - Python docstrings
   - Bash `# description` comments
   - File headers
3. Caches results in `~/.cache/t-tools.json`
4. Presents interactive fzf picker

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TOOLS_DIR` | `~/Tools` | Directory to scan for tools |
| `T_CACHE` | `~/.cache/t-tools.json` | Cache file location |

## License

MIT
