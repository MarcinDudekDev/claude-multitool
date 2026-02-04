# Claude Multitool

**Run multiple Claude Code sessions like a team of AI developers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/macOS-supported-brightgreen.svg)]()
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet.svg)]()

---

## The Problem

You're deep in a coding session with Claude Code. You need to:
- Check something in another project without losing context
- Run a long task in the background while continuing work
- Remember that solution you found last week
- Have Claude review code while you keep building

**Claude Code is powerful, but it runs one session at a time.**

## The Solution

Claude Multitool turns Claude Code into a **team of AI agents** that can:

- **Work in parallel** across multiple projects in tmux
- **Message each other** to delegate tasks and share results
- **Remember everything** with semantic search across sessions
- **Self-organize** with battle-tested planning workflows

---

## Quick Demo

```bash
# See all your Claude sessions at a glance
op --status
# ┌─────────────┬──────────┬─────────────────────┐
# │ Session     │ Status   │ Task                │
# ├─────────────┼──────────┼─────────────────────┤
# │ api-server  │ ✓ idle   │ -                   │
# │ frontend    │ ⚡ working│ Implementing auth   │
# │ docs        │ ⏸ perms  │ Waiting for input   │
# └─────────────┴──────────┴─────────────────────┘

# Send a task to another session
op api-server "Add rate limiting to the /users endpoint"

# Message between sessions (auto-queues if busy)
msg frontend "Auth is ready, you can integrate now"

# Search your memory across all sessions
memory search "how did we handle pagination"
```

<!--
TODO: Add GIF demos
![Session orchestration demo](docs/images/op-demo.gif)
-->

---

## Installation

### One-liner (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/MarcinDudekDev/claude-multitool/main/install.sh | bash
```

### Manual Installation

```bash
# Clone the repo
git clone https://github.com/MarcinDudekDev/claude-multitool.git
cd claude-multitool

# Run the installer
./scripts/install.sh

# Or install specific components
./scripts/install.sh --layer 0      # Just the basics
./scripts/install.sh --memory       # Add memory system
./scripts/install.sh --all          # Everything
```

### Requirements

| Requirement | Why |
|-------------|-----|
| macOS | Primary platform (Linux planned) |
| tmux | Session management |
| Python 3.8+ | Core tools |
| fzf | Interactive selection |
| Docker | Memory system (optional) |

---

## What's Inside

### Session Orchestration

| Tool | What it does | Example |
|------|--------------|---------|
| **`op`** | Full session orchestrator | `op myproject "build the API"` |
| **`p`** | Quick project picker | `p` → fuzzy search → open |
| **`msg`** | Inter-session messaging | `msg backend "ready for review"` |
| **`pane-status`** | Detect session state | Returns `idle`, `working`, `perms` |
| **`inbox-daemon`** | Background message queue | Auto-delivers when idle |

### Memory System

| Tool | What it does | Example |
|------|--------------|---------|
| **`memory`** | Graph-vector memory with semantic search | `memory search "auth pattern"` |
| **`memorize`** | Quick memory storage | `memorize "use JWT for auth"` |

> **How it works:** Memories are stored in HelixDB with embeddings for semantic search. Find solutions by meaning, not just keywords.

### Utilities

| Tool | What it does |
|------|--------------|
| **`t`** | Interactive tool selector (like a command palette) |
| **`img-optimize`** | Local TinyPNG alternative (no API needed) |
| **`design-compare`** | Compare mockup vs implementation |
| **`mobile-claude`** | Access sessions from your phone |
| **`time-tracking`** | Extract time spent from transcripts |

### Workflows

| Workflow | What it does |
|----------|--------------|
| **`batman`** | RLM-inspired deep planning: reconnaissance → plan → execute |
| **`gemini-analyzer`** | Delegate large codebase analysis to Gemini CLI |

### Skills (Claude Code Extensions)

Drop these into `~/.claude/skills/` for instant Claude Code superpowers:

| Skill | What it does |
|-------|--------------|
| **`datastar`** | Build reactive hypermedia UIs |
| **`git-workflow`** | Token-efficient git operations |
| **`pair-code`** | Multi-model code review |
| **`stario`** | Python web framework (Starlette + DataStar) |
| **`safe-ssh`** | Whitelisted SSH wrappers |
| **`ux-reviewer`** | UX/accessibility audits |

---

## Usage Examples

### Orchestrate Multiple Projects

```bash
# Start a new session for a project
op my-api

# Check what all sessions are doing
op --status

# Send a task to a specific session
op my-api "refactor the user service to use dependency injection"

# Open window for a session that needs attention
op -a frontend
```

### Memory That Persists

```bash
# Store something important
memorize "Production DB is on port 5433, not 5432" --importance 9

# Find it later with semantic search
memory search "database port"
# → Returns the memory even if you search "postgres connection"

# Tag memories for organization
memorize "Use Pico.css for simple projects" --tags "css,preferences"
```

### Inter-Session Communication

```bash
# Send a message (queues automatically if recipient is busy)
msg backend "API changes ready for integration"

# Check message queue
inbox-daemon queue

# Messages delivered automatically when session becomes idle
```

### Batman Workflow (Deep Planning)

For complex tasks, use the batman workflow to prevent "context rot":

```
/batman Implement user authentication with OAuth2
```

This triggers:
1. **Batman** (Planner): Deep reconnaissance, creates detailed plan
2. **Robin** (Executor): Implements each step
3. **Alfred** (QA): Verifies everything works

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         op (orchestrator)                    │
│                    Full session management                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │   msg   │     │    p    │     │ memory  │
    │messaging│     │ picker  │     │ system  │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │  pane   │     │   fzf   │     │ HelixDB │
    │ status  │     │         │     │ Docker  │
    └─────────┘     └─────────┘     └─────────┘

Layer 2 ──────────────────────────────────────────
Layer 1 ──────────────────────────────────────────
Layer 0 ──────────────────────────────────────────
```

**Dependency Layers:**
- **Layer 0**: Standalone tools (no dependencies)
- **Layer 1**: Requires Layer 0
- **Layer 2**: Full orchestration

---

## Configuration

All tools use environment variables with sensible defaults:

```bash
# Session management
export CLAUDE_PROJECTS_DIR="$HOME/Projects"
export TMUX_SESSION_PREFIX="claude-"

# Memory system
export HELIX_MEMORY_DIR="$HOME/.helix-memory"
export OLLAMA_REMOTE_URL=""  # Optional: remote embedding server

# Tools auto-detection
export PANE_STATUS=""  # Auto-detected from common paths
export MSG_TOOL=""     # Auto-detected
```

---

## Roadmap

- [ ] Linux support
- [ ] Web dashboard for session monitoring
- [ ] VSCode extension
- [ ] Memory sync across machines
- [ ] Custom workflow builder

---

## Contributing

Contributions welcome! This toolkit grew from real daily usage patterns.

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Run tests: `./scripts/test.sh`
5. Submit a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

MIT - See [LICENSE](LICENSE)

---

## Credits

Built by developers who run 5+ Claude Code sessions daily and needed better tooling.

**Star this repo** if you find it useful!
