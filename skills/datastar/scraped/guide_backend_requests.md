# Source: https://data-star.dev/guide/backend_requests

Backend Requests Guide 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) GuideStart building with explanations and interactive demos.[](/guide/getting_started)[](/guide/reactive_signals)[](/guide/datastar_expressions)[](/guide/backend_requests)[](#sending-signals)[](#nesting-signals)[](#reading-signals)[](#sse-events)[``](#data-indicator)[](#backend-actions)[](#congratulations)[](/guide/the_tao_of_datastar)[](/guide/datastar_expressions)[](/guide/the_tao_of_datastar)
# Backend Requests

Between [attributes](/reference/attributes) and [actions](/reference/actions), Datastar provides you with everything you need to build hypermedia-driven applications. Using this approach, the backend drives state to the frontend and acts as the single source of truth, determining what actions the user can take next.
## Sending Signals [#](#sending-signals)

By default, all signals (except for local signals whose keys begin with an underscore) are sent in an object with every backend request. When using a `GET` request, the signals are sent as a `datastar` query parameter, otherwise they are sent as a JSON body.

By sending **all** signals in every request, the backend has full access to the frontend state. This is by design. It is **not** recommended to send partial signals, but if you must, you can use the [`filterSignals`](/reference/actions#filterSignals) option to filter the signals sent to the backend.
### Nesting Signals [#](#nesting-signals)

Signals can be nested, making it easier to target signals in a more granular way on the backend.

Using dot-notation:
```
<div data-signals:foo.bar="1"></div>
```

Using object syntax:
```
<div data-signals="{foo: {bar: 1}}"></div>
```

Using two-way binding:
```
<input data-bind:foo.bar />
```

A practical use-case of nested signals is when you have repetition of state on a page. The following example tracks the open/closed state of a menu on both desktop and mobile devices, and the [toggleAll()](/reference/actions#toggleAll) action to toggle the state of all menus at once.
```
<div data-signals="{menu: {isOpen: {desktop: false, mobile: false}}}">
    <button data-on:click="@toggleAll({include: /^menu\.isOpen\./})">
        Open/close menu
    </button>
</div>
```

## Reading Signals [#](#reading-signals)

To read signals from the backend, JSON decode the `datastar` query param for `GET` requests, and the request body for all other methods.

All [SDKs](/reference/sdks) provide a helper function to read signals. Here’s how you would read the nested signal `foo.bar` from an incoming request.

No example found for Clojure
```
[ 1](#66acc484fc23e471_line_1)using StarFederation.Datastar.DependencyInjection;
[ 2](#66acc484fc23e471_line_2)
[ 3](#66acc484fc23e471_line_3)// Adds Datastar as a service
[ 4](#66acc484fc23e471_line_4)builder.Services.AddDatastar();
[ 5](#66acc484fc23e471_line_5)
[ 6](#66acc484fc23e471_line_6)public record Signals
[ 7](#66acc484fc23e471_line_7){
[ 8](#66acc484fc23e471_line_8)    [JsonPropertyName("foo")] [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
[ 9](#66acc484fc23e471_line_9)    public FooSignals? Foo { get; set; } = null;

    public record FooSignals
    {
        [JsonPropertyName("bar")] [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
        public string? Bar { get; set; }
    }
}

app.MapGet("/read-signals", async (IDatastarService datastarService) =>
{
    Signals? mySignals = await datastarService.ReadSignalsAsync<Signals>();
    var bar = mySignals?.Foo?.Bar;
});
```

```
[ 1](#90572ca558eb6621_line_1)import ("github.com/starfederation/datastar-go/datastar")
[ 2](#90572ca558eb6621_line_2)
[ 3](#90572ca558eb6621_line_3)type Signals struct {
[ 4](#90572ca558eb6621_line_4)    Foo struct {
[ 5](#90572ca558eb6621_line_5)        Bar string `json:"bar"`
[ 6](#90572ca558eb6621_line_6)    } `json:"foo"`
[ 7](#90572ca558eb6621_line_7)}
[ 8](#90572ca558eb6621_line_8)
[ 9](#90572ca558eb6621_line_9)signals := &Signals{}
if err := datastar.ReadSignals(request, signals); err != nil {
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
}
```

No example found for Java
```
[ 1](#7a559ddc10e7ab40_line_1)@Serializable
[ 2](#7a559ddc10e7ab40_line_2)data class Signals(
[ 3](#7a559ddc10e7ab40_line_3)    val foo: String,
[ 4](#7a559ddc10e7ab40_line_4))
[ 5](#7a559ddc10e7ab40_line_5)
[ 6](#7a559ddc10e7ab40_line_6)val jsonUnmarshaller: JsonUnmarshaller<Signals> = { json -> Json.decodeFromString(json) }
[ 7](#7a559ddc10e7ab40_line_7)
[ 8](#7a559ddc10e7ab40_line_8)val request: Request =
[ 9](#7a559ddc10e7ab40_line_9)    postRequest(
        body =
            """
            {
                "foo": "bar"
            }
            """.trimIndent(),
    )

val signals = readSignals(request, jsonUnmarshaller)
```

```
use starfederation\datastar\ServerSentEventGenerator;

// Reads all signals from the request.
$signals = ServerSentEventGenerator::readSignals();
```

```
from datastar_py.fastapi import datastar_response, read_signals

@app.get("/updates")
@datastar_response
async def updates(request: Request):
    # Retrieve a dictionary with the current state of the signals from the frontend
    signals = await read_signals(request)
```

```
# Setup with request
datastar = Datastar.new(request:, response:)

# Read signals
some_signal = datastar.signals[:some_signal]
```

No example found for Rust

No example found for TypeScript
## SSE Events [#](#sse-events)

Datastar can stream zero or more [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) (SSE) from the web server to the browser. There’s no special backend plumbing required to use SSE, just some special syntax. Fortunately, SSE is straightforward and [provides us with some advantages](/essays/event_streams_all_the_way_down), in addition to allowing us to send multiple events in a single response (in contrast to sending `text/html` or `application/json` responses).

First, set up your backend in the language of your choice. Familiarize yourself with [sending SSE events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#sending_events_from_the_server), or use one of the backend [SDKs](/reference/sdks) to get up and running even faster. We’re going to use the SDKs in the examples below, which set the appropriate headers and format the events for us.

The following code would exist in a controller action endpoint in your backend.
```
[ 1](#31967697c6e12f0b_line_1);; Import the SDK's api and your adapter
[ 2](#31967697c6e12f0b_line_2)(require
[ 3](#31967697c6e12f0b_line_3) '[starfederation.datastar.clojure.api :as d*]
[ 4](#31967697c6e12f0b_line_4) '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]])
[ 5](#31967697c6e12f0b_line_5)
[ 6](#31967697c6e12f0b_line_6);; in a ring handler
[ 7](#31967697c6e12f0b_line_7)(defn handler [request]
[ 8](#31967697c6e12f0b_line_8)  ;; Create an SSE response
[ 9](#31967697c6e12f0b_line_9)  (->sse-response request
                  {on-open
                   (fn [sse]
                     ;; Patches elements into the DOM
                     (d*/patch-elements! sse
                                         "<div id=\"question\">What do you put in a toaster?</div>")

                     ;; Patches signals
                     (d*/patch-signals! sse "{response: '', answer: 'bread'}"))}))
```

```
[ 1](#48c09764e15d9bdc_line_1)using StarFederation.Datastar.DependencyInjection;
[ 2](#48c09764e15d9bdc_line_2)
[ 3](#48c09764e15d9bdc_line_3)// Adds Datastar as a service
[ 4](#48c09764e15d9bdc_line_4)builder.Services.AddDatastar();
[ 5](#48c09764e15d9bdc_line_5)
[ 6](#48c09764e15d9bdc_line_6)app.MapGet("/", async (IDatastarService datastarService) =>
[ 7](#48c09764e15d9bdc_line_7){
[ 8](#48c09764e15d9bdc_line_8)    // Patches elements into the DOM.
[ 9](#48c09764e15d9bdc_line_9)    await datastarService.PatchElementsAsync(@"<div id=""question"">What do you put in a toaster?</div>");

    // Patches signals.
    await datastarService.PatchSignalsAsync(new { response = "", answer = "bread" });
});
```

```
[ 1](#aed428a208316c97_line_1)import ("github.com/starfederation/datastar-go/datastar")
[ 2](#aed428a208316c97_line_2)
[ 3](#aed428a208316c97_line_3)// Creates a new `ServerSentEventGenerator` instance.
[ 4](#aed428a208316c97_line_4)sse := datastar.NewSSE(w,r)
[ 5](#aed428a208316c97_line_5)
[ 6](#aed428a208316c97_line_6)// Patches elements into the DOM.
[ 7](#aed428a208316c97_line_7)sse.PatchElements(
[ 8](#aed428a208316c97_line_8)    `<div id="question">What do you put in a toaster?</div>`
[ 9](#aed428a208316c97_line_9))

// Patches signals.
sse.PatchSignals([]byte(`{response: '', answer: 'bread'}`))
```

```
[ 1](#cd481fded6ff187e_line_1)import starfederation.datastar.utils.ServerSentEventGenerator;
[ 2](#cd481fded6ff187e_line_2)
[ 3](#cd481fded6ff187e_line_3)// Creates a new `ServerSentEventGenerator` instance.
[ 4](#cd481fded6ff187e_line_4)AbstractResponseAdapter responseAdapter = new HttpServletResponseAdapter(response);
[ 5](#cd481fded6ff187e_line_5)ServerSentEventGenerator generator = new ServerSentEventGenerator(responseAdapter);
[ 6](#cd481fded6ff187e_line_6)
[ 7](#cd481fded6ff187e_line_7)// Patches elements into the DOM.
[ 8](#cd481fded6ff187e_line_8)generator.send(PatchElements.builder()
[ 9](#cd481fded6ff187e_line_9)    .data("<div id=\"question\">What do you put in a toaster?</div>")
    .build()
);

// Patches signals.
generator.send(PatchSignals.builder()
    .data("{\"response\": \"\", \"answer\": \"\"}")
    .build()
);
```

```
val generator = ServerSentEventGenerator(response)

generator.patchElements(
    elements = """<div id="question">What do you put in a toaster?</div>""",
)

generator.patchSignals(
    signals = """{"response": "", "answer": "bread"}""",
)
```

```
[ 1](#87f15801a1f2f185_line_1)use starfederation\datastar\ServerSentEventGenerator;
[ 2](#87f15801a1f2f185_line_2)
[ 3](#87f15801a1f2f185_line_3)// Creates a new `ServerSentEventGenerator` instance.
[ 4](#87f15801a1f2f185_line_4)$sse = new ServerSentEventGenerator();
[ 5](#87f15801a1f2f185_line_5)
[ 6](#87f15801a1f2f185_line_6)// Patches elements into the DOM.
[ 7](#87f15801a1f2f185_line_7)$sse->patchElements(
[ 8](#87f15801a1f2f185_line_8)    '<div id="question">What do you put in a toaster?</div>'
[ 9](#87f15801a1f2f185_line_9));

// Patches signals.
$sse->patchSignals(['response' => '', 'answer' => 'bread']);
```

```
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.litestar import DatastarResponse

async def endpoint():
    return DatastarResponse([
        SSE.patch_elements('<div id="question">What do you put in a toaster?</div>'),
        SSE.patch_signals({"response": "", "answer": "bread"})
    ])
```

```
[ 1](#e86f05b84ed0ad5b_line_1)require 'datastar'
[ 2](#e86f05b84ed0ad5b_line_2)
[ 3](#e86f05b84ed0ad5b_line_3)# Create a Datastar::Dispatcher instance
[ 4](#e86f05b84ed0ad5b_line_4)
[ 5](#e86f05b84ed0ad5b_line_5)datastar = Datastar.new(request:, response:)
[ 6](#e86f05b84ed0ad5b_line_6)
[ 7](#e86f05b84ed0ad5b_line_7)# In a Rack handler, you can instantiate from the Rack env
[ 8](#e86f05b84ed0ad5b_line_8)# datastar = Datastar.from_rack_env(env)
[ 9](#e86f05b84ed0ad5b_line_9)
# Start a streaming response
datastar.stream do |sse|
  # Patches elements into the DOM
  sse.patch_elements %(<div id="question">What do you put in a toaster?</div>)

  # Patches signals
  sse.patch_signals(response: '', answer: 'bread')
end
```

```
[ 1](#aee54ef0aa2a2e24_line_1)use datastar::prelude::*;
[ 2](#aee54ef0aa2a2e24_line_2)use async_stream::stream;
[ 3](#aee54ef0aa2a2e24_line_3)
[ 4](#aee54ef0aa2a2e24_line_4)Sse(stream! {
[ 5](#aee54ef0aa2a2e24_line_5)    // Patches elements into the DOM.
[ 6](#aee54ef0aa2a2e24_line_6)    yield PatchElements::new("<div id='question'>What do you put in a toaster?</div>").into();
[ 7](#aee54ef0aa2a2e24_line_7)
[ 8](#aee54ef0aa2a2e24_line_8)    // Patches signals.
[ 9](#aee54ef0aa2a2e24_line_9)    yield PatchSignals::new("{response: '', answer: 'bread'}").into();
})
```

```
// Creates a new `ServerSentEventGenerator` instance (this also sends required headers)
ServerSentEventGenerator.stream(req, res, (stream) => {
      // Patches elements into the DOM.
     stream.patchElements(`<div id="question">What do you put in a toaster?</div>`);

     // Patches signals.
     stream.patchSignals({'response':  '', 'answer': 'bread'});
});
```

The `PatchElements()` function updates the provided HTML element into the DOM, replacing the element with `id="question"`. An element with the ID `question` must *already* exist in the DOM.

The `PatchSignals()` function updates the `response` and `answer` signals into the frontend signals.

With our backend in place, we can now use the `data-on:click` attribute to trigger the [`@get()`](/reference/actions#get) action, which sends a `GET` request to the `/actions/quiz` endpoint on the server when a button is clicked.
```
[ 1](#a8cb65609608ef82_line_1)<div
[ 2](#a8cb65609608ef82_line_2)    data-signals="{response: '', answer: ''}"
[ 3](#a8cb65609608ef82_line_3)    data-computed:correct="$response.toLowerCase() == $answer"
[ 4](#a8cb65609608ef82_line_4)>
[ 5](#a8cb65609608ef82_line_5)    <div id="question"></div>
[ 6](#a8cb65609608ef82_line_6)    <button data-on:click="@get('/actions/quiz')">Fetch a question</button>
[ 7](#a8cb65609608ef82_line_7)    <button
[ 8](#a8cb65609608ef82_line_8)        data-show="$answer != ''"
[ 9](#a8cb65609608ef82_line_9)        data-on:click="$response = prompt('Answer:') ?? ''"
    >
        BUZZ
    </button>
    <div data-show="$response != ''">
        You answered “<span data-text="$response"></span>”.
        <span data-show="$correct">That is correct ✅</span>
        <span data-show="!$correct">
        The correct answer is “<span data-text="$answer"></span>” 🤷
        </span>
    </div>
</div>
```

Now when the `Fetch a question` button is clicked, the server will respond with an event to modify the `question` element in the DOM and an event to modify the `response` and `answer` signals. We’re driving state from the backend!Demo

...Fetch a question BUZZ

You answered “”. That is correct ✅ The correct answer is “” 🤷
### `data-indicator` [#](#data-indicator)

The [`data-indicator`](/reference/attributes#data-indicator) attribute sets the value of a signal to `true` while the request is in flight, otherwise `false`. We can use this signal to show a loading indicator, which may be desirable for slower responses.
```
<div id="question"></div>
<button
    data-on:click="@get('/actions/quiz')"
    data-indicator:fetching
>
    Fetch a question
</button>
<div data-class:loading="$fetching" class="indicator"></div>
```
Demo

...Fetch a question
## Backend Actions [#](#backend-actions)

We’re not limited to sending just `GET` requests. Datastar provides [backend actions](/reference/actions#backend-actions) for each of the methods available: `@get()`, `@post()`, `@put()`, `@patch()` and `@delete()`.

Here’s how we can send an answer to the server for processing, using a `POST` request.
```
<button data-on:click="@post('/actions/quiz')">
    Submit answer
</button>
```

One of the benefits of using SSE is that we can send multiple events (patch elements and patch signals) in a single response.
```
(d*/patch-elements! sse "<div id=\"question\">...</div>")
(d*/patch-elements! sse "<div id=\"instructions\">...</div>")
(d*/patch-signals! sse "{answer: '...', prize: '...'}")
```

```
datastarService.PatchElementsAsync(@"<div id=""question"">...</div>");
datastarService.PatchElementsAsync(@"<div id=""instructions"">...</div>");
datastarService.PatchSignalsAsync(new { answer = "...", prize = "..." } );
```

```
sse.PatchElements(`<div id="question">...</div>`)
sse.PatchElements(`<div id="instructions">...</div>`)
sse.PatchSignals([]byte(`{answer: '...', prize: '...'}`))
```

```
[ 1](#32f2ae5f635f04b0_line_1)generator.send(PatchElements.builder()
[ 2](#32f2ae5f635f04b0_line_2)    .data("<div id=\"question\">...</div>")
[ 3](#32f2ae5f635f04b0_line_3)    .build()
[ 4](#32f2ae5f635f04b0_line_4));
[ 5](#32f2ae5f635f04b0_line_5)generator.send(PatchElements.builder()
[ 6](#32f2ae5f635f04b0_line_6)    .data("<div id=\"instructions\">...</div>")
[ 7](#32f2ae5f635f04b0_line_7)    .build()
[ 8](#32f2ae5f635f04b0_line_8));
[ 9](#32f2ae5f635f04b0_line_9)generator.send(PatchSignals.builder()
    .data("{\"answer\": \"...\", \"prize\": \"...\"}")
    .build()
);
```

```
generator.patchElements(
    elements = """<div id="question">...</div>""",
)
generator.patchElements(
    elements = """<div id="instructions">...</div>""",
)
generator.patchSignals(
    signals = """{"answer": "...", "prize": "..."}""",
)
```

```
$sse->patchElements('<div id="question">...</div>');
$sse->patchElements('<div id="instructions">...</div>');
$sse->patchSignals(['answer' => '...', 'prize' => '...']);
```

```
return DatastarResponse([
    SSE.patch_elements('<div id="question">...</div>'),
    SSE.patch_elements('<div id="instructions">...</div>'),
    SSE.patch_signals({"answer": "...", "prize": "..."})
])
```

```
datastar.stream do |sse|
  sse.patch_elements('<div id="question">...</div>')
  sse.patch_elements('<div id="instructions">...</div>')
  sse.patch_signals(answer: '...', prize: '...')
end
```

```
yield PatchElements::new("<div id='question'>...</div>").into()
yield PatchElements::new("<div id='instructions'>...</div>").into()
yield PatchSignals::new("{answer: '...', prize: '...'}").into()
```

```
stream.patchElements('<div id="question">...</div>');
stream.patchElements('<div id="instructions">...</div>');
stream.patchSignals({'answer': '...', 'prize': '...'});
```

> In addition to your browser’s dev tools, the [Datastar Inspector](/datastar_pro#datastar-inspector) can be used to monitor and inspect SSE events received by Datastar.

Read more about SSE events in the [reference](/reference/sse_events).
## Congratulations [#](#congratulations)

You’ve actually read the entire guide! You should now know how to use Datastar to build reactive applications that communicate with the backend using backend requests and SSE events.

Feel free to dive into the [reference](/reference) and explore the [examples](/examples) next, to learn more about what you can do with Datastar.[](/guide/datastar_expressions)[](/guide/the_tao_of_datastar)[](/star_federation)[](https://www.arcustech.com/)