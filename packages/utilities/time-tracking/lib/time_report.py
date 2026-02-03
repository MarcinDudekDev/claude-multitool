#!/usr/bin/env python3
"""
Time tracking report generator from Claude Code transcripts.
Parses JSONL transcript files and generates usage reports.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict
from typing import Optional
import argparse
import html

PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Folders to exclude
EXCLUDE_FOLDERS = {"subagents"}

# Max session duration (sessions longer than this are likely artifacts)
MAX_SESSION_HOURS = 8

# Cache for project mapping
_project_mapping = None


def path_to_folder_name(path: str) -> str:
    """Convert a file path to Claude's folder name format."""
    # Claude replaces both / and . with -
    folder_name = path.replace("/", "-").replace(".", "-")
    # Keep leading dash (from leading /)
    return folder_name


def load_project_mapping() -> dict:
    """Load project name mapping from 'p --list' command."""
    global _project_mapping
    if _project_mapping is not None:
        return _project_mapping

    _project_mapping = {}
    try:
        result = subprocess.run(
            ["p", "--list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if ": " in line:
                    name, path = line.split(": ", 1)
                    folder_name = path_to_folder_name(path)
                    _project_mapping[folder_name] = name.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return _project_mapping


def parse_timestamp(ts: str) -> Optional[datetime]:
    """Parse ISO timestamp to datetime (timezone-aware UTC)."""
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt
    except (ValueError, TypeError):
        return None


def extract_project_name(folder_name: str) -> str:
    """Extract readable project name from folder path using p tool mapping."""
    mapping = load_project_mapping()

    # Try exact match first
    if folder_name in mapping:
        return mapping[folder_name]

    # Try prefix match (folder might have subdirectory)
    for folder_key, project_name in mapping.items():
        if folder_name.startswith(folder_key):
            return project_name

    # Fallback: extract from folder name
    # Format: -Users-username--project-name
    parts = folder_name.split("-")

    # Get current username dynamically
    import os
    username = os.path.basename(os.path.expanduser('~')).lower()
    skip_words = {"users", "home", username, "wp", "test", "sites", "local", "wordpress",
                  "claude", "plugins", "skills", "hooks", "plans", "main", "content",
                  "themes", "child", "projects", "documents"}

    meaningful = []
    for part in parts:
        if part.lower() not in skip_words and len(part) > 2:
            meaningful.append(part)

    if meaningful:
        return meaningful[0]

    return folder_name.split("-")[-1] or folder_name


def is_user_prompt(entry: dict) -> bool:
    """Check if entry is a user prompt (not tool result, not command)."""
    if entry.get("type") != "user":
        return False

    message = entry.get("message", {})
    content = message.get("content")

    # Must be string content (not array of tool results)
    if not isinstance(content, str):
        return False

    # Exclude command messages
    if "<command-name>" in content or "<local-command>" in content:
        return False

    # Exclude system reminders only
    if content.strip().startswith("<system-reminder>") and content.strip().endswith("</system-reminder>"):
        return False

    return True


def clean_prompt_text(text: str) -> str:
    """Clean user prompt text for display as summary."""
    # Remove XML-style tags and their content
    text = re.sub(r'<system-reminder>.*?</system-reminder>', '', text, flags=re.DOTALL)
    text = re.sub(r'<local-command-caveat>.*?</local-command-caveat>', '', text, flags=re.DOTALL)
    text = re.sub(r'<local-command.*?>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)  # Remove any remaining tags

    text = text.strip()

    # Skip generic/unhelpful prompts
    skip_patterns = [
        r'^Implement the following plan:?',
        r'^Continue with',
        r'^Please continue',
        r'^ok$',
        r'^yes$',
        r'^y$',
        r'^go$',
        r'^do it$',
    ]
    for pattern in skip_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return None

    # Take first meaningful line
    for line in text.split('\n'):
        line = line.strip()
        if line and len(line) > 5:  # Skip very short lines
            if len(line) > 60:
                return line[:57] + "..."
            return line

    return None


def parse_session_for_date(jsonl_path: Path, target_date: datetime.date) -> Optional[dict]:
    """Parse a session file and return data only for entries on target date."""
    session = {
        "path": jsonl_path,
        "summary": None,
        "first_prompt": None,
        "user_prompts": 0,
        "timestamps": []
    }

    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Get summary (always capture it)
                if entry.get("type") == "summary":
                    session["summary"] = entry.get("summary", "")
                    continue

                # Get timestamp from entry or snapshot
                ts = None
                if entry.get("type") == "file-history-snapshot":
                    snapshot = entry.get("snapshot", {})
                    ts = parse_timestamp(snapshot.get("timestamp"))
                elif "timestamp" in entry:
                    ts = parse_timestamp(entry.get("timestamp"))

                # Skip if no timestamp or not on target date
                if not ts:
                    continue

                # Convert to local date for comparison
                local_dt = ts.astimezone()
                if local_dt.date() != target_date:
                    continue

                # This entry is on the target date
                session["timestamps"].append(ts)

                # Count user prompts and capture first useful one
                if is_user_prompt(entry):
                    session["user_prompts"] += 1
                    if session["first_prompt"] is None:
                        content = entry.get("message", {}).get("content", "")
                        cleaned = clean_prompt_text(content)
                        if cleaned:  # Only set if we got something useful
                            session["first_prompt"] = cleaned

    except (IOError, OSError) as e:
        print(f"Warning: Could not read {jsonl_path}: {e}", file=sys.stderr)
        return None

    # Only return if we have activity on this date
    if not session["timestamps"]:
        return None

    # Calculate time span for this date only
    session["first_timestamp"] = min(session["timestamps"])
    session["last_timestamp"] = max(session["timestamps"])

    # Skip sessions longer than MAX_SESSION_HOURS (likely artifacts)
    duration = session["last_timestamp"] - session["first_timestamp"]
    if duration > timedelta(hours=MAX_SESSION_HOURS):
        return None

    return session


def get_session_display_summary(session: dict) -> str:
    """Get display summary: prefer summary, fallback to first prompt."""
    if session.get("summary"):
        return session["summary"]
    if session.get("first_prompt"):
        return session["first_prompt"]
    return None


def format_duration(delta: timedelta) -> str:
    """Format timedelta as human-readable string."""
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        return "0s"
    if total_seconds < 60:
        return f"{total_seconds}s"

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


def get_sessions_for_date(target_date: datetime.date) -> dict:
    """Get all sessions with activity on target date, grouped by project."""
    projects = defaultdict(list)

    if not PROJECTS_DIR.exists():
        return projects

    for project_folder in PROJECTS_DIR.iterdir():
        if not project_folder.is_dir():
            continue

        folder_name = project_folder.name

        # Skip excluded folders
        if folder_name.lower() in EXCLUDE_FOLDERS:
            continue

        project_name = extract_project_name(folder_name)

        # Check each JSONL file
        for jsonl_file in project_folder.glob("*.jsonl"):
            try:
                # Quick check: skip files not modified recently (optimization)
                mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
                days_old = (datetime.now() - mtime).days
                if days_old > 30:  # Skip files older than 30 days
                    continue

                session = parse_session_for_date(jsonl_file, target_date)
                if session and session["user_prompts"] > 0:
                    projects[project_name].append(session)
            except (IOError, OSError):
                continue

    return projects


def generate_terminal_report(projects: dict, target_date: datetime.date) -> str:
    """Generate terminal-formatted report."""
    lines = []
    lines.append(f"\n=== {target_date.strftime('%Y-%m-%d (%A)')} ===\n")

    if not projects:
        lines.append("No activity found for this date.\n")
        return "\n".join(lines)

    total_duration = timedelta()
    total_prompts = 0

    # Sort by number of prompts (descending)
    sorted_projects = sorted(projects.items(), key=lambda x: sum(s["user_prompts"] for s in x[1]), reverse=True)

    for project_name, sessions in sorted_projects:
        project_prompts = sum(s["user_prompts"] for s in sessions)

        # Calculate project duration (sum of individual session durations)
        project_duration = timedelta()
        for s in sessions:
            if s["first_timestamp"] and s["last_timestamp"]:
                project_duration += s["last_timestamp"] - s["first_timestamp"]

        total_duration += project_duration
        total_prompts += project_prompts

        lines.append(f"{project_name} ({format_duration(project_duration)}, {project_prompts} prompts)")

        # Sort sessions by start time
        sorted_sessions = sorted(sessions, key=lambda s: s["first_timestamp"] or datetime.min.replace(tzinfo=timezone.utc))

        for session in sorted_sessions:
            summary = get_session_display_summary(session)
            if session["first_timestamp"] and session["last_timestamp"]:
                duration = session["last_timestamp"] - session["first_timestamp"]
                dur_str = format_duration(duration)
                start_time = session["first_timestamp"].astimezone().strftime("%H:%M")
            else:
                dur_str = "?"
                start_time = "?"

            if summary:
                lines.append(f'  [{start_time}] "{summary}" ({dur_str}, {session["user_prompts"]}p)')
            else:
                lines.append(f'  [{start_time}] ({dur_str}, {session["user_prompts"]}p)')

        lines.append("")

    lines.append(f"TOTAL: {format_duration(total_duration)} across {len(projects)} projects, {total_prompts} prompts")

    return "\n".join(lines)


def generate_h_commands(all_data: dict, dates: list) -> list:
    """Generate 'h add' commands for time tracking.

    Returns list of command strings for each project/day combination.
    Hours rounded to nearest 0.5h (min 0.5h).
    """
    commands = []

    for date in sorted(dates):
        projects = all_data.get(date, {})
        if not projects:
            continue

        date_str = date.strftime("%Y-%m-%d")

        for project_name, sessions in sorted(projects.items()):
            # Calculate total duration for this project on this date
            total_duration = timedelta()
            summaries = []

            for s in sessions:
                if s["first_timestamp"] and s["last_timestamp"]:
                    total_duration += s["last_timestamp"] - s["first_timestamp"]
                summary = get_session_display_summary(s)
                if summary:
                    summaries.append(summary)

            # Round hours to nearest 0.5h (min 0.5h)
            total_hours = total_duration.total_seconds() / 3600
            rounded_hours = max(0.5, round(total_hours * 2) / 2)

            # Combine summaries, truncate to ~60 chars, escape quotes
            combined_summary = "; ".join(summaries)
            if len(combined_summary) > 60:
                combined_summary = combined_summary[:57] + "..."
            # Escape single quotes for shell
            combined_summary = combined_summary.replace("'", "'\\''")

            cmd = f"h add {project_name} {rounded_hours} '{combined_summary}' --date {date_str}"
            commands.append(cmd)

    return commands


def generate_html_report(all_data: dict, dates: list) -> str:
    """Generate HTML report for multiple dates."""

    # Calculate totals
    total_duration = timedelta()
    total_prompts = 0
    project_totals = defaultdict(lambda: {"duration": timedelta(), "prompts": 0, "sessions": 0})

    for date in dates:
        projects = all_data.get(date, {})
        for project_name, sessions in projects.items():
            for s in sessions:
                project_totals[project_name]["prompts"] += s["user_prompts"]
                project_totals[project_name]["sessions"] += 1
                if s["first_timestamp"] and s["last_timestamp"]:
                    dur = s["last_timestamp"] - s["first_timestamp"]
                    project_totals[project_name]["duration"] += dur
                    total_duration += dur
            total_prompts += sum(s["user_prompts"] for s in sessions)

    # Find max duration for progress bar scaling
    max_duration = max((p["duration"] for p in project_totals.values()), default=timedelta(hours=1))
    if max_duration.total_seconds() == 0:
        max_duration = timedelta(hours=1)

    date_range_str = f"{min(dates).strftime('%b %d')} - {max(dates).strftime('%b %d, %Y')}" if len(dates) > 1 else dates[0].strftime("%B %d, %Y")

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Code Time Report</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: #fff;
        }}
        .subtitle {{ color: #888; margin-bottom: 2rem; }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .card-label {{ color: #888; font-size: 0.85rem; text-transform: uppercase; }}
        .card-value {{ font-size: 2rem; font-weight: 600; color: #fff; }}
        .project-card {{
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}
        .project-name {{ font-size: 1.25rem; font-weight: 600; color: #fff; }}
        .project-stats {{ color: #888; font-size: 0.9rem; }}
        .progress-bar {{
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 1rem;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        .sessions {{ margin-top: 1rem; }}
        .session {{
            padding: 0.75rem;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }}
        .session-summary {{ color: #fff; margin-bottom: 0.25rem; }}
        .session-meta {{ color: #666; font-size: 0.8rem; }}
        .date-section {{ margin-top: 2rem; }}
        .date-header {{
            font-size: 1.1rem;
            color: #888;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        details {{
            margin-bottom: 0.5rem;
        }}
        details summary {{
            cursor: pointer;
            padding: 0.75rem;
            background: rgba(255,255,255,0.03);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.08);
            list-style: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        details summary::-webkit-details-marker {{ display: none; }}
        details summary::before {{
            content: "▶";
            margin-right: 0.5rem;
            font-size: 0.7rem;
            transition: transform 0.2s;
        }}
        details[open] summary::before {{
            transform: rotate(90deg);
        }}
        details[open] summary {{
            border-radius: 8px 8px 0 0;
            margin-bottom: 0;
        }}
        .details-content {{
            background: rgba(0,0,0,0.15);
            border: 1px solid rgba(255,255,255,0.08);
            border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 0.75rem;
        }}
        .summary-left {{ display: flex; align-items: center; }}
        .summary-right {{ color: #888; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Claude Code Time Report</h1>
        <p class="subtitle">{date_range_str}</p>

        <div class="summary-cards">
            <div class="card">
                <div class="card-label">Total Time</div>
                <div class="card-value">{format_duration(total_duration)}</div>
            </div>
            <div class="card">
                <div class="card-label">Projects</div>
                <div class="card-value">{len(project_totals)}</div>
            </div>
            <div class="card">
                <div class="card-label">Prompts</div>
                <div class="card-value">{total_prompts}</div>
            </div>
        </div>

        <h2 style="color: #fff; margin-bottom: 1rem;">Projects Overview</h2>
'''

    # Sort projects by duration
    sorted_projects = sorted(project_totals.items(), key=lambda x: x[1]["duration"], reverse=True)

    for project_name, totals in sorted_projects:
        pct = (totals["duration"].total_seconds() / max_duration.total_seconds()) * 100
        html_content += f'''
        <div class="project-card">
            <div class="project-header">
                <span class="project-name">{html.escape(project_name)}</span>
                <span class="project-stats">{format_duration(totals["duration"])} | {totals["prompts"]} prompts | {totals["sessions"]} sessions</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {pct:.1f}%"></div>
            </div>
        </div>
'''

    # Generate h add commands section
    h_commands = generate_h_commands(all_data, dates)
    if h_commands:
        commands_text = html.escape('\n'.join(h_commands))
        html_content += f'''
        <h2 style="color: #fff; margin: 2rem 0 1rem;">Time Tracking Commands</h2>
        <div class="project-card">
            <button onclick="navigator.clipboard.writeText(document.getElementById('h-commands').textContent).then(() => this.textContent = 'Copied!').catch(() => this.textContent = 'Failed')" style="background: linear-gradient(90deg, #6366f1, #8b5cf6); color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; margin-bottom: 1rem; font-size: 0.9rem;">Copy All</button>
            <pre id="h-commands" style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; overflow-x: auto; font-size: 0.85rem; line-height: 1.6; white-space: pre-wrap; word-break: break-all;">{commands_text}</pre>
        </div>
'''

    # Daily breakdown
    for date in sorted(dates, reverse=True):
        projects = all_data.get(date, {})
        if not projects:
            continue

        # Calculate daily totals
        day_duration = timedelta()
        day_prompts = 0
        for sessions in projects.values():
            for s in sessions:
                day_prompts += s["user_prompts"]
                if s["first_timestamp"] and s["last_timestamp"]:
                    day_duration += s["last_timestamp"] - s["first_timestamp"]

        html_content += f'''
        <details class="date-section">
            <summary>
                <span class="summary-left">{date.strftime("%A, %B %d")}</span>
                <span class="summary-right">{format_duration(day_duration)} | {day_prompts} prompts | {len(projects)} projects</span>
            </summary>
            <div class="details-content">
'''
        for project_name, sessions in sorted(projects.items(), key=lambda x: sum(s["user_prompts"] for s in x[1]), reverse=True):
            proj_duration = timedelta()
            proj_prompts = sum(s["user_prompts"] for s in sessions)
            for s in sessions:
                if s["first_timestamp"] and s["last_timestamp"]:
                    proj_duration += s["last_timestamp"] - s["first_timestamp"]

            html_content += f'''
                <details>
                    <summary>
                        <span class="summary-left">{html.escape(project_name)}</span>
                        <span class="summary-right">{format_duration(proj_duration)} | {proj_prompts}p | {len(sessions)} sessions</span>
                    </summary>
                    <div class="details-content">
'''
            for session in sorted(sessions, key=lambda s: s["first_timestamp"] or datetime.min.replace(tzinfo=timezone.utc)):
                summary = get_session_display_summary(session)
                if session["first_timestamp"] and session["last_timestamp"]:
                    duration = session["last_timestamp"] - session["first_timestamp"]
                    dur_str = format_duration(duration)
                    start_time = session["first_timestamp"].astimezone().strftime("%H:%M")
                else:
                    dur_str = "?"
                    start_time = "?"

                summary_html = html.escape(summary) if summary else "<em>No description</em>"

                html_content += f'''
                        <div class="session">
                            <div class="session-summary">{summary_html}</div>
                            <div class="session-meta">{start_time} | {dur_str} | {session["user_prompts"]} prompts</div>
                        </div>
'''
            html_content += '''
                    </div>
                </details>
'''
        html_content += '''
            </div>
        </details>
'''

    html_content += '''
    </div>
</body>
</html>
'''
    return html_content


def get_week_dates() -> list:
    """Get dates from Monday to today (current work week)."""
    today = datetime.now().date()
    # Monday is 0, Sunday is 6
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday)

    # Generate dates from Monday to today
    dates = []
    current = today
    while current >= monday:
        dates.append(current)
        current -= timedelta(days=1)

    return dates


def main():
    parser = argparse.ArgumentParser(description="Generate time tracking report from Claude Code transcripts")
    parser.add_argument("date", nargs="?", help="Target date (YYYY-MM-DD), defaults to today")
    parser.add_argument("days_back", nargs="?", type=int, default=None, help="Number of days to go back from target date")
    parser.add_argument("--terminal", "-t", action="store_true", help="Output terminal text instead of HTML")

    args = parser.parse_args()

    # Parse target date
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        # Generate date range
        days_back = args.days_back if args.days_back is not None else 0
        dates = [target_date - timedelta(days=i) for i in range(days_back + 1)]
    else:
        # Default: current week (Monday to today) for HTML, just today for terminal
        if args.terminal:
            target_date = datetime.now().date()
            days_back = args.days_back if args.days_back is not None else 0
            dates = [target_date - timedelta(days=i) for i in range(days_back + 1)]
        else:
            dates = get_week_dates()

    # Collect data for all dates
    all_data = {}
    for date in dates:
        all_data[date] = get_sessions_for_date(date)

    if args.terminal:
        for date in sorted(dates, reverse=True):
            print(generate_terminal_report(all_data[date], date))
    else:
        html_content = generate_html_report(all_data, dates)
        output_path = Path("/tmp/time-report.html")
        output_path.write_text(html_content)
        print(f"Report saved to {output_path}")
        # Open in browser using subprocess
        subprocess.run(["open", str(output_path)], check=False)


if __name__ == "__main__":
    main()
