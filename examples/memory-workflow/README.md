# Memory Workflow Example

Use the memory system to persist knowledge across sessions and projects.

## Why Memory?

Without memory:
- "How did we handle auth last month?" → Search through old chats
- "What was that pagination pattern?" → Re-invent it
- "What's the DB password?" → Ask someone

With memory:
- Semantic search finds answers instantly
- Solutions persist across sessions
- Team knowledge compounds over time

## Basic Usage

### Store Important Information

```bash
# Store a solution you just figured out
memorize "Use cursor-based pagination for large datasets, not offset" --importance 8

# Store project-specific info
memorize "Production DB is on port 5433, staging is 5432" --importance 9 --tags "db,production"

# Store a preference
memorize "Always use Pico.css for simple projects" --tags "css,preferences"
```

### Search Your Memory

```bash
# Find by meaning, not just keywords
memory search "how to paginate"
# → Returns cursor pagination memory

memory search "database connection"
# → Returns DB port memory

# Filter by tags
memory search "css" --tag preferences
```

## Advanced Usage

### Importance Levels

| Level | Use for |
|-------|---------|
| 1-3 | Nice to know |
| 4-6 | Useful context |
| 7-8 | Important decisions |
| 9-10 | Critical info (credentials, breaking changes) |

```bash
# Critical info
memorize "NEVER delete users table directly, use soft delete" --importance 10

# Just useful
memorize "The client prefers blue buttons" --importance 4
```

### Tags for Organization

```bash
# Multiple tags
memorize "JWT tokens expire in 24h for web, 30d for mobile" \
  --tags "auth,jwt,mobile,web"

# Search by tag
memory search --tag auth
```

### Memory in Claude Sessions

In your Claude Code session:
```
# Claude can search memories
recall auth patterns

# Claude can store learnings
memorize "This project uses repository pattern for data access"
```

## Workflow Examples

### Code Review Memory

```bash
# After a code review
memorize "In this codebase, always add error boundaries around async components" \
  --tags "react,error-handling" --importance 7
```

### Debugging Memory

```bash
# After solving a tricky bug
memorize "CORS errors with credentials: add withCredentials: true to axios AND Access-Control-Allow-Credentials header" \
  --tags "cors,debugging,axios" --importance 8
```

### Architecture Decisions

```bash
# After making a decision
memorize "Chose PostgreSQL over MongoDB for this project: need ACID transactions for payments" \
  --tags "architecture,database,decisions" --importance 8
```

## Tips

- **Store solutions, not problems** - "Use X" not "Had issue with Y"
- **Be specific** - Include the "why" not just the "what"
- **Tag consistently** - Use lowercase, plural forms
- **High importance sparingly** - Reserve 9-10 for truly critical info
- **Search before asking** - `memory search` before researching again
