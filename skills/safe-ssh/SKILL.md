---
name: safe-ssh
description: Whitelisted SSH command wrappers for safe remote server operations. Each wrapper executes ONE specific command - no arbitrary SSH access.
domain: ssh
type: cli-tool
frequency: daily
commands:
  - ssh-ls
  - ssh-cat
  - ssh-tail
  - ssh-status
  - ssh-df
  - ssh-ps
  - ssh-docker-ps
  - ssh-grep
  - ssh-wp
tools:
  - ~/Tools/ssh-ls
  - ~/Tools/ssh-cat
  - ~/Tools/ssh-tail
  - ~/Tools/ssh-status
  - ~/Tools/ssh-df
  - ~/Tools/ssh-ps
  - ~/Tools/ssh-docker-ps
  - ~/Tools/ssh-grep
  - ~/Tools/ssh-wp
---

# Safe SSH Wrappers

Single-purpose SSH command wrappers that are whitelisted for Claude Code agents. Each script executes exactly ONE remote command - preventing arbitrary SSH access while enabling useful remote operations.

## Why This Exists

Instead of whitelisting `Bash('ssh server *')` (dangerous), each wrapper is whitelisted individually:
```
Bash(~/Tools/ssh-ls:*)
Bash(~/Tools/ssh-cat:*)
...
```

The wrapper IS the whitelist. Agent cannot run `rm -rf` because there's no `ssh-rm` tool.

## Architecture

Scripts live in skill directory, symlinked to ~/Tools/:
```
~/.claude/skills/safe-ssh/scripts/ssh-*  (actual scripts)
~/Tools/ssh-*                             (symlinks)
```

## Available Commands

All commands support additional flags passed through to the remote command.

| Command | Usage | Description |
|---------|-------|-------------|
| `ssh-ls` | `ssh-ls <host> [args...]` | List directory contents |
| `ssh-cat` | `ssh-cat <host> <file> [args...]` | Read file contents |
| `ssh-tail` | `ssh-tail <host> <file> [args...]` | Tail file (default 100 lines) |
| `ssh-grep` | `ssh-grep <host> <pattern> [path] [args...]` | Search files recursively |
| `ssh-status` | `ssh-status <host> <service> [args...]` | Check systemctl service status |
| `ssh-df` | `ssh-df <host> [args...]` | Check disk space (default -h) |
| `ssh-ps` | `ssh-ps <host> [pattern]` | List processes (optional grep) |
| `ssh-docker-ps` | `ssh-docker-ps <host> [args...]` | List Docker containers (default -a) |
| `ssh-wp` | `ssh-wp <host> <dir> <wp-cmd...>` | Run WP-CLI from specific directory |

## Examples

### Basic Operations
```bash
# List web directory with details
ssh-ls anna152 -la /var/www

# Read nginx config with line numbers
ssh-cat anna152 /etc/nginx/nginx.conf -n

# Tail error log (last 50 lines)
ssh-tail anna152 /var/log/nginx/error.log -50

# Follow log in real-time
ssh-tail anna152 /var/log/nginx/error.log -f

# Search for error (case insensitive, with line numbers)
ssh-grep anna152 "error" /var/log/nginx/ -i -n

# Check nginx status without pager
ssh-status anna152 nginx --no-pager

# Check disk space with filesystem type
ssh-df anna152 -T

# Find node processes
ssh-ps anna152 node

# List running containers only
ssh-docker-ps anna152
```

### WordPress CLI
```bash
# List plugins
ssh-wp anna152 /var/www/wpmultitool.com plugin list

# Get site URL
ssh-wp anna152 /var/www/wpmultitool.com option get siteurl

# List users
ssh-wp anna152 /var/www/wpmultitool.com user list --format=table

# Flush cache
ssh-wp anna152 /var/www/wpmultitool.com cache flush

# Run database query
ssh-wp anna152 /var/www/wpmultitool.com db query "SELECT * FROM wp_options LIMIT 5"

# Export database
ssh-wp anna152 /var/www/wpmultitool.com db export --add-drop-table
```

## Known SSH Hosts

Use aliases from `~/.ssh/config`:
- `anna152` - Playground VPS
- Others as configured

## Adding New Wrappers

1. Create script in `~/.claude/skills/safe-ssh/scripts/ssh-<command>`
2. Make executable: `chmod +x`
3. Symlink: `ln -s ~/.claude/skills/safe-ssh/scripts/ssh-<command> ~/Tools/`
4. Add to whitelist: `Bash(~/Tools/ssh-<command>:*)`
5. Update this SKILL.md (commands + tools frontmatter)

Template:
```bash
#!/bin/bash
# SSH <command> wrapper - <description>
# Usage: ssh-<command> <host> [args...]
# Examples:
#   ssh-<command> anna152 arg1 arg2

[[ -z "$1" ]] && { echo "Usage: ssh-<command> <host> [args...]"; exit 1; }

host="$1"
shift
ssh "$host" "<command> $*"
```

## Security Model

- **Server-side**: No restrictions needed (optional extra layer)
- **Client-side**: Each wrapper whitelisted individually
- **Agent access**: Can only run commands with existing wrappers
- **Extensible**: Add new wrappers as needed
