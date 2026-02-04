# Basic Setup Example

Minimal configuration to get started with Claude Multitool.

## Quick Start

1. **Install the tools:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/MarcinDudekDev/claude-multitool/main/install.sh | bash
   ```

2. **Add environment variables (optional):**
   ```bash
   # Copy the example config
   cat .env.example >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Start your first session:**
   ```bash
   # Open a project
   op my-project

   # Or use the interactive picker
   p
   ```

## What You Get

After installation, you'll have these commands:

| Command | What it does |
|---------|--------------|
| `op` | Session orchestrator |
| `p` | Project picker |
| `msg` | Inter-session messaging |
| `memory` | Semantic memory search |
| `memorize` | Quick memory storage |

## Next Steps

- See [multi-session example](../multi-session/) for running parallel sessions
- See [memory-workflow example](../memory-workflow/) for using the memory system
