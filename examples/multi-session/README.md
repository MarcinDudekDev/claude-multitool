# Multi-Session Workflow Example

Run multiple Claude Code sessions working on different parts of your project.

## Scenario

You're building a full-stack app with:
- `api` - Backend API
- `frontend` - React/Vue frontend
- `docs` - Documentation

## Setup

```bash
# Start all three sessions
op api
op frontend
op docs

# Check their status
op --status
```

## Workflow

### 1. Start with the API

```bash
# Send a task to the API session
op api "Create user authentication endpoints with JWT"
```

### 2. Work on frontend while API builds

```bash
# Switch to frontend
op frontend "Set up the login page component"
```

### 3. Notify when ready

```bash
# From API session, message frontend when auth is done
msg frontend "Auth endpoints ready: POST /auth/login, POST /auth/register"
```

### 4. Check on sessions

```bash
op --status
# ┌───────────┬──────────┬─────────────────────────┐
# │ Session   │ Status   │ Task                    │
# ├───────────┼──────────┼─────────────────────────┤
# │ api       │ ✓ idle   │ -                       │
# │ frontend  │ ⚡ working│ Integrating auth        │
# │ docs      │ ✓ idle   │ -                       │
# └───────────┴──────────┴─────────────────────────┘
```

### 5. Handle blocked sessions

```bash
# If a session needs user input
op -a frontend  # Opens the window so you can respond
```

## Message Queue

Messages are queued if the recipient is busy:

```bash
# Send while frontend is working
msg frontend "Also add forgot password flow"

# Check queue
inbox-daemon queue
# → 1 message queued for frontend

# Message auto-delivers when frontend becomes idle
```

## Tips

- **Keep sessions focused** - One domain per session
- **Use messages for coordination** - Don't context-switch yourself
- **Check status regularly** - `op --status` is your dashboard
- **Let the queue work** - Messages deliver automatically when sessions are ready
