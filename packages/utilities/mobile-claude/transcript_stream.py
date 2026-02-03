#!/usr/bin/env python3
"""Real-time transcript streaming for Claude sessions."""

import asyncio
import json
import re
import random
from pathlib import Path
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from watchfiles import awatch

router = APIRouter()

_URL_RE = re.compile(r'https?://[^\s&<"\']+')
_PATH_RE = re.compile(r'(/Users/|/private/)[^\s&<"\']+')
_LINK_STYLE = 'color:#60a5fa;text-decoration:underline;cursor:pointer;'


def linkify(text: str) -> str:
    """Turn URLs and file paths into clickable links. Call AFTER HTML-escaping."""
    text = _URL_RE.sub(lambda m: f'<a href="{m.group()}" target="_blank" style="{_LINK_STYLE}">{m.group()}</a>', text)
    text = _PATH_RE.sub(lambda m: f'<a href="#" onclick="fetch(\'/api/open?path={m.group()}\');return false;" style="{_LINK_STYLE}">{m.group()}</a>', text)
    return text


PROJECTS_DIR = Path.home() / '.claude' / 'projects'


@router.get("/api/open")
async def open_file(path: str):
    """Open a local file in its default macOS app."""
    import subprocess
    subprocess.Popen(["open", path])
    return {"ok": True}


def extract_content(content) -> list[dict]:
    """Extract all content blocks from message content."""
    blocks = []
    if isinstance(content, str):
        if content.strip():
            blocks.append({'type': 'text', 'text': content.strip()})
    elif isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get('type')
            if btype == 'text' and block.get('text'):
                blocks.append({'type': 'text', 'text': block['text']})
            elif btype == 'tool_use':
                name = block.get('name', 'unknown')
                inp = block.get('input', {})
                # Summarize tool input
                if name == 'Bash':
                    summary = inp.get('command', '')
                elif name in ('Read', 'Write', 'Edit'):
                    summary = inp.get('file_path', '')
                elif name == 'Grep':
                    summary = f"pattern={inp.get('pattern', '')}"
                elif name == 'Glob':
                    summary = f"pattern={inp.get('pattern', '')}"
                elif name == 'Task':
                    summary = inp.get('description', '')
                else:
                    summary = str(inp)[:300]
                blocks.append({'type': 'tool_use', 'name': name, 'summary': summary})
            elif btype == 'tool_result':
                content_text = block.get('content', '')
                if isinstance(content_text, list):
                    content_text = ' '.join(str(c.get('text', ''))[:100] for c in content_text if isinstance(c, dict))
                result_text = str(content_text)[:300].strip() or '✓ (no output)'
                blocks.append({'type': 'tool_result', 'text': result_text})
    return blocks


def parse_msg_line(line: str) -> dict | None:
    """Parse a single JSONL line, return message dict or None."""
    line = line.strip()
    if not line:
        return None
    # Quick filter - skip non-message lines
    if '"type":"user"' not in line and '"type":"assistant"' not in line and '"type":"queue-operation"' not in line:
        return None
    try:
        obj = json.loads(line)
        msg_type = obj.get('type')

        # Handle queued user messages (sent while assistant is working)
        if msg_type == 'queue-operation' and obj.get('operation') == 'enqueue':
            content = obj.get('content', '').strip()
            if content:
                return {
                    'type': 'user',
                    'role': 'user',
                    'blocks': [{'type': 'text', 'text': content}],
                    'timestamp': obj.get('timestamp', '')[:19].replace('T', ' ')
                }
            return None

        if msg_type not in ('user', 'assistant'):
            return None
        raw_content = obj.get('message', {}).get('content', '')
        blocks = extract_content(raw_content)
        if not blocks:
            return None

        # Determine actual role: user messages containing tool_result are from TOOL, not human
        role = msg_type  # 'user' or 'assistant'
        if msg_type == 'user':
            # Check if this is a tool_result (not human input)
            if isinstance(raw_content, list) and raw_content:
                first_block_type = raw_content[0].get('type') if isinstance(raw_content[0], dict) else None
                if first_block_type == 'tool_result':
                    role = 'tool'

        return {
            'type': msg_type,
            'role': role,  # 'user', 'assistant', or 'tool'
            'blocks': blocks,
            'timestamp': obj.get('timestamp', '')[:19].replace('T', ' ')
        }
    except (json.JSONDecodeError, AttributeError):
        return None


def render_message(msg: dict) -> str:
    """Render a message as HTML with color-coded borders."""
    import hashlib
    # Generate stable ID from timestamp + role + content hash
    role = msg.get('role', msg['type'])
    content_hash = hashlib.md5(str(msg.get('blocks', [])).encode()).hexdigest()[:8]
    msg_id = f"msg-{msg.get('timestamp', '').replace(' ', '-').replace(':', '-')}-{role}-{content_hash}"

    if role == 'user':
        color = '#3b82f6'  # Blue - human user
        label = 'YOU'
        align = 'right'
        border_side = 'right'
    elif role == 'tool':
        color = '#8b5cf6'  # Purple - tool results
        label = 'TOOL'
        align = 'left'
        border_side = 'left'
    else:
        color = '#10b981'  # Green - assistant
        label = 'CLAUDE'
        align = 'left'
        border_side = 'left'

    timestamp = msg.get('timestamp', '')

    # Render all blocks
    content_parts = []
    for block in msg.get('blocks', []):
        if block['type'] == 'text':
            text = block['text'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            text = text.replace('\n', '<br>')
            text = linkify(text)
            content_parts.append(f'<div style="line-height: 1.5;">{text}</div>')
        elif block['type'] == 'tool_use':
            name = block.get('name', 'Tool')
            summary = block.get('summary', '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            summary = linkify(summary)
            content_parts.append(f'<div style="background: #1e3a5f; padding: 8px; border-radius: 4px; margin: 4px 0; font-family: monospace; font-size: 12px; white-space: pre-wrap; word-break: break-all;"><span style="color: #f59e0b;">⚡ {name}</span> <span style="color: #94a3b8;">{summary}</span></div>')
        elif block['type'] == 'tool_result':
            text = block.get('text', '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            text = linkify(text)
            preview = text[:200]
            has_more = len(text) > 200
            if has_more:
                uid = f"tr{random.randint(10000,99999)}"
                content_parts.append(f'<div style="background: #1a2e1a; padding: 8px; border-radius: 4px; margin: 4px 0; font-family: monospace; font-size: 11px; color: #86efac;"><div id="{uid}-short">{preview}… <a href="#" onclick="document.getElementById(\'{uid}-short\').style.display=\'none\';document.getElementById(\'{uid}-full\').style.display=\'block\';return false;" style="color:#f59e0b;text-decoration:underline;cursor:pointer;">show more</a></div><div id="{uid}-full" style="display:none;white-space:pre-wrap;word-break:break-all;">{text} <a href="#" onclick="document.getElementById(\'{uid}-full\').style.display=\'none\';document.getElementById(\'{uid}-short\').style.display=\'block\';return false;" style="color:#f59e0b;text-decoration:underline;cursor:pointer;">show less</a></div></div>')
            else:
                content_parts.append(f'<div style="background: #1a2e1a; padding: 8px; border-radius: 4px; margin: 4px 0; font-family: monospace; font-size: 11px; color: #86efac; white-space: pre-wrap; word-break: break-all;">{text}</div>')

    content_html = ''.join(content_parts)

    # User messages: right-aligned with right border
    if align == 'right':
        return f'''<div id="{msg_id}" style="border-right: 3px solid {color}; padding: 12px; margin: 8px 0 8px 20%; background: rgba(59,130,246,0.1); text-align: right;"><div style="font-size: 11px; color: #888; margin-bottom: 4px;">[{timestamp}] {label}</div>{content_html}</div>'''
    else:
        return f'''<div id="{msg_id}" style="border-left: 3px solid {color}; padding: 12px; margin: 8px 0; background: rgba(255,255,255,0.02);"><div style="font-size: 11px; color: #888; margin-bottom: 4px;">[{timestamp}] {label}</div>{content_html}</div>'''


@router.get("/api/transcripts")
async def list_transcripts():
    """List all JSONL conversation files from projects directory."""
    transcripts = []

    if not PROJECTS_DIR.exists():
        return {"transcripts": []}

    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        # Find all .jsonl files recursively
        for jsonl_file in project_dir.rglob('*.jsonl'):
            stat = jsonl_file.stat()
            # Create a friendly name from the path
            rel_path = jsonl_file.relative_to(PROJECTS_DIR)
            name = str(rel_path)

            transcripts.append({
                'name': name,
                'path': str(jsonl_file),
                'mtime': stat.st_mtime
            })

    # Sort by modification time, newest first
    transcripts.sort(key=lambda x: x['mtime'], reverse=True)

    # Build project ID mapping from 'p --list'
    project_map = {}
    try:
        import subprocess
        p_script = str(Path.home() / 'Tools' / 'p')
        result = subprocess.run(['python3', p_script, '--list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    pid, ppath = line.split(':', 1)
                    project_map[ppath.strip().rstrip('/')] = pid.strip()
    except Exception:
        pass

    # Build reverse map: encode each project path the same way Claude does
    def encode_path(p):
        """Encode path like Claude does: /Users/me/project -> -Users-me-project"""
        return p.replace('/', '-').replace('.', '-')

    encoded_to_pid = {}
    for ppath, pid in project_map.items():
        encoded_to_pid[encode_path(ppath)] = pid

    # Sort by length descending so longest (most specific) match wins
    sorted_encoded = sorted(encoded_to_pid.items(), key=lambda x: len(x[0]), reverse=True)

    # Enrich transcripts with project ID
    for t in transcripts:
        t['project'] = ''
        try:
            rel = Path(t['path']).relative_to(PROJECTS_DIR)
            encoded_dir = rel.parts[0]
            if encoded_dir in encoded_to_pid:
                t['project'] = encoded_to_pid[encoded_dir]
            else:
                for enc, pid in sorted_encoded:
                    # Must match at a path-segment boundary (followed by - or end)
                    if encoded_dir.startswith(enc) and (
                        len(encoded_dir) == len(enc) or encoded_dir[len(enc)] == '-'
                    ):
                        t['project'] = pid
                        break
        except (ValueError, IndexError):
            pass

    return {"transcripts": transcripts}


BASE64_PATTERN = re.compile(r'[A-Za-z0-9+/]{100,}={0,2}')


def truncate_base64(text: str) -> str:
    """Replace long base64 strings with placeholder."""
    return BASE64_PATTERN.sub('(base64 truncated)', text)


def render_raw_line(line: str, line_num: int) -> str | None:
    """Render a raw JSONL line for debugging."""
    line = line.strip()
    if not line:
        return None
    try:
        obj = json.loads(line)
        msg_type = obj.get('type', 'unknown')
        timestamp = obj.get('timestamp', '')[:19].replace('T', ' ')

        # Color by type
        if msg_type == 'user':
            color = '#3b82f6'
        elif msg_type == 'assistant':
            color = '#10b981'
        else:
            color = '#6b7280'

        # Format JSON nicely, truncate base64
        content = json.dumps(obj, indent=2, ensure_ascii=False)
        content = truncate_base64(content)
        content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        content = content.replace('\n', '<br>').replace('  ', '&nbsp;&nbsp;')

        return f'''<div id="raw-{line_num}" style="border-left: 3px solid {color}; padding: 8px; margin: 4px 0; background: rgba(0,0,0,0.3); font-family: monospace; font-size: 11px;"><div style="color: #888; margin-bottom: 4px;">Line {line_num} | {msg_type} | {timestamp}</div><div style="white-space: pre-wrap; word-break: break-all;">{content}</div></div>'''
    except json.JSONDecodeError:
        return None


async def stream_transcript_updates(session_path: str, raw: bool = False) -> AsyncGenerator[str, None]:
    """Watch a transcript file and stream new messages as they arrive."""
    file_path = Path(session_path)

    if not file_path.exists():
        yield f'data: {{"error": "File not found"}}\n\n'
        return

    # Track current file offset and line number
    offset = 0
    line_num = 0

    # Send initial content
    with open(file_path, 'r') as f:
        for line in f:
            line_num += 1
            if raw:
                fragment = render_raw_line(line, line_num)
            else:
                msg = parse_msg_line(line)
                fragment = render_message(msg) if msg else None

            if fragment:
                # SSE data lines cannot contain raw newlines — split across data: lines
                lines = fragment.replace('\n', '&#10;')
                event = f'event: datastar-patch-elements\n'
                event += f'data: elements {lines}\n\n'
                yield event
        offset = f.tell()

    # Watch for file changes
    async for changes in awatch(file_path):
        # Read new content from last offset
        try:
            with open(file_path, 'r') as f:
                f.seek(offset)
                new_lines = f.readlines()
                offset = f.tell()

                for line in new_lines:
                    line_num += 1
                    if raw:
                        fragment = render_raw_line(line, line_num)
                    else:
                        msg = parse_msg_line(line)
                        fragment = render_message(msg) if msg else None

                    if fragment:
                        lines = fragment.replace('\n', '&#10;')
                        event = f'event: datastar-patch-elements\n'
                        event += f'data: elements {lines}\n\n'
                        yield event
        except Exception as e:
            # File might be temporarily unavailable
            await asyncio.sleep(0.1)
            continue


@router.get("/stream")
async def stream_events(session: str, raw: int = 0):
    """SSE endpoint for streaming transcript updates."""
    return StreamingResponse(
        stream_transcript_updates(session, raw=bool(raw)),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
