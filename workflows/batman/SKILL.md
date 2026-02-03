---
name: batman
aliases: [zen, focus, prepare, bat]
description: RLM-inspired deep preparation mode. Forces thorough reconnaissance before action with hard blocking. Prevents context rot through file-based state management.
domain: workflow
type: system
frequency: daily
commands: []
---

# /batman - Deep Preparation Mode

> **STOP - DO NOT USE THIS SKILL MANUALLY**
>
> This skill is documentation for the **@agent-batman** subagent.
>
> **Correct usage:**
> ```
> Task(
>   subagent_type="batman",
>   prompt="<your task here>"
> )
> ```
>
> The agent runs in background, handles all phases internally, and returns a clean summary.
> Reading this file directly pollutes your context. Spawn the agent instead.

---

## Agent Ecosystem

Batman is an **ORCHESTRATOR**, not a worker. It delegates all actual work to subagents.

```
                    batman (orchestrator)
                         │
         ┌───────────────┼───────────────┐
         │               │               │
      robin           robin           alfred
   (code gen)       (commands)        (QA)
```

### Tool Restrictions

| Agent | Allowed Tools | Purpose |
|-------|---------------|---------|
| batman | Read, Glob, Grep, Write, Task | Orchestration ONLY |
| robin | Read, Glob, Grep, Write, Edit, Bash | Execute subtasks |
| alfred | Read, Glob, Grep, Bash | QA verification |

**Batman CANNOT use**: Bash, Edit, WebFetch, dev-browser

This is enforced by the `tools` frontmatter in the agent definition.

### Why Delegation?

1. **Context isolation** - Each subagent has clean context
2. **Cost efficiency** - Use haiku for simple tasks, sonnet for code
3. **Accountability** - Track which subagent did what in progress.json
4. **Parallelization** - Independent subtasks can run concurrently

---

## Agent Reference (for @agent-batman internal use)

**"I orchestrate. I do not execute."**

## How It Works

The batman agent handles everything internally:
- Recon → Plan → **Spawn robin** → Apply outputs → **Alfred verification** → Return summary

Main context sees only task + result. All meta-work stays in the agent's isolated context.

**CRITICAL**: Batman spawns subagents for ALL work. If batman uses Bash or Edit directly, the run has FAILED.

## Subagents

### robin - Code Generation
```python
Task(
    subagent_type="robin",
    prompt="Read .batman/prompts/1.md and execute"
)
```
Robin reads the prompt file, executes, writes to `.batman/outputs/`.

### alfred - QA Verification

Batman automatically spawns **@agent-alfred** after applying changes. Alfred:
- Reads requirements from `.batman/PREP.md`
- Runs actual tests (not just --help)
- Tests edge cases from requirements
- Reports PASS/FAIL with specific issues

This catches bugs like wrong paths, missing imports, or logic errors that "look correct" but don't work.

## Manual Mode (Legacy - NOT RECOMMENDED)

Batman mode forces thorough preparation before action, inspired by Recursive Language Models (RLM) research that shows context rot degrades performance. Instead of stuffing everything into context, we store state externally and interact programmatically.

## Why This Exists

1. **Context rot is real** - Performance degrades as conversation fills with errors, retries, verbose outputs
2. **Instructions get ignored** - I can read "prepare first" and still act impulsively
3. **Soft reminders don't work** - Only hard blocks prevent bypass
4. **Checkpointing beats context** - Files persist, conversation context degrades

## Core Principles (RLM-Inspired)

```
PRINCIPLE 1: Context is external
  - State lives in .batman/ files, not conversation
  - Re-read files to re-anchor, don't trust "memory"

PRINCIPLE 2: Minimal parent context
  - I orchestrate, subagents work
  - Each interaction: read state → decide → dispatch → write state

PRINCIPLE 3: Hard blocking
  - Hook PREVENTS action, not just reminds
  - Can't bypass through cleverness

PRINCIPLE 4: Progressive disclosure
  - Peek/grep before full read
  - Load only what's needed for current step
```

## State Directory Structure

```
.batman/
├── status.json          # Current phase, can-proceed flags
├── PREP.md              # Full preparation document (human-readable)
├── context.json         # Project context (subagents read this)
├── progress.json        # Completed subtasks, outputs
├── handoff.md           # Auto-generated on interrupt
├── apply.json           # Maps outputs → target files
├── prompts/             # One prompt file per subtask
│   ├── 1_task.md
│   ├── 2_task.md
│   └── ...
└── outputs/             # Subagents write here (sandbox)
    ├── 1_task.txt       # Contains complete file content
    ├── 2_task.txt
    └── ...
```

## RLM Principle: Subagents Work in Sandbox

1. **Prompts in files** - Each subtask has `.batman/prompts/N_task.md`
2. **Explicit permissions in prompt** - Each prompt states: "Read: ANY | Write: ONLY .batman/outputs/N.txt"
3. **Subagents write to sandbox** - Output is complete file content, not diffs
4. **Apply step copies to real files** - After validation, copy outputs to targets
5. **Hook enforces sandbox** - Blocks writes outside .batman/ when lock active

## Prompt File Template

```markdown
# .batman/prompts/N_task.md

## Permissions
Read: ANY file
Write: ONLY .batman/outputs/N_task.txt

## Context
Read: .batman/context.json

## Previous Outputs
Read: .batman/outputs/M_previous.txt (or "none")

## Task
[What to do]

## Instructions
1. Read [source file]
2. [Specific changes]
3. Write COMPLETE modified file to output

## Output
Write to: .batman/outputs/N_task.txt
Target: [real file path - for apply step]
```

## status.json Schema

```json
{
  "phase": "recon|approval|execution|complete|aborted",
  "started_at": "2025-01-07T12:00:00Z",
  "task": "Original task description",
  "flags": {
    "prep_complete": false,
    "user_approved": false,
    "lock_active": false
  },
  "current_subtask": null,
  "completed_subtasks": [],
  "failed_subtasks": []
}
```

## Workflow

### Phase 1: RECON (Read-Only)

```
/batman <task description>
         │
         ▼
┌─────────────────────────────────────────┐
│ 1. Create .batman/ directory            │
│ 2. Write status.json (phase: recon)     │
│ 3. Enter Plan Mode (built-in read-only) │
│ 4. Recall relevant memories             │
│ 5. Explore codebase (Glob/Grep/Read)    │
│ 6. Identify ALL files to read/write     │
│ 7. List ALL tools needed                │
│ 8. Write PREP.md                        │
│ 9. Write task_queue.json                │
│ 10. Write context.json                  │
│ 11. Update status.json (prep_complete)  │
└─────────────────────────────────────────┘
```

### PREP.md Template

```markdown
# Batman Preparation: [Task Name]

## Mission
[1-2 sentence goal]

## Reconnaissance Summary
- Relevant memories recalled: [count]
- Files explored: [count]
- Key findings: [bullets]

## Files Inventory

### To Read (before any action)
| File | Purpose | Priority |
|------|---------|----------|
| src/auth.ts | Understand existing auth | P0 |
| ... | ... | ... |

### To Write/Modify
| File | Action | Risk |
|------|--------|------|
| src/middleware/jwt.ts | Create | Low |
| src/routes/*.ts | Modify (add auth) | Medium |
| ... | ... | ... |

## Tools Required
- [ ] Bash: npm install jsonwebtoken
- [ ] Edit: Multiple route files
- [ ] Task: Spawn subagents

## Permissions Needed
- [ ] Write to src/middleware/
- [ ] Edit src/routes/*.ts (5 files)
- [ ] Bash: npm install

## Questions Resolved
- Q: Where is auth configured? A: .env + src/config/auth.ts
- Q: Existing middleware pattern? A: src/middleware/logger.ts

## Risk Assessment
- **High risk**: Modifying all route files
- **Mitigation**: Create backup, test each route

## Subtask Preview
[Summary of task_queue.json - see full file for details]
```

### Phase 2: APPROVAL (Conversation)

```
After PREP.md is written:
         │
         ▼
┌─────────────────────────────────────────┐
│ Show: PREP.md summary to user           │
│ Show: Subtask table + cost estimate     │
│ Ask: "Proceed? (add notes if needed)"   │
│                                         │
│ User response:                          │
│ • "go" → Phase 3                        │
│ • "go, but X" → Update context, Phase 3 │
│ • "wait, what about X" → Answer, re-ask │
│ • "abort" → Clean up                    │
└─────────────────────────────────────────┘
         │
         ▼
Update status.json: user_approved = true
```

### Phase 3: EXECUTION (Sandbox)

```
On approval:
         │
         ▼
┌─────────────────────────────────────────┐
│ 1. Exit Plan Mode                       │
│ 2. Generate .batman/prompts/*.md        │
│ 3. Generate .batman/apply.json          │
│ 4. Set status.json: lock_active = true  │
│ 5. Hook BLOCKS writes outside .batman/  │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ For each subtask:                       │
│   a. Spawn: "Read .batman/prompts/N.md  │
│      and execute"                       │
│   b. Subagent reads prompt file         │
│   c. Subagent reads context.json        │
│   d. Subagent reads previous outputs    │
│   e. Subagent writes .batman/outputs/N  │
│   f. Update progress.json               │
│                                         │
│ Subagents: Read ANY, Write ONLY sandbox │
│ Parent: Orchestrate ONLY, never work    │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ APPLY STEP (after all subtasks):        │
│   a. Review .batman/outputs/*           │
│   b. For each in apply.json:            │
│      Copy output → target file          │
│   c. Run tests                          │
└─────────────────────────────────────────┘
```

### apply.json Format

```json
{
  "mappings": [
    {
      "output": ".batman/outputs/1_add_flag.txt",
      "target": "~/dev-browser/skills/dev-browser/dev-browser.sh"
    },
    {
      "output": ".batman/outputs/2_update_goto.txt",
      "target": "~/dev-browser/skills/dev-browser/scripts/goto.ts"
    }
  ]
}
```

### Phase 4: COMPLETION / INTERRUPT

```
On completion:
├── Update status.json: phase = complete
├── Remove lock_active flag
├── Memorize key learnings
└── Report summary to user

On interrupt (/clear, session end, abort):
├── Generate handoff.md from current state
├── Remove lock_active flag
└── Next session can: /batman resume
```

## Commands

```
/batman <task>        # Start new batman session
/batman status        # Show current phase, progress
/batman pause         # Suspend lock for manual intervention
/batman resume        # Resume from .batman/ state (same or new session)
/batman abort         # Clean abort, save handoff, remove lock
```

## Hook Enforcement

The `batman_enforcer.py` hook runs on PreToolUse:

```python
BLOCKED when lock_active AND tool in [Write, Edit, Bash(write commands)]:
  → Return error: "Batman lock active. Use subagents or /batman pause"

BLOCKED when phase == "recon" AND tool == "ExitPlanMode":
  → Check: prep_complete == true?
  → Check: PREP.md exists?
  → Check: task_queue.json exists?
  → If any missing: "Complete preparation before exiting plan mode"

ALLOWED:
  → Read, Glob, Grep (always)
  → Task() spawning (always)
  → Write to .batman/ directory (state management)
```

## Re-Anchoring Protocol

**After EVERY subtask or when confused:**

```
1. Read .batman/status.json
   → What phase am I in?
   → What's the current subtask?

2. Read .batman/progress.json
   → What's already done?
   → What failed?

3. Read .batman/PREP.md (if needed)
   → What was the original mission?
   → What files am I touching?

4. Then proceed with next action
```

This prevents context drift by treating files as ground truth, not conversation history.

## Integration with Existing Skills

```
/batman uses internally:
├── /decompose → Creates task_queue.json
├── /recall → Fetches relevant memories in Phase 1
├── /memorize → Stores learnings on completion
├── /handoff → Generates handoff.md on interrupt
└── Plan Mode → Built-in read-only for Phase 1
```

## Anti-Patterns

```
❌ Acting before PREP.md is written
❌ Skipping user approval
❌ Working directly instead of spawning subagents
❌ Trusting conversation context over .batman/ files
❌ Ignoring the lock and trying to bypass
❌ Half-assing PREP.md to pass the gate faster
```

## Success Metrics

After implementing a task with Batman mode:

- [ ] PREP.md accurately predicted all files touched
- [ ] No "surprise" files discovered mid-execution
- [ ] Subagents completed without needing manual intervention
- [ ] Context stayed small (few re-reads needed)
- [ ] User approved once, not multiple corrections

## Escape Hatches

```bash
# If CLI stuck or hook misbehaving:
rm -rf .batman/

# If need manual intervention:
/batman pause   # Then work manually, then /batman resume

# If task was wrong:
/batman abort   # Saves handoff, cleans up
```

## Example Session

```
User: /batman add JWT authentication to the API

Claude: Starting Batman mode...
        Creating .batman/ directory
        Entering Plan Mode (read-only)

        [Recalls 3 relevant memories about auth patterns]
        [Explores src/ - finds existing middleware, routes]
        [Identifies 8 files to read, 6 to modify]

        Writing PREP.md...
        Writing task_queue.json (4 subtasks, est. $0.18)...

        ## Preparation Complete

        **Mission:** Add JWT auth middleware and protect all API routes

        **Files to modify:** 6 (routes/*, middleware/)
        **Subtasks:** 4 (2 haiku search, 2 sonnet implement)
        **Est. cost:** $0.18

        [Shows subtask table]

        Proceed? (add notes if needed)

User: go, but use RS256 not HS256

Claude: Noted. Updating context.json with RS256 requirement.

        Exiting Plan Mode...
        Activating lock...

        Spawning subtask 1/4: [haiku] Find existing auth patterns
        → Output: .batman/outputs/1_auth_patterns.json ✓

        Spawning subtask 2/4: [haiku] List all route files
        → Output: .batman/outputs/2_routes.json ✓

        Spawning subtask 3/4: [sonnet] Implement JWT middleware (RS256)
        → Output: src/middleware/jwt.ts ✓

        Spawning subtask 4/4: [sonnet] Add auth to routes
        → Output: .batman/outputs/4_protected.json ✓

        All subtasks complete.
        Removing lock...

        ## Summary
        - Created: src/middleware/jwt.ts
        - Modified: 5 route files
        - Tests: [recommend running npm test]

        Memorizing: "API uses RS256 JWT, middleware in src/middleware/jwt.ts"
```
