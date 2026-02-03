# Source: https://data-star.dev/essays/im_a_teapot

I’m a Teapot 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) EssaysHow we landed here, and where we’re headed next.[](/essays/greedy_developer)[](/essays/v1_and_beyond)[](/essays/the_road_to_v1)[](/essays/htmx_sucks)[](/essays/another_dependency)[](/essays/event_streams_all_the_way_down)[](/essays/im_a_teapot)[](/essays/grugs_around_the_fire)[](/essays/haikus)[](/essays/yes_you_want_a_build_step)[](/essays/why_another_framework)[](/essays/event_streams_all_the_way_down)[](/essays/grugs_around_the_fire)
# I’m a Teapot

A discussion on the [htmx Discord](https://discord.com/channels/725789699527933952/1156332851093065788) started talking about HTTP status codes. Apparently I hold the minority opinion that if
- Are using HTTP as your UI interface
- Humans are using your UI
- You are using [HOWL](https://htmx.org/essays/hypermedia-on-whatever-youd-like/)
- Have complete control over the backend

Then you should only ***ever*** be usings either the 2xx or 3xx series of status codes. The 4xx and 5xx series are for machines and should never be seen by humans. The 4xx series is for client errors and the 5xx series is for server errors. If you are using HTTP as your UI interface then you should be handling all errors on the client side. If you are using a 4xx or 5xx series code then you are doing something wrong.

[This](https://discord.com/channels/725789699527933952/1156332851093065788/1156377394530242622) section is the most relevant:
> 

**@alex** — What if the user enters a URL they don’t have access to?

**@delaneyj** — then you redirect them or create a you aren’t allowed page no?

**@Deniz A. (dz4k)** —HTTP/1.1 200 OK
Content-Type: text/html
<H1>Error 404</H1>

**@alex** — Great solution, no notes

It might be a little tongue in cheek but the point is valid. If you are using HTTP as your UI interface then you should be using the 2xx and 3xx series of status codes. If you are using the 4xx or 5xx series then you are doing something wrong.
## Hypermedia is for humans [#](#hypermedia-is-for-humans)
 

The whole point of [HOWL](https://htmx.org/essays/hypermedia-on-whatever-youd-like/) is to make your UI driven by HATEOAS and users do not care about the underlying protocol. Redirecting a users or explaining why they aren’t authorized then it should be done in the UI. If you need to expose an API there are far more efficient and explicit ways to do that such as [gRPC](https://grpc.io/), [dRPC](https://docs.drpc.org/), or [Buf’s Connect](https://buf.build/blog/connect-a-better-grpc). If that’s too limiting then you can always go to a distributed highly available super-cluster via [NATS](https://nats.io/).
## What does Datastar do? [#](#what-does-datastar-do?)
 

If it’s a 3xx we redirect, 2xx we merge the HTML fragment, and anything else throws an error. I’m considering even forcing a `window.alert` on top of throwing the error. If you get at client error or server error ***when you control both sides*** then it’s a bug, and you should be fixing it.

[](/essays/event_streams_all_the_way_down)[](/essays/grugs_around_the_fire)[](/star_federation)[](https://www.arcustech.com/)