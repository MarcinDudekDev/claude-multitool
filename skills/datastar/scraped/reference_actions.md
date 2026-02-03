# Source: https://data-star.dev/reference/actions

Actions Reference 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ReferenceUsage reference for attributes, actions, SSE events, etc.[](/reference/attributes)[](/reference/actions)[``](#peek)[``](#setall)[``](#toggleall)[](#backend-actions)[``](#get)[``](#post)[``](#put)[``](#patch)[``](#delete)[](#options)[](#request-cancellation)[](#response-handling)[](#events)[](#pro-actions)[``](#clipboard)[``](#fit)[](/reference/rocket)[](/reference/sse_events)[](/reference/sdks)[](/reference/security)[](/reference/attributes)[](/reference/rocket)
# Actions

Datastar provides actions (helper functions) that can be used in Datastar expressions.
> The `@` prefix designates actions that are safe to use in expressions. This is a security feature that prevents arbitrary JavaScript from being executed in the browser. Datastar uses [`Function()` constructors](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/Function) to create and execute these actions in a secure and controlled sandboxed environment.
### `@peek()` [#](#peek)

> `@peek(callable: () => any)`

Allows accessing signals without subscribing to their changes in expressions.
```
<div data-text="$foo + @peek(() => $bar)"></div>
```

In the example above, the expression in the `data-text` attribute will be re-evaluated whenever `$foo` changes, but it will *not* be re-evaluated when `$bar` changes, since it is evaluated inside the `@peek()` action.
### `@setAll()` [#](#setall)

> `@setAll(value: any, filter?: {include: RegExp, exclude?: RegExp})`

Sets the value of all matching signals (or all signals if no filter is used) to the expression provided in the first argument. The second argument is an optional filter object with an `include` property that accepts a regular expression to match signal paths. You can optionally provide an `exclude` property to exclude specific patterns.
> The [Datastar Inspector](/datastar_pro#datastar-inspector) can be used to inspect and filter current signals and view signal patch events in real-time.
```
[ 1](#d69cd974fcb9f7cc_line_1)<!-- Sets the `foo` signal only -->
[ 2](#d69cd974fcb9f7cc_line_2)<div data-signals:foo="false">
[ 3](#d69cd974fcb9f7cc_line_3)    <button data-on:click="@setAll(true, {include: /^foo$/})"></button>
[ 4](#d69cd974fcb9f7cc_line_4)</div>
[ 5](#d69cd974fcb9f7cc_line_5)
[ 6](#d69cd974fcb9f7cc_line_6)<!-- Sets all signals starting with `user.` -->
[ 7](#d69cd974fcb9f7cc_line_7)<div data-signals="{user: {name: '', nickname: ''}}">
[ 8](#d69cd974fcb9f7cc_line_8)    <button data-on:click="@setAll('johnny', {include: /^user\./})"></button>
[ 9](#d69cd974fcb9f7cc_line_9)</div>

<!-- Sets all signals except those ending with `_temp` -->
<div data-signals="{data: '', data_temp: '', info: '', info_temp: ''}">
    <button data-on:click="@setAll('reset', {include: /.*/, exclude: /_temp$/})"></button>
</div>
```

### `@toggleAll()` [#](#toggleall)

> `@toggleAll(filter?: {include: RegExp, exclude?: RegExp})`

Toggles the boolean value of all matching signals (or all signals if no filter is used). The argument is an optional filter object with an `include` property that accepts a regular expression to match signal paths. You can optionally provide an `exclude` property to exclude specific patterns.
> The [Datastar Inspector](/datastar_pro#datastar-inspector) can be used to inspect and filter current signals and view signal patch events in real-time.
```
[ 1](#7419d4b8527c8da6_line_1)<!-- Toggles the `foo` signal only -->
[ 2](#7419d4b8527c8da6_line_2)<div data-signals:foo="false">
[ 3](#7419d4b8527c8da6_line_3)    <button data-on:click="@toggleAll({include: /^foo$/})"></button>
[ 4](#7419d4b8527c8da6_line_4)</div>
[ 5](#7419d4b8527c8da6_line_5)
[ 6](#7419d4b8527c8da6_line_6)<!-- Toggles all signals starting with `is` -->
[ 7](#7419d4b8527c8da6_line_7)<div data-signals="{isOpen: false, isActive: true, isEnabled: false}">
[ 8](#7419d4b8527c8da6_line_8)    <button data-on:click="@toggleAll({include: /^is/})"></button>
[ 9](#7419d4b8527c8da6_line_9)</div>

<!-- Toggles signals starting with `settings.` -->
<div data-signals="{settings: {darkMode: false, autoSave: true}}">
    <button data-on:click="@toggleAll({include: /^settings\./})"></button>
</div>
```

## Backend Actions [#](#backend-actions)

### `@get()` [#](#get)

> `@get(uri: string, options={  })`

Sends a `GET` request to the backend using the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API). The URI can be any valid endpoint and the response must contain zero or more [Datastar SSE events](/reference/sse_events).
```
<button data-on:click="@get('/endpoint')"></button>
```

By default, requests are sent with a `Datastar-Request: true` header, and a `{datastar: *}` object containing all existing signals, except those beginning with an underscore. This behavior can be changed using the [`filterSignals`](#filterSignals) option, which allows you to include or exclude specific signals using regular expressions.
> When using a `get` request, the signals are sent as a query parameter, otherwise they are sent as a JSON body.

When a page is hidden (in a background tab, for example), the default behavior for `get` requests is for the SSE connection to be closed, and reopened when the page becomes visible again. To keep the connection open when the page is hidden, set the [`openWhenHidden`](#openWhenHidden) option to `true`.
```
<button data-on:click="@get('/endpoint', {openWhenHidden: true})"></button>
```

It’s possible to send form encoded requests by setting the `contentType` option to `form`. This sends requests using `application/x-www-form-urlencoded` encoding.
```
<button data-on:click="@get('/endpoint', {contentType: 'form'})"></button>
```

It’s also possible to send requests using `multipart/form-data` encoding by specifying it in the `form` element’s [`enctype`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/enctype) attribute. This should be used when uploading files. See the [form data example](/examples/form_data).
```
<form enctype="multipart/form-data">
    <input type="file" name="file" />
    <button data-on:click="@get('/endpoint', {contentType: 'form'})"></button>
</form>
```

### `@post()` [#](#post)

> `@post(uri: string, options={  })`

Works the same as [`@get()`](#get) but sends a `POST` request to the backend.
```
<button data-on:click="@post('/endpoint')"></button>
```

### `@put()` [#](#put)

> `@put(uri: string, options={  })`

Works the same as [`@get()`](#get) but sends a `PUT` request to the backend.
```
<button data-on:click="@put('/endpoint')"></button>
```

### `@patch()` [#](#patch)

> `@patch(uri: string, options={  })`

Works the same as [`@get()`](#get) but sends a `PATCH` request to the backend.
```
<button data-on:click="@patch('/endpoint')"></button>
```

### `@delete()` [#](#delete)

> `@delete(uri: string, options={  })`

Works the same as [`@get()`](#get) but sends a `DELETE` request to the backend.
```
<button data-on:click="@delete('/endpoint')"></button>
```

### Options [#](#options)

All of the actions above take a second argument of options.
- `contentType` – The type of content to send. A value of `json` sends all signals in a JSON request. A value of `form` tells the action to look for the closest form to the element on which it is placed (unless a `selector` option is provided), perform validation on the form elements, and send them to the backend using a form request (no signals are sent). Defaults to `json`.
- `filterSignals` – A filter object with an `include` property that accepts a regular expression to match signal paths (defaults to all signals: `/.*/`), and an optional `exclude` property to exclude specific signal paths (defaults to all signals that do not have a `_` prefix: `/(^_|\._).*/`).
> The [Datastar Inspector](/datastar_pro#datastar-inspector) can be used to inspect and filter current signals and view signal patch events in real-time.
- `selector` – Optionally specifies a form to send when the `contentType` option is set to `form`. If the value is `null`, the closest form is used. Defaults to `null`.
- `headers` – An object containing headers to send with the request.
- `openWhenHidden` – Whether to keep the connection open when the page is hidden. Useful for dashboards but can cause a drain on battery life and other resources when enabled. Defaults to `false` for `get` requests, and `true` for all other HTTP methods.
- `payload` – Allows the fetch payload to be overridden with a custom object.
- `retry` – Determines when to retry requests. Can be `'auto'` (default, retries on network errors only), `'error'` (retries on `4xx` and `5xx` responses), `'always'` (retries on all non-`204` responses except redirects), or `'never'` (disables retries). Defaults to `'auto'`.
- `retryInterval` – The retry interval in milliseconds. Defaults to `1000` (one second).
- `retryScaler` – A numeric multiplier applied to scale retry wait times. Defaults to `2`.
- `retryMaxWaitMs` – The maximum allowable wait time in milliseconds between retries. Defaults to `30000` (30 seconds).
- `retryMaxCount` – The maximum number of retry attempts. Defaults to `10`.
- `requestCancellation` – Controls request cancellation behavior. Can be `'auto'` (default, cancels existing requests on the same element), `'disabled'` (allows concurrent requests), or an `AbortController` instance for custom control. Defaults to `'auto'`.
```
<button data-on:click="@get('/endpoint', {
    filterSignals: {include: /^foo\./},
    headers: {
        'X-Csrf-Token': 'JImikTbsoCYQ9oGOcvugov0Awc5LbqFsZW6ObRCxuq',
    },
    openWhenHidden: true,
    requestCancellation: 'disabled',
})"></button>
```

### Request Cancellation [#](#request-cancellation)

By default, when a new fetch request is initiated on an element, any existing request on that same element is automatically cancelled. This prevents multiple concurrent requests from conflicting with each other and ensures clean state management.

For example, if a user rapidly clicks a button that triggers a backend action, only the most recent request will be processed:
```
<!-- Clicking this button multiple times will cancel previous requests (default behavior) -->
<button data-on:click="@get('/slow-endpoint')">Load Data</button>
```

This automatic cancellation happens at the element level, meaning requests on different elements can run concurrently without interfering with each other.

You can control this behavior using the [`requestCancellation`](#requestCancellation) option:
```
<!-- Allow concurrent requests (no automatic cancellation) -->
<button data-on:click="@get('/endpoint', {requestCancellation: 'disabled'})">Allow Multiple</button>

<!-- Custom abort controller for fine-grained control -->
<div data-signals:controller="new AbortController()">
    <button data-on:click="@get('/endpoint', {requestCancellation: $controller})">Start Request</button>
    <button data-on:click="$controller.abort()">Cancel Request</button>
</div>
```

### Response Handling [#](#response-handling)

Backend actions automatically handle different response content types:
- `text/event-stream` – Standard SSE responses with [Datastar SSE events](/reference/sse_events).
- `text/html` – HTML elements to patch into the DOM.
- `application/json` – JSON encoded signals to patch.
- `text/javascript` – JavaScript code to execute in the browser.
#### `text/html`

When returning HTML (`text/html`), the server can optionally include the following response headers:
- `datastar-selector` – A CSS selector for the target elements to patch
- `datastar-mode` – How to patch the elements (`outer`, `inner`, `remove`, `replace`, `prepend`, `append`, `before`, `after`). Defaults to `outer`.
- `datastar-use-view-transition` – Whether to use the [View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API) when patching elements.
```
response.headers.set('Content-Type', 'text/html')
response.headers.set('datastar-selector', '#my-element')
response.headers.set('datastar-mode', 'inner')
response.body = '<p>New content</p>'
```

#### `application/json`

When returning JSON (`application/json`), the server can optionally include the following response header:
- `datastar-only-if-missing` – If set to `true`, only patch signals that don’t already exist.
```
response.headers.set('Content-Type', 'application/json')
response.headers.set('datastar-only-if-missing', 'true')
response.body = JSON.stringify({ foo: 'bar' })
```

#### `text/javascript`

When returning JavaScript (`text/javascript`), the server can optionally include the following response header:
- `datastar-script-attributes` – Sets the script element’s attributes using a JSON encoded string.
```
response.headers.set('Content-Type', 'text/javascript')
response.headers.set('datastar-script-attributes', JSON.stringify({ type: 'module' }))
response.body = 'console.log("Hello from server!");'
```

### Events [#](#events)

All of the actions above trigger `datastar-fetch` events during the fetch request lifecycle. The event type determines the stage of the request.
- `started` – Triggered when the fetch request is started.
- `finished` – Triggered when the fetch request is finished.
- `error` – Triggered when the fetch request encounters an error.
- `retrying` – Triggered when the fetch request is retrying.
- `retries-failed` – Triggered when all fetch retries have failed.
```
<div data-on:datastar-fetch="
    evt.detail.type === 'error' && console.log('Fetch error encountered')
"></div>
```

## Pro Actions [#](#pro-actions)

### `@clipboard()` [#](#clipboard)[Pro](/datastar_pro)

> `@clipboard(text: string, isBase64?: boolean)`

Copies the provided text to the clipboard. If the second parameter is `true`, the text is treated as [Base64](https://developer.mozilla.org/en-US/docs/Glossary/Base64) encoded, and is decoded before copying.
> Base64 encoding is useful when copying content that contains special characters, quotes, or code fragments that might not be valid within HTML attributes. This prevents parsing errors and ensures the content is safely embedded in `data-*` attributes.
```
<!-- Copy plain text -->
<button data-on:click="@clipboard('Hello, world!')"></button>

<!-- Copy base64 encoded text (will decode before copying) -->
<button data-on:click="@clipboard('SGVsbG8sIHdvcmxkIQ==', true)"></button>
```

### `@fit()` [#](#fit)[Pro](/datastar_pro)

> `@fit(v: number, oldMin: number, oldMax: number, newMin: number, newMax: number, shouldClamp=false, shouldRound=false)`

Linearly interpolates a value from one range to another. This is useful for converting between different scales, such as mapping a slider value to a percentage or converting temperature units.

The optional `shouldClamp` parameter ensures the result stays within the new range, and `shouldRound` rounds the result to the nearest integer.
```
[ 1](#b61835fa80d48826_line_1)<!-- Convert a 0-100 slider to 0-255 RGB value -->
[ 2](#b61835fa80d48826_line_2)<div>
[ 3](#b61835fa80d48826_line_3)    <input type="range" min="0" max="100" value="50" data-bind:slider-value>
[ 4](#b61835fa80d48826_line_4)    <div data-computed:rgb-value="@fit($sliderValue, 0, 100, 0, 255)">
[ 5](#b61835fa80d48826_line_5)        RGB Value: <span data-text="$rgbValue"></span>
[ 6](#b61835fa80d48826_line_6)    </div>
[ 7](#b61835fa80d48826_line_7)</div>
[ 8](#b61835fa80d48826_line_8)
[ 9](#b61835fa80d48826_line_9)<!-- Convert Celsius to Fahrenheit -->
<div>
    <input type="number" data-bind:celsius value="20" />
    <div data-computed:fahrenheit="@fit($celsius, 0, 100, 32, 212)">
        <span data-text="$celsius"></span>°C = <span data-text="$fahrenheit.toFixed(1)"></span>°F
    </div>
</div>

<!-- Map mouse position to element opacity (clamped) -->
<div
    data-signals:mouse-x="0"
    data-computed:opacity="@fit($mouseX, 0, window.innerWidth, 0, 1, true)"
    data-on:mousemove__window="$mouseX = evt.clientX"
    data-attr:style="'opacity: ' + $opacity"
>
    Move your mouse horizontally to change opacity
</div>
```
[](/reference/attributes)[](/reference/rocket)[](/star_federation)[](https://www.arcustech.com/)