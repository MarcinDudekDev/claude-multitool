#!/usr/bin/env python3
"""Mobile Claude - Access tmux sessions from your phone via Tailscale.

This version uses capture-pane + send-keys instead of attaching,
which avoids the "dots" sizing issue entirely.
"""

import asyncio
import subprocess
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse

from transcript_stream import router as transcript_router

app = FastAPI(title="Mobile Claude")
STATIC_DIR = Path(__file__).parent / "static"

# Mount transcript streaming router
app.include_router(transcript_router)


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/transcript")
async def transcript_viewer():
    return FileResponse(STATIC_DIR / "transcript.html")


@app.get("/api/sessions")
async def list_sessions():
    """List all tmux sessions with their windows."""
    result = subprocess.run(
        ["tmux", "list-sessions", "-F", "#{session_name}:#{session_windows}:#{session_attached}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return {"sessions": [], "error": "No tmux sessions"}

    sessions = []
    for line in result.stdout.strip().split("\n"):
        if line:
            parts = line.split(":")
            sessions.append({
                "name": parts[0],
                "windows": int(parts[1]) if len(parts) > 1 else 1,
                "attached": parts[2] == "1" if len(parts) > 2 else False
            })
    return {"sessions": sessions}


@app.post("/api/sessions/{name}")
async def create_session(name: str, run_claude: bool = False):
    """Create a new tmux session, optionally with Claude Code running."""
    check = subprocess.run(["tmux", "has-session", "-t", name], capture_output=True)
    if check.returncode == 0:
        return {"created": name, "existed": True}

    if run_claude:
        result = subprocess.run(
            ["tmux", "new-session", "-d", "-s", name, "-c", str(Path.home() / "Tools"), "claude"],
            capture_output=True, text=True
        )
    else:
        result = subprocess.run(
            ["tmux", "new-session", "-d", "-s", name],
            capture_output=True, text=True
        )
    if result.returncode != 0:
        return JSONResponse({"error": result.stderr}, status_code=400)
    return {"created": name, "claude": run_claude}


def get_pane_size(session: str) -> tuple[int, int]:
    """Get pane width and height."""
    result = subprocess.run(
        ["tmux", "display-message", "-t", session, "-p", "#{pane_width},#{pane_height}"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        try:
            parts = result.stdout.strip().split(",")
            return int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            pass
    return 80, 24  # Default


def capture_pane(session: str) -> tuple[str, int, int, int, int]:
    """Capture pane content with cursor position, scrollback, and dimensions."""
    # Get pane content with scrollback (-S -150 = last 150 lines)
    content_result = subprocess.run(
        ["tmux", "capture-pane", "-t", session, "-p", "-e", "-S", "-150"],
        capture_output=True, text=True
    )
    content = content_result.stdout if content_result.returncode == 0 else ""

    # Get cursor position
    cursor_result = subprocess.run(
        ["tmux", "display-message", "-t", session, "-p", "#{cursor_x},#{cursor_y}"],
        capture_output=True, text=True
    )
    cursor_x, cursor_y = 0, 0
    if cursor_result.returncode == 0:
        try:
            parts = cursor_result.stdout.strip().split(",")
            cursor_x, cursor_y = int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            pass

    # Get pane dimensions
    cols, rows = get_pane_size(session)

    return content, cursor_x, cursor_y, cols, rows


def send_keys(session: str, keys: str):
    """Send keys to the tmux session."""
    subprocess.run(
        ["tmux", "send-keys", "-t", session, "-l", keys],  # -l for literal
        capture_output=True
    )


def send_special_key(session: str, key: str):
    """Send special key (Enter, C-c, etc.) to the tmux session."""
    subprocess.run(
        ["tmux", "send-keys", "-t", session, key],
        capture_output=True
    )


@app.websocket("/ws/{session}")
async def terminal_ws(websocket: WebSocket, session: str):
    """WebSocket endpoint - uses capture-pane instead of attaching (no dots!)."""
    await websocket.accept()

    last_content = ""
    last_cols = 0

    async def send_updates():
        """Periodically capture pane and send updates."""
        nonlocal last_content, last_cols
        while True:
            await asyncio.sleep(0.1)  # 100ms refresh rate
            try:
                content, cursor_x, cursor_y, cols, rows = capture_pane(session)

                # Send resize command if cols changed
                if cols != last_cols:
                    last_cols = cols
                    # Send special resize message (client will parse this)
                    await websocket.send_text(f"\x1b]RESIZE:{cols},{rows}\x07")

                if content != last_content:
                    last_content = content
                    # Clear screen, send content, position cursor
                    cursor_pos = f"\x1b[{cursor_y + 1};{cursor_x + 1}H"
                    await websocket.send_text(f"\x1b[2J\x1b[H{content}{cursor_pos}")
            except Exception:
                break

    update_task = asyncio.create_task(send_updates())

    try:
        while True:
            data = await websocket.receive()
            text = ""
            if "bytes" in data:
                text = data["bytes"].decode("utf-8", errors="ignore")
            elif "text" in data:
                text = data["text"]

            if text:
                # Handle special keys
                if text == "\r" or text == "\n":
                    send_special_key(session, "Enter")
                elif text == "\x03":  # Ctrl+C
                    send_special_key(session, "C-c")
                elif text == "\x04":  # Ctrl+D
                    send_special_key(session, "C-d")
                elif text == "\x1a":  # Ctrl+Z
                    send_special_key(session, "C-z")
                elif text == "\x7f" or text == "\x08":  # Backspace
                    send_special_key(session, "BSpace")
                elif text == "\x1b[A":  # Up arrow
                    send_special_key(session, "Up")
                elif text == "\x1b[B":  # Down arrow
                    send_special_key(session, "Down")
                elif text == "\x1b[C":  # Right arrow
                    send_special_key(session, "Right")
                elif text == "\x1b[D":  # Left arrow
                    send_special_key(session, "Left")
                elif text.startswith("\x1b"):  # Other escape sequences
                    pass  # Ignore for now
                else:
                    send_keys(session, text)
    except WebSocketDisconnect:
        pass
    finally:
        update_task.cancel()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8847)
