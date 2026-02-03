# Source: https://data-star.dev/how_tos/bind_keydown_events_to_specific_keys

How to bind keydown events to specific keys 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) How-TosTackling specific use cases and requirements.[](/how_tos/bind_keydown_events_to_specific_keys)[](/how_tos/keep_datastar_code_dry)[](/how_tos/load_more_list_items)[](/how_tos/poll_the_backend_at_regular_intervals)[](/how_tos/prevent_sse_connections_closing)[](/how_tos/redirect_the_page_from_the_backend)[]()[](/how_tos/keep_datastar_code_dry)
# How to bind keydown events to specific keys

The [`data-on`](/reference/attributes#data-on) attribute allows us to attach an event listener to any element, and run an expression whenever the event is triggered. We can use this to listen for keydown events and run an expression only when a specific key or key combination is pressed.
## Goal [#](#goal)
 

Our goal is to show an alert whenever the user presses the `Enter` key, or a combination of the `Ctrl` and `L` keys. Demo

Press `Enter` or `Ctrl + L` 
## Steps [#](#steps)
 

The `data-on:keydown` attribute will listen for keydown events only on the element on which it is placed, by default. We can listen for events on the `window` element to capture keydown events globally, by adding the `__window` modifier.
```
<div data-on:keydown__window="alert('Key pressed')"></div>
```
 

This will show an alert whenever the user presses *any* key. To limit the alert to only the `Enter` key, we can use the `evt.key` property to check the key that was pressed. The `evt` variable represents the event object and is always available in the expression.
```
<div data-on:keydown__window="evt.key === 'Enter' && alert('Key pressed')"></div>
```
 

We can add the `Ctrl` and `L` key combination by checking the `evt.ctrlKey` and `evt.key` properties.
```
<div data-on:keydown__window="evt.ctrlKey && evt.key === 'l' && alert('Key pressed')"></div>
```
 

Finally, we can combine the two expressions to show an alert whenever the user presses the `Enter` key, or the `Ctrl` and `L` keys.
```
<div data-on:keydown__window="(evt.key === 'Enter' || (evt.ctrlKey && evt.key === 'l')) && alert('Key pressed')"></div>
```
 

Sometimes, we may want to prevent the default behavior of the keydown event, such as submitting a form when the `Enter` key is pressed. We can do this by calling `evt.preventDefault()`.
```
<div data-on:keydown__window="evt.key === 'Enter' && (evt.preventDefault(), alert('Key pressed'))"></div>
```
 
## Conclusion [#](#conclusion)
 

The `evt` variable is always available in [`data-on`](/reference/attributes#data-on) attribute expressions. In the case of the [`keydown`](https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event) event, which is a [`KeyboardEvent`](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent), we can perform actions conditionally, based on any of the event’s properties.[]()[](/how_tos/keep_datastar_code_dry)[](/star_federation)[](https://www.arcustech.com/)