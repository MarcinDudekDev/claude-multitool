# time-tracking

Time tracking system for Claude Code sessions.

## Components

| File | Lines | Description |
|------|-------|-------------|
| `h` | 635 | Manual time tracking CLI |
| `time-report` | 10 | Report generator wrapper |
| `lib/time_report.py` | 735 | Automatic time extraction from transcripts |

## Features

### Automatic Time Extraction (`time-report`)
- Parses Claude Code JSONL transcripts
- Calculates session duration from timestamps
- Generates HTML and terminal reports
- Creates `h add` commands for manual tracking

### Manual Time Tracking (`h`)
- Interactive mode with fzf project selection
- Quick add: `h add <project> <hours> [note]`
- View: `h today`, `h week`, `h day`, `h project`
- Edit/delete entries
- Stores in `~/.claude/hours.json`

## Requirements

- Python 3.8+
- fzf (for interactive mode)

## Installation

```bash
ln -s /path/to/h ~/.local/bin/h
ln -s /path/to/time-report ~/.local/bin/time-report
```

## Usage

```bash
# Generate report from Claude transcripts
time-report              # Today
time-report 2024-01-15   # Specific date
time-report --html       # HTML format

# Manual time tracking
h                        # Interactive mode
h add myproject 2.5 "Fixed auth bug"
h today                  # Today's entries
h week                   # This week
h report                 # Summary report
```

## Data Storage

- Automatic: Reads from `~/.claude/projects/*/`
- Manual: Stores in `~/.claude/hours.json`
- Projects: Uses `~/.claude/projects.json` (shared with `p` tool)

## License

MIT
