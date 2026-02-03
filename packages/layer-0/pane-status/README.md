# pane-status

Session state detection for Claude Code in tmux.

## Features

- Detect if Claude TUI is running in a pane
- Check if Claude is actively working (spinner visible)
- Detect real user input vs placeholder text
- Check if pane is safe to send messages to

## Requirements

- tmux

## Installation

```bash
# Add to PATH or symlink
ln -s /path/to/pane-status ~/.local/bin/pane-status
```

## Usage

### As a Command

```bash
# Human-readable output
pane-status myproject

# JSON output for scripts
pane-status myproject --json
```

Example output:
```
Session: myproject
  Claude running: true
  Claude working: false
  Has input text: false
  Pane active:    true
  Safe to send:   true
```

### As a Library

```bash
source /path/to/pane-status

# Check if Claude is running
if is_claude_running "myproject"; then
    echo "Claude is active"
fi

# Check if safe to send messages
if is_pane_safe_to_send "myproject"; then
    tmux send-keys -t myproject "Hello" Enter
fi

# Ensure Claude is started, auto-start if needed
if ensure_claude_started "myproject" "continue"; then
    echo "Claude ready"
fi
```

## Functions

| Function | Description |
|----------|-------------|
| `is_claude_running` | Check if Claude TUI shows ❯ prompt |
| `is_claude_working` | Check for spinner or action in progress |
| `has_input_text` | Detect real input (not placeholder) |
| `is_pane_active` | Check if pane is focused |
| `is_pane_safe_to_send` | Combined check: running, not working, no input |
| `ensure_claude_started` | Auto-start Claude if not running |
| `get_pane_content` | Capture pane content (last N lines) |

## How It Works

The script uses tmux's `capture-pane` to analyze terminal content:

1. **Running detection**: Looks for the ❯ prompt character
2. **Working detection**: Scans for spinner characters (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏) or ✱ with ...
3. **Input detection**: Uses ANSI escape code analysis to distinguish real input from dim placeholder text

## License

MIT
