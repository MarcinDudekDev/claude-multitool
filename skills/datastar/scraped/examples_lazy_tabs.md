# Source: https://data-star.dev/examples/lazy_tabs

Lazy Tabs Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/lazy_load)[](/examples/on_signal_patch)
# Lazy Tabs 
DemoTab 0Tab 1Tab 2Tab 3Tab 4Tab 5Tab 6Tab 7

Et esse nemo fuga in laboriosam. Voluptatem tempore quia doloribus sit eum. Deserunt ex repellendus adipisci libero placeat. Quae dolores dolorem nobis quasi distinctio. Quia accusantium laudantium doloribus facere ullam. Quis officiis corporis voluptatum consequatur quos. Earum repellat repellendus aperiam ipsa id. Ut aspernatur pariatur delectus fugiat impedit. Et eveniet in quia nobis sed. 
## HTML [#](#html)
 
```
[ 1](#ed7a29af0c4044c8_line_1)<div id="demo">
[ 2](#ed7a29af0c4044c8_line_2)    <div role="tablist">
[ 3](#ed7a29af0c4044c8_line_3)        <button
[ 4](#ed7a29af0c4044c8_line_4)            role="tab"
[ 5](#ed7a29af0c4044c8_line_5)            aria-selected="true"
[ 6](#ed7a29af0c4044c8_line_6)            data-on:click="@get('/examples/lazy_tabs/0')"
[ 7](#ed7a29af0c4044c8_line_7)        >
[ 8](#ed7a29af0c4044c8_line_8)            Tab 0
[ 9](#ed7a29af0c4044c8_line_9)        </button>
        <button
            role="tab"
            aria-selected="false"
            data-on:click="@get('/examples/lazy_tabs/1')"
        >
            Tab 1
        </button>
        <button
            role="tab"
            aria-selected="false"
            data-on:click="@get('/examples/lazy_tabs/2')"
        >
            Tab 2
        </button>
        <!-- More tabs... -->
    </div>
    <div role="tabpanel">
        <p>Lorem ipsum dolor sit amet...</p>
        <p>Consectetur adipiscing elit...</p>
        <!-- Tab content -->
    </div>
</div>
```
 
## Explanation [#](#explanation)
 

This example shows how easy it is to implement tabs using Datastar. Following the principles of Hypertext As The Engine Of Application State, the selected tab is a part of the application state. Therefore, to display and select tabs in your application, simply include the tab markup in the returned HTML fragment.[](/examples/lazy_load)[](/examples/on_signal_patch)[](/star_federation)[](https://www.arcustech.com/)