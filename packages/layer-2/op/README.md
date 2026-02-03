# op - Session Orchestrator

Open projects and send tasks to Claude sessions with intelligent delivery.

## Features

- Open project windows with iTerm2 + tmux
- Send prompts to running sessions
- Automatic status detection (idle/working/blocked)
- Session restart with proper cleanup
- Date-based project discovery
- Auto report-back instructions

## Requirements

- Python 3.8+
- tmux
- iTerm2 (macOS)
- p (Layer 0) - project picker
- msg (Layer 1) - messaging

## Installation

```bash
# Add to PATH
ln -s /path/to/op ~/.local/bin/op

# Optional: set tool locations if not in standard paths
export P_TOOL=~/.local/bin/p
export MSG_TOOL=~/.local/bin/msg
```

## Common Operations

```bash
# Open project window
op myproject

# Open and send task (auto-detects text vs file)
op myproject "Fix the bug in auth.py"
op myproject ~/prompts/task.md

# Check all session statuses
op --status

# Restart Claude in a project
op --restart myproject
```

## Opening Projects

```bash
op project1 project2       # Open multiple
op --yesterday             # Projects from yesterday
op --recent 5              # 5 most recent projects
op --default               # Saved default set
op                         # Same as --default
```

## Sending Prompts

```bash
op --prompt project "text"       # Send prompt text
op --prompt-file project file.md # Send from file
op -c project "follow-up"        # Continue context (no /clear)
```

## Managing Sessions

```bash
op --status              # Show all project statuses
op --status --quick      # Skip stability check (faster)
op --restart project     # Restart Claude
op --restart-all         # Restart all idle sessions
op -a project            # Attach to existing tmux session
```

## Session States

| State | Icon | Description |
|-------|------|-------------|
| idle | ✓ | Ready for input |
| working | ⚡ | Processing (spinner visible) |
| question | ? | Asking user a question |
| blocked:permission | ⏸ | Waiting for permission |
| shell | ○ | Claude not running |

## Context Management

By default, sending a new task to a running session uses `/clear` first for fresh context. Use `-c/--continue` for follow-ups:

```bash
op project "New task"      # Fresh context (/clear first)
op -c project "Continue"   # Keep existing context
```

## Advanced Options

```bash
op --attach project        # Reopen iTerm for existing tmux
op -a project              # Short form
op --no-tmux project       # Plain iTerm (no tmux)
op --mobile project        # Also start mobile server
op --save-default p1 p2    # Save as default set
op --dry-run project       # Preview without opening
op --no-report project     # Skip auto report-back
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `P_TOOL` | Path to p (project picker) |
| `MSG_TOOL` | Path to msg (messaging) |
| `PROJECTS_REGISTRY` | Path to projects.json |
| `OP_CONFIG_DIR` | Config directory |
| `TILE_APP` | Window tiling app |
| `MOBILE_CLAUDE_DIR` | Mobile server directory |

## License

MIT
