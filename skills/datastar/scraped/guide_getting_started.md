# Source: https://data-star.dev/guide/getting_started

Getting Started Guide 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) GuideStart building with explanations and interactive demos.[](/guide/getting_started)[](#installation)[``](#data-*)[](#patching-elements)[](/guide/reactive_signals)[](/guide/datastar_expressions)[](/guide/backend_requests)[](/guide/the_tao_of_datastar)[]()[](/guide/reactive_signals)
# Getting Started

Datastar simplifies frontend development, allowing you to build backend-driven, interactive UIs using a [hypermedia-first](https://hypermedia.systems/hypermedia-a-reintroduction/) approach that extends and enhances HTML.

Datastar provides backend reactivity like [htmx](https://htmx.org/) and frontend reactivity like [Alpine.js](https://alpinejs.dev/) in a lightweight frontend framework that doesn’t require any npm packages or other dependencies. It provides two primary functions:
- Modify the DOM and state by sending events from your backend.
- Build reactivity into your frontend using standard `data-*` HTML attributes.
> Other useful resources include an AI-generated [deep wiki](https://deepwiki.com/starfederation/datastar), LLM-ingestible [code samples](https://context7.com/websites/data-star_dev), and [single-page docs](/docs).
## Installation [#](#installation)

The quickest way to use Datastar is to include it using a `script` tag that fetches it from a CDN.
```
<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/[[email protected]](/cdn-cgi/l/email-protection)/bundles/datastar.js"></script>
```

If you prefer to host the file yourself, download the [script](https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.7/bundles/datastar.js) or create your own bundle using the [bundler](/bundler), then include it from the appropriate path.
```
<script type="module" src="/path/to/datastar.js"></script>
```

To import Datastar using a package manager such as npm, Deno, or Bun, you can use an import statement.
```
// @ts-expect-error (only required for TypeScript projects)
import 'https://cdn.jsdelivr.net/gh/starfederation/[[email protected]](/cdn-cgi/l/email-protection)/bundles/datastar.js'
```

## `data-*` [#](#data-*)

At the core of Datastar are `[data-*](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/Use_data_attributes)` HTML attributes (hence the name). They allow you to add reactivity to your frontend and interact with your backend in a declarative way.
> The Datastar [VSCode extension](https://marketplace.visualstudio.com/items?itemName=starfederation.datastar-vscode) and [IntelliJ plugin](https://plugins.jetbrains.com/plugin/26072-datastar-support) provide autocompletion for all available `data-*` attributes.

The [`data-on`](/reference/attributes#data-on) attribute can be used to attach an event listener to an element and execute an expression whenever the event is triggered. The value of the attribute is a [Datastar expression](/guide/datastar_expressions) in which JavaScript can be used.
```
<button data-on:click="alert('I’m sorry, Dave. I’m afraid I can’t do that.')">
    Open the pod bay doors, HAL.
</button>
```
DemoOpen the pod bay doors, HAL. 

We’ll explore more data attributes in the [next section of the guide](/guide/reactive_signals).
## Patching Elements [#](#patching-elements)

With Datastar, the backend *drives* the frontend by **patching** (adding, updating and removing) HTML elements in the DOM.

Datastar receives elements from the backend and manipulates the DOM using a morphing strategy (by default). Morphing ensures that only modified parts of the DOM are updated, and that only data attributes that have changed are [reapplied](/reference/attributes#attribute-evaluation-order), preserving state and improving performance.

Datastar provides [actions](/reference/actions#backend-actions) for sending requests to the backend. The [`@get()`](/reference/actions#get) action sends a `GET` request to the provided URL using a [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) request.
```
<button data-on:click="@get('/endpoint')">
    Open the pod bay doors, HAL.
</button>
<div id="hal"></div>
```

> Actions in Datastar are helper functions that have the syntax `@actionName()`. Read more about actions in the [reference](/reference/actions).

If the response has a `content-type` of `text/html`, the top-level HTML elements will be morphed into the existing DOM based on the element IDs. 
```
<div id="hal">
    I’m sorry, Dave. I’m afraid I can’t do that.
</div>
```

We call this a “Patch Elements” event because multiple elements can be patched into the DOM at once.DemoOpen the pod bay doors, HAL. `Waiting for an order...` 

In the example above, the DOM must contain an element with a `hal` ID in order for morphing to work. Other [patching strategies](/reference/sse_events#datastar-patch-elements) are available, but morph is the best and simplest choice in most scenarios.

If the response has a `content-type` of `text/event-stream`, it can contain zero or more [SSE events](/reference/sse_events). The example above can be replicated using a `datastar-patch-elements` SSE event.
```
event: datastar-patch-elements
data: elements <div id="hal">
data: elements     I’m sorry, Dave. I’m afraid I can’t do that.
data: elements </div>


```

Because we can send as many events as we want in a stream, and because it can be a long-lived connection, we can extend the example above to first send HAL’s response and then, after a few seconds, reset the text.
```
[ 1](#75425fcee443f5f8_line_1)event: datastar-patch-elements
[ 2](#75425fcee443f5f8_line_2)data: elements <div id="hal">
[ 3](#75425fcee443f5f8_line_3)data: elements     I’m sorry, Dave. I’m afraid I can’t do that.
[ 4](#75425fcee443f5f8_line_4)data: elements </div>
[ 5](#75425fcee443f5f8_line_5)
[ 6](#75425fcee443f5f8_line_6)event: datastar-patch-elements
[ 7](#75425fcee443f5f8_line_7)data: elements <div id="hal">
[ 8](#75425fcee443f5f8_line_8)data: elements     Waiting for an order...
[ 9](#75425fcee443f5f8_line_9)data: elements </div>


```
DemoOpen the pod bay doors, HAL. `Waiting for an order...`

Here’s the code to generate the SSE events above using the SDKs.
```
[ 1](#9a2ca1e5256b094d_line_1);; Import the SDK's api and your adapter
[ 2](#9a2ca1e5256b094d_line_2)(require
[ 3](#9a2ca1e5256b094d_line_3) '[starfederation.datastar.clojure.api :as d*]
[ 4](#9a2ca1e5256b094d_line_4) '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]])
[ 5](#9a2ca1e5256b094d_line_5)
[ 6](#9a2ca1e5256b094d_line_6);; in a ring handler
[ 7](#9a2ca1e5256b094d_line_7)(defn handler [request]
[ 8](#9a2ca1e5256b094d_line_8)  ;; Create an SSE response
[ 9](#9a2ca1e5256b094d_line_9)  (->sse-response request
                  {on-open
                   (fn [sse]
                     ;; Patches elements into the DOM
                     (d*/patch-elements! sse
                                         "<div id=\"hal\">I’m sorry, Dave. I’m afraid I can’t do that.</div>")
                     (Thread/sleep 1000)
                     (d*/patch-elements! sse
                                         "<div id=\"hal\">Waiting for an order...</div>"))}))
```

```
[ 1](#f44629edb0ee8e24_line_1)using StarFederation.Datastar.DependencyInjection;
[ 2](#f44629edb0ee8e24_line_2)
[ 3](#f44629edb0ee8e24_line_3)// Adds Datastar as a service
[ 4](#f44629edb0ee8e24_line_4)builder.Services.AddDatastar();
[ 5](#f44629edb0ee8e24_line_5)
[ 6](#f44629edb0ee8e24_line_6)app.MapGet("/", async (IDatastarService datastarService) =>
[ 7](#f44629edb0ee8e24_line_7){
[ 8](#f44629edb0ee8e24_line_8)    // Patches elements into the DOM.
[ 9](#f44629edb0ee8e24_line_9)    await datastarService.PatchElementsAsync(@"<div id=""hal"">I’m sorry, Dave. I’m afraid I can’t do that.</div>");

    await Task.Delay(TimeSpan.FromSeconds(1));

    await datastarService.PatchElementsAsync(@"<div id=""hal"">Waiting for an order...</div>");
});
```

```
[ 1](#12da9ecc5eb6c0ce_line_1)import (
[ 2](#12da9ecc5eb6c0ce_line_2)    "github.com/starfederation/datastar-go/datastar"
[ 3](#12da9ecc5eb6c0ce_line_3)    time
[ 4](#12da9ecc5eb6c0ce_line_4))
[ 5](#12da9ecc5eb6c0ce_line_5)
[ 6](#12da9ecc5eb6c0ce_line_6)// Creates a new `ServerSentEventGenerator` instance.
[ 7](#12da9ecc5eb6c0ce_line_7)sse := datastar.NewSSE(w,r)
[ 8](#12da9ecc5eb6c0ce_line_8)
[ 9](#12da9ecc5eb6c0ce_line_9)// Patches elements into the DOM.
sse.PatchElements(
    `<div id="hal">I’m sorry, Dave. I’m afraid I can’t do that.</div>`
)

time.Sleep(1 * time.Second)

sse.PatchElements(
    `<div id="hal">Waiting for an order...</div>`
)
```

```
[ 1](#ec0a8b6cb3b2f9f2_line_1)import starfederation.datastar.utils.ServerSentEventGenerator;
[ 2](#ec0a8b6cb3b2f9f2_line_2)
[ 3](#ec0a8b6cb3b2f9f2_line_3)// Creates a new `ServerSentEventGenerator` instance.
[ 4](#ec0a8b6cb3b2f9f2_line_4)AbstractResponseAdapter responseAdapter = new HttpServletResponseAdapter(response);
[ 5](#ec0a8b6cb3b2f9f2_line_5)ServerSentEventGenerator generator = new ServerSentEventGenerator(responseAdapter);
[ 6](#ec0a8b6cb3b2f9f2_line_6)
[ 7](#ec0a8b6cb3b2f9f2_line_7)// Patches elements into the DOM.
[ 8](#ec0a8b6cb3b2f9f2_line_8)generator.send(PatchElements.builder()
[ 9](#ec0a8b6cb3b2f9f2_line_9)    .data("<div id=\"hal\">I’m sorry, Dave. I’m afraid I can’t do that.</div>")
    .build()
);

Thread.sleep(1000);

generator.send(PatchElements.builder()
    .data("<div id=\"hal\">Waiting for an order...</div>")
    .build()
);
```

```
[ 1](#f3e018490b34e95c_line_1)val generator = ServerSentEventGenerator(response)
[ 2](#f3e018490b34e95c_line_2)
[ 3](#f3e018490b34e95c_line_3)generator.patchElements(
[ 4](#f3e018490b34e95c_line_4)    elements = """<div id="hal">I’m sorry, Dave. I’m afraid I can’t do that.</div>""",
[ 5](#f3e018490b34e95c_line_5))
[ 6](#f3e018490b34e95c_line_6)
[ 7](#f3e018490b34e95c_line_7)Thread.sleep(ONE_SECOND)
[ 8](#f3e018490b34e95c_line_8)
[ 9](#f3e018490b34e95c_line_9)generator.patchElements(
    elements = """<div id="hal">Waiting for an order...</div>""",
)
```

```
[ 1](#bba6804d8105c490_line_1)use starfederation\datastar\ServerSentEventGenerator;
[ 2](#bba6804d8105c490_line_2)
[ 3](#bba6804d8105c490_line_3)// Creates a new `ServerSentEventGenerator` instance.
[ 4](#bba6804d8105c490_line_4)$sse = new ServerSentEventGenerator();
[ 5](#bba6804d8105c490_line_5)
[ 6](#bba6804d8105c490_line_6)// Patches elements into the DOM.
[ 7](#bba6804d8105c490_line_7)$sse->patchElements(
[ 8](#bba6804d8105c490_line_8)    '<div id="hal">I’m sorry, Dave. I’m afraid I can’t do that.</div>'
[ 9](#bba6804d8105c490_line_9));

sleep(1);

$sse->patchElements(
    '<div id="hal">Waiting for an order...</div>'
);
```

```
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response

@app.get('/open-the-bay-doors')
@datastar_response
async def open_doors(request):
    yield SSE.patch_elements('<div id="hal">I’m sorry, Dave. I’m afraid I can’t do that.</div>')
    await asyncio.sleep(1)
    yield SSE.patch_elements('<div id="hal">Waiting for an order...</div>')
```

```
[ 1](#67f62b7db54d2b98_line_1)require 'datastar'
[ 2](#67f62b7db54d2b98_line_2)
[ 3](#67f62b7db54d2b98_line_3)# Create a Datastar::Dispatcher instance
[ 4](#67f62b7db54d2b98_line_4)
[ 5](#67f62b7db54d2b98_line_5)datastar = Datastar.new(request:, response:)
[ 6](#67f62b7db54d2b98_line_6)
[ 7](#67f62b7db54d2b98_line_7)# In a Rack handler, you can instantiate from the Rack env
[ 8](#67f62b7db54d2b98_line_8)# datastar = Datastar.from_rack_env(env)
[ 9](#67f62b7db54d2b98_line_9)
# Start a streaming response
datastar.stream do |sse|
  # Patches elements into the DOM.
  sse.patch_elements %(<div id="hal">I’m sorry, Dave. I’m afraid I can’t do that.</div>)

  sleep 1
  
  sse.patch_elements %(<div id="hal">Waiting for an order...</div>)
end
```

```
[ 1](#dce2e42a1bbf1134_line_1)use async_stream::stream;
[ 2](#dce2e42a1bbf1134_line_2)use datastar::prelude::*;
[ 3](#dce2e42a1bbf1134_line_3)use std::thread;
[ 4](#dce2e42a1bbf1134_line_4)use std::time::Duration;
[ 5](#dce2e42a1bbf1134_line_5)
[ 6](#dce2e42a1bbf1134_line_6)Sse(stream! {
[ 7](#dce2e42a1bbf1134_line_7)    // Patches elements into the DOM.
[ 8](#dce2e42a1bbf1134_line_8)    yield PatchElements::new("<div id='hal'>I’m sorry, Dave. I’m afraid I can’t do that.</div>").into();
[ 9](#dce2e42a1bbf1134_line_9)
    thread::sleep(Duration::from_secs(1));
    
    yield PatchElements::new("<div id='hal'>Waiting for an order...</div>").into();
})
```

```
// Creates a new `ServerSentEventGenerator` instance (this also sends required headers)
ServerSentEventGenerator.stream(req, res, (stream) => {
    // Patches elements into the DOM.
    stream.patchElements(`<div id="hal">I’m sorry, Dave. I’m afraid I can’t do that.</div>`);

    setTimeout(() => {
        stream.patchElements(`<div id="hal">Waiting for an order...</div>`);
    }, 1000);
});
```

> In addition to your browser’s dev tools, the [Datastar Inspector](/datastar_pro#datastar-inspector) can be used to monitor and inspect SSE events received by Datastar.

We’ll cover event streams and [SSE events](/reference/sse_events) in more detail [later in the guide](/guide/backend_requests), but as you can see, they are just plain text events with a special syntax, made simpler by the [SDKs](/reference/sdks).[]()[](/guide/reactive_signals)[](/star_federation)[](https://www.arcustech.com/)