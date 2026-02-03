# DataStar Best Practices

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Signal names | snake_case | `player_name`, `is_loading` |
| Private signals | Prefix with `_` | `_internal_state` |
| Computed signals | Descriptive | `full_name`, `total_price`, `is_valid` |
| Indicators | Action-based | `loading`, `saving`, `deleting` |

## Performance

### Debounce Search Inputs (300-500ms)
```html
<input data-on:input__debounce-500="@get('/search')" />
```

### Throttle Scroll/Resize (100ms)
```html
<div data-on:scroll__throttle-100="@post('/track')" />
```

### Lazy Loading with Intersects
```html
<div data-intersects="@get('/load-more')">Loading...</div>
```

### Keep Computed Signals Simple
Heavy calculations belong on the backend, not in data-computed.

## Error Handling

```html
<div data-signals="{error: ''}">
    <button data-on:click="@post('/save')"
            data-on:datastar-fetch:error="$error = evt.detail.message">
        Save
    </button>
    <div data-show="$error"
         data-text="$error"
         style="display:none"
         class="error"></div>
</div>
```

## Security

- **Backend validates ALL signal data** - never trust client
- DataStar uses sandboxed Function() constructors
- Signal values are JSON - no code injection risk
- Always sanitize HTML before sending via SSE

## When to Use DataStar

### Good Fit
- Server-rendered apps needing interactivity
- Real-time dashboards/collaborative tools
- Forms with complex validation
- Multi-step workflows
- Live data visualization
- CRUD applications

### Not Ideal For
- Offline-first applications
- Heavy client-side computation
- Complex client-side routing (use SPA instead)
- Gaming or animation-heavy apps

## Anti-Patterns to Avoid

### DON'T: Use localStorage for state
```html
<!-- WRONG - DataStar can't access localStorage -->
<div data-signals="{cart: localStorage.getItem('cart')}">
```

### DON'T: Try to iterate in HTML
```html
<!-- WRONG - no data-for in DataStar -->
<div data-for="item in $items">
```

### DON'T: Access window.Datastar
DataStar is not a JS library - use HTML attributes only.

### DON'T: Chain with datastar-fetch events
```html
<!-- WRONG - triggers on ALL fetches -->
<div data-on:datastar-fetch:success="@get('/next')">
```

### DO: Use data-effect for reactive actions
```html
<!-- CORRECT -->
<div data-effect="$ready && @get('/stream')">
```
