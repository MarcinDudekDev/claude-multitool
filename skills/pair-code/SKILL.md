---
name: pair-code
description: This skill should be used when the user asks to "pair program", "pair code", "multi-model review", "code review with gemini", "let gemini implement", "let claude implement", "have another model review", "iterative code review", or mentions using multiple AI models for implementation and review workflows.
version: 2.0.0
---

# Multi-Model Pair Programming

Orchestrate iterative code implementation and review cycles between AI models. One model implements changes, another reviews, repeating until approved or max rounds reached.

## When to Use

- Implementing features that benefit from a second opinion
- Code changes requiring careful review
- Comparing implementation styles between models
- Getting faster/cheaper reviews with `--quick` mode

## Core Command

```bash
~/Tools/pair-code "<task>" <files...> [options]
```

### Required Arguments

| Argument | Description |
|----------|-------------|
| `task` | Description of the coding task in quotes |
| `files` | One or more files to modify (space-separated) |

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `--implementer MODEL` | `-i` | Model for implementation (default: claude) |
| `--reviewer MODEL` | `-r` | Model for review (default: claude) |
| `--quick` | `-q` | Use haiku for review (faster/cheaper) |
| `--max-rounds N` | `-m` | Max review rounds (default: 3) |
| `--dry-run` | | Preview without making changes |
| `--no-git` | | Skip git branch creation |
| `--json` | | Request JSON formatted review |
| `--timeout N` | `-t` | Timeout per model call in seconds |

### Available Models

- `claude` - Claude (default)
- `gemini` - Google Gemini
- `opencode` - OpenCode

## Common Workflows

### Quick Review (Haiku)

For faster, cheaper reviews on simple changes:

```bash
~/Tools/pair-code "fix typo in README" README.md -q
```

### Cross-Model Review

Gemini implements, Claude reviews (diverse perspectives):

```bash
~/Tools/pair-code "add input validation" form.py -i gemini -r claude
```

### Flipped Workflow

Claude implements, Gemini reviews:

```bash
~/Tools/pair-code "refactor auth module" auth.py -i claude -r gemini
```

### Preview Mode

See what would happen without changes:

```bash
~/Tools/pair-code "add logging" utils.py --dry-run
```

### Multiple Files

```bash
~/Tools/pair-code "update error handling" api.py handlers.py utils.py
```

## Safety Features

- **File backup**: Files backed up before modification
- **Auto-restore**: On failure, files restored from backup
- **Git branching**: Creates feature branch (unless `--no-git`)
- **Retry logic**: Exponential backoff on model failures (2s, 4s, 8s)

## Model Selection Guide

| Scenario | Implementer | Reviewer | Command |
|----------|-------------|----------|---------|
| Quality focus | claude | claude | (default) |
| Fast iteration | gemini | claude -q | `-i gemini -q` |
| Diverse review | claude | gemini | `-r gemini` |
| Budget conscious | gemini | claude -q | `-i gemini -q` |

## Output Interpretation

The tool shows:
1. **Session header** - Models, task, files
2. **Round N** - Each implementation/review cycle
3. **Implementation** - Model's code changes
4. **Review** - Approval or requested changes
5. **Result** - SUCCESS or max rounds reached

### JSON Mode

With `--json`, reviews return structured data:

```json
{
  "verdict": "APPROVED" | "CHANGES_REQUESTED",
  "summary": "Brief assessment",
  "issues": ["List of issues if any"]
}
```

## Troubleshooting

### Model not available

Check available models:
```bash
python3 -c "import sys; sys.path.insert(0, '$HOME/Tools'); from importlib import import_module; a = import_module('pair-code-adapters'); print(a.get_available_models())"
```

### Files not found

Verify paths are correct and files exist before running.

### Timeout errors

Increase timeout for large files:
```bash
~/Tools/pair-code "complex refactor" big-file.py -t 600
```

## Additional Resources

### Reference Files

- **`references/model-comparison.md`** - Detailed comparison of model strengths
- **`references/advanced-workflows.md`** - Complex multi-file workflows

### Examples

- **`examples/quick-fix.sh`** - Simple typo fix example
- **`examples/cross-model.sh`** - Cross-model review example
