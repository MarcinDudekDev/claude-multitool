# Source: https://data-star.dev/examples/progress_bar

Progress Bar Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/on_signal_patch)[](/examples/progressive_load)
# Progress Bar 
Demo 
## HTML [#](#html)
 
```
[ 1](#adbd50637fc297fc_line_1)<div id="progress-bar"
[ 2](#adbd50637fc297fc_line_2)     data-init="@get('/examples/progress_bar/updates', {openWhenHidden: true})"
[ 3](#adbd50637fc297fc_line_3)>
[ 4](#adbd50637fc297fc_line_4)    <svg
[ 5](#adbd50637fc297fc_line_5)        width="200"
[ 6](#adbd50637fc297fc_line_6)        height="200"
[ 7](#adbd50637fc297fc_line_7)        viewbox="-25 -25 250 250"
[ 8](#adbd50637fc297fc_line_8)        style="transform: rotate(-90deg)"
[ 9](#adbd50637fc297fc_line_9)    >
        <circle
            r="90"
            cx="100"
            cy="100"
            fill="transparent"
            stroke="#e0e0e0"
            stroke-width="16px"
            stroke-dasharray="565.48px"
            stroke-dashoffset="565px"
        ></circle>
        <circle
            r="90"
            cx="100"
            cy="100"
            fill="transparent"
            stroke="#6bdba7"
            stroke-width="16px"
            stroke-linecap="round"
            stroke-dashoffset="282px"
            stroke-dasharray="565.48px"
        ></circle>
        <text
            x="44px"
            y="115px"
            fill="#6bdba7"
            font-size="52px"
            font-weight="bold"
            style="transform:rotate(90deg) translate(0px, -196px)"
        >50%</text>
    </svg>
    
    <div data-on:click="@get('/examples/progress_bar/updates', {openWhenHidden: true})">
        <!-- When progress is 100% -->
        <button>
            Completed! Try again?
        </button>
    </div>
</div>
```
 
## Explanation [#](#explanation)
 

This example shows an updating progress graphic using SSE. The server sends down a new progress bar svg every 500 milliseconds causing the client to update. After the progress is complete, the server sends down a button allowing the user to restart the progress bar.
### Note [#](#note)
 

The `openWhenHidden` option is used to keep the connection open even when the progress bar is not visible. This is useful for when the user navigates away from the page and then returns.[](/examples/on_signal_patch)[](/examples/progressive_load)[](/star_federation)[](https://www.arcustech.com/)