# mobile-claude

Access Claude Code sessions from your phone via web browser.

## Features

- View all tmux sessions
- Real-time transcript streaming via WebSocket
- Send messages to any session
- Mobile-optimized UI
- Works over Tailscale for secure remote access

## Requirements

- Python 3.8+
- FastAPI + uvicorn
- tmux (sessions to access)
- Tailscale (optional, for remote access)

## Installation

```bash
cd mobile-claude

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Start server
python server.py

# Or with uvicorn directly
uvicorn server:app --host 0.0.0.0 --port 8080
```

Access at `http://localhost:8080` or via Tailscale IP.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Mobile UI |
| `GET /transcript` | Transcript viewer |
| `GET /api/sessions` | List tmux sessions |
| `POST /api/sessions/{name}` | Create session |
| `WS /ws/{session}` | WebSocket for real-time updates |

## Architecture

```
mobile-claude/
├── server.py              # FastAPI app
├── transcript_stream.py   # WebSocket transcript streaming
├── static/
│   ├── index.html        # Session list UI
│   └── transcript.html   # Transcript viewer
└── requirements.txt
```

## Remote Access

For phone access outside your network:

1. Install Tailscale on both devices
2. Start server: `python server.py`
3. Access via Tailscale IP: `http://100.x.x.x:8080`

## License

MIT
