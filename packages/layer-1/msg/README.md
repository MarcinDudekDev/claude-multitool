# msg - Inter-Session Messaging

Send messages between Claude Code sessions via tmux with automatic queuing.

## Features

- Send messages to any tmux session running Claude
- Automatic queuing when target is busy/offline
- Message types: info, question, blocked, completed
- Raw prompt mode for delegation
- iTerm2 fallback for non-tmux sessions

## Requirements

- tmux
- pane-status (Layer 0)
- osascript (optional, for iTerm2 fallback)

## Installation

```bash
# Add to PATH
ln -s /path/to/msg ~/.local/bin/msg

# Set pane-status location (if not in standard path)
export PANE_STATUS=~/.local/bin/pane-status
```

## Usage

```bash
# Basic message
msg projectname "Your message here"

# Message types
msg projectname --question "Which approach: A or B?"
msg projectname --blocked "Waiting for API key"
msg projectname --completed "Task finished"

# Raw prompt mode (for delegation - no envelope)
msg projectname --prompt "Fix the bug in X"

# Force queue (don't try live delivery)
msg projectname --queue "Offline message"

# Force send even if window active
msg projectname --force "Urgent message"

# Start fresh session vs continue
msg projectname --new "Start fresh task"
msg projectname --continue "Follow-up on previous"
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--question` | `-q` | Mark as question (❓) |
| `--blocked` | `-b` | Mark as blocked (🚫) |
| `--completed` | `-c` | Mark as completed (✅) |
| `--prompt` | `-p` | Raw text mode (no envelope) |
| `--queue` | | Force queue instead of live send |
| `--force` | `-f` | Send even if window is active |
| `--new` | `-n` | Start fresh Claude session |
| `--continue` | | Continue existing session (default) |

## Message Format

Messages are formatted with an envelope:
```
📨 [source-project]: Your message here
```

In `--prompt` mode, text is sent raw without envelope.

## Queuing

Messages are queued in `~/.claude/inbox/<project>.jsonl` when:
- Target session doesn't exist
- Claude is not running in target
- Claude is busy (working)
- Real input text is in the prompt

Use `inbox-daemon` to auto-deliver queued messages.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PANE_STATUS` | Path to pane-status script |

## License

MIT
