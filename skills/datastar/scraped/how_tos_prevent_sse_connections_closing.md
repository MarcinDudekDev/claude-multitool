# Source: https://data-star.dev/how_tos/prevent_sse_connections_closing

How to prevent SSE connections closing 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) How-TosTackling specific use cases and requirements.[](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/keep_datastar_code_dry)[](/how_tos/load_more_list_items)[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/prevent_sse_connections_closing)[](/how_tos/redirect_the_page_from_the_backend)[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/redirect_the_page_from_the_backend)
# How to prevent SSE connections closing

When a page is hidden (in a background tab, for example), the default behavior is for the SSE connection to be closed, and reopened when the page becomes visible again. This is to save resources on both the client and server.

To keep the connection open even when the page is hidden, you can set the [`openWhenHidden`](/reference/actions#openWhenHidden) option to `true`.
```
<button data-on:click="@get('/endpoint', {openWhenHidden: true})"></button>
```
 
### CQRS Pattern [#](#cqrs-pattern)
 

When using the [CQRS pattern](https://martinfowler.com/bliki/CQRS.html), it’s best to design event streams with interruptions in mind, since they can occur for many reasons beyond just tab switching. The simplest way to ensure resilience is to use a “fat morph” approach: send the complete desired state of the main content area with each update instead of incremental changes like append, which are much more vulnerable to interruptions.

Here’s a simple example of a CQRS approach in which the main content area is always kept up to date. This way, you can leave `openWhenHidden` as is, and if the SSE connection is interrupted for any reason, the next event will contain the complete and correct state of the main content area.
```
<div data-init="@get('/cqrs_endpoint')"></div>
<div id="main">
    ...
</div>
```
[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/redirect_the_page_from_the_backend)[](/star_federation)[](https://www.arcustech.com/)