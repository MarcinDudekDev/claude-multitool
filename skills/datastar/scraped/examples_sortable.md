# Source: https://data-star.dev/examples/sortable

Sortable Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/progressive_load)[](/examples/svg_morphing)
# Sortable 
Demo

[Item 1]() [Item 2]() [Item 3]() [Item 4]() [Item 5]() 
## Explanation [#](#explanation)
 

Datastar allows you to listen for custom events using `data-on` and react to them by modifying signals.
```
[ 1](#ed2fbbd75494ef68_line_1)<div data-signals:order-info="'Initial order'" data-text="$orderInfo"></div>
[ 2](#ed2fbbd75494ef68_line_2)<div id="sortContainer" data-on:reordered="$orderInfo = event.detail.orderInfo">
[ 3](#ed2fbbd75494ef68_line_3)    <button>Item 1</button>
[ 4](#ed2fbbd75494ef68_line_4)    <button>Item 2</button>
[ 5](#ed2fbbd75494ef68_line_5)    <button>Item 3</button>
[ 6](#ed2fbbd75494ef68_line_6)    <button>Item 4</button>
[ 7](#ed2fbbd75494ef68_line_7)    <button>Item 5</button>
[ 8](#ed2fbbd75494ef68_line_8)</div>
[ 9](#ed2fbbd75494ef68_line_9)
<script type="module">
    import Sortable from 'https://cdn.jsdelivr.net/npm/sortablejs/+esm'
    new Sortable(sortContainer, {
        animation: 150,
        ghostClass: 'opacity-25',
        onEnd: (evt) => {
            sortContainer.dispatchEvent(
                new CustomEvent('reordered', {detail: {
                    orderInfo: `Moved from position ${evt.oldIndex + 1} to ${evt.newIndex + 1}`
                }})
            )
        }
    })
</script>
```
 

We create an `orderInfo` signal and modify it whenever a `reordered` event is triggered.

We instruct the [SortableJS](https://sortablejs.github.io/Sortable/) library to dispatch a custom event `reordered` whenever the sortable list is changed.  This event contains the order information that we can use to update the `orderInfo` signal.[](/examples/progressive_load)[](/examples/svg_morphing)[](/star_federation)[](https://www.arcustech.com/)