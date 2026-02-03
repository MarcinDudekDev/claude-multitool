---
name: datastar
description: Build reactive hypermedia web applications with backend-driven UI updates. 10.7KB framework combining HTMX-style backend reactivity with Alpine.js-style frontend reactivity.
domain: frontend
type: framework
frequency: occasional
commands: [datastar]
tools: [~/Tools/memory]
---

# DataStar

Build reactive web applications with server-driven updates and declarative HTML attributes.

## Quick Start

```html
<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.7/bundles/datastar.js"></script>
```

**CRITICAL:** Signal names MUST use snake_case: `{player_name: ''}` NOT `{playerName: ''}`

## Core Concepts

### Signals (State)
```html
<div data-signals="{count: 0, name: ''}">
    <input data-bind:name />
    <div data-text="$count"></div>
    <div data-computed:doubled="$count * 2" data-text="$doubled"></div>
</div>
```

### Actions (Backend Requests)
```html
<button data-on:click="@get('/data')">Load</button>
<button data-on:click="@post('/save')" data-indicator:saving>Save</button>
```

### Backend Responses (SSE)
```
event: datastar-patch-elements
data: elements <div id="foo">Content</div>

event: datastar-patch-signals
data: signals {count: 5}
```

## Expert Agent

For DataStar work, the **datastar-expert** agent should be used. It has:
- Deep knowledge of all 19 gotchas
- Access to patterns, examples, and references
- Self-updating capability (can fetch latest docs)
- Memory integration (learns from past mistakes)

## Knowledge Modules

| Module | Description |
|--------|-------------|
| `modules/gotchas.md` | 19 critical pitfalls with fixes |
| `modules/core.md` | Architecture, signals, actions |
| `modules/best-practices.md` | Naming, performance, security |
| `modules/debugging.md` | Common errors and solutions |

## Reference Files

| Reference | Description |
|-----------|-------------|
| `references/attributes.md` | All data-* attributes |
| `references/actions.md` | All @ actions |
| `references/patterns.md` | UI patterns (forms, lists, etc.) |
| `references/sse-events.md` | SSE protocol, SDK examples |

## Examples

| Example | Description |
|---------|-------------|
| `examples/realtime-counter.html` | Simplest reactive example |
| `examples/form-validation.html` | Form with client-side validation |
| `examples/dynamic-list.html` | Add/remove items via SSE |
| `examples/todo-app.html` | Complete todo application |
| `examples/wp-sse-endpoint.php` | WordPress SSE handler |

## Top 5 Gotchas

1. **snake_case signals** - `player_name` not `playerName`
2. **Server is source of truth** - No localStorage for state
3. **Missing IDs** - Elements need `id=` for morphing
4. **FOUC prevention** - Add `style="display:none"` to data-show
5. **PHP output buffering** - Disable with `ob_end_clean()` for SSE

See `modules/gotchas.md` for all 19 gotchas.

## Memory Integration

Search DataStar memories:
```bash
~/Tools/memory search "datastar"
~/Tools/memory tag "datastar"
```

Store new learning:
```bash
~/Tools/memory store "learning" -t fact -i 8 -g "datastar"
```

## Command

Use `/datastar` for quick access:
- `/datastar` - Overview
- `/datastar gotchas` - List all gotchas
- `/datastar gotcha 5` - Specific gotcha detail
- `/datastar examples` - List examples
- `/datastar memory` - DataStar memories

## When to Use DataStar

**Good fit:** Server-rendered apps, real-time dashboards, forms, CRUD apps, multi-step workflows

**Not ideal:** Offline-first apps, heavy client computation, complex routing, gaming

## Scraped Documentation (55 pages from data-star.dev)

Full website content scraped as markdown in `scraped/` directory:

| Directory prefix | Count | Content |
|-----------------|-------|---------|
| `scraped/guide_*.md` | 5 | Getting started, signals, expressions, backend, tao |
| `scraped/reference_*.md` | 6 | Attributes, actions, rocket, SSE events, SDKs, security |
| `scraped/examples_*.md` | 27 | Active search, animations, bulk update, click-to-edit, todomvc, etc. |
| `scraped/how_tos_*.md` | 6 | Keydown binding, DRY code, polling, SSE keepalive, redirects |
| `scraped/essays_*.md` | 11 | Design philosophy, HTMX comparison, build steps, framework rationale |

## Training Dataset

`dataset.jsonl` — 508 instruction/output pairs (533KB) for fine-tuning:

| Category | Count | Source |
|----------|-------|--------|
| reference | 287 | Reference pages + skills knowledge |
| concept | 63 | Guide pages + core module |
| code_generation | 59 | Examples (HTML + backend snippets) |
| debugging | 31 | Gotchas + debugging module |
| sdk | 20 | GitHub repo SDK source + test cases |
| best_practices | 14 | Best practices module |
| howto | 12 | How-to articles |
| architecture | 11 | Essays |
| synthetic | 11 | Hand-crafted common Q&A |

## Official Resources

- **Docs:** https://data-star.dev
- **GitHub:** https://github.com/starfederation/datastar
- **Version:** 1.0.0-RC.7 (current)
