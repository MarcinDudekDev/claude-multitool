---
name: stario
description: Python web framework for real-time hypermedia applications. Built on Starlette + DataStar with Go-style handlers (Context, Writer), SSE streaming via w.patch/sync.
domain: backend
type: framework
frequency: occasional
commands: [stario]
tools: []
---

# Stario 2.0

Python web framework for real-time hypermedia. Built for DataStar integration.

## Quick Start

```bash
uv add stario
uv run python main.py
```

```python
import asyncio
from stario import Context, RichTracer, Stario, Writer

async def home(c: Context, w: Writer) -> None:
    w.html(Div("Hello Stario!"))  # For stario.html DSL elements

async def main():
    with RichTracer() as tracer:
        app = Stario(tracer)
        app.get("/", home)
        await app.serve(host="127.0.0.1", port=8000)

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Concepts

### Handler Signature (Go-style)

All handlers have the same signature:

```python
async def handler(c: Context, w: Writer) -> None:
    # c = Context (request, signals, app state)
    # w = Writer (response methods)
```

### Route Registration

```python
app = Stario(tracer)  # Pass tracer to constructor
app.get("/", home)
app.get("/search", search)
app.post("/save", save_data)
app.get("/load/*", load_item)  # Catch-all: c.req.tail = rest of path
```

### Response Methods

```python
# For stario.html DSL elements:
w.html(Div({"id": "main"}, "Content"))

# For raw HTML strings (from Jinja):
w.respond(html_string.encode(), b"text/html; charset=utf-8")

# Other responses:
w.json({"key": "value"})
w.text("Plain text")
w.redirect("/other-path")
```

### SSE Streaming (w.patch / w.sync)

```python
from stario.html import SafeString

async def stream_data(c: Context, w: Writer) -> None:
    # Update signals (reactive data)
    w.sync({"count": 5, "status": "loading"})

    # Patch DOM elements - use SafeString for raw HTML!
    w.patch(SafeString('<div id="results">Updated</div>'))

    # Or use stario.html DSL (no SafeString needed):
    w.patch(Div({"id": "results"}, "Updated"))
```

**IMPORTANT**: `w.patch()` expects `HtmlElement` type. Raw HTML strings get escaped! Wrap in `SafeString()`.

### Path Parameters (Catch-all)

Stario uses `/*` catch-all syntax, not `{param}`:

```python
app.get("/load/*", load_handler)
app.get("/define/*", define_handler)

async def load_handler(c: Context, w: Writer) -> None:
    item_name = c.req.tail  # Gets path after /load/
```

### Parsing Signals

DataStar sends signals with `$` prefix. Two options:

```python
# Option 1: Raw dict (recommended for Jinja templates)
async def search(c: Context, w: Writer) -> None:
    signals = await c.signals()
    q = signals.get("$q", "")  # Note: $ prefix!

# Option 2: Dataclass (for stario.html DSL apps)
# Note: Only works if signals DON'T have $ prefix
@dataclass
class HomeSignals:
    count: int = 0

async def increment(c: Context, w: Writer) -> None:
    signals = await c.signals(HomeSignals)
    signals.count += 1
    w.sync(signals)
```

### DataStar HTML DSL

```python
from stario import at, data
from stario.html import Div, Button

Div(
    data.signals({"count": 0}),          # data-signals='{...}'
    data.on("click", "$count++"),        # data-on-click="$count++"
    data.text("$count"),                 # data-text="$count"
)

Button(
    data.on("click", at.get("/load")),   # data-on-click="@get('/load')"
    "Load Data"
)
```

## Templates vs HTML DSL

**Option 1: Jinja templates (use w.respond)**
```python
from jinja2 import Environment, FileSystemLoader
templates = Environment(loader=FileSystemLoader("templates"))

async def home(c: Context, w: Writer) -> None:
    html = templates.get_template("index.html").render()
    w.respond(html.encode(), b"text/html; charset=utf-8")
```

**Option 2: stario.html DSL (use w.html)**
```python
from stario.html import Html, Head, Body, Div

async def home(c: Context, w: Writer) -> None:
    w.html(Html(Head(...), Body(Div("Hello"))))
```

## Key Differences from FastAPI + datastar-py

| FastAPI Pattern | Stario Pattern |
|-----------------|----------------|
| `@app.get("/path")` | `app.get("/path", handler)` |
| `async def handler(request):` | `async def handler(c: Context, w: Writer):` |
| `return HTMLResponse(html)` | `w.respond(html.encode(), b"text/html...")` |
| `yield SSE.patch_elements(html)` | `w.patch(SafeString(html))` |
| `yield SSE.patch_signals(dict)` | `w.sync(dict)` |
| `/items/{id}` path param | `/items/*` + `c.req.tail` |

## Gotchas

1. **Handler signature**: Always `(c: Context, w: Writer) -> None`
2. **Raw HTML strings**: Use `SafeString()` with `w.patch()` or `w.html()`
3. **Path params**: Use `/*` catch-all, access via `c.req.tail`
4. **Signal $ prefix**: DataStar sends `$q`, access as `signals.get("$q")`
5. **Python 3.14+ required**: Uses latest Python features
6. **Use `uv run`**: Manages venv automatically

## Resources

- [Stario GitHub](https://github.com/Bobowski/stario)
- [Stario Docs](https://stario.dev)
- [DataStar](https://data-star.dev)
