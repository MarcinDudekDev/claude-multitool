# Source: https://data-star.dev/guide/datastar_expressions

Datastar Expressions Guide 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) GuideStart building with explanations and interactive demos.[](/guide/getting_started)[](/guide/reactive_signals)[](/guide/datastar_expressions)[](#datastar-expressions)[](#using-javascript)[](#external-scripts)[](#web-components)[](#executing-scripts)[](/guide/backend_requests)[](/guide/the_tao_of_datastar)[](/guide/reactive_signals)[](/guide/backend_requests)
# Datastar Expressions

Datastar expressions are strings that are evaluated by `data-*` attributes. While they are similar to JavaScript, there are some important differences that make them more powerful for declarative hypermedia applications.
## Datastar Expressions [#](#datastar-expressions)

The following example outputs `1` because we’ve defined `foo` as a signal with the initial value `1`, and are using `$foo` in a `data-*` attribute.
```
<div data-signals:foo="1">
    <div data-text="$foo"></div>
</div>
```

A variable `el` is available in every Datastar expression, representing the element that the attribute is attached to.
```
<div data-text="el.offsetHeight"></div>
```

When Datastar evaluates the expression `$foo`, it first converts it to the signal value, and then evaluates that expression in a sandboxed context. This means that JavaScript can be used in Datastar expressions.
```
<div data-text="$foo.length"></div>
```

JavaScript operators are also available in Datastar expressions. This includes (but is not limited to) the ternary operator `?:`, the logical OR operator `||`, and the logical AND operator `&&`. These operators are helpful in keeping Datastar expressions terse.
```
[ 1](#334c802ff056426c_line_1)// Output one of two values, depending on the truthiness of a signal
[ 2](#334c802ff056426c_line_2)<div data-text="$landingGearRetracted ? 'Ready' : 'Waiting'"></div>
[ 3](#334c802ff056426c_line_3)
[ 4](#334c802ff056426c_line_4)// Show a countdown if the signal is truthy or the time remaining is less than 10 seconds
[ 5](#334c802ff056426c_line_5)<div data-show="$landingGearRetracted || $timeRemaining < 10">
[ 6](#334c802ff056426c_line_6)    Countdown
[ 7](#334c802ff056426c_line_7)</div>
[ 8](#334c802ff056426c_line_8)
[ 9](#334c802ff056426c_line_9)// Only send a request if the signal is truthy
<button data-on:click="$landingGearRetracted && @post('/launch')">
    Launch
</button>
```

Multiple statements can be used in a single expression by separating them with a semicolon.
```
<div data-signals:foo="1">
    <button data-on:click="$landingGearRetracted = true; @post('/launch')">
        Force launch
    </button>
</div>
```

Expressions may span multiple lines, but a semicolon must be used to separate statements. Unlike JavaScript, line breaks alone are not sufficient to separate statements.
```
<div data-signals:foo="1">
    <button data-on:click="
        $landingGearRetracted = true; 
        @post('/launch')
    ">
        Force launch
    </button>
</div>
```

## Using JavaScript [#](#using-javascript)

Most of your JavaScript logic should go in `data-*` attributes, since reactive signals and actions only work in [Datastar expressions](/guide/datastar_expressions).
> Caution: if you find yourself trying to do too much in Datastar expressions, **you are probably overcomplicating it™**.

Any JavaScript functionality you require that cannot belong in `data-*` attributes should be extracted out into [external scripts](#external-scripts) or, better yet, [web components](#web-components).
> Always encapsulate state and send **props down, events up**. 
### External Scripts [#](#external-scripts)

When using external scripts, you should pass data into functions via arguments and return a result. Alternatively, listen for custom events dispatched from them (props down, events up).

In this way, the function is encapsulated – all it knows is that it receives input via an argument, acts on it, and optionally returns a result or dispatches a custom event – and `data-*` attributes can be used to drive reactivity.
```
<div data-signals:result>
    <input data-bind:foo 
        data-on:input="$result = myfunction($foo)"
    >
    <span data-text="$result"></span>
</div>
```

```
function myfunction(data) {
    return `You entered: ${data}`;
}
```

If your function call is asynchronous then it will need to dispatch a custom event containing the result. While asynchronous code *can* be placed within Datastar expressions, Datastar will *not* await it.
```
<div data-signals:result>
    <input data-bind:foo 
           data-on:input="myfunction(el, $foo)"
           data-on:mycustomevent__window="$result = evt.detail.value"
    >
    <span data-text="$result"></span>
</div>
```

```
async function myfunction(element, data) {
    const value = await new Promise((resolve) => {
        setTimeout(() => resolve(`You entered: ${data}`), 1000);
    });
    element.dispatchEvent(
        new CustomEvent('mycustomevent', {detail: {value}})
    );
}
```

See the [sortable example](/examples/sortable).
### Web Components [#](#web-components)

[Web components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components) allow you create reusable, encapsulated, custom elements. They are native to the web and require no external libraries or frameworks. Web components unlock [custom elements](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements) – HTML tags with custom behavior and styling.

When using web components, pass data into them via attributes and listen for custom events dispatched from them (*props down, events up*).

In this way, the web component is encapsulated – all it knows is that it receives input via an attribute, acts on it, and optionally dispatches a custom event containing the result – and `data-*` attributes can be used to drive reactivity.
```
<div data-signals:result="''">
    <input data-bind:foo />
    <my-component
        data-attr:src="$foo"
        data-on:mycustomevent="$result = evt.detail.value"
    ></my-component>
    <span data-text="$result"></span>
</div>
```

```
[ 1](#2014036fa8cc027d_line_1)class MyComponent extends HTMLElement {
[ 2](#2014036fa8cc027d_line_2)    static get observedAttributes() {
[ 3](#2014036fa8cc027d_line_3)        return ['src'];
[ 4](#2014036fa8cc027d_line_4)    }
[ 5](#2014036fa8cc027d_line_5)
[ 6](#2014036fa8cc027d_line_6)    attributeChangedCallback(name, oldValue, newValue) {
[ 7](#2014036fa8cc027d_line_7)        const value = `You entered: ${newValue}`;
[ 8](#2014036fa8cc027d_line_8)        this.dispatchEvent(
[ 9](#2014036fa8cc027d_line_9)            new CustomEvent('mycustomevent', {detail: {value}})
        );
    }
}

customElements.define('my-component', MyComponent);
```

Since the `value` attribute is allowed on web components, it is also possible to use `data-bind` to bind a signal to the web component’s value. Note that a `change` event must be dispatched so that the event listener used by `data-bind` is triggered by the value change.

See the [web component example](/examples/web_component).
## Executing Scripts [#](#executing-scripts)

Just like elements and signals, the backend can also send JavaScript to be executed on the frontend using [backend actions](/reference/actions#backend-actions).
```
<button data-on:click="@get('/endpoint')">
    What are you talking about, HAL?
</button>
```

If a response has a `content-type` of `text/javascript`, the value will be executed as JavaScript in the browser.
```
alert('This mission is too important for me to allow you to jeopardize it.')
```
DemoWhat are you talking about, HAL?

If the response has a `content-type` of `text/event-stream`, it can contain zero or more [SSE events](/reference/sse_events). The example above can be replicated by including a `script` tag inside of a `datastar-patch-elements` SSE event.
```
event: datastar-patch-elements
data: elements <div id="hal">
data: elements     <script>alert('This mission is too important for me to allow you to jeopardize it.')</script>
data: elements </div>


```

If you *only* want to execute a script, you can `append` the script tag to the `body`.
```
event: datastar-patch-elements
data: mode append
data: selector body
data: elements <script>alert('This mission is too important for me to allow you to jeopardize it.')</script>


```

Most SDKs have an `ExecuteScript` helper function for executing a script. Here’s the code to generate the SSE event above using the Go SDK.
```
sse := datastar.NewSSE(writer, request)
sse.ExecuteScript(`alert('This mission is too important for me to allow you to jeopardize it.')`)
```
DemoWhat are you talking about, HAL?

We’ll cover event streams and [SSE events](/reference/sse_events) in more detail [later in the guide](/guide/backend_requests), but as you can see, they are just plain text events with a special syntax, made simpler by the [SDKs](/reference/sdks).[](/guide/reactive_signals)[](/guide/backend_requests)[](/star_federation)[](https://www.arcustech.com/)