# Source: https://data-star.dev/examples/on_signal_patch

On Signal Patch Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/lazy_tabs)[](/examples/progress_bar)
# On Signal Patch 
Demo Update Message Increment Counter Clear All Changes
### Current Values

Counter: 

Message: 
### Counter Changes Only

### All Signal Changes
 
## Explanation [#](#explanation)
 
```
[ 1](#e18437496ab12440_line_1)<div data-signals="{counter: 0, message: 'Hello World', allChanges: [], counterChanges: []}">
[ 2](#e18437496ab12440_line_2)    <div class="actions">
[ 3](#e18437496ab12440_line_3)        <button data-on:click="$message = `Updated: ${performance.now().toFixed(2)}`">
[ 4](#e18437496ab12440_line_4)            Update Message
[ 5](#e18437496ab12440_line_5)        </button>
[ 6](#e18437496ab12440_line_6)        <button data-on:click="$counter++">
[ 7](#e18437496ab12440_line_7)            Increment Counter
[ 8](#e18437496ab12440_line_8)        </button>
[ 9](#e18437496ab12440_line_9)        <button
            class="error"
            data-on:click="$allChanges.length = 0; $counterChanges.length = 0"
        >
            Clear All Changes
        </button>
    </div>
    <div>
        <h3>Current Values</h3>
        <p>Counter: <span data-text="$counter"></span></p>
        <p>Message: <span data-text="$message"></span></p>
    </div>
    <div
        data-on-signal-patch="$counterChanges.push(patch)"
        data-on-signal-patch-filter="{include: /^counter$/}"
    >
        <h3>Counter Changes Only</h3>
        <pre data-json-signals__terse="{include: /^counterChanges/}"></pre>
    </div>
    <div
        data-on-signal-patch="$allChanges.push(patch)"
        data-on-signal-patch-filter="{exclude: /allChanges|counterChanges/}"
    >
        <h3>All Signal Changes</h3>
        <pre data-json-signals__terse="{include: /^allChanges/}"></pre>
    </div>
</div>
```
 

The [`data-on-signal-patch`](/reference/attributes#data-on-signal-patch) plugin allows you to execute an expression whenever signals are patched. This is useful for tracking changes, updating dependent values, or triggering side effects.

You can filter which signals to watch using the `data-on-signal-patch-filter` attribute with include/exclude patterns, as seen above.[](/examples/lazy_tabs)[](/examples/progress_bar)[](/star_federation)[](https://www.arcustech.com/)