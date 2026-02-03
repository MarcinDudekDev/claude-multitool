# Source: https://data-star.dev/how_tos/poll_the_backend_at_regular_intervals

How to poll the backend at regular intervals 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) How-TosTackling specific use cases and requirements.[](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/keep_datastar_code_dry)[](/how_tos/load_more_list_items)[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/prevent_sse_connections_closing)[](/how_tos/redirect_the_page_from_the_backend)[](/how_tos/load_more_list_items)[](/how_tos/prevent_sse_connections_closing)
# How to poll the backend at regular intervals

Polling is a pull-based mechanism for fetching data from the server at regular intervals. It is useful when you want to refresh the UI on the frontend, based on real-time data from the backend. 

This in contrast to a push-based mechanism, in which a long-lived SSE connection is kept open between the client and the server, and the server pushes updates to the client whenever necessary. Push-based mechanisms are more efficient than polling, and can be achieved using Datastar, but may be less desirable for some backends.

In PHP, for example, keeping long-lived SSE connections is fine for a dashboard in which users are authenticated, as the number of connections are limited. For a public-facing website, however, it is not recommended to open many long-lived connections, due to the architecture of most PHP servers.
## Goal [#](#goal)
 

Our goal is to poll the backend at regular intervals (starting at 5 second intervals) and update the UI accordingly. The backend will determine changes to the DOM and be able to control the rate at which the frontend polls based on some criteria. For this example, we will simply output the server time, increasing the polling frequency to 1 second during the last 10 seconds of every minute. The criteria could of course be anything such as the number of times previously polled, the user’s role, load on the server, etc.Demo

 
## Steps [#](#steps)
 

The `data-on-interval` attribute allows us to run an expression at a regular interval. We’ll use it to send a `GET` request to the backend, and use the `__duration` modifier to set the interval duration.
```
<div id="time"
     data-on-interval__duration.5s="@get('/endpoint')"
></div>
```
 

In addition to the interval, we could also run the expression immediately by adding `.leading` to the modifier.
```
<div id="time"
     data-on-interval__duration.5s.leading="@get('/endpoint')"
></div>
```
 

Most of the time, however, we’d just render the current time on page load using a backend templating language.
```
<div id="time"
     data-on-interval__duration.5s="@get('/endpoint')"
>
     {{ now }}
</div>
```
 

Now our backend can respond to each request with a [`datastar-patch-elements`](/reference/sse_events#datastar-patch-elements) event with an updated version of the element.
```
event: datastar-patch-elements
data: elements <div id="time" data-on-interval__duration.5s="@get('/endpoint')">
data: elements     {{ now }}
data: elements </div>


```
 

Be careful not to add `.leading` to the modifier in the response, as it will cause the frontend to immediately send another request.

Here’s how it might look using the SDKs.
```
[ 1](#7d165402c607feaa_line_1)(require
[ 2](#7d165402c607feaa_line_2)  '[starfederation.datastar.clojure.api :as d*]
[ 3](#7d165402c607feaa_line_3)  '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]])
[ 4](#7d165402c607feaa_line_4)  '[some.hiccup.library :refer [html]])
[ 5](#7d165402c607feaa_line_5)
[ 6](#7d165402c607feaa_line_6)(import
[ 7](#7d165402c607feaa_line_7)  'java.time.format.DateTimeFormatter
[ 8](#7d165402c607feaa_line_8)  'java.time.LocalDateTime)
[ 9](#7d165402c607feaa_line_9)
(def formatter (DateTimeFormatter/ofPattern "YYYY-MM-DD HH:mm:ss"))

(defn handle [ring-request]
   (->sse-response ring-request
     {on-open
      (fn [sse]
        (d*/patch-elements! sse
          (html [:div#time {:data-on-interval__duration.5s (d*/sse-get "/endpoint")}
                  (LocalDateTime/.format (LocalDateTime/now) formatter)])))}))

        (d*/close-sse! sse))}))
```

```
[ 1](#b951f07346761715_line_1)using StarFederation.Datastar.DependencyInjection;
[ 2](#b951f07346761715_line_2)
[ 3](#b951f07346761715_line_3)app.MapGet("/endpoint", async (IDatastarService datastarService) =>
[ 4](#b951f07346761715_line_4){
[ 5](#b951f07346761715_line_5)    var currentTime = DateTime.Now.ToString("yyyy-MM-dd hh:mm:ss");
[ 6](#b951f07346761715_line_6)    await datastarService.PatchElementsAsync($"""
[ 7](#b951f07346761715_line_7)        <div id="time" data-on-interval__duration.5s="@get('/endpoint')">
[ 8](#b951f07346761715_line_8)            {currentTime}
[ 9](#b951f07346761715_line_9)        </div>
    """);
});
```

```
[ 1](#a831f6ee400e82f6_line_1)import (
[ 2](#a831f6ee400e82f6_line_2)    "time"
[ 3](#a831f6ee400e82f6_line_3)    "github.com/starfederation/datastar-go/datastar"
[ 4](#a831f6ee400e82f6_line_4))
[ 5](#a831f6ee400e82f6_line_5)
[ 6](#a831f6ee400e82f6_line_6)currentTime := time.Now().Format("2006-01-02 15:04:05")
[ 7](#a831f6ee400e82f6_line_7)
[ 8](#a831f6ee400e82f6_line_8)sse := datastar.NewSSE(w, r)
[ 9](#a831f6ee400e82f6_line_9)sse.PatchElements(fmt.Sprintf(`
    <div id="time" data-on-interval__duration.5s="@get('/endpoint')">
        %s
    </div>
`, currentTime))
```

No example found for Java
```
[ 1](#dacc5069bcffcdb1_line_1)val now: LocalDateTime = currentTime()
[ 2](#dacc5069bcffcdb1_line_2)
[ 3](#dacc5069bcffcdb1_line_3)val generator = ServerSentEventGenerator(response)
[ 4](#dacc5069bcffcdb1_line_4)
[ 5](#dacc5069bcffcdb1_line_5)generator.patchElements(
[ 6](#dacc5069bcffcdb1_line_6)    elements =
[ 7](#dacc5069bcffcdb1_line_7)        """
[ 8](#dacc5069bcffcdb1_line_8)        <div id="time" data-on-interval__duration.5s="@get('/endpoint')">
[ 9](#dacc5069bcffcdb1_line_9)            $now
        </div>
        """.trimIndent(),
)
```

```
[ 1](#1dae7cc74a8aab5e_line_1)use starfederation\datastar\ServerSentEventGenerator;
[ 2](#1dae7cc74a8aab5e_line_2)
[ 3](#1dae7cc74a8aab5e_line_3)$currentTime = date('Y-m-d H:i:s');
[ 4](#1dae7cc74a8aab5e_line_4)
[ 5](#1dae7cc74a8aab5e_line_5)$sse = new ServerSentEventGenerator();
[ 6](#1dae7cc74a8aab5e_line_6)$sse->patchElements(`
[ 7](#1dae7cc74a8aab5e_line_7)    <div id="time"
[ 8](#1dae7cc74a8aab5e_line_8)         data-on-interval__duration.5s="@get('/endpoint')"
[ 9](#1dae7cc74a8aab5e_line_9)    >
        $currentTime
    </div>
`);
```

```
[ 1](#8fddb7b041c04674_line_1)from datastar_py import ServerSentEventGenerator as SSE
[ 2](#8fddb7b041c04674_line_2)from datastar_py.sanic import DatastarResponse
[ 3](#8fddb7b041c04674_line_3)
[ 4](#8fddb7b041c04674_line_4)@app.get("/endpoint")
[ 5](#8fddb7b041c04674_line_5)async def endpoint():
[ 6](#8fddb7b041c04674_line_6)    current_time = datetime.now()
[ 7](#8fddb7b041c04674_line_7)
[ 8](#8fddb7b041c04674_line_8)    return DatastarResponse(SSE.patch_elements(f"""
[ 9](#8fddb7b041c04674_line_9)        <div id="time" data-on-interval__duration.5s="@get('/endpoint')">
            {current_time:%Y-%m-%d %H:%M:%S}
        </div>
    """))
```

```
[ 1](#e00429d3ed4d59b4_line_1)datastar = Datastar.new(request:, response:)
[ 2](#e00429d3ed4d59b4_line_2)
[ 3](#e00429d3ed4d59b4_line_3)current_time = Time.now.strftime('%Y-%m-%d %H:%M:%S')
[ 4](#e00429d3ed4d59b4_line_4)
[ 5](#e00429d3ed4d59b4_line_5)datastar.patch_elements <<~FRAGMENT
[ 6](#e00429d3ed4d59b4_line_6)    <div id="time"
[ 7](#e00429d3ed4d59b4_line_7)         data-on-interval__duration.5s="@get('/endpoint')"
[ 8](#e00429d3ed4d59b4_line_8)    >
[ 9](#e00429d3ed4d59b4_line_9)        #{current_time}
    </div>
FRAGMENT
```

```
[ 1](#8f31f75bacc7570_line_1)use datastar::prelude::*;
[ 2](#8f31f75bacc7570_line_2)use chrono::Local;
[ 3](#8f31f75bacc7570_line_3)use async_stream::stream;
[ 4](#8f31f75bacc7570_line_4)
[ 5](#8f31f75bacc7570_line_5)let current_time = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
[ 6](#8f31f75bacc7570_line_6)
[ 7](#8f31f75bacc7570_line_7)Sse(stream! {
[ 8](#8f31f75bacc7570_line_8)    yield PatchElements::new(
[ 9](#8f31f75bacc7570_line_9)        format!(
            "<div id='time' data-on-interval__duration.5s='@get(\"/endpoint\")'>{}</div>",
            current_time
        )
    ).into();
})
```

```
[ 1](#63cfe6ab410c2453_line_1)import { createServer } from "node:http";
[ 2](#63cfe6ab410c2453_line_2)import { ServerSentEventGenerator } from "../npm/esm/node/serverSentEventGenerator.js";
[ 3](#63cfe6ab410c2453_line_3)
[ 4](#63cfe6ab410c2453_line_4)const server = createServer(async (req, res) => {
[ 5](#63cfe6ab410c2453_line_5)  const currentTime = new Date().toISOString();
[ 6](#63cfe6ab410c2453_line_6)  
[ 7](#63cfe6ab410c2453_line_7)  ServerSentEventGenerator.stream(req, res, (sse) => {
[ 8](#63cfe6ab410c2453_line_8)    sse.patchElements(`
[ 9](#63cfe6ab410c2453_line_9)       <div id="time"
          data-on-interval__duration.5s="@get('/endpoint')"
       >
         ${currentTime}
       </div>
    `);
  });
});
```
 

Our second requirement was that the polling frequency should increase to 1 second during the last 10 seconds of every minute. To make this possible, we’ll calculate and output the interval duration based on the current seconds of the minute.
```
[ 1](#2ee1a4d425010a46_line_1)(require
[ 2](#2ee1a4d425010a46_line_2)  '[starfederation.datastar.clojure.api :as d*]
[ 3](#2ee1a4d425010a46_line_3)  '[starfederation.datastar.clojure.adapter.http-kit :refer [->sse-response on-open]])
[ 4](#2ee1a4d425010a46_line_4)  '[some.hiccup.library :refer [html]])
[ 5](#2ee1a4d425010a46_line_5)
[ 6](#2ee1a4d425010a46_line_6)(import
[ 7](#2ee1a4d425010a46_line_7)  'java.time.format.DateTimeFormatter
[ 8](#2ee1a4d425010a46_line_8)  'java.time.LocalDateTime)
[ 9](#2ee1a4d425010a46_line_9)
(def date-time-formatter (DateTimeFormatter/ofPattern "YYYY-MM-DD HH:mm:ss"))
(def seconds-formatter (DateTimeFormatter/ofPattern "ss"))

(defn handle [ring-request]
  (->sse-response ring-request
    {on-open
     (fn [sse]
       (let [now (LocalDateTime/now)
             current-time (LocalDateTime/.format now date-time-formatter)
             seconds (LocalDateTime/.format now seconds-formatter)
             duration (if (neg? (compare seconds "50"))
                         "5"
                         "1")]
         (d*/patch-elements! sse
           (html [:div#time {(str "data-on-interval__duration." duration "s")
                             (d*/sse-get "/endpoint")}
                   current-time]))))}))

         (d*/close-sse! sse))}))
```

```
[ 1](#cd4508291778a772_line_1)using StarFederation.Datastar.DependencyInjection;
[ 2](#cd4508291778a772_line_2)
[ 3](#cd4508291778a772_line_3)app.MapGet("/endpoint", async (IDatastarService datastarService) =>
[ 4](#cd4508291778a772_line_4){
[ 5](#cd4508291778a772_line_5)    var currentTime = DateTime.Now.ToString("yyyy-MM-dd hh:mm:ss");
[ 6](#cd4508291778a772_line_6)    var currentSeconds = DateTime.Now.Second;
[ 7](#cd4508291778a772_line_7)    var duration = currentSeconds < 50 ? 5 : 1;
[ 8](#cd4508291778a772_line_8)    await datastarService.PatchElementsAsync($"""
[ 9](#cd4508291778a772_line_9)        <div id="time" data-on-interval__duration.{duration}s="@get('/endpoint')">
            {currentTime}
        </div>
    """);
});
```

```
[ 1](#64eef37cd423d7e9_line_1)import (
[ 2](#64eef37cd423d7e9_line_2)    "time"
[ 3](#64eef37cd423d7e9_line_3)    "github.com/starfederation/datastar-go/datastar"
[ 4](#64eef37cd423d7e9_line_4))
[ 5](#64eef37cd423d7e9_line_5)
[ 6](#64eef37cd423d7e9_line_6)currentTime := time.Now().Format("2006-01-02 15:04:05")
[ 7](#64eef37cd423d7e9_line_7)currentSeconds := time.Now().Format("05")
[ 8](#64eef37cd423d7e9_line_8)duration := 1
[ 9](#64eef37cd423d7e9_line_9)if currentSeconds < "50" {
    duration = 5
}

sse := datastar.NewSSE(w, r)
sse.PatchElements(fmt.Sprintf(`
    <div id="time" data-on-interval__duration.%ds="@get('/endpoint')">
        %s
    </div>
`, duration, currentTime))
```

No example found for Java
```
[ 1](#d9ec9b72da71d558_line_1)val now: LocalDateTime = currentTime()
[ 2](#d9ec9b72da71d558_line_2)val currentSeconds = now.second
[ 3](#d9ec9b72da71d558_line_3)val duration = if (currentSeconds < 50) 5 else 1
[ 4](#d9ec9b72da71d558_line_4)
[ 5](#d9ec9b72da71d558_line_5)val generator = ServerSentEventGenerator(response)
[ 6](#d9ec9b72da71d558_line_6)
[ 7](#d9ec9b72da71d558_line_7)generator.patchElements(
[ 8](#d9ec9b72da71d558_line_8)    elements =
[ 9](#d9ec9b72da71d558_line_9)        """
        <div id="time" data-on-interval__duration.${duration}s="@get('/endpoint')">
            $now
        </div>
        """.trimIndent(),
)
```

```
[ 1](#20f2426647c3056c_line_1)use starfederation\datastar\ServerSentEventGenerator;
[ 2](#20f2426647c3056c_line_2)
[ 3](#20f2426647c3056c_line_3)$currentTime = date('Y-m-d H:i:s');
[ 4](#20f2426647c3056c_line_4)$currentSeconds = date('s');
[ 5](#20f2426647c3056c_line_5)$duration = $currentSeconds < 50 ? 5 : 1;
[ 6](#20f2426647c3056c_line_6)
[ 7](#20f2426647c3056c_line_7)$sse = new ServerSentEventGenerator();
[ 8](#20f2426647c3056c_line_8)$sse->patchElements(`
[ 9](#20f2426647c3056c_line_9)    <div id="time"
         data-on-interval__duration.${duration}s="@get('/endpoint')"
    >
        $currentTime
    </div>
`);
```

```
[ 1](#68391923164a053a_line_1)from datastar_py import ServerSentEventGenerator as SSE
[ 2](#68391923164a053a_line_2)from datastar_py.sanic import DatastarResponse
[ 3](#68391923164a053a_line_3)
[ 4](#68391923164a053a_line_4)@app.get("/endpoint")
[ 5](#68391923164a053a_line_5)async def endpoint():
[ 6](#68391923164a053a_line_6)    current_time = datetime.now()
[ 7](#68391923164a053a_line_7)    duration = 5 if current_time.seconds < 50 else 1
[ 8](#68391923164a053a_line_8)
[ 9](#68391923164a053a_line_9)    return DatastarResponse(SSE.patch_elements(f"""
        <div id="time" data-on-interval__duration.{duration}s="@get('/endpoint')">
            {current_time:%Y-%m-%d %H:%M:%S}
        </div>
    """))
```

```
[ 1](#5e08c6c7840593ae_line_1)datastar = Datastar.new(request:, response:)
[ 2](#5e08c6c7840593ae_line_2)
[ 3](#5e08c6c7840593ae_line_3)now = Time.now
[ 4](#5e08c6c7840593ae_line_4)current_time = now.strftime('%Y-%m-%d %H:%M:%S')
[ 5](#5e08c6c7840593ae_line_5)current_seconds = now.strftime('%S').to_i
[ 6](#5e08c6c7840593ae_line_6)duration = current_seconds < 50 ? 5 : 1
[ 7](#5e08c6c7840593ae_line_7)
[ 8](#5e08c6c7840593ae_line_8)datastar.patch_elements <<~FRAGMENT
[ 9](#5e08c6c7840593ae_line_9)    <div id="time"
         data-on-interval__duration.#{duration}s="@get('/endpoint')"
    >
        #{current_time}
    </div>
FRAGMENT
```

```
[ 1](#6164d3f3c335c6df_line_1)use datastar::prelude::*;
[ 2](#6164d3f3c335c6df_line_2)use chrono::Local;
[ 3](#6164d3f3c335c6df_line_3)use async_stream::stream;
[ 4](#6164d3f3c335c6df_line_4)
[ 5](#6164d3f3c335c6df_line_5)let current_time = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
[ 6](#6164d3f3c335c6df_line_6)let current_seconds = Local::now().second();
[ 7](#6164d3f3c335c6df_line_7)let duration = if current_seconds < 50 {
[ 8](#6164d3f3c335c6df_line_8)    5
[ 9](#6164d3f3c335c6df_line_9)} else {
    1
};

Sse(stream! {
    yield PatchElements::new(
        format!(
            "<div id='time' data-on-interval__duration.{}s='@get(\"/endpoint\")'>{}</div>",
            duration,
            current_time,
        )
    ).into();
})
```

```
[ 1](#792eb4f3cfe332e8_line_1)import { createServer } from "node:http";
[ 2](#792eb4f3cfe332e8_line_2)import { ServerSentEventGenerator } from "../npm/esm/node/serverSentEventGenerator.js";
[ 3](#792eb4f3cfe332e8_line_3)
[ 4](#792eb4f3cfe332e8_line_4)const server = createServer(async (req, res) => {
[ 5](#792eb4f3cfe332e8_line_5)  const currentTime = new Date();
[ 6](#792eb4f3cfe332e8_line_6)  const duration = currentTime.getSeconds > 50 ? 5 : 1;
[ 7](#792eb4f3cfe332e8_line_7)
[ 8](#792eb4f3cfe332e8_line_8)  ServerSentEventGenerator.stream(req, res, (sse) => {
[ 9](#792eb4f3cfe332e8_line_9)    sse.patchElements(`
       <div id="time"
          data-on-interval__duration.${duration}s="@get('/endpoint')"
       >
         ${currentTime.toISOString()}
       </div>
    `);
  });
});
```
 
## Conclusion [#](#conclusion)
 

Using this approach, we not only end up with a way to poll the backend at regular intervals, but we can also control the rate at which the frontend polls based on whatever criteria our backend requires.[](/how_tos/load_more_list_items)[](/how_tos/prevent_sse_connections_closing)[](/star_federation)[](https://www.arcustech.com/)