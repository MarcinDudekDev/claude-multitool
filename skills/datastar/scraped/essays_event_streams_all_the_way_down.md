# Source: https://data-star.dev/essays/event_streams_all_the_way_down

Event streams all the way down 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) EssaysHow we landed here, and where we’re headed next.[](/essays/greedy_developer)[](/essays/v1_and_beyond)[](/essays/the_road_to_v1)[](/essays/htmx_sucks)[](/essays/another_dependency)[](/essays/event_streams_all_the_way_down)[](/essays/im_a_teapot)[](/essays/grugs_around_the_fire)[](/essays/haikus)[](/essays/yes_you_want_a_build_step)[](/essays/why_another_framework)[](/essays/another_dependency)[](/essays/im_a_teapot)
# Event streams all the way down

[SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) is a really great idea. With a single request you can create a server driven stream of events. Using this for driving Datastar’s [htmx](https://htmx.org/) like fragments plugin is a natural fit. The only problem is that SSE doesn’t support anything but the `GET` method. This means that you can’t use SSE to send data to the server. This is a problem for htmx, because htmx uses the `POST` method to send data to the server. So, what to do?
## The Solution [#](#the-solution)
 

`text/event-stream` MIME type is the underlying protocol for [Server Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events). It is a simple protocol that is easy to implement. It is also a simple protocol to extend. So, we can extend it to support `POST`,`PUT`,`PATCH`,`DELETE` requests. The majority of the code is in how your read and buffer results from [fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) calls. The rest is just a matter of parsing the request and sending the appropriate response. The great part is the server side still just uses the same libraries or helpers that it would use for SSE.

This means every data fragment is an OOB in htmx terms.

This is easy to debug, easy to create, and still makes use of middlewares like compression. It’s just HTML fragments but wrapped in a protocol that allows for streaming and server driven events.[](/essays/another_dependency)[](/essays/im_a_teapot)[](/star_federation)[](https://www.arcustech.com/)