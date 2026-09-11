# claude-transcript

Shared library for parsing Claude Code transcript JSONL files. Consolidates transcript parsing from 7+ independent implementations into one importable + CLI tool.

## Install

Symlink to `~/Tools/` (done by `install.sh`):

```bash
ln -sf .../claude-transcript/claude_transcript.py ~/Tools/claude_transcript.py
ln -sf ~/Tools/claude_transcript.py ~/Tools/claude-transcript
```

## Usage as library

```python
import sys, os; sys.path.insert(0, os.path.expanduser("~/Tools"))
from claude_transcript import metrics, extract_text, recent_exchanges
```

### Key functions

| Function | Description | Replaces |
|----------|-------------|----------|
| `extract_text(content)` | Extract text from string or content blocks | 7 implementations |
| `parse_line(line)` | Parse single JSONL line | 7 implementations |
| `has_text_content(entry)` | True if entry has real text (not tool_use/thinking) | **NEW** - fixes turn inflation |
| `metrics(path)` | `{size_bytes, assistant_turns, user_turns}` | context_monitor naive scan |
| `iter_messages(path, types, offset)` | Yield parsed messages | common.py parse_transcript |
| `tail_messages(path, nbytes)` | Read last N bytes, parse | tts_realtime.py tail read |
| `recent_exchanges(path, count)` | Last N user->assistant pairs | incremental_scribe.py |
| `load_offset(path)` / `save_offset(path, offset)` | File-locked offset tracking | transcript-extract.py |

## Usage as CLI

```bash
claude-transcript <file.jsonl>                  # metrics summary
claude-transcript --metrics <file.jsonl>        # JSON metrics
claude-transcript --chat <file.jsonl>           # full conversation
claude-transcript --last <file.jsonl>           # last exchange
claude-transcript --exchanges 5 <file.jsonl>    # last 5 exchanges
```

Incremental mode (`--new`) emits only the assistant turns added since the
last `--new` call, tracked per-file by byte offset:

```bash
claude-transcript --new <file.jsonl>              # new turns, advance offset
claude-transcript --new --format json <file.jsonl> # one JSON object per line (JSONL)
claude-transcript --new --truncate 500 <file.jsonl> # max chars for tool_result/args (default 200)
claude-transcript --new --dry-run <file.jsonl>    # print turns without advancing offset
claude-transcript --new --reset <file.jsonl>      # clear saved offset, then exit
```

## Turn counting fix

The naive method of counting `"type":"assistant"` lines inflates turn counts 3-6x because assistant entries include tool-only responses, thinking blocks, and meta messages. `has_text_content()` filters to only entries with actual text output.
