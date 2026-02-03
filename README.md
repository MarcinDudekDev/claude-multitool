# claude-multitool

Open-source Claude Code orchestration toolkit - multi-session management, persistent memory, and battle-tested workflows.

## Features

- **Multi-session orchestration** - Manage multiple Claude Code sessions in tmux
- **Inter-session messaging** - Send tasks and receive status updates between sessions
- **Persistent memory** - Graph-vector memory system with semantic search
- **Battle-tested workflows** - Production patterns extracted from real usage
- **Utility tools** - Image optimization, design comparison, time tracking, and more

## What's Included

### Session Management (packages/)

| Layer | Tool | Description |
|-------|------|-------------|
| 0 | `pane-status` | Session state detection for Claude in tmux |
| 0 | `p` | Interactive project picker with fzf |
| 1 | `msg` | Inter-session messaging with auto-queuing |
| 1 | `inbox-daemon` | Background message queue processor |
| 2 | `op` | Full session orchestrator (iTerm2 + tmux) |

### Memory System (packages/memory/)

| Tool | Description |
|------|-------------|
| `helix-memory` | Graph-vector memory using HelixDB |
| `memorize` | Simple memory storage wrapper |

### Utilities (packages/utilities/)

| Tool | Description |
|------|-------------|
| `t` | Interactive tool selector with fzf |
| `mobile-claude` | Phone access to Claude sessions via web |
| `img-optimize` | Local TinyPNG alternative |
| `design-compare` | Visual comparison (mockup vs implementation) |
| `time-tracking` | Time tracking from Claude transcripts |

### Workflows (workflows/)

| Workflow | Description |
|----------|-------------|
| `batman` | RLM-inspired deep planning (batman/robin/alfred agents) |
| `gemini-analyzer` | Delegate large codebase analysis to Gemini CLI |

### Skills (skills/)

| Skill | Description |
|-------|-------------|
| `datastar` | Reactive hypermedia framework |
| `git-workflow` | Token-efficient git operations |
| `pair-code` | Multi-model code review |
| `stario` | Python web framework (Starlette + DataStar) |
| `safe-ssh` | Whitelisted SSH command wrappers |
| `ux-reviewer` | UX/accessibility review |

## Architecture

Components are organized by dependency layer:

```
Layer 0 (Standalone):
├── pane-status     → tmux only
└── p               → fzf only

Layer 1 (Requires Layer 0):
├── msg             → pane-status
└── inbox-daemon    → pane-status

Layer 2 (Requires Layer 1):
└── op              → p + msg

Memory (Independent):
├── helix-memory    → Docker + Python
└── memorize        → helix-memory
```

## Quick Start

```bash
# Clone
git clone https://github.com/youruser/claude-multitool.git
cd claude-multitool

# Install Layer 0 (standalone tools)
ln -s $PWD/packages/layer-0/pane-status/pane-status ~/.local/bin/
ln -s $PWD/packages/layer-0/p/p ~/.local/bin/

# Install Layer 1 (messaging)
ln -s $PWD/packages/layer-1/msg/msg ~/.local/bin/
ln -s $PWD/packages/layer-1/inbox-daemon/inbox-daemon ~/.local/bin/

# Install Layer 2 (orchestration)
ln -s $PWD/packages/layer-2/op/op ~/.local/bin/

# Install memory system
ln -s $PWD/packages/memory/helix-memory/memory ~/.local/bin/
ln -s $PWD/packages/memory/memorize/memorize ~/.local/bin/
```

## Requirements

- macOS (Linux support planned)
- tmux
- Python 3.8+
- fzf (for project picker)
- Docker (for memory system)

## Directory Structure

```
claude-multitool/
├── packages/
│   ├── layer-0/           # pane-status, p
│   ├── layer-1/           # msg, inbox-daemon
│   ├── layer-2/           # op
│   ├── memory/            # helix-memory, memorize
│   └── utilities/         # t, mobile-claude, img-optimize, etc.
├── skills/                # Claude Code skills
├── workflows/             # batman, gemini-analyzer
├── examples/              # Usage examples
└── scripts/               # Installation scripts
```

## License

MIT - See [LICENSE](LICENSE)

## Contributing

Contributions welcome! Please open an issue or PR.
