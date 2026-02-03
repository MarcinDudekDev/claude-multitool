#!/usr/bin/env python3
"""
SessionEnd hook: Auto-generate batman handoff if session ends mid-task.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def main():
    # Get current working directory
    cwd = os.environ.get("PWD", os.getcwd())
    batman_dir = Path(cwd) / ".batman"
    status_file = batman_dir / "status.json"
    handoff_file = batman_dir / "handoff.md"

    # Check if batman session is active
    if not status_file.exists():
        sys.exit(0)

    try:
        with open(status_file) as f:
            status = json.load(f)
    except:
        sys.exit(0)

    phase = status.get("phase", "")

    # Only generate handoff if in active phases
    if phase not in ("recon", "approval", "execution"):
        sys.exit(0)

    # Generate handoff
    content = f"""# Batman Session Handoff (Auto-generated)

Session ended unexpectedly at {datetime.now().isoformat()}

## Task
{status.get('task', 'Unknown')}

## Status at End
- Phase: {phase}
- Completed subtasks: {len(status.get('completed_subtasks', []))}
- Failed subtasks: {len(status.get('failed_subtasks', []))}

## Flags
- prep_complete: {status.get('flags', {}).get('prep_complete', False)}
- user_approved: {status.get('flags', {}).get('user_approved', False)}
- lock_active: {status.get('flags', {}).get('lock_active', False)}

## Completed Subtasks
"""
    for st in status.get('completed_subtasks', []):
        content += f"- [x] {st}\n"

    content += "\n## Failed Subtasks\n"
    for st in status.get('failed_subtasks', []):
        content += f"- [ ] {st} (FAILED)\n"

    if status.get('current_subtask'):
        content += f"\n## Current/In-Progress\n- [ ] {status['current_subtask']}\n"

    content += """
## To Resume

1. Start new Claude session in the same directory
2. Run: `/batman resume` or read this file and continue manually
3. Check .batman/status.json and .batman/progress.json for full state

## Files to Check
- .batman/PREP.md - Original preparation
- .batman/task_queue.json - Subtask definitions
- .batman/context.json - Project context
- .batman/progress.json - Detailed progress
"""

    try:
        with open(handoff_file, 'w') as f:
            f.write(content)

        # Also remove the lock if active (so next session can start clean)
        if status.get('flags', {}).get('lock_active'):
            status['flags']['lock_active'] = False
            status['_interrupted_at'] = datetime.now().isoformat()
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)

    except Exception as e:
        # Don't fail the session end for handoff errors
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
