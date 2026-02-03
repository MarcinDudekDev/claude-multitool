# claude-multitool

Open-source Claude Code orchestration toolkit - multi-session management, persistent memory, and battle-tested workflows.

## Features

- **Multi-session orchestration** - Manage multiple Claude Code sessions in tmux
- **Inter-session messaging** - Send tasks and receive status updates between sessions
- **Persistent memory** - Graph-vector memory system with semantic search
- **Battle-tested workflows** - Production patterns extracted from real usage

## Architecture

Components are organized by dependency layer for flexible adoption:

```
Layer 0 (Standalone - no internal deps):
├── pane-status     → Session state detection
└── p               → Project picker

Layer 1 (Depends on Layer 0):
├── msg             → Inter-session messaging
└── inbox-daemon    → Background queue processor

Layer 2 (Depends on Layer 1):
└── op              → Session orchestrator

Memory System (Parallel track):
├── helix-memory    → Graph-vector memory
└── memorize        → Memory CLI wrapper
```

## Quick Start

```bash
# Install standalone tools only
./scripts/install-layer.sh 0

# Install messaging (includes layer 0)
./scripts/install-layer.sh 1

# Install full orchestration (includes layers 0-2)
./scripts/install.sh
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
│   ├── layer-0/          # Standalone tools
│   ├── layer-1/          # Messaging layer
│   ├── layer-2/          # Orchestration
│   └── memory/           # Memory system
├── skills/               # Claude Code skills
├── workflows/            # Higher-level patterns
├── examples/             # Usage examples
└── scripts/              # Installation scripts
```

## Documentation

- [Architecture](ARCHITECTURE.md) - Full dependency tree and data flow
- [Installation](docs/INSTALL.md) - Detailed setup instructions
- [Usage Guide](docs/USAGE.md) - Common patterns and examples

## License

MIT - See [LICENSE](LICENSE)

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.
