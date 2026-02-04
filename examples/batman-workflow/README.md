# Batman Workflow Example

Deep planning workflow for complex tasks. Prevents "context rot" by doing thorough reconnaissance before coding.

## When to Use Batman

**Good fit:**
- Implementing features that touch 3+ files
- Refactoring with unclear scope
- Tasks where you've gotten stuck before
- Complex integrations

**Overkill for:**
- Single file changes
- Bug fixes with known location
- Adding a simple endpoint

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  /batman "Implement user authentication with OAuth2"        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  BATMAN (Planner)                                           │
│  - Reads existing code structure                            │
│  - Identifies all files that need changes                   │
│  - Creates detailed PREP.md with step-by-step plan          │
│  - Lists dependencies and potential blockers                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  ROBIN (Executor)                                           │
│  - Follows PREP.md step by step                             │
│  - Implements each task                                     │
│  - Updates progress                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  ALFRED (QA)                                                │
│  - Verifies implementation matches plan                     │
│  - Runs tests                                               │
│  - Reports any issues                                       │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### Basic

```
/batman Implement user authentication with OAuth2
```

### With Context

```
/batman Refactor the payment service to use the new Stripe API
```

### Check Progress

The workflow creates files in `.batman/`:
- `PREP.md` - The detailed plan
- `task_queue.json` - Task status
- `prompts/` - Individual task prompts

## Example Output

### PREP.md

```markdown
# OAuth2 Authentication Implementation

## Reconnaissance Summary
- Current auth: session-based in `/src/auth/`
- User model: `/src/models/user.py`
- Routes: `/src/routes/auth.py`

## Implementation Plan

### Phase 1: Dependencies
- [ ] Add `authlib` to requirements.txt
- [ ] Add OAuth provider configs to `.env`

### Phase 2: Backend
- [ ] Create `/src/auth/oauth.py` - OAuth flow handlers
- [ ] Update `/src/models/user.py` - Add OAuth fields
- [ ] Update `/src/routes/auth.py` - Add OAuth endpoints

### Phase 3: Frontend
- [ ] Add OAuth buttons to login page
- [ ] Handle OAuth callback

### Phase 4: Testing
- [ ] Unit tests for OAuth handlers
- [ ] Integration test for full flow

## Risks
- Existing sessions may conflict with OAuth tokens
- Need to handle account linking for existing users
```

## Tips

- **Read the plan before approving** - Batman shows you PREP.md first
- **Adjust scope early** - Easier to remove tasks from plan than code
- **Trust the process** - Robin follows the plan, Alfred verifies
- **Use for learning** - The plan teaches you the codebase structure
