# Git Workflow Reference

## Quick Status & Navigation

**See what changed:**
```bash
git diff --name-only              # Modified files only
git status --short                # Compact status view
```

**Current branch info:**
```bash
git branch -vv                    # Current + tracking branch
git log --oneline -5              # Last 5 commits
```

## Staging & Commits

**Stage changes:**
```bash
git add .                         # Stage all changes
git add <file>                    # Stage specific file
git add -p                        # Interactive staging (choose hunks)
```

**Commit with author info:**
```bash
git commit -m "message"
git commit -m "message" --author="Name <email@example.com>"
```

**Add coauthor (in commit message):**
```
Commit message

Co-authored-by: Name <email@example.com>
```

## Viewing Changes

**Before committing:**
```bash
git diff                          # Unstaged changes
git diff --cached                 # Staged changes only
git diff HEAD~1                   # Changes since last commit
```

**After committing:**
```bash
git log --oneline                 # Commit history
git show <commit-hash>            # Full commit details
git log -p -1                     # Last commit with diff
```

## Efficient Workflows

**Quick commit cycle:**
```bash
git add .
git commit -m "feature: description"
git log --oneline -1              # Verify
```

**Check before push:**
```bash
git diff origin/main...HEAD       # Changes vs remote
git log origin/main..HEAD --oneline # Unpushed commits
```

**Undo changes:**
```bash
git restore <file>                # Discard unstaged changes
git restore --staged <file>       # Unstage file
git reset HEAD~1                  # Undo last commit (keep changes)
git reset --hard HEAD~1           # Discard last commit
```

## Branch Management

**Create & switch:**
```bash
git checkout -b feature/name      # Create + switch
git switch feature/name           # Switch (if exists)
git branch -d feature/name        # Delete local branch
```

**Sync with remote:**
```bash
git fetch                         # Update remote tracking
git pull                          # Fetch + merge
git rebase origin/main            # Rebase on main
```

## Token-Efficient Patterns

Instead of verbose output, use:
- `git status --short` (not full status)
- `git diff --name-only` (not full diff)
- `git log --oneline` (not verbose log)
- Script/automate repeated queries

## Coauthor Setup

Add to commit message template or script:
```
Co-authored-by: Name <email@example.com>
Co-authored-by: Another Person <another@example.com>
```

Or use git hooks for automation.
