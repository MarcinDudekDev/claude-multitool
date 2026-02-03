# Datastar Actions Reference

Actions are helper functions prefixed with `@` that provide secure, sandboxed operations.

## Backend Actions

### @get(url, options?)
Send GET request.

```html
<button data-on:click="@get('/data')">Fetch</button>
<button data-on:click="@get('/api', {indicator: 'loading'})">Load</button>
```

### @post(url, options?)
Send POST request.

```html
<button data-on:click="@post('/save')">Save</button>
```

### @put(url, options?)
Send PUT request.

```html
<button data-on:click="@put('/update')">Update</button>
```

### @patch(url, options?)
Send PATCH request.

```html
<button data-on:click="@patch('/partial')">Patch</button>
```

### @delete(url, options?)
Send DELETE request.

```html
<button data-on:click="@delete('/item')">Delete</button>
```

## Request Options

All backend actions accept an options object:

```javascript
{
	// Content type: 'json' (default), 'form', 'text'
	contentType: 'json',
	
	// Signal filter for what to send
	filterSignals: {
		include: /.*/, // regex
		exclude: /(^_|\._).*/ // exclude signals starting with _
	},
	
	// Form selector (when contentType is 'form')
	selector: null, // defaults to closest form
	
	// Additional headers
	headers: {},
	
	// Keep connection open when page hidden
	openWhenHidden: false,
	
	// Retry interval for SSE (ms)
	retryInterval: 1000,
	
	// Loading indicator signal name
	indicator: 'loading'
}
```

## Frontend Actions

### @setAll(value, filter?)
Set all matching signals to value.

```html
<!-- Set all signals -->
<button data-on:click="@setAll(0)">Reset All</button>

<!-- Set specific signals -->
<button data-on:click="@setAll(true, {include: /^flag/})">Enable Flags</button>

<!-- Exclude certain signals -->
<button data-on:click="@setAll('', {include: /.*/, exclude: /_temp$/})">Clear</button>
```

### @toggleAll(filter?)
Toggle all matching boolean signals.

```html
<!-- Toggle all booleans -->
<button data-on:click="@toggleAll()">Toggle All</button>

<!-- Toggle specific signals -->
<button data-on:click="@toggleAll({include: /^menu\.isOpen\./})">Toggle Menus</button>
```

### @peek(expression)
Access signal without subscribing to changes.

```html
<!-- This won't re-evaluate when $bar changes -->
<div data-text="@peek($bar) + $foo"></div>
```

## Response Types

### text/html
Morphs elements into DOM by ID.

```html
<!-- Backend returns -->
<div id="result">Updated content</div>
```

### application/json
Merges signals using JSON Merge Patch.

```javascript
// Backend returns
{foo: 'bar', count: 42}
```

### text/event-stream
Streams Server-Sent Events.

```
event: datastar-patch-elements
data: elements <div id="foo">content</div>

event: datastar-patch-signals
data: signals {count: 5}
```

### text/javascript
Executes JavaScript.

```javascript
// Backend returns
console.log('Hello from server');
alert('Data saved');
```

## Fetch Events

All backend actions trigger lifecycle events:

- `datastar-fetch:started` - Request begins
- `datastar-fetch:progress` - Download progress (ReadableStream)
- `datastar-fetch:ended` - Request completes
- `datastar-fetch:error` - Request fails

```html
<div data-on:datastar-fetch:started="$loading = true"
	 data-on:datastar-fetch:ended="$loading = false">
</div>
```
