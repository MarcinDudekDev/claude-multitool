# Source: https://data-star.dev/how_tos/redirect_the_page_from_the_backend

How to redirect the page from the backend 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) How-TosTackling specific use cases and requirements.[](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/keep_datastar_code_dry)[](/how_tos/load_more_list_items)[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/prevent_sse_connections_closing)[](/how_tos/redirect_the_page_from_the_backend)[](/how_tos/prevent_sse_connections_closing)[]()
# How to redirect the page from the backend

Redirecting to another page is a common task that can be done from the backend by patching a `script` tag into the DOM using a [`datastar-patch-elements`](/reference/sse_events#datastar-patch-elements) SSE event. Since this results in a browser redirect, existing signals will *not* persist to the new page.
## Goal [#](#goal)
 

Our goal is to indicate to the user that they will be redirected, wait 3 seconds, and then redirect them to `/guide`, all from the backend.DemoClick to be redirected from the backend

 
## Steps [#](#steps)
 

We’ll place a `data-on:click` attribute on a button and use the `get` action to send a `GET` request to the backend. We’ll include an empty indicator `div` to show the user that they will be redirected.
```
<button data-on:click="@get('/endpoint')">
    Click to be redirected from the backend
</button>
<div id="indicator"></div>
```
 

We’ll set up our backend to first send a `datastar-patch-elements` event with a populated indicator fragment, then wait 3 seconds, and then send another `datastar-patch-elements` SSE event to append a `script` tag that redirects the page.
```
[ 1](#552bc0cb1061695c_line_1)event: datastar-patch-elements
[ 2](#552bc0cb1061695c_line_2)data: elements <div id="indicator">Redirecting in 3 seconds...</div>
[ 3](#552bc0cb1061695c_line_3)
[ 4](#552bc0cb1061695c_line_4)// Wait 3 seconds
[ 5](#552bc0cb1061695c_line_5)
[ 6](#552bc0cb1061695c_line_6)event: datastar-patch-elements
[ 7](#552bc0cb1061695c_line_7)data: selector body
[ 8](#552bc0cb1061695c_line_8)data: mode append
[ 9](#552bc0cb1061695c_line_9)data: elements <script>window.location.href = "/guide"</script>


```
 

All SDKs provide an `ExecuteScript` helper function that wraps the provided code in a `script` tag and patches it into the DOM.
```
[ 1](#639af440b12e989f_line_1)(require
[ 2](#639af440b12e989f_line_2)  '[starfederation.datastar.clojure.api :as d*]
[ 3](#639af440b12e989f_line_3)  '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]]
[ 4](#639af440b12e989f_line_4)  '[some.hiccup.library :refer [html]])
[ 5](#639af440b12e989f_line_5)
[ 6](#639af440b12e989f_line_6)
[ 7](#639af440b12e989f_line_7)(defn handle [ring-request]
[ 8](#639af440b12e989f_line_8)  (->sse-response ring-request
[ 9](#639af440b12e989f_line_9)    {on-open
      (fn [sse]
        (d*/patch-elements! sse
          (html [:div#indicator "Redirecting in 3 seconds..."]))
        (Thread/sleep 3000)
        (d*/execute-script! sse "window.location = \"/guide\"")
        (d*/close-sse! sse)}))
```

```
using StarFederation.Datastar.DependencyInjection;

app.MapGet("/redirect", async (IDatastarService datastarService) =>
{
    await datastarService.PatchElementsAsync("""<div id="indicator">Redirecting in 3 seconds...</div>""");
    await Task.Delay(TimeSpan.FromSeconds(3));
    await datastarService.ExecuteScriptAsync("""window.location = "/guide";""");
});
```

```
[ 1](#11a0be49bec73dc2_line_1)import (
[ 2](#11a0be49bec73dc2_line_2)    "time"
[ 3](#11a0be49bec73dc2_line_3)    "github.com/starfederation/datastar-go/datastar"
[ 4](#11a0be49bec73dc2_line_4))
[ 5](#11a0be49bec73dc2_line_5)
[ 6](#11a0be49bec73dc2_line_6)sse := datastar.NewSSE(w, r)
[ 7](#11a0be49bec73dc2_line_7)sse.PatchElements(`
[ 8](#11a0be49bec73dc2_line_8)    <div id="indicator">Redirecting in 3 seconds...</div>
[ 9](#11a0be49bec73dc2_line_9)`)
time.Sleep(3 * time.Second)
sse.ExecuteScript(`
    window.location = "/guide"
`)
```

No example found for Java
```
[ 1](#18934163a75c9ad4_line_1)val generator = ServerSentEventGenerator(response)
[ 2](#18934163a75c9ad4_line_2)
[ 3](#18934163a75c9ad4_line_3)generator.patchElements(
[ 4](#18934163a75c9ad4_line_4)    elements =
[ 5](#18934163a75c9ad4_line_5)        """
[ 6](#18934163a75c9ad4_line_6)        <div id="indicator">Redirecting in 3 seconds...</div>
[ 7](#18934163a75c9ad4_line_7)        """.trimIndent(),
[ 8](#18934163a75c9ad4_line_8))
[ 9](#18934163a75c9ad4_line_9)
Thread.sleep(3 * ONE_SECOND)

generator.executeScript(
    script = "window.location.href = '/success'",
)
```

```
[ 1](#8c6b123fff64dd34_line_1)use starfederation\datastar\ServerSentEventGenerator;
[ 2](#8c6b123fff64dd34_line_2)
[ 3](#8c6b123fff64dd34_line_3)$sse = new ServerSentEventGenerator();
[ 4](#8c6b123fff64dd34_line_4)$sse->patchElements(`
[ 5](#8c6b123fff64dd34_line_5)    <div id="indicator">Redirecting in 3 seconds...</div>
[ 6](#8c6b123fff64dd34_line_6)`);
[ 7](#8c6b123fff64dd34_line_7)sleep(3);
[ 8](#8c6b123fff64dd34_line_8)$sse->executeScript(`
[ 9](#8c6b123fff64dd34_line_9)    window.location = "/guide"
`);
```

```
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response

@app.get("/redirect")
@datastar_response
async def redirect_from_backend():
    yield SSE.patch_elements('<div id="indicator">Redirecting in 3 seconds...</div>')
    await asyncio.sleep(3)
    yield SSE.execute_script('window.location = "/guide"')
```

```
datastar = Datastar.new(request:, response:)

datastar.stream do |sse|
  sse.patch_elements '<div id="indicator">Redirecting in 3 seconds...</div>'
  sleep 3
  sse.execute_script 'window.location = "/guide"'
end
```

```
use datastar::prelude::*;
use async_stream::stream;
use core::time::Duration;

Sse(stream! {
    yield PatchElements::new("<div id='indicator'>Redirecting in 3 seconds...</div>").into();
    tokio::time::sleep(core::time::Duration::from_secs(3)).await;
    yield ExecuteScript::new("window.location = '/guide'").into();
});
```

```
[ 1](#d69a5f8d3ec779fa_line_1)import { createServer } from "node:http";
[ 2](#d69a5f8d3ec779fa_line_2)import { ServerSentEventGenerator } from "../npm/esm/node/serverSentEventGenerator.js";
[ 3](#d69a5f8d3ec779fa_line_3)
[ 4](#d69a5f8d3ec779fa_line_4)const server = createServer(async (req, res) => {
[ 5](#d69a5f8d3ec779fa_line_5)
[ 6](#d69a5f8d3ec779fa_line_6)  ServerSentEventGenerator.stream(req, res, async (sse) => {
[ 7](#d69a5f8d3ec779fa_line_7)    sse.patchElements(`
[ 8](#d69a5f8d3ec779fa_line_8)      <div id="indicator">Redirecting in 3 seconds...</div>
[ 9](#d69a5f8d3ec779fa_line_9)    `);

    setTimeout(() => {
      sse.executeScript(`window.location = "/guide"`);
    }, 3000);
  });
});
```
 

Note that in Firefox, if a redirect happens within a `script` tag then the URL is *replaced*, rather than *pushed*, meaning that the previous URL won’t show up in the back history (or back/forward navigation).

To work around this, you can wrap the redirect in a `setTimeout` function call. See [issue #529](https://github.com/starfederation/datastar/issues/529) for reference.
```
[ 1](#fc4b5e5413ee0af1_line_1)(require
[ 2](#fc4b5e5413ee0af1_line_2)  '[starfederation.datastar.clojure.api :as d*]
[ 3](#fc4b5e5413ee0af1_line_3)  '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]]
[ 4](#fc4b5e5413ee0af1_line_4)  '[some.hiccup.library :refer [html]])
[ 5](#fc4b5e5413ee0af1_line_5)
[ 6](#fc4b5e5413ee0af1_line_6)
[ 7](#fc4b5e5413ee0af1_line_7)(defn handle [ring-request]
[ 8](#fc4b5e5413ee0af1_line_8)  (->sse-response ring-request
[ 9](#fc4b5e5413ee0af1_line_9)    {on-open
      (fn [sse]
        (d*/patch-elements! sse
          (html [:div#indicator "Redirecting in 3 seconds..."]))
        (Thread/sleep 3000)
        (d*/execute-script! sse
          "setTimeout(() => window.location = \"/guide\")"
        (d*/close-sse! sse))}))
```

```
using StarFederation.Datastar.DependencyInjection;

app.MapGet("/redirect", async (IDatastarService datastarService) =>
{
    await datastarService.PatchElementsAsync("""<div id="indicator">Redirecting in 3 seconds...</div>""");
    await Task.Delay(TimeSpan.FromSeconds(3));
    await datastarService.ExecuteScriptAsync("""setTimeout(() => window.location = "/guide");""");
});
```

```
[ 1](#103f190896f4077f_line_1)import (
[ 2](#103f190896f4077f_line_2)    "time"
[ 3](#103f190896f4077f_line_3)    "github.com/starfederation/datastar-go/datastar"
[ 4](#103f190896f4077f_line_4))
[ 5](#103f190896f4077f_line_5)
[ 6](#103f190896f4077f_line_6)sse := datastar.NewSSE(w, r)
[ 7](#103f190896f4077f_line_7)sse.PatchElements(`
[ 8](#103f190896f4077f_line_8)    <div id="indicator">Redirecting in 3 seconds...</div>
[ 9](#103f190896f4077f_line_9)`)
time.Sleep(3 * time.Second)
sse.ExecuteScript(`
    setTimeout(() => window.location = "/guide")
`)
```

No example found for Java
```
[ 1](#f460db9cd3fcaaf_line_1)val generator = ServerSentEventGenerator(response)
[ 2](#f460db9cd3fcaaf_line_2)
[ 3](#f460db9cd3fcaaf_line_3)generator.patchElements(
[ 4](#f460db9cd3fcaaf_line_4)    elements =
[ 5](#f460db9cd3fcaaf_line_5)        """
[ 6](#f460db9cd3fcaaf_line_6)        <div id="indicator">Redirecting in 3 seconds...</div>
[ 7](#f460db9cd3fcaaf_line_7)        """.trimIndent(),
[ 8](#f460db9cd3fcaaf_line_8))
[ 9](#f460db9cd3fcaaf_line_9)
Thread.sleep(3 * ONE_SECOND)

generator.executeScript(
    script = "setTimeout(() => window.location = '/guide')",
)
```

```
[ 1](#78629bb0a6cc1697_line_1)use starfederation\datastar\ServerSentEventGenerator;
[ 2](#78629bb0a6cc1697_line_2)
[ 3](#78629bb0a6cc1697_line_3)$sse = new ServerSentEventGenerator();
[ 4](#78629bb0a6cc1697_line_4)$sse->patchElements(`
[ 5](#78629bb0a6cc1697_line_5)    <div id="indicator">Redirecting in 3 seconds...</div>
[ 6](#78629bb0a6cc1697_line_6)`);
[ 7](#78629bb0a6cc1697_line_7)sleep(3);
[ 8](#78629bb0a6cc1697_line_8)$sse->executeScript(`
[ 9](#78629bb0a6cc1697_line_9)    setTimeout(() => window.location = "/guide")
`);
```

```
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response

@app.get("/redirect")
@datastar_response
async def redirect_from_backend():
    yield SSE.patch_elements('<div id="indicator">Redirecting in 3 seconds...</div>')
    await asyncio.sleep(3)
    yield SSE.execute_script('setTimeout(() => window.location = "/guide")')
```

```
[ 1](#40ae940b0e346f21_line_1)datastar = Datastar.new(request:, response:)
[ 2](#40ae940b0e346f21_line_2)
[ 3](#40ae940b0e346f21_line_3)datastar.stream do |sse|
[ 4](#40ae940b0e346f21_line_4)  sse.patch_elements '<div id="indicator">Redirecting in 3 seconds...</div>'
[ 5](#40ae940b0e346f21_line_5)
[ 6](#40ae940b0e346f21_line_6)  sleep 3
[ 7](#40ae940b0e346f21_line_7)
[ 8](#40ae940b0e346f21_line_8)  sse.execute_script <<~JS
[ 9](#40ae940b0e346f21_line_9)    setTimeout(() => {
      window.location = '/guide'
    })
  JS
end
```

```
use datastar::prelude::*;
use async_stream::stream;
use core::time::Duration;

Sse(stream! {
    yield PatchElements::new("<div id='indicator'>Redirecting in 3 seconds...</div>").into();
    tokio::time::sleep(core::time::Duration::from_secs(3)).await;
    yield ExecuteScript::new("setTimeout(() => window.location = '/guide')").into();
});
```

```
[ 1](#83dab29be6cdedee_line_1)import { createServer } from "node:http";
[ 2](#83dab29be6cdedee_line_2)import { ServerSentEventGenerator } from "../npm/esm/node/serverSentEventGenerator.js";
[ 3](#83dab29be6cdedee_line_3)
[ 4](#83dab29be6cdedee_line_4)const server = createServer(async (req, res) => {
[ 5](#83dab29be6cdedee_line_5)
[ 6](#83dab29be6cdedee_line_6)  ServerSentEventGenerator.stream(req, res, async (sse) => {
[ 7](#83dab29be6cdedee_line_7)    sse.patchElements(`
[ 8](#83dab29be6cdedee_line_8)      <div id="indicator">Redirecting in 3 seconds...</div>
[ 9](#83dab29be6cdedee_line_9)    `);

    setTimeout(() => {
      sse.executeScript(`setTimeout(() => window.location = "/guide")`);
    }, 3000);
  });
});
```
 

Some SDKs provide a helper method that automatically wraps the statement in a `setTimeout` function call, so you don’t have to worry about doing so (you’re welcome!).
```
[ 1](#471dffe0d9427ce7_line_1)(require
[ 2](#471dffe0d9427ce7_line_2)  '[starfederation.datastar.clojure.api :as d*]
[ 3](#471dffe0d9427ce7_line_3)  '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]]
[ 4](#471dffe0d9427ce7_line_4)  '[some.hiccup.library :refer [html]])
[ 5](#471dffe0d9427ce7_line_5)
[ 6](#471dffe0d9427ce7_line_6)
[ 7](#471dffe0d9427ce7_line_7)(defn handler [ring-request]
[ 8](#471dffe0d9427ce7_line_8)  (->sse-response ring-request
[ 9](#471dffe0d9427ce7_line_9)    {on-open
      (fn [sse]
        (d*/patch-elements! sse
          (html [:div#indicator "Redirecting in 3 seconds..."]))
        (Thread/sleep 3000)
        (d*/redirect! sse "/guide")
        (d*/close-sse! sse))}))
```

```
using StarFederation.Datastar.DependencyInjection;
using StarFederation.Datastar.Scripts;

app.MapGet("/redirect", async (IDatastarService datastarService) =>
{
    await datastarService.PatchElementsAsync("""<div id="indicator">Redirecting in 3 seconds...</div>""");
    await Task.Delay(TimeSpan.FromSeconds(3));
    await datastarService.Redirect("/guide");
});
```

```
[ 1](#7f3d919b2457de12_line_1)import (
[ 2](#7f3d919b2457de12_line_2)    "time"
[ 3](#7f3d919b2457de12_line_3)    "github.com/starfederation/datastar-go/datastar"
[ 4](#7f3d919b2457de12_line_4))
[ 5](#7f3d919b2457de12_line_5)
[ 6](#7f3d919b2457de12_line_6)sse := datastar.NewSSE(w, r)
[ 7](#7f3d919b2457de12_line_7)sse.PatchElements(`
[ 8](#7f3d919b2457de12_line_8)    <div id="indicator">Redirecting in 3 seconds...</div>
[ 9](#7f3d919b2457de12_line_9)`)
time.Sleep(3 * time.Second)
sse.Redirect("/guide")
```

No example found for Java
```
[ 1](#cf4ec5558ca011d2_line_1)val generator = ServerSentEventGenerator(response)
[ 2](#cf4ec5558ca011d2_line_2)
[ 3](#cf4ec5558ca011d2_line_3)generator.patchElements(
[ 4](#cf4ec5558ca011d2_line_4)    elements =
[ 5](#cf4ec5558ca011d2_line_5)        """
[ 6](#cf4ec5558ca011d2_line_6)        <div id="indicator">Redirecting in 3 seconds...</div>
[ 7](#cf4ec5558ca011d2_line_7)        """.trimIndent(),
[ 8](#cf4ec5558ca011d2_line_8))
[ 9](#cf4ec5558ca011d2_line_9)
Thread.sleep(3 * ONE_SECOND)

generator.redirect("/guide")
```

```
use starfederation\datastar\ServerSentEventGenerator;

$sse = new ServerSentEventGenerator();
$sse->patchElements(`
    <div id="indicator">Redirecting in 3 seconds...</div>
`);
sleep(3);
$sse->location('/guide');
```

```
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response

@app.get("/redirect")
@datastar_response
async def redirect_from_backend():
    yield SSE.patch_elements('<div id="indicator">Redirecting in 3 seconds...</div>')
    await asyncio.sleep(3)
    yield SSE.redirect("/guide")
```

```
datastar = Datastar.new(request:, response:)

datastar.stream do |sse|
  sse.patch_elements '<div id="indicator">Redirecting in 3 seconds...</div>'

  sleep 3

  sse.redirect '/guide'
end
```

No example found for Rust

No example found for TypeScript 
## Conclusion [#](#conclusion)
 

Redirecting to another page can be done from the backend thanks to the ability to patch `script` tags into the DOM using the [`datastar-patch-elements`](/reference/sse_events#datastar-patch-elements) SSE event, or to execute JavaScript using an SDK.[](/how_tos/prevent_sse_connections_closing)[]()[](/star_federation)[](https://www.arcustech.com/)