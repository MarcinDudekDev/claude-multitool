# Source: https://data-star.dev/examples/custom_event

Custom Event Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/click_to_load)[](/examples/custom_plugin)
# Custom Event 
Demo

 
## HTML [#](#html)
 
```
[ 1](#d6006464c0bfe634_line_1)<p
[ 2](#d6006464c0bfe634_line_2)    id="foo"
[ 3](#d6006464c0bfe634_line_3)    data-signals:_event-details
[ 4](#d6006464c0bfe634_line_4)    data-on:myevent="$_eventDetails = evt.detail"
[ 5](#d6006464c0bfe634_line_5)    data-text="`Last Event Details: ${$_eventDetails}`"
[ 6](#d6006464c0bfe634_line_6)></p>
[ 7](#d6006464c0bfe634_line_7)<script>
[ 8](#d6006464c0bfe634_line_8)    const foo = document.getElementById("foo");
[ 9](#d6006464c0bfe634_line_9)    setInterval(() => {
        foo.dispatchEvent(
            new CustomEvent("myevent", {
                detail: JSON.stringify({
                    eventTime: new Date().toLocaleTimeString(),
                }),
            })
        );
    }, 1000);
</script>
```
 
## Explanation [#](#explanation)
 

The `data-on` attribute can listen to any event, including custom events. In this example, we are listening to a custom event myevent on the foo element. When the event is triggered, the `$_eventDetails` signal is set to the event’s details.

This is primarily used when interacting with Web Components or other custom elements that emit custom events.
### Note [#](#note)
 

There is an extra variable `evt` available in the event handler that contains the event object. This is used to access the event details like `evt.detail` in this example.[](/examples/click_to_load)[](/examples/custom_plugin)[](/star_federation)[](https://www.arcustech.com/)