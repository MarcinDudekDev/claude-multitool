# inbox-daemon - Message Queue Processor

Background daemon that auto-delivers queued messages when Claude sessions become idle.

## Features

- Polls every 3 seconds for queued messages
- Delivers only when target is idle (not working)
- Handles message ordering and delays
- Auto-starts Claude if needed
- Atomic file locking to prevent race conditions

## Requirements

- tmux
- Python 3
- pane-status (Layer 0)

## Installation

```bash
# Add to PATH
ln -s /path/to/inbox-daemon ~/.local/bin/inbox-daemon

# Set pane-status location (if not in standard path)
export PANE_STATUS=~/.local/bin/pane-status
```

## Usage

```bash
# Start daemon
inbox-daemon start

# Stop daemon
inbox-daemon stop

# Check status + queued messages
inbox-daemon status

# Show only queued messages
inbox-daemon queue
inbox-daemon q  # alias
```

## How It Works

1. Messages sent via `msg` are queued in `~/.claude/inbox/<project>.jsonl`
2. Daemon polls every 3s, checks each target session
3. Only delivers when target shows idle status (not working, no input)
4. 5s minimum delay between messages to same project
5. After delivery, waits for Claude to return to idle

## Message Flow

```
msg projectname "task"
    ↓ (target busy)
~/.claude/inbox/projectname.jsonl
    ↓ (daemon polls)
inbox-daemon detects idle
    ↓ (delivers)
Claude receives message
```

## Files

| Path | Description |
|------|-------------|
| `~/.claude/inbox/*.jsonl` | Queued messages |
| `~/.claude/inbox/*.read.jsonl` | Delivered (archived) |
| `~/.claude/inbox-daemon.pid` | Daemon PID file |
| `~/.claude/inbox-daemon.log` | Delivery log |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PANE_STATUS` | Path to pane-status script |

## License

MIT
