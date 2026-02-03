# p - Project Picker

Interactive project picker using fzf for Claude Code workflows.

## Features

- Interactive fuzzy search with fzf
- Auto-discovery from `~/.claude/projects/`
- Project type detection (Python, Node, WordPress, etc.)
- Non-interactive mode for scripts
- JSON output for automation

## Requirements

- Python 3.8+
- fzf (`brew install fzf` or `apt install fzf`)

## Installation

```bash
# Add to PATH
ln -s /path/to/p ~/.local/bin/p

# Add shell function to ~/.zshrc or ~/.bashrc for cd integration
p() { local d; d=$(command p "$@") && [ -n "$d" ] && cd "$d"; }
```

## Usage

### Interactive Mode

```bash
p              # Open fzf picker
p myproj       # Pre-filter with query
```

### Non-Interactive (for scripts)

```bash
p --goto myproject    # Output path for exact/fuzzy match
p --path myproject    # Alias for --goto
p --current           # JSON info of project based on cwd
p --search query      # JSON array of matching projects
p --info              # JSON info of current project
p --info query        # JSON array of search results
p --list              # Plain list of all projects
```

### Project Management

```bash
p --add [name] [path]  # Register directory (uses cwd if no path)
p --remove             # Interactive removal with fzf
p --sync               # Re-scan ~/.claude/projects/
p --cleanup            # Remove duplicate entries
p --redetect           # Re-detect types for 'unknown' entries
p --merge SRC DST      # Merge projects (sessions, hours)
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `P_REGISTRY` | `~/.claude/projects.json` | Project registry file |
| `CLAUDE_PROJECTS` | `~/.claude/projects/` | Claude projects directory |
| `WP_TEST_SITES` | `~/.wp-test/sites/` | WordPress test sites |
| `ITERM_SYNC` | (none) | Optional iTerm2 sync script |

## Examples

### Automation

```bash
# Change to project directory
cd "$(p --goto myproject)"

# Run Claude in project
cd "$(p --goto myproject)" && claude -c

# Check current project
p --current | jq -r '.name'

# Find WordPress projects
p --search wp | jq -r '.[].name'
```

### Shell Function with Claude

```bash
# Add to ~/.zshrc
pc() { local d; d=$(command p "$@") && [ -n "$d" ] && cd "$d" && claude -c; }
```

## Project Registry

Projects are stored in `~/.claude/projects.json`:

```json
{
  "myproject": {
    "path": "/Users/me/Projects/myproject",
    "type": "python",
    "added": "2024-01-15",
    "last_accessed": "2024-01-20"
  }
}
```

## Type Detection

Automatically detects project type based on:

| Type | Detection |
|------|-----------|
| python | `requirements.txt`, `pyproject.toml`, `.venv`, `*.py` files |
| node | `package.json` |
| wordpress | `wp-config.php`, `wordpress/` directory |
| rust | `Cargo.toml` |
| go | `go.mod` |

## License

MIT
