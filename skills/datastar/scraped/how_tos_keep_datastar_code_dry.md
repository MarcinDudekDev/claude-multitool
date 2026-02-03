# Source: https://data-star.dev/how_tos/keep_datastar_code_dry

How to keep Datastar code DRY 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) How-TosTackling specific use cases and requirements.[](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/keep_datastar_code_dry)[](/how_tos/load_more_list_items)[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/prevent_sse_connections_closing)[](/how_tos/redirect_the_page_from_the_backend)[](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/load_more_list_items)
# How to keep Datastar code DRY

The question of how to keep things DRY (Don’t Repeat Yourself) comes up often when using Datastar. One commonly used example concerns preventing the repetition of a backend action.
```
<button data-on:click="@get('/endpoint')">Click me</button>
<button data-on:click="@get('/endpoint')">No, click me!</button>
<button data-on:click="@get('/endpoint')">Click us all!</button>
```
 

The common misconception is that Datastar should provide shorthand syntax for the repeated `@get` action. The answer is that this should be solved using your templating language. For example:
```
{% set action = "@get('/endpoint')" %}
<button data-on:click="{{ action }}">Click me</button>
<button data-on:click="{{ action }}">No, click me!</button>
<button data-on:click="{{ action }}">Click us all!</button>
```
 

Alternatively, using a loop:
```
{% set labels = ['Click me', 'No, click me!', 'Click us all!'] %}
{% for label in labels %}
    <button data-on:click="@get('/endpoint')">{{ label }}</button>
{% endfor %}
```
 

Thanks to [event bubbling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling), a single event listener can be attached to a parent element instead of each button:
```
<div data-on:click="evt.target.tagName == 'BUTTON' 
    && @get('/endpoint')
">
    <button>Click me</button>
    <button>No, click me!</button>
    <button>Click us all!</button>
</div>
```
 

This is the pattern that both the [Blinksy](https://play.putyourlightson.com/blinksy) and [Checkboxes](https://checkboxes.andersmurphy.com/) demos use to prevent registering multiple event listeners for the same action, while being able to send a corresponding ID for each button clicked.
```
<div data-on:click="evt.target.tagName == 'BUTTON' 
    && ($id = evt.target.dataset.id)
    && @get('/endpoint')
">
    <button data-id="1">Click me</button>
    <button data-id="2">No, click me!</button>
    <button data-id="3">Click us all!</button>
</div>
```
 Click me No, click me! Click us all![](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/load_more_list_items)[](/star_federation)[](https://www.arcustech.com/)