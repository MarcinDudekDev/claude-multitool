# Datastar Attributes Reference

## State Management

### data-signals
Define reactive state variables.

```html
<!-- Single signal -->
<div data-signals:foo="'initial'"></div>

<!-- Multiple signals -->
<div data-signals="{foo: 'bar', count: 0}"></div>

<!-- Nested signals -->
<div data-signals="{user: {name: 'John', age: 30}}"></div>
```

**Naming modifiers:**
- `__case` - Convert signal name casing
- `__ifmissing` - Only set if signal doesn't exist

### data-bind
Two-way binding between signal and element value.

```html
<input data-bind:username />
<input data-bind:email type="email" />
```

**Modifiers:**
- `__number` - Parse as number
- `__debounce` - Debounce updates (ms)

### data-computed
Create derived read-only signals.

```html
<!-- Inline expression -->
<div data-computed:fullName="$firstName + ' ' + $lastName"></div>

<!-- Object syntax -->
<div data-computed="{total: () => $price * $quantity}"></div>
```

### data-ref
Store element reference as signal.

```html
<div data-ref:myDiv></div>
<button data-on:click="$myDiv.classList.toggle('active')">Toggle</button>
```

## Display & Visibility

### data-text
Set text content from expression.

```html
<div data-text="$count"></div>
<div data-text="$name.toUpperCase()"></div>
```

### data-show
Toggle element visibility.

```html
<div data-show="$isVisible"></div>
<div data-show="$count > 5"></div>
```

### data-class
Conditionally add/remove classes.

```html
<!-- Single class -->
<div data-class:active="$isActive"></div>

<!-- Multiple classes -->
<div data-class="{active: $isActive, hidden: !$isVisible}"></div>
```

### data-attr
Set element attributes.

```html
<!-- Single attribute -->
<button data-attr:disabled="$loading">Submit</button>

<!-- Multiple attributes -->
<div data-attr="{title: $tooltip, disabled: $loading}"></div>
```

## Events

### data-on
Attach event listeners.

```html
<!-- Click event -->
<button data-on:click="$count++">Increment</button>

<!-- Multiple events -->
<input data-on:input="$value = el.value" 
	   data-on:blur="@post('/save')">

<!-- Custom events -->
<div data-on:mycustomevent="$data = evt.detail"></div>
```

**Event modifiers:**
- `__window` - Listen on window
- `__document` - Listen on document
- `__outside` - Trigger when clicking outside element
- `__once` - Fire only once
- `__passive` - Passive event listener
- `__capture` - Capture phase
- `__debounce` - Debounce (ms)
- `__throttle` - Throttle (ms)

**Key modifiers:**
- `__enter`, `__escape`, `__space`, `__up`, `__down`, etc.

### data-indicator
Set signal to true during request.

```html
<button data-on:click="@get('/data')" 
		data-indicator:loading>
	Fetch
</button>
<div data-show="$loading">Loading...</div>
```

## Side Effects

### data-effect
Execute expression when signals change.

```html
<div data-effect="console.log($count)"></div>
<div data-effect="$count > 10 && @post('/alert')"></div>
```

## Persistence

### data-persist
Persist signals to localStorage.

```html
<!-- Default key -->
<div data-persist></div>

<!-- Custom key -->
<div data-persist:myKey></div>
```

**Modifiers:**
- `__session` - Use sessionStorage

### data-query-string
Sync signals with URL query params.

```html
<div data-query-string></div>
<div data-query-string="{include: /search/, exclude: /temp/}"></div>
```

**Modifiers:**
- `__filter` - Filter empty values
- `__history` - Enable browser history

## Evaluation Control

### data-init
Run once on element initialization. Best for signal initialization.

```html
<!-- Initialize signals -->
<div data-init="$count = 0"></div>
```

**WARNING:** `data-init` does NOT reliably support backend actions (`@get`/`@post`) in Datastar RC.6/RC.7. For SSE auto-connect, use `data-effect` with a condition instead:

```html
<!-- CORRECT: SSE stream on page load using data-effect -->
<div data-signals="{stream_connected: false}">
	<div data-effect="!$stream_connected && @get('/stream')"></div>
	<div id="timeline">Loading...</div>
</div>
```

This pattern fires once when `$stream_connected` is false (initial load), then stops after SSE sets it to true.

### data-intersects
Execute when element enters viewport.

```html
<div data-intersects="@get('/load-more')"></div>
```

**Options:**
- `threshold` - Intersection threshold (0-1)
- `rootMargin` - Margin around root
- `root` - Root element selector
