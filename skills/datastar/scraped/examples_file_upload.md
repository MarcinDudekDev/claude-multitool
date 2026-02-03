# Source: https://data-star.dev/examples/file_upload

File Upload Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/event_bubbling)[](/examples/form_data)
# File Upload 
Demo

Pick anything less than 1 MiB Submit 
## Explanation [#](#explanation)
 

In this example we show how to create a file upload form that will be submitted via fetch.
```
[ 1](#ccb583ab572f5945_line_1)<label>
[ 2](#ccb583ab572f5945_line_2)    <p>Pick anything less than 1MB</p>
[ 3](#ccb583ab572f5945_line_3)    <input type="file" data-bind:files multiple/>
[ 4](#ccb583ab572f5945_line_4)</label>
[ 5](#ccb583ab572f5945_line_5)<button
[ 6](#ccb583ab572f5945_line_6)    class="warning"
[ 7](#ccb583ab572f5945_line_7)    data-on:click="$files.length && @post('/examples/file_upload')"
[ 8](#ccb583ab572f5945_line_8)    data-attr:aria-disabled="`${!$files.length}`"
[ 9](#ccb583ab572f5945_line_9)>
    Submit
</button>
```
 

We don’t need a form because everything is encoded as signals and automatically sent to the server. We `POST` the form to `/examples/file_upload`, since the `input` is using `data-bind` the file’s contents will be automatically encoded as base64. 
### Note [#](#note)
 

If you try to upload a file that is too large you will get an error message in the console.[](/examples/event_bubbling)[](/examples/form_data)[](/star_federation)[](https://www.arcustech.com/)