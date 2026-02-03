# Source: https://data-star.dev/examples/event_bubbling

Event Bubbling Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/edit_row)[](/examples/file_upload)
# Event Bubbling 
Demo

Key pressed: KEY
ELSE CM OM FETCH SET EXEC TEST
ALARM 3 2 1 ENTER CLEAR 
## HTML [#](#html)
 
```
[ 1](#24552c422b1244a2_line_1)<div id="demo">
[ 2](#24552c422b1244a2_line_2)    Key pressed: <span data-text="$key"></span>
[ 3](#24552c422b1244a2_line_3)    <div id="button-container" data-on:click="$key = evt.target.dataset.id">
[ 4](#24552c422b1244a2_line_4)        <button data-id="KEY ELSE" class="gray">KEY<br/>ELSE</button>
[ 5](#24552c422b1244a2_line_5)        <button data-id="CM">CM</button>
[ 6](#24552c422b1244a2_line_6)        <button data-id="OM">OM</button>
[ 7](#24552c422b1244a2_line_7)        <button data-id="FETCH">FETCH</button>
[ 8](#24552c422b1244a2_line_8)        <button data-id="SET">SET</button>
[ 9](#24552c422b1244a2_line_9)        <button data-id="EXEC">EXEC</button>
        <button data-id="TEST ALARM" class="gray">TEST<br/>ALARM</button>
        <button data-id="3">3</button>
        <button data-id="2">2</button>
        <button data-id="1">1</button>
        <button data-id="ENTER">ENTER</button>
        <button data-id="CLEAR">CLEAR</button>
    </div>
</div>

<style>
    #button-container {
        pointer-events: none;
    }
</style>
```
 
## Explanation [#](#explanation)
 

This example shows how [event bubbling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling) can be leveraged using Datastar. A `data-on:click` attribute on the parent container of the buttons. When any button is clicked, the event bubbles up to the parent, where we can access the clicked button’s `data-id` attribute via `evt.target.dataset.id`. This allows us to handle all button clicks with a single event listener.

Note the `pointer-events: none;` style on the button container. This is to prevent the container from sending click events.[](/examples/edit_row)[](/examples/file_upload)[](/star_federation)[](https://www.arcustech.com/)