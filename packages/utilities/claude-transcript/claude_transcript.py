#!/usr/bin/env python3
"""
claude_transcript - Shared library for parsing Claude Code transcript JSONL files.

Consolidates transcript parsing from 7+ independent implementations into one
importable + CLI tool.

Usage as library:
    import sys, os; sys.path.insert(0, os.path.expanduser("~/Tools"))
    from claude_transcript import metrics, extract_text, iter_messages

Usage as CLI:
    claude-transcript <file.jsonl>                  # metrics summary
    claude-transcript --metrics <file.jsonl>        # JSON metrics
    claude-transcript --chat <file.jsonl>           # full conversation
    claude-transcript --last <file.jsonl>           # last exchange
    claude-transcript --exchanges 5 <file.jsonl>    # last 5 exchanges
"""

import fcntl
import json
import os
import sys
from pathlib import Path

OFFSET_FILE = Path(
    os.environ.get('TRANSCRIPT_OFFSET_FILE')
    or (Path.home() / '.cache' / 'transcript-offsets.json')
)


# ============================================================================
# Content extraction — consolidates 7 implementations
# ============================================================================

def extract_text(content) -> str:
    """Extract text from message content (string or content blocks array).

    Handles both string content (user messages) and list-of-blocks content
    (assistant messages with text/tool_use/thinking blocks).
    """
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        texts = [b.get('text', '') for b in content
                 if isinstance(b, dict) and b.get('type') == 'text']
        return '\n'.join(texts).strip()
    return ''


# ============================================================================
# Line parsing — consolidates 7 implementations
# ============================================================================

def parse_line(line: str) -> dict | None:
    """Parse a single JSONL line into a normalized message dict.

    Returns {type, uuid, parent, content, timestamp, is_meta, raw_content}
    or None if the line is not a user/assistant message.

    Uses quick string filter before JSON parse for speed.
    """
    line = line.strip()
    if not line:
        return None
    # Quick filter - skip non-message lines
    if '"type":"user"' not in line and '"type":"assistant"' not in line \
       and '"type": "user"' not in line and '"type": "assistant"' not in line:
        return None
    try:
        obj = json.loads(line)
        msg_type = obj.get('type')
        if msg_type not in ('user', 'assistant'):
            return None
        raw_content = obj.get('message', {}).get('content', '')
        return {
            'type': msg_type,
            'uuid': obj.get('uuid'),
            'parent': obj.get('parentUuid'),
            'content': extract_text(raw_content),
            'raw_content': raw_content,
            'timestamp': obj.get('timestamp', '')[:19].replace('T', ' '),
            'is_meta': obj.get('isMeta', False),
            'usage': obj.get('message', {}).get('usage', {}),
        }
    except (json.JSONDecodeError, AttributeError):
        return None


# ============================================================================
# Content classification — fixes context_monitor calibration
# ============================================================================

def has_text_content(entry: dict) -> bool:
    """True if an entry has actual text output (not just tool_use/thinking).

    For parsed dicts from parse_line(): checks 'raw_content' for text blocks.
    For raw JSONL dicts: checks message.content blocks directly.

    This is the key function that fixes turn-counting inflation:
    assistant entries that only contain tool_use or thinking blocks
    are NOT real text responses.
    """
    # Handle raw JSONL entry (direct from json.loads)
    raw = entry.get('raw_content') or entry.get('message', {}).get('content', '')

    if isinstance(raw, str):
        return bool(raw.strip())

    if isinstance(raw, list):
        for block in raw:
            if isinstance(block, dict) and block.get('type') == 'text':
                text = block.get('text', '').strip()
                if text:
                    return True
        return False

    return False


# ============================================================================
# Iteration
# ============================================================================

def iter_messages(path, types=None, offset=0):
    """Yield parsed messages from a JSONL transcript file.

    Args:
        path: Path to .jsonl file
        types: Optional set/list of types to include (e.g. {'user', 'assistant'})
        offset: Byte offset to start reading from
    """
    with open(path, 'r') as f:
        if offset:
            f.seek(offset)
        for line in f:
            msg = parse_line(line)
            if msg is None:
                continue
            if types and msg['type'] not in types:
                continue
            yield msg


# ============================================================================
# Metrics — what context_monitor needs
# ============================================================================

def metrics(path) -> dict:
    """Compute transcript metrics with accurate turn counting.

    Returns {size_bytes, assistant_turns, user_turns}.
    assistant_turns counts ONLY entries with real text content,
    not tool-only or thinking-only responses.
    """
    p = Path(path)
    size_bytes = p.stat().st_size

    user_turns = 0
    assistant_turns = 0

    with open(path, 'r') as f:
        for line in f:
            msg = parse_line(line)
            if msg is None:
                continue
            if msg['type'] == 'user':
                # Real user messages have string content, not tool_result lists
                if isinstance(msg['raw_content'], str) and msg['content'] and not msg['is_meta']:
                    user_turns += 1
            elif msg['type'] == 'assistant':
                if not msg['is_meta'] and has_text_content(msg):
                    assistant_turns += 1

    return {
        'size_bytes': size_bytes,
        'assistant_turns': assistant_turns,
        'user_turns': user_turns,
    }


def fast_metrics(path) -> dict:
    """O(1) transcript metrics for large files using incremental offset tracking.

    For files < 500KB: falls back to full metrics().
    For files >= 500KB: reads only new data since last call, accumulates counts.
    Handles file truncation (new session) by resetting counts.
    """
    p = Path(path)
    size_bytes = p.stat().st_size

    if size_bytes < 512_000:  # 500KB
        return metrics(path)

    key = str(p.resolve())
    data = _load_offset_data()
    entry = _normalize_entry(data.get(key, 0))

    saved_offset = entry['offset']

    # File truncated or replaced (new session) — reset
    if saved_offset > size_bytes:
        saved_offset = 0
        entry = {'offset': 0, 'user_turns': 0, 'assistant_turns': 0}

    # Read only new bytes
    user_turns = entry['user_turns']
    assistant_turns = entry['assistant_turns']

    with open(path, 'r') as f:
        f.seek(saved_offset)
        for line in f:
            msg = parse_line(line)
            if msg is None:
                continue
            if msg['type'] == 'user':
                if isinstance(msg['raw_content'], str) and msg['content'] and not msg['is_meta']:
                    user_turns += 1
            elif msg['type'] == 'assistant':
                if not msg['is_meta'] and has_text_content(msg):
                    assistant_turns += 1
        new_offset = f.tell()

    # Save updated state
    data[key] = {'offset': new_offset, 'user_turns': user_turns, 'assistant_turns': assistant_turns}
    _save_offset_data(data)

    return {
        'size_bytes': size_bytes,
        'assistant_turns': assistant_turns,
        'user_turns': user_turns,
    }


# ============================================================================
# Tail read — what tts_realtime needs
# ============================================================================

def tail_messages(path, nbytes=50000, types=None) -> list:
    """Read last N bytes of transcript, parse messages.

    Efficient for hooks that only need recent messages without
    reading the entire file.
    """
    messages = []
    try:
        with open(path, 'rb') as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - nbytes))
            tail = f.read().decode('utf-8', errors='ignore')
    except (OSError, IOError):
        return []

    for line in tail.split('\n'):
        msg = parse_line(line)
        if msg is None:
            continue
        if types and msg['type'] not in types:
            continue
        messages.append(msg)

    return messages


# ============================================================================
# Exchange pairing — what incremental_scribe/session_extract need
# ============================================================================

def _is_real_user_message(msg: dict) -> bool:
    """Check if a parsed message is a real user message (not tool_result, not meta)."""
    if msg['type'] != 'user':
        return False
    if msg['is_meta']:
        return False
    # Real user messages have string content with actual text
    if isinstance(msg['raw_content'], str) and len(msg['content']) > 5:
        return True
    return False


def recent_exchanges(path, count=3) -> list:
    """Get last N user->assistant exchange pairs from transcript.

    Returns list of dicts: [{'user': parsed_msg, 'assistant': parsed_msg}, ...]
    Skips tool_results, meta messages, and assistant responses without text.
    """
    exchanges = []
    current_exchange = {}

    for msg in iter_messages(path):
        if _is_real_user_message(msg):
            # New exchange starts with real user message
            if current_exchange.get('user') and current_exchange.get('assistant'):
                exchanges.append(current_exchange)
            current_exchange = {'user': msg}

        elif msg['type'] == 'assistant' and current_exchange.get('user'):
            if has_text_content(msg):
                current_exchange['assistant'] = msg

    # Add last exchange if complete
    if current_exchange.get('user') and current_exchange.get('assistant'):
        exchanges.append(current_exchange)

    return exchanges[-count:] if len(exchanges) >= count else exchanges


# ============================================================================
# Offset tracking — what transcript-extract needs
# ============================================================================

def _load_offset_data() -> dict:
    """Load the full offset file. Returns raw dict."""
    if not OFFSET_FILE.exists():
        return {}
    try:
        with open(OFFSET_FILE, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                return json.load(f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_offset_data(data: dict):
    """Write the full offset file atomically."""
    OFFSET_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OFFSET_FILE, 'w') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            json.dump(data, f, indent=2)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _normalize_entry(val) -> dict:
    """Normalize offset entry — backwards-compatible with old int format."""
    if isinstance(val, int):
        return {'offset': val, 'user_turns': 0, 'assistant_turns': 0}
    if isinstance(val, dict):
        return {
            'offset': val.get('offset', 0),
            'user_turns': val.get('user_turns', 0),
            'assistant_turns': val.get('assistant_turns', 0),
        }
    return {'offset': 0, 'user_turns': 0, 'assistant_turns': 0}


def load_offset(path) -> int:
    """Load the last-read byte offset for a transcript file.

    Backwards-compatible: old int entries and new dict entries both work.
    """
    data = _load_offset_data()
    return _normalize_entry(data.get(str(Path(path).resolve()), 0))['offset']


def _update_offset_locked(mutate):
    """Read-modify-write the whole offset store under ONE exclusive lock.

    Both the read and the write happen while the same fd holds LOCK_EX, so
    concurrent writers (the turn watcher + interactive calls) can neither corrupt
    the JSON nor lose each other's updates to different keys. Always writes the
    dict format, so it never regresses claude-transcript's richer entries.
    """
    OFFSET_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(OFFSET_FILE, os.O_RDWR | os.O_CREAT, 0o644)
    with os.fdopen(fd, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            raw = f.read()
            try:
                data = json.loads(raw) if raw.strip() else {}
            except json.JSONDecodeError:
                data = {}
            mutate(data)
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def save_offset(path, offset: int):
    """Save the last-read byte offset for a transcript file (dict format).

    Preserves any existing turn counts on the entry; atomic under a single lock.
    """
    key = str(Path(path).resolve())

    def mutate(data):
        entry = _normalize_entry(data.get(key, 0))
        entry['offset'] = offset
        data[key] = entry

    _update_offset_locked(mutate)


def clear_offset(path):
    """Remove the offset entry for a file (used by --reset). Non-destructive to
    every other entry; atomic under a single lock."""
    key = str(Path(path).resolve())
    _update_offset_locked(lambda data: data.pop(key, None))


# ============================================================================
# Pair extraction (for transcript-extract.py compatibility)
# ============================================================================

def get_new_pairs(filepath, start_offset=0):
    """Read file from offset, extract all user->assistant pairs.

    Returns (pairs_list, new_offset) where pairs_list is [(user_msg, asst_msg), ...].
    Walks up parent chain to find real user messages.
    Groups consecutive assistant responses to same user question.
    """
    messages = []
    uuid_map = {}

    with open(filepath, 'r') as f:
        f.seek(start_offset)
        while True:
            line = f.readline()
            if not line:
                break
            msg = parse_line(line)
            if msg:
                messages.append(msg)
                uuid_map[msg['uuid']] = msg
        new_offset = f.tell()

    def find_real_user(uuid, visited=None):
        if visited is None:
            visited = set()
        if not uuid or uuid in visited:
            return None
        visited.add(uuid)
        node = uuid_map.get(uuid)
        if not node:
            return None
        if node['type'] == 'user':
            if (node['content'] and not node['is_meta']
                    and not node['content'].startswith('<')):
                return node
        return find_real_user(node.get('parent'), visited)

    user_to_assistant = {}
    for msg in messages:
        if msg['type'] == 'assistant' and msg['content']:
            user_msg = find_real_user(msg['parent'])
            if user_msg:
                user_uuid = user_msg['uuid']
                existing = user_to_assistant.get(user_uuid)
                if not existing or len(msg['content']) > len(existing[1]['content']):
                    user_to_assistant[user_uuid] = (user_msg, msg)

    pairs = list(user_to_assistant.values())
    pairs.sort(key=lambda p: p[0]['timestamp'])
    return pairs, new_offset


def stream_chat(filepath, skip_meta=False):
    """Stream all chat messages from file, merging consecutive same-type."""
    for msg in iter_messages(filepath):
        if skip_meta:
            if msg['is_meta'] or msg['content'].startswith('<'):
                continue
        if msg['content']:
            yield msg


# ============================================================================
# Incremental turn extraction — what a turn-by-turn watcher needs
# ============================================================================
#
# Pairs (get_new_pairs) are the WRONG granularity for watching a live executor:
# an executor session is often 1 user turn followed by dozens of assistant turns
# that are pure tool_use/tool_result, so a pair-based reader returns nothing for
# the whole run. These functions emit ONE record per assistant turn (text +
# tool_use), per real user message, and per tool_result batch (truncated).

def summarize_tool_use(block: dict, max_chars: int = 300) -> dict:
    """Compact {name, summary} for a tool_use block. Summary is the argument
    that matters per tool (Bash->command, Read/Write/Edit->file_path, ...),
    truncated so it never floods a watcher's token budget."""
    name = block.get('name', 'unknown')
    inp = block.get('input') or {}
    if not isinstance(inp, dict):
        summary = str(inp)
    elif name == 'Bash':
        summary = inp.get('command', '')
    elif name in ('Read', 'Write', 'Edit', 'MultiEdit'):
        summary = inp.get('file_path', '')
    elif name == 'NotebookEdit':
        summary = inp.get('notebook_path', '')
    elif name in ('Grep', 'Glob'):
        summary = inp.get('pattern', '')
    elif name in ('Task', 'Agent'):
        summary = inp.get('description') or inp.get('prompt', '')
    else:
        summary = json.dumps(inp, ensure_ascii=False)
    summary = str(summary).strip()
    if len(summary) > max_chars:
        summary = summary[:max_chars] + '…'
    return {'name': name, 'summary': summary}


def _truncate(text: str, max_chars: int) -> str:
    text = str(text).strip()
    return text[:max_chars] + '…' if len(text) > max_chars else text


def message_to_turn(msg: dict, tool_result_chars: int = 200) -> dict | None:
    """Build a compact turn record from a parse_line() message, or None if the
    entry carries nothing useful (e.g. a thinking-only assistant entry).

    Shapes:
      {'type':'assistant','timestamp','text','tools':[{name,summary}]}
      {'type':'user','timestamp','text'}
      {'type':'tool_result','timestamp','results':[str,...]}
    """
    raw = msg.get('raw_content', '')
    ts = msg.get('timestamp', '')

    if msg['type'] == 'assistant':
        tools = []
        if isinstance(raw, list):
            for b in raw:
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    tools.append(summarize_tool_use(b))
        text = msg.get('content', '')
        if not text and not tools:
            return None  # thinking-only / empty — skip
        return {'type': 'assistant', 'timestamp': ts, 'text': text, 'tools': tools}

    if msg['type'] == 'user':
        if isinstance(raw, list):
            results = []
            for b in raw:
                if isinstance(b, dict) and b.get('type') == 'tool_result':
                    content = b.get('content', '')
                    if isinstance(content, list):
                        content = ' '.join(
                            str(c.get('text', '')) for c in content if isinstance(c, dict)
                        )
                    results.append(_truncate(content, tool_result_chars) or '(no output)')
            if results:
                return {'type': 'tool_result', 'timestamp': ts, 'results': results}
            return None
        # string content = a real human message
        if isinstance(raw, str) and msg.get('content') and not msg.get('is_meta'):
            return {'type': 'user', 'timestamp': ts, 'text': msg['content']}
        return None

    return None


def get_new_turns(filepath, start_offset: int = 0, tool_result_chars: int = 200):
    """Read from start_offset, return (turns, new_offset).

    Partial-line safe: only consumes up to the last newline and advances the
    offset by exactly those bytes, so a turn written while Claude is mid-flush is
    picked up next call instead of being split and dropped. Caller is responsible
    for resetting start_offset to 0 when the file was truncated (offset > size).
    """
    with open(filepath, 'rb') as f:
        f.seek(start_offset)
        chunk = f.read()

    nl = chunk.rfind(b'\n')
    if nl == -1:
        return [], start_offset  # no complete new line yet
    complete = chunk[:nl + 1]
    new_offset = start_offset + len(complete)

    turns = []
    for line in complete.decode('utf-8', errors='replace').splitlines():
        msg = parse_line(line)
        if not msg:
            continue
        turn = message_to_turn(msg, tool_result_chars)
        if turn:
            turns.append(turn)
    return turns, new_offset


def format_turn_text(turn: dict) -> str:
    """Human-readable rendering of one turn (mirrors --chat style)."""
    ts = turn.get('timestamp', '')
    if turn['type'] == 'assistant':
        out = [f"[{ts}] ASSISTANT:"]
        if turn.get('text'):
            out.append(turn['text'])
        for t in turn.get('tools', []):
            out.append(f"  ⚡ {t['name']}: {t['summary']}" if t['summary'] else f"  ⚡ {t['name']}")
        return '\n'.join(out)
    if turn['type'] == 'user':
        return f"[{ts}] USER:\n{turn['text']}"
    if turn['type'] == 'tool_result':
        return f"[{ts}] TOOL_RESULT:\n" + '\n'.join(turn['results'])
    return ''


# ============================================================================
# CLI
# ============================================================================

def _cli():
    import argparse

    p = argparse.ArgumentParser(
        prog='claude-transcript',
        description='Parse and analyze Claude Code transcript JSONL files'
    )
    p.add_argument('file', help='Path to .jsonl transcript')
    p.add_argument('--metrics', action='store_true', help='JSON metrics output')
    p.add_argument('--chat', action='store_true', help='Full conversation')
    p.add_argument('--last', action='store_true', help='Last exchange')
    p.add_argument('--exchanges', type=int, metavar='N', help='Last N exchanges')
    p.add_argument('--new', action='store_true',
                   help='Incremental: emit assistant turns (text + tool_use) added '
                        'since the last --new call, tracked by byte offset')
    p.add_argument('--format', choices=['text', 'json'], default='text',
                   help='--new output format; json = one JSON object per line (JSONL)')
    p.add_argument('--truncate', type=int, default=200, metavar='N',
                   help='--new: max chars for tool_result / tool args (default 200)')
    p.add_argument('--dry-run', action='store_true',
                   help='--new: print turns but do NOT advance the saved offset')
    p.add_argument('--reset', action='store_true',
                   help='--new: clear the saved offset for this file, then exit')

    args = p.parse_args()
    path = Path(args.file).resolve()

    if args.reset:
        clear_offset(path)
        print(f"Reset offset for {path.name}", file=sys.stderr)
        return

    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    if args.new:
        start_offset = load_offset(path)
        size = path.stat().st_size
        if start_offset > size:  # truncated / new session — start over
            start_offset = 0
        turns, new_offset = get_new_turns(path, start_offset, args.truncate)

        for turn in turns:
            if args.format == 'json':
                print(json.dumps(turn, ensure_ascii=False))
            else:
                print(format_turn_text(turn) + '\n')
        if not turns and args.format != 'json':
            print(f"No new turns in {path.name}", file=sys.stderr)

        if not args.dry_run:
            save_offset(path, new_offset)
        return

    if args.chat:
        msgs = list(stream_chat(path, skip_meta=True))
        # Merge consecutive same-type
        merged = []
        for m in msgs:
            if merged and merged[-1]['type'] == m['type']:
                merged[-1]['content'] += '\n\n' + m['content']
            else:
                merged.append(m.copy())
        for m in merged:
            role = 'USER' if m['type'] == 'user' else 'ASSISTANT'
            print(f"[{m['timestamp']}] {role}:\n{m['content']}\n")

    elif args.last:
        exs = recent_exchanges(path, count=1)
        if exs:
            ex = exs[-1]
            u, a = ex['user'], ex['assistant']
            print(f"[{u['timestamp']}] USER:\n{u['content']}\n")
            print(f"[{a['timestamp']}] ASSISTANT:\n{a['content']}\n")
        else:
            print("No exchanges found.", file=sys.stderr)

    elif args.exchanges:
        exs = recent_exchanges(path, count=args.exchanges)
        for ex in exs:
            u, a = ex['user'], ex['assistant']
            print(f"[{u['timestamp']}] USER:\n{u['content']}\n")
            print(f"[{a['timestamp']}] ASSISTANT:\n{a['content']}\n")
            print("---\n")

    else:
        # Default: metrics summary (--metrics for JSON)
        m = metrics(path)
        if args.metrics:
            print(json.dumps(m, indent=2))
        else:
            size_kb = m['size_bytes'] / 1024
            print(f"Size:            {size_kb:.1f} KB")
            print(f"User turns:      {m['user_turns']}")
            print(f"Assistant turns:  {m['assistant_turns']}")


if __name__ == '__main__':
    _cli()
