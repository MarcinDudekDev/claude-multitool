---
name: stario
description: Python 3.14 web framework for real-time hypermedia apps. Own asyncio HTTP server (not ASGI), Go-style async handlers (Context, Writer), routes registered in an async-generator bootstrap(app, span) hook, markup attributes as POSITIONAL DICTS, and Datastar 1.0 SSE via a per-response SSE(writer) object.
domain: backend
type: framework
frequency: occasional
commands: [stario]
tools: []
---

# Stario 4.1

Small Python framework for realtime hypermedia apps. Asyncio-native HTTP stack
with its **own** built-in server (TCP or Unix socket) — **not an ASGI app**,
so it does not run under Uvicorn / Hypercorn / Gunicorn. The `stario` CLI
drives it via a `bootstrap(app, span)` entry point.

Docs: <https://stario.dev/docs> · Source: <https://github.com/bobowski/stario>

> **This skill documents 4.1.x, with 4.2 and 5.0 delta lists right below. Read the 5.0 list first for new code.** 4.0.0 (2026-06-25) was a hard break from 3.x:
> import paths, the bootstrap contract, markup calls, routing and the SSE API
> all changed, and the CLI lost every runtime flag. If you are reading 3.x code
> or a 3.x-era memory, see **Migrating 3.x to 4.x** at the bottom.
>
> Verified against the installed package `stario==4.1.1` on Python 3.14.7
> (2026-09-16) — read from source / `inspect.signature`, with the core shape
> smoke-tested against a running server. The docs site tracks 4.x.
>
> **4.2.0 deltas (measured on a real 4.2 app, 2026-09-24): where they conflict with the examples below, 4.2 wins:**
> - `app.add(Route("GET", "/u/{user}"), handler)`. `Route.get/post` classmethods are deprecated, and `Route.get(path)` takes only the path.
> - `StaticAssets(...).register(app)` is gone: use `assets = stario.Assets(dir, url_prefix=...)` + `await assets.attach(app)` in bootstrap; `assets.href("app.css")` gives the fingerprinted URL.
> - `responses.html(w, ...)` is **sync**, so `await` on it raises TypeError. `SSE` writes (`open`, `patch_elements`, `patch_signals`) are sync too.
> - Programmatic serve: `with NoOpTracer() as tr: Server(bootstrap, tr, config=ServerConfig(host=..., port=...)).run()`. `STARIO_*` env vars only affect the `stario` CLI.
> - Path params: `c.match.params["user"]`; query: `c.req.query.get("x")`; hold an SSE stream open with `async for ev in c.alive(queue_iter)` (cancels on disconnect).
> - `read_signals` raises `StarioError` on bad JSON, but deep-nested or wrong-typed signals get PAST it and 500 later: validate every signal's TYPE at the boundary and return 400. Never `str()` a client value (repr recursion 500s at around 70k nesting depth).
> - Datastar: `@get(url, {openWhenHidden: true})` for a per-tab stream, else a backgrounded tab drops it. `data-init` only fires under an element with `data-signals`.
>
> **5.0.x deltas (measured porting two real apps 4.3 -> 5.0.4, 2026-10-15). Where they conflict with anything above, 5 wins:**
> - Compiled package (Cython llhttp/nghttp2); wheels only for macOS arm64 / Linux glibc, CPython 3.12-3.14(t). No CLI: `asyncio.run(stario.serve(bootstrap, config=ServerConfig(host=..., port=...)))`. `serve(**host/port)` kwargs are gone.
> - `stario.responses` is gone: `w.html(x, status)`, `w.json`, `w.text`, `w.redirect`, `w.empty`; `w.respond(body, ctype, status)`, `write_headers`, `write`, `end` survive. `await w.drain()` = write-side backpressure (replace any `w._transport.get_write_buffer_size()` polling).
> - `HttpException` and `App.on_error` are gone. Use an app-local exception + `stario.http.middleware.catch_errors(...)` mounted with `app.use("/", ...)`; it only answers before headers are sent.
> - **SECURITY GOTCHA, cost a VERIFY round:** 5 percent-decodes each path segment BEFORE binding `{param}`, so `%2F` arrives as a literal `/` in a single-segment param (4.3 kept it as `%2F`). Every handler that built a filesystem path from a `{param}` became a traversal sink (`/api/clear/..%2f..%2fX` unlinked a file outside the data dir). Fix it as an invariant: middleware that 404s when a non-catch-all param holds `/` or `\`, PLUS validate ids at the sink. Encoded dot-segments (`%2e%2e/`) are canonicalised and 308-redirected before routing.
> - `stario.testing` harness/dispatch/transport are gone; `TestClient` speaks real HTTP/1.1 through the production protocol. A mid-body client cut surfaces as `RuntimeError("...Connection closed...")`, not "chunked". Writes on a closed connection are silent no-ops.

## Quick start

```bash
uv venv --python 3.14 && uv pip install stario
uv run stario watch main:bootstrap --watch .
STARIO_PORT=8765 uv run stario serve main:bootstrap
```

```python
# main.py
from stario import App, Context, Writer, Route, Span
from stario.markup import html as h
import stario.responses as responses

async def home(c: Context, w: Writer) -> None:
    await responses.html(w, h.Html(
        h.Head(h.Title("Hello")),
        h.Body(h.H1({"class": "title"}, "Hello world")),
    ))

async def bootstrap(app: App, span: Span):
    app.add(Route.get("/"), home)
    yield
    # teardown here
```

---

## Gotchas — read these first

### 1. Markup attributes are POSITIONAL DICTS, not kwargs

This is the highest-frequency error when writing 4.x, because every single
element goes through it and the failure is a bare `TypeError`.

```python
h.Div(id="out")                          # TypeError: unexpected keyword 'id'
h.Div({"id": "out", "class": "card"}, h.P("body"))   # correct
```

Attribute mappings come **before** any children. Several leading mappings are
allowed and render **in order** — they are *not* merged or deduplicated, so a
duplicate key renders as a duplicate attribute. The first non-mapping argument
starts the children; a mapping after that is an error.

Helpers `classes(*tokens)` and `styles({...})` from `stario.markup.attributes`
return pre-rendered `Attrs` fragments and also go in the leading positional slot.

### 2. `bootstrap` must be an async GENERATOR with exactly one `yield`

```python
async def bootstrap(app, span):     # startup above the yield
    app.add(Route.get("/"), home)
    yield
    ...                             # teardown below it
```

The CLI calls `inspect.isasyncgenfunction()` and **refuses a plain coroutine at
load time**, not at request time. A 3.x `async def bootstrap(...) -> None`
will not start at all.

### 3. `App()` requires a running event loop

Construct it inside `serve()`, inside bootstrap, or in async test code —
otherwise `StarioError("App() requires a running event loop")`.
`App.on_error` handlers must be `async def`.

### 4. One `SSE(w)` per response — there is no module-level `sse.*`

`from stario import datastar as ds` is **gone**, and so are the module-level
`datastar.sse.patch_elements` / `patch_signals` helpers that 3.x used.

### 5. CLI runtime flags are gone — configure with `STARIO_*` env vars

`--host`, `--port`, `--tracer`, compression, limits, timeouts, `--loop`,
`--unix-socket` were all removed in 4.0. **Stario does not auto-load dotenv
files.** `stario init` and the packaged CLI templates are gone too.

### 6. Elements are lazy tuples — `str(el)` is NOT HTML

Stario markup builds a nested tuple and only renders at write time. Printing an
element gives you a tuple repr, which looks like a bug but is not:

```python
str(h.Div({"id": "out"}, "x"))            # "('<div', ' id=\"out\"', ['x'], '</div>')"

from stario.markup import render
render(h.Div({"id": "out"}, "x"))         # '<div id="out">x</div>'   <- what you want
```

Use `stario.markup.render()` in tests, snapshots, and anywhere you need the
actual string. Handlers and `SSE.patch_elements` render for you — do not
pre-render before passing markup to them.

---

## Where symbols live

| Import from | Symbols |
|---|---|
| `stario` (root) | `App`, `Context`, `Writer`, `Route`, `UrlPath`, `Span`, `Handler`, `Middleware`, `HttpException`, `RedirectException`, `AssetManifest`, `StaticAssets`, `Relay` |
| `stario.routing` | `Route`, `UrlPath`, `Segment`, `normalize_path`, `append_query_fragment` |
| `stario.http` | `App`, `Context`, `Writer`, `Request`, `Router`, `Headers`, `ParsedQuery`, `RouteMatch`, `Middleware` |
| `stario.markup` | `html as h`, `svg`, `baked`, `render`, `escape`, `SafeString`, `Comment`, `Tag`, `Attrs`, `aria`, `slots`, `wire` |
| `stario.markup.attributes` | `classes`, `styles` |
| `stario.datastar` | `SSE`, `ModuleScript`, `at`, `data`, `read_signals` |
| `stario.responses` | `html`, `text`, `json`, `redirect`, `empty` |
| `stario.cookies`, `stario.testing`, `stario.telemetry` | as named |

The package root re-exports **framework primitives only**. `Router` and
`Request` are NOT at the root — import them from `stario.http`.

## Routing

```python
from stario import Route, UrlPath

app.add(Route.get("/"), home)              # 4.1+ preferred form
app.add(Route.post("/generate"), generate)
app.get("/items/{id}", show_item)          # path+method form, still present
app.use("/admin", auth_mw)                 # middleware scoped to a prefix
app.not_found("/api", api_404)             # prefix-scoped 404 / 405
app.method_not_allowed("/api", api_405)
```

`Route` (new in 4.1.0) is one method on one `UrlPath`:
`Route.get/query/post/put/patch/delete/head/options`. `UrlPath` stays the
method-free location used for composition, `href()`, and middleware prefixes:

```python
UrlPath.href(params=None, /, *, query=None, fragment=None, **params_kwargs) -> str
UrlPath("/users", host="api.example.com")      # host-aware; {tenant}.example.com works
```

**There is no `url_for` and there are no route names.** Build links from the
`Route` / `UrlPath` object itself.

HTTP `QUERY` (RFC 10008) is supported: `Route.query`, `app.query`,
`TestClient.query` — safe and idempotent, with the *body* carrying the query.
`at.fetch` deliberately does not emit `@query`; Datastar has no such action.

## Datastar / SSE

```python
from stario.datastar import SSE, ModuleScript, at, data, read_signals

async def generate(c: Context, w: Writer) -> None:
    signals = await read_signals(c.req)         # plain keys, NO leading "$"
    sse = SSE(w)
    sse.open()                                   # optional: headers before a slow first chunk
    sse.patch_signals({"status": "loading"})
    sse.patch_elements(h.Div({"id": "out"}, "hello"), selector="#out", mode="outer")
```

```python
SSE.patch_elements(content, *, mode=None, selector=None, namespace=None,
                   view_transition=False, view_transition_selector=None)
SSE.patch_signals(payload, *, only_if_missing=False)
SSE.navigate(url)                                # 3.x: sse.redirect(...)
SSE.remove(selector)
SSE.execute_script(code, *, auto_remove=True)    # 3.x: sse.execute(...)
```

`mode` in `outer | inner | prepend | append | before | after`;
`namespace` in `svg | mathml`. `content` may be `bytes`, `str`, or Stario markup.
Signal names and dotted paths are Python **snake_case**; prefer nested JSON
objects over dotted signal paths in `patch_signals`.

`read_signals(c.req)` reads the body on POST/PUT/PATCH and the `datastar` query
param on GET/DELETE.

Wire output:

```
event: datastar-patch-signals
data: signals {"n":2}

event: datastar-patch-elements
data: elements <div id="out">hello</div>
```

**Attributes** (`data.*`): `signals`, `signal`, `json_signals`, `on`,
`on_intersect`, `on_interval`, `on_raf`, `on_resize`, `on_signal_patch`, `text`,
`show`, `bind`, `class_`, `classes`, `style`, `styles`, `computed`, `effect`,
`init`, `ref`, `indicator`, `persist`, `ignore`, `ignore_morph`, `preserve_attr`,
`query_string`, `replace_url`, `scroll_into_view`, `view_transition`, `animate`,
`custom_validity`, `match_media`.

**Actions** (`at.*`): `get`, `post`, `put`, `patch`, `delete`, `fetch`, `peek`,
`set_all`, `toggle_all`, `clipboard`, `intl`, `fit`.

```python
data.on(event, expression, *, once, passive, capture, delay, debounce, throttle,
        view_transition, target, prevent, stop, case='kebab')
at.post(url, queries=None, *, content_type, include, exclude, selector, headers,
        open_when_hidden, payload, retry, retry_interval_ms, retry_scaler,
        retry_max_wait_ms, retry_max_count, request_cancellation)
```

Two 4.1.1 fixes worth knowing: `data.bind(name, prop=...)` / `data.bind(name,
event=...)` now emit a **key-only** attribute (Datastar bind is exclusive —
signal in the key *or* the value, never both, else Datastar raises
`KeyAndValueProvided`); and `data.persist(session=True)` emits
`data-persist__session` when `storage_key` is omitted.

`ModuleScript(src=DATASTAR_CDN_URL)` — default pins `datastar@v1.0.2` (jsDelivr).

## Responses

Unchanged from 3.x: `responses.html(w, content, status=200)`, `text`, `json`,
`redirect(w, url, status=307)`, `empty(w, status=204)`.

## Static assets

```python
from stario import AssetManifest, StaticAssets

manifest = AssetManifest("./static", url_prefix="/static")   # scans + fingerprints
StaticAssets(manifest).register(app)
manifest.href("app.css")                                     # fingerprinted URL
```

`AssetManifest(directory='./static', *, url_prefix='/static',
hash_chunk_size=4194304, include_hidden=False, follow_symlinks=False)` —
**hidden files are excluded by default**; pass `include_hidden=True` when
dotfiles are intentional.

`StaticAssets(manifest, *, cache_control='public, max-age=31536000, immutable',
cache_max_size=1048576, filesystem_chunk_size=65536,
precompress=('br','zstd','gzip'), content_types=None, compression=...)`, then
`.register(app)`. Supports `Range: bytes=…` on large streamed files (206/416,
one range per request) and exposes `StaticAssets.stats`.

## Running it & configuration

```bash
stario serve main:bootstrap
stario watch main:bootstrap --watch app/        # --watch / --watch-ignore only
STARIO_PORT=8765 STARIO_TRACER=noop python -m stario.cli.main serve main:bootstrap
```

`serve` / `watch` take **only the app spec**. Everything else is `STARIO_*` env:
`STARIO_PORT`, `STARIO_HOST`, `STARIO_TRACER`, `STARIO_LOOP`,
`STARIO_REUSE_ADDR`, `STARIO_TRACERS_SQLITE*`, `STARIO_TRACERS_JSON*`, …
(`stario serve --help` lists them). `ServerConfig` / `RequestPolicy` in
`stario.http.config` are the programmatic equivalents. CLI entry point is
`stario.cli.main:main`.

⚠️ With `STARIO_TRACER=noop` nothing reaches the span sink — anything that counts
log lines needs plain stdout writes.

⚠️ Pick a dedicated port per project; do not hardcode a common one like 8000.

## Errors, tasks, testing, telemetry

- `HttpException` is **4xx/5xx bodies only**. Use `RedirectException` for 3xx
  (standalone type, target in `.location`) and `responses.*` for 2xx.
  `HttpException.respond()` was removed.
- `ClientDisconnected`'s default handler calls `Writer.abort()` — no body.
- `app.create_task(coro, name=...)` for shutdown-aware background work;
  `app.shutdown` is a future, `app.shutting_down` a bool,
  `app.signal_shutdown()` completes it.
- Tests: `async with stario.testing.TestClient(bootstrap)` (pytest-asyncio) —
  takes an `App` *or* a bootstrap; `base_url='http://testserver'`,
  `follow_redirects=True`, `request_timeout=30.0`.
- Telemetry: `Tracer.create(..., parent=)` / `on_end(span)`; `Span.step()`,
  `Span.new_trace()`, `Span.link()`; `tracer.stats()` -> `TelemetryStats`.
  Traceback formatting moved to `stario.telemetry.formatters`
  (`stario.telemetry.tracebacks` removed). Bundled tracers lost `from_env()`.
  Finished spans ignore mutations after `end()`.
- **Delete old `stario-traces.sqlite3` files before upgrading** — there is no
  in-place SQLite migration.
- `TTYTracer` is the CLI default. (`RichTracer` went away back in 3.x.)

---

## Migrating 3.x to 4.x

Not a diffable update — import paths, the bootstrap contract and the markup call
convention all changed. Rewrite rather than patch.

| 3.x | 4.x |
|---|---|
| `h.Div(id="out", cls="card")` | `h.Div({"id": "out", "class": "card"}, ...)` — positional dict |
| `async def bootstrap(app, span) -> None:` | async generator with exactly one `yield` |
| `from stario import html as h` | `from stario.markup import html as h` |
| `from stario import datastar as ds` | `from stario.datastar import SSE, at, data, read_signals` |
| `sse.patch_elements(w, ...)` (module-level) | `sse = SSE(w)` then `sse.patch_elements(...)` |
| `sse.redirect(...)` | `SSE.navigate(...)` |
| `sse.execute(...)` | `SSE.execute_script(...)` |
| `app.mount(...)` / `Router.mount` | register full path patterns on `App`; `StaticAssets(manifest).register(app)` |
| `Router.push_middleware(...)` | `app.use(pattern, *middleware)` |
| `App.url_for(name, ...)` / route `name=` | `UrlPath(...).href(...)` / `Route.href(...)` / `AssetManifest.href(...)` — no route names exist |
| `stario serve --port N --tracer noop` | `STARIO_PORT=N STARIO_TRACER=noop stario serve ...` |
| `HttpException` for redirects | `RedirectException` |
| `stario init` | (removed) |
