# DataStar Gotchas

## Quick Reference

| # | Issue | Symptom | Fix |
|---|-------|---------|-----|
| 1 | snake_case signals | Silent failure, signals don't update | Rename to snake_case |
| 2 | Server-side state only | State resets, can't access localStorage | Move ALL state to server |
| 3 | Missing IDs | Wrong element updates | Add unique `id=` to morphed elements |
| 4 | FOUC on data-show | Flash of content before JS loads | Add `style="display:none"` |
| 5 | PHP output buffering | SSE hangs, "network error" | `while (ob_get_level()) ob_end_clean();` |
| 6 | SSE event names (v1.0) | Events not received | Use `datastar-patch-*` not `datastar-merge-*` |
| 7 | Signals not defined | Expression errors | Define parent signals before children |
| 8 | JSON response merge | Signals not deleted | Use `{obsolete: null}` to delete |
| 9 | SSE stays open | Connection persists | Close explicitly when done |
| 10 | No loops in DataStar | Trying to iterate in HTML | Render lists on backend, send HTML |
| 11 | Not a JS library | Accessing window.Datastar | Use declarative HTML attributes only |
| 12 | Event chaining wrong | All fetches trigger handler | Use `data-effect` not `data-on:datastar-fetch` |
| 13 | filterSignals syntax | Payload filtering fails | Use regex: `{filterSignals: {include: /^id$/}}` |
| 14 | executeScript unsupported | Script events ignored | Use MutationObserver instead (RC.7) |
| 15 | CSS animations work | Wondering about transitions | Use keyframe animations, they work! |
| 16 | Patch multiple fragments | Need to update several areas | Call `patchElements` multiple times |
| 17 | Elements must exist | `PatchElementsNoTargetsFound` | Render hidden elements, don't conditionally skip |
| 18 | Sibling signals shared | All buttons send same value | Set signal explicitly in click handler |
| 19 | Animation restart | Animation doesn't replay | Add `data-ts="timestamp"` to force re-render |

---

## Detailed Gotchas

### Gotcha #1: Signal names MUST be snake_case

**Symptom:** Signals don't update, no error shown.

**Wrong:**
```html
<div data-signals="{playerName: '', gameOver: false}">
```

**Correct:**
```html
<div data-signals="{player_name: '', game_over: false}">
```

**Detection pattern:** `data-signals=".*[a-z][A-Z]`

---

### Gotcha #2: Server-Side State is MANDATORY

DataStar expressions run in a **sandboxed Function() constructor**. They CANNOT access:
- `window` or `document`
- `localStorage` or `sessionStorage`
- Global variables (even if set via `window.myVar`)

**NEVER use localStorage for cart/user state with DataStar.** This is the #1 mistake.

**Correct approach (The DataStar Way):**
- Store ALL state on the server (session, cookie, database)
- Signals mirror server state, not client storage
- Every `@post`/`@get` sends signals -> server updates state -> returns SSE
- Server is the **single source of truth**

**Wrong approach (will waste hours debugging):**
- Storing cart in localStorage
- Trying to read localStorage in DataStar expressions
- Custom events to bridge JS <-> DataStar
- Vanilla JS workarounds for state

**See:** https://data-star.dev/shop for official shopping cart example

---

### Gotcha #3: Missing IDs

**Symptom:** Wrong element updates, morphing fails.

Elements that will be updated by SSE MUST have `id` attributes.

```html
<!-- Wrong - no ID -->
<div class="result"></div>

<!-- Correct -->
<div id="result" class="result"></div>
```

---

### Gotcha #4: FOUC (Flash of Unstyled Content)

**Problem:** Elements with `data-show` flash visible before JS loads.

**Fix:** Add inline style to hide by default:
```html
<div data-show="$loading" style="display:none">Loading...</div>
```

---

### Gotcha #5: PHP Output Buffering Breaks SSE

**Symptom:** SSE endpoint hangs, no events received, "network error" in console.

**Fix:** Add at TOP of PHP SSE handler:
```php
// CRITICAL: Disable ALL output buffering (WordPress adds multiple levels)
while (ob_get_level()) {
    ob_end_clean();
}
set_time_limit(0);
ignore_user_abort(true);

header('Content-Type: text/event-stream');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('X-Accel-Buffering: no'); // Nginx
header('Connection: keep-alive');

// Disable compression
ini_set('output_buffering', 'off');
ini_set('zlib.output_compression', false);
if (function_exists('apache_setenv')) {
    apache_setenv('no-gzip', '1');
}
```

---

### Gotcha #6: SSE Event Names Changed (v1.0)

**Old (deprecated):**
```
event: datastar-merge-signals
event: datastar-merge-fragments
```

**New (use these):**
```
event: datastar-patch-signals
data: signals {count: 5}

event: datastar-patch-elements
data: elements <div id="foo">Content</div>
```

---

### Gotcha #7: Signals Must Be Defined Before Use

Define parent signals before using them in children. DOM order matters.

```html
<!-- Wrong - using undefined signal -->
<div data-text="$count"></div>
<div data-signals="{count: 0}">...</div>

<!-- Correct - define first -->
<div data-signals="{count: 0}">
    <div data-text="$count"></div>
</div>
```

---

### Gotcha #10: NO LOOPS IN DATASTAR

DataStar does NOT have `data-for` or iteration. Render lists on backend and send HTML via `datastar-patch-elements`.

**Wrong (won't work):**
```html
<div data-for="item in $items">...</div>
```

**Correct:**
```html
<!-- Frontend -->
<div id="items-list"></div>

<!-- Backend sends HTML -->
event: datastar-patch-elements
data: elements <div id="items-list"><div>Item 1</div><div>Item 2</div></div>
```

---

### Gotcha #12: Event Chaining - Use data-effect

Don't use `data-on:datastar-fetch` for chaining - it's a global listener that triggers for ALL fetch events.

**Wrong:**
```html
<div data-on:datastar-fetch:success="@get('/next')">...</div>
```

**Correct - Use data-effect:**
```html
<div data-signals="{joined: false, connected: false}"
     data-effect="$joined && !$connected && @get('/stream')">
</div>
```

---

### Gotcha #13: filterSignals Syntax

Use regex patterns, not arrays.

**Wrong:**
```html
<button data-on:click="@post('/api', {only: ['id', 'name']})">
```

**Correct:**
```html
<button data-on:click="@post('/api', {filterSignals: {include: /^(id|name)$/}})">
```

---

### Gotcha #17: Elements Must Exist for Patching

Elements that SSE will patch MUST exist in DOM. Use `style="display:none"` instead of conditional PHP.

**Wrong:**
```php
<?php if ($show_notice): ?>
    <div id="notice">...</div>
<?php endif; ?>
```

**Correct:**
```html
<div id="notice" style="<?= $show_notice ? '' : 'display:none' ?>">...</div>
```

---

### Gotcha #18: CRITICAL - Sibling Signals Share Global State

When multiple sibling elements define the same signal name, they share GLOBAL state - last value wins!

**Wrong - all buttons send last product's ID:**
```html
{% for product in products %}
<article data-signals="{product_id: '{{ product.id }}'}">
    <button data-on:click="@post('/api/cart/add')">Add</button>
</article>
{% endfor %}
```

**Correct - set signal explicitly in click:**
```html
<section data-signals="{product_id: ''}">
{% for product in products %}
<article>
    <button data-on:click="$product_id = '{{ product.id }}'; @post('/api/cart/add')">Add</button>
</article>
{% endfor %}
</section>
```

---

### Gotcha #19: Animation Restart on Re-patch

When patching the same element multiple times (e.g., toast notifications), CSS animations won't restart because browser sees same element.

**Fix:** Add unique attribute to force re-render:
```html
<div class="toast" data-ts="<?= time() ?>">Message</div>
```

Or generate timestamp in backend:
```php
Datastar::patchElements('<div class="toast" data-ts="' . time() . '">Saved!</div>');
```
