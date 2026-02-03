# Source: https://data-star.dev/how_tos/load_more_list_items

How to load more list items 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) How-TosTackling specific use cases and requirements.[](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/keep_datastar_code_dry)[](/how_tos/load_more_list_items)[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/prevent_sse_connections_closing)[](/how_tos/redirect_the_page_from_the_backend)[](/how_tos/keep_datastar_code_dry)[](/how_tos/poll_the_backend_at_regular_intervals)
# How to load more list items

Loading more list items into the DOM from the backend is a common alternative to pagination. What makes it different is that we need to append the new items to the existing list, rather than replace them.
## Goal [#](#goal)
 

Our goal is to incrementally append list items into a specific part of the DOM, each time a button is clicked. Once five items are visible, the button should be removed.Demo
- Item 1Click to load another item 
## Steps [#](#steps)
 

We’ll give the list item container and the button unique IDs, so that we can target them individually.

We’ll use a `data-signals` attribute to set the initial `offset` to `1`, and a `data-on:click` button that will send a `GET` request to the backend.
```
<div id="list">
<div>Item 1</div>
</div>
<button id="load-more" 
        data-signals:offset="1" 
        data-on:click="@get('/how_tos/load_more/data')">
Click to load another item
</button>
```
 

The backend will receive the `offset` signal and, if not above the max number of allowed items, will return the next item to be appended to the list.

We’ll set up our backend to send a [`datastar-patch-elements`](/reference/sse_events#datastar-patch-elements) event with the `selector` option set to `#list` and the `mode` option set to `append`. This tells Datastar to _append_ the elements *into* the `#list` container (rather than the default behaviour of replacing it).
```
event: datastar-patch-elements
data: selector #list
data: mode append
data: elements <div>Item 2</div>


```
 

In addition, we’ll send a [`datastar-patch-signals`](/reference/sse_events#datastar-patch-signals) event to update the `offset`.
```
event: datastar-patch-signals
data: signals {offset: 2}


```
 

In the case when all five list items have been shown, we’ll remove the button from the DOM entirely.
```
event: datastar-patch-elements
data: selector #load-more
data: mode remove


```
 

Here’s how it might look using the SDKs.
```
[ 1](#b10c47f28beda9b_line_1)(require
[ 2](#b10c47f28beda9b_line_2)  '[starfederation.datastar.clojure.api :as d*]
[ 3](#b10c47f28beda9b_line_3)  '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]]
[ 4](#b10c47f28beda9b_line_4)  '[some.hiccup.library :refer [html]]
[ 5](#b10c47f28beda9b_line_5)  '[some.json.library :refer [read-json-str write-json-str]]))
[ 6](#b10c47f28beda9b_line_6)
[ 7](#b10c47f28beda9b_line_7)
[ 8](#b10c47f28beda9b_line_8)(def max-offset 5)
[ 9](#b10c47f28beda9b_line_9)
(defn handler [ring-request]
  (->sse-response ring-request
    {on-open
     (fn [sse]
       (let [d*-signals (-> ring-request d*/get-signals read-json-str)
             offset (get d*-signals "offset")
             limit 1
             new-offset (+ offset limit)]

         (d*/patch-elements! sse
                             (html [:div "Item " new-offset])
                             {d*/selector   "#list"
                              d*/merge-mode d*/mm-append})

         (if (< new-offset max-offset)
           (d*/patch-signals! sse (write-json-str {"offset" new-offset}))
           (d*/remove-fragment! sse "#load-more"))

         (d*/close-sse! sse)))}))
```

```
[ 1](#7287f54b959bd6ba_line_1)using System.Text.Json;
[ 2](#7287f54b959bd6ba_line_2)using StarFederation.Datastar;
[ 3](#7287f54b959bd6ba_line_3)using StarFederation.Datastar.DependencyInjection;
[ 4](#7287f54b959bd6ba_line_4)
[ 5](#7287f54b959bd6ba_line_5)public class Program
[ 6](#7287f54b959bd6ba_line_6){
[ 7](#7287f54b959bd6ba_line_7)    public record OffsetSignals(int offset);
[ 8](#7287f54b959bd6ba_line_8)
[ 9](#7287f54b959bd6ba_line_9)    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        builder.Services.AddDatastar();
        var app = builder.Build();

        app.MapGet("/more", async (IDatastarService datastarService) =>
        {
            var max = 5;
            var limit = 1;
            var signals = await datastarService.ReadSignalsAsync<OffsetSignals>();
            var offset = signals.offset;
            if (offset < max)
            {
                var newOffset = offset + limit;
                await datastarService.PatchElementsAsync($"<div>Item {newOffset}</div>", new()
                {
                    Selector = "#list",
                    PatchMode = PatchElementsMode.Append,
                });
                if (newOffset < max)
                    await datastarService.PatchSignalsAsync(new OffsetSignals(newOffset));
                else
                    await datastarService.RemoveElementAsync("#load-more");
            }
        });

        app.Run();
    }
}
```

```
[ 1](#85420d92552e31ed_line_1)import (
[ 2](#85420d92552e31ed_line_2)    "fmt"
[ 3](#85420d92552e31ed_line_3)    "net/http"
[ 4](#85420d92552e31ed_line_4)
[ 5](#85420d92552e31ed_line_5)    "github.com/go-chi/chi/v5"
[ 6](#85420d92552e31ed_line_6)    "github.com/starfederation/datastar-go/datastar"
[ 7](#85420d92552e31ed_line_7))
[ 8](#85420d92552e31ed_line_8)
[ 9](#85420d92552e31ed_line_9)type OffsetSignals struct {
    Offset int `json:"offset"`
}

signals := &OffsetSignals{}
if err := datastar.ReadSignals(r, signals); err != nil {
    http.Error(w, err.Error(), http.StatusBadRequest)
}

max := 5
limit := 1
offset := signals.Offset

sse := datastar.NewSSE(w, r)

if offset < max {
    newOffset := offset + limit
    sse.PatchElements(fmt.Sprintf(`<div>Item %d</div>`, newOffset),
        datastar.WithSelectorID("list"),
        datastar.WithModeAppend(),
    )
    if newOffset < max {
        sse.PatchSignals([]byte(fmt.Sprintf(`{offset: %d}`, newOffset)))
    } else {
        sse.RemoveElements(`#load-more`)
    }
}
```

No example found for Java
```
[ 1](#42e51d7dc8668af_line_1)@Serializable
[ 2](#42e51d7dc8668af_line_2)data class OffsetSignals(
[ 3](#42e51d7dc8668af_line_3)    val offset: Int,
[ 4](#42e51d7dc8668af_line_4))
[ 5](#42e51d7dc8668af_line_5)
[ 6](#42e51d7dc8668af_line_6)val signals =
[ 7](#42e51d7dc8668af_line_7)    readSignals(
[ 8](#42e51d7dc8668af_line_8)        request,
[ 9](#42e51d7dc8668af_line_9)        { json: String -> Json.decodeFromString<OffsetSignals>(json) },
    )

val max = 5
val limit = 1
val offset = signals.offset

val generator = ServerSentEventGenerator(response)

if (offset < max) {
    val newOffset = offset + limit

    generator.patchElements(
        elements = "<div>Item $newOffset</div>",
        options =
            PatchElementsOptions(
                selector = "#list",
                mode = ElementPatchMode.Append,
            ),
    )

    if (newOffset < max) {
        generator.patchSignals(
            signals = """{"offset": $newOffset}""",
        )
    } else {
        generator.patchElements(
            options =
                PatchElementsOptions(
                    selector = "#load-more",
                    mode = ElementPatchMode.Remove,
                ),
        )
    }
}
```

```
[ 1](#760124b9ebb84a04_line_1)use starfederation\datastar\enums\ElementPatchMode;
[ 2](#760124b9ebb84a04_line_2)use starfederation\datastar\ServerSentEventGenerator;
[ 3](#760124b9ebb84a04_line_3)
[ 4](#760124b9ebb84a04_line_4)$signals = ServerSentEventGenerator::readSignals();
[ 5](#760124b9ebb84a04_line_5)
[ 6](#760124b9ebb84a04_line_6)$max = 5;
[ 7](#760124b9ebb84a04_line_7)$limit = 1;
[ 8](#760124b9ebb84a04_line_8)$offset = $signals['offset'] ?? 1;
[ 9](#760124b9ebb84a04_line_9)
$sse = new ServerSentEventGenerator();

if ($offset < $max) {
    $newOffset = $offset + $limit;
    $sse->patchElements("<div>Item $newOffset</div>", [
        'selector' => '#list',
        'mode' => ElementPatchMode::Append,
    ]);
    if (newOffset < $max) {
        $sse->patchSignals(['offset' => $newOffset]);
    } else {
        $sse->removeElements('#load-more');
    }
}
```

```
[ 1](#c1046aa822102a35_line_1)from datastar_py import ServerSentEventGenerator as SSE
[ 2](#c1046aa822102a35_line_2)from datastar_py.consts import ElementPatchMode
[ 3](#c1046aa822102a35_line_3)from datastar_py.fastapi import datastar_response, ReadSignals
[ 4](#c1046aa822102a35_line_4)
[ 5](#c1046aa822102a35_line_5)MAX_ITEMS = 5
[ 6](#c1046aa822102a35_line_6)
[ 7](#c1046aa822102a35_line_7)@app.get("/how_tos/load_more/data")
[ 8](#c1046aa822102a35_line_8)@datastar_response
[ 9](#c1046aa822102a35_line_9)async def load_data(signals: ReadSignals):
    if signals["offset"] < MAX_ITEMS:
        new_offset = signals["offset"] + 1
        yield SSE.patch_elements(
            f"<div>Item {new_offset}</div>",
            mode=ElementPatchMode.APPEND,
            selector="#list"
        )
        if new_offset < MAX_ITEMS:
            yield SSE.patch_signals({"offset": new_offset})
        else:
            yield SSE.remove_elements("#load-more")
```

No example found for Ruby

No example found for Rust

No example found for TypeScript 
## Conclusion [#](#conclusion)
 

While using the default mode of `outer` is generally recommended, appending to a list is a good example of when to use the `append` mode.[](/how_tos/keep_datastar_code_dry)[](/how_tos/poll_the_backend_at_regular_intervals)[](/star_federation)[](https://www.arcustech.com/)