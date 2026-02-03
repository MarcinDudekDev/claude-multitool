# helix-memory

Graph-vector memory system for Claude Code using HelixDB.

## Features

- **Semantic search**: Find memories by meaning, not just keywords
- **Auto-categorization**: AI-powered memory classification
- **Project tagging**: Automatic project detection from working directory
- **Graph relationships**: Link related memories together
- **Credential management**: Secure storage with special handling
- **Health monitoring**: Watchdog for auto-restart

## Requirements

- Docker (for HelixDB)
- Python 3.8+
- Ollama (optional, for local embeddings)
- Gemini API key (optional, for cloud embeddings)

## Installation

```bash
# 1. Add to PATH
ln -s /path/to/memory ~/.local/bin/memory

# 2. Copy config
cp .helix-memory.conf.example ~/.helix-memory.conf

# 3. Start HelixDB
memory start

# 4. Verify
memory status
```

## Quick Start

```bash
# Store a memory (auto-categorized)
memory store "User prefers Pico.css over Tailwind"

# Store with explicit category
memory store -t preference -i 10 "Always test before marking complete"

# Search memories
memory search "css framework"

# List recent memories
memory list --limit 10

# Show memory details
memory show <id>
```

## Commands

### Service Management
```bash
memory start        # Start HelixDB (auto-starts Docker)
memory stop         # Stop HelixDB
memory restart      # Restart HelixDB
memory status       # Check status and memory count
memory watchdog daemon  # Enable auto-restart on crash
```

### Memory Operations
```bash
memory store <content>     # Store with auto-categorization
memory search <query>      # Semantic search
memory list [--limit N]    # List memories
memory show <id>           # Show memory details
memory delete <id>         # Delete memory
memory recall <topic>      # Alias for search
```

### Curation
```bash
memory health              # Health report
memory garbage             # Find garbage memories
memory dedup               # Find duplicates
memory curate              # AI-powered curation
```

## Configuration

Create `~/.helix-memory.conf`:

```ini
[helix]
url = http://localhost:6969
data_dir = ~/helix-memory

[paths]
helix_bin = ~/.local/bin/helix
cache_dir = ~/.cache/helix-memory

[tools]
p_tool = ~/.local/bin/p
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HELIX_URL` | HelixDB connection URL |
| `GEMINI_API_KEY` | Google Gemini API key (for embeddings) |
| `OLLAMA_URL` | Local Ollama URL |
| `OLLAMA_REMOTE_URL` | Remote Ollama URL (optional) |

## Categories

| Category | Use | Typical Importance |
|----------|-----|-------------------|
| `preference` | Workflows, tool choices | 8-10 |
| `decision` | Technical choices made | 7-9 |
| `fact` | Setup, config, paths | 6-8 |
| `context` | Project background | 6-8 |
| `task` | TODOs, blockers | 5-8 |
| `solution` | Problems solved | 6-9 |

## Architecture

```
helix-memory/
├── memory              # CLI wrapper (bash)
├── hooks/
│   └── common.py       # Shared utilities (2.3K lines)
├── scripts/
│   ├── memory_helper.py  # Main helper (2K lines)
│   └── watchdog.py     # Auto-restart daemon
├── db/
│   ├── schema.hx       # HelixDB schema
│   └── queries.hx      # HelixDB queries
└── helix.toml          # HelixDB config
```

## License

MIT
