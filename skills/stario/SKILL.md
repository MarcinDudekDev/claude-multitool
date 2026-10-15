---
name: stario
description: Stario 5 - Python web framework for real-time hypermedia apps with Datastar. Own compiled asyncio HTTP server (not ASGI), Go-style async handlers (Context, Writer), async-generator bootstrap(app, span), markup attributes as positional dicts, Datastar SSE via SSE(w). Use when writing or porting a Stario app.
---

# Stario 5

Python framework for realtime hypermedia apps. It runs its **own** compiled HTTP
server and is not ASGI, so Uvicorn, Hypercorn and Gunicorn don't apply.
Docs: <https://stario.dev/docs> · Source: <https://github.com/bobowski/stario>

Verified against `stario==5.0.4` on Python 3.14 (2026-10-15). Wheels exist only for
macOS arm64 and Linux glibc, CPython 3.12-3.14. If you are reading 3.x or 4.x code,
see **Porting from 4.x** at the bottom. Don't copy old idioms forward.

## Minimal app

```python
# main.py
import asyncio
from stario import App, Context, Writer, Route, Span, ServerConfig, h, serve
from stario.datastar import SSE, ModuleScript, at, data, read_signals

HOME = Route("GET /")
INC = Route("POST /inc")

async def home(c: Context, w: Writer) -> None:
    w.html(h.Html(
        h.Head(ModuleScript()),                       # Datastar 1.0 from jsDelivr
        h.Body(h.Div(
            data.signals({"n": 0}),
            h.Button(data.on("click", at.post(INC.href())), "+"),
            h.Span({"id": "n"}, data.text("$n")),
        )),
    ))

async def inc(c: Context, w: Writer) -> None:
    sig = await read_signals(c.req)
    n = sig.get("n", 0)
    if not isinstance(n, int):                        # signals are untrusted
        return w.text("bad n", 400)
    SSE(w).patch_signals({"n": n + 1})

async def bootstrap(app: App, span: Span):
    app.add(HOME, home)
    app.add(INC, inc)
    yield                                             # teardown below

if __name__ == "__main__":
    asyncio.run(serve(bootstrap, config=ServerConfig(host="127.0.0.1", port=8765)))
```

There is no CLI. `serve(bootstrap, *, config=None, tracer=None)` is the entry point.

## Gotchas

1. **Attributes are positional dicts, not kwargs.** `h.Div(id="x")` raises `TypeError`.
   Write `h.Div({"id": "x", "class": "card"}, child, ...)`. Dicts come before
   children. Several leading dicts render in order and are not merged, so a duplicate
   key renders twice. `data.*` and `classes(...)` go in the same leading slot.
2. **`bootstrap` is an async generator with exactly one `yield`.** Startup goes above it
   and shutdown below. A plain `async def ... -> None` is rejected.
3. **Writer methods are sync.** `w.html(...)`, `SSE(w).patch_*` and friends return
   `None`, so `await w.html(...)` is a `TypeError`. The only awaitable is
   `await w.drain()`, which provides backpressure on large streamed writes.
4. **`str(element)` is not HTML.** Markup is lazy tuples. Use
   `stario.markup.render(el)` in tests and snapshots. Handlers render for you.
5. **Path params are percent-decoded before binding (security).** `/u/a%2Fb` gives
   `c.match.params["user"] == "a/b"`. Any handler that builds a filesystem path from
   a `{param}` is a traversal sink. Validate ids at the sink, e.g. with
   `re.fullmatch(r"[\w-]+", x)`, or add middleware that 404s when a single-segment
   param contains `/` or `\`.
6. **Validate signal types at the boundary.** `read_signals` raises `StarioError` on
   bad JSON, but wrong types and deep nesting get past it and fail later as 500s.
   Check every field and return 400.
7. **Datastar streams:** use `at.get(url, open_when_hidden=True)` for a per-tab
   stream, or a backgrounded tab drops it. `data.init` only fires under an element
   that has `data.signals`.

## Handlers and routing

```python
USER = Route("GET /u/{user}")          # one segment
FILE = Route("GET /f/{path...}")       # catch-all
SEND = Route("POST", "/rooms/{id}/send")   # two-arg form also works

app.add(USER, handler, middleware=[mw])
app.use("/admin", auth_mw)             # Middleware = Callable[[Handler], Handler]
app.not_found("/api", api_404)
app.method_not_allowed("/api", api_405)

USER.href("bob", query={"tab": "x"})   # -> /u/bob?tab=x ; there is no url_for
```

In a handler: `c.match.params["user"]`, `c.req.query.get("q")`, `await c.req.body()`,
`c.state` (per-request dict), and `c.app`. `c.disconnected` and `c.closing` report
the client and server state.

Responses go through `w`: `html(content, status)`, `text`, `json`,
`redirect(url, 307)`, `empty(204)`, and `respond(body, content_type, status)`. For
streaming, use `write_headers(status)` + `write(bytes)` + `end()`. Writes on a
closed connection are silent no-ops.

## Errors

```python
from stario import RedirectException
from stario.http.middleware import catch_errors

class NotFound(Exception): ...

async def not_found(c, w, exc): w.text("not found", 404)

app.use("/", catch_errors(NotFound, respond=not_found))   # in bootstrap
raise RedirectException(308, USER.href("bob"))            # in a handler
```

`catch_errors` only answers while nothing has been sent (`w.started` is False).
After that it re-raises and the response is aborted.

## Datastar / SSE

```python
sse = SSE(w)                  # one per response
sse.open()                    # optional: send headers before a slow first chunk
sse.patch_signals({"status": "ok"}, only_if_missing=False)
sse.patch_elements(h.Div({"id": "out"}, "hi"), selector="#out", mode="outer")
sse.remove("#toast"); sse.navigate("/done"); sse.execute_script("console.log(1)")
```

`mode` is one of `outer | inner | prepend | append | before | after`. Signal keys are
snake_case with no `$`. Hold a stream open until the client leaves with
`async for ev in c.alive(source): ...`, which cancels the task on disconnect or
shutdown.

Attributes live on `data.*` (`signals`, `on`, `text`, `show`, `bind`, `class_`,
`computed`, `effect`, `init`, `ref`, `indicator`, `persist`, `ignore_morph`, ...).
Actions live on `at.*` (`get`, `post`, `put`, `patch`, `delete`, `peek`, ...).
`stario.markup.data` is for static `data-*` HTML attributes only.

For pub/sub across connections, use `Relay`:
`async with relay.subscribe("room.*") as sub: async for subject, msg in sub: ...`
and `relay.publish("room.1", msg)`. Nothing is queued before the `async with` is
entered.

## Static files

```python
from stario import Assets, Files

assets = Assets("static", "/static")    # fingerprinted, immutable caching
await assets.attach(app)                # in bootstrap
assets.href("app.css")                  # -> /static/app.<hash>.css

uploads = Files("uploads", "/uploads")  # live files: ETag + Range
```

Hidden files are excluded unless `include_hidden=True`.

## Testing

```python
from stario.testing import TestClient

async def test_inc():
    async with TestClient(bootstrap) as client:
        r = await client.post("/inc", json={"n": 2})
        assert r.status_code == 200 and '"n":3' in r.text
```

`TestClient` speaks real HTTP/1.1 through the production protocol. It also has
`get/put/patch/delete/query/stream`, and `follow_redirects=True` by default.

## Porting from 4.x

| 4.x | 5.x |
|---|---|
| `stario serve main:bootstrap`, `STARIO_*` env | `asyncio.run(serve(bootstrap, config=ServerConfig(...)))` |
| `import stario.responses as responses; responses.html(w, x)` | `w.html(x)` |
| `Route.get("/x")` | `Route("GET /x")` |
| `AssetManifest` + `StaticAssets(...).register(app)` | `await Assets(dir, prefix).attach(app)` |
| `HttpException`, `App.on_error` | app exception + `catch_errors(...)` |
| `{param}` kept `%2F` encoded | decoded to `/`: re-audit filesystem sinks (gotcha 5) |
| `w._transport.get_write_buffer_size()` polling | `await w.drain()` |
| `from stario.markup import html as h` | still works; `from stario import h` is shorter |
