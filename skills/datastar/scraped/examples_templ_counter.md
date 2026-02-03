# Source: https://data-star.dev/examples/templ_counter

Templ Counter Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/svg_morphing)[](/examples/title_update)
# Templ Counter 
DemoIncrement Global: 342Increment User: 0 
## HTML [#](#html)
 
```
[ 1](#17beb731204885a1_line_1)<div data-init="@get('/examples/templ_counter/updates')">
[ 2](#17beb731204885a1_line_2)    <!-- Global Counter -->
[ 3](#17beb731204885a1_line_3)    <button
[ 4](#17beb731204885a1_line_4)        id="global"
[ 5](#17beb731204885a1_line_5)        class="info"
[ 6](#17beb731204885a1_line_6)        data-on:click="@patch('/examples/templ_counter/global')"
[ 7](#17beb731204885a1_line_7)    >
[ 8](#17beb731204885a1_line_8)        Global Clicks: 0
[ 9](#17beb731204885a1_line_9)    </button>

    <!-- User Counter -->
    <button
        id="user"
        class="success"
        data-on:click="@patch('/examples/templ_counter/user')"
    >
        User Clicks: 0
    </button>
</div>
```
 
## Explanation [#](#explanation)
 

This example demonstrates two counters - a global counter shared across all users and a user-specific counter. The counters are updated via server-sent events (SSE) and increment when clicked.[](/examples/svg_morphing)[](/examples/title_update)[](/star_federation)[](https://www.arcustech.com/)