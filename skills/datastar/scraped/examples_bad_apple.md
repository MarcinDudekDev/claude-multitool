# Source: https://data-star.dev/examples/bad_apple

Bad Apple Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/animations)[](/examples/bulk_update)
# Bad Apple 
Demo   
## Explanation [#](#explanation)
 

Per a conversation on the [htmx meme discord channel](https://discordapp.com/channels/725789699527933952/996832027083026563/1276380165613813894) there was an offhand remark about adding the [Bad Apple Music video](https://www.youtube.com/watch?v=FtutLA63Cp8) as a benchmark. Thought it'd be fun to do so. We take the [already converted](https://github.com/trung-kieen/bad-apple-ascii) frames of video and turn them into a ZSTD compressed Gob file that’s embedded in the server binary. This makes the whole animation about 1.9MB. We then stream the frames to the client and update the contents of a pre tag with the frames. The percentage is updated with the current frame number.
```
[ 1](#19fba88959271494_line_1)<label
[ 2](#19fba88959271494_line_2)    data-signals="{_percentage: 0, _contents: 'bad apple frames go here'}"
[ 3](#19fba88959271494_line_3)    data-init="@get('/examples/bad_apple/updates')"
[ 4](#19fba88959271494_line_4)>
[ 5](#19fba88959271494_line_5)    <span data-text="`Percentage: ${$_percentage.toFixed(2)}%`"></span>
[ 6](#19fba88959271494_line_6)    <input
[ 7](#19fba88959271494_line_7)        type="range"
[ 8](#19fba88959271494_line_8)        min="0"
[ 9](#19fba88959271494_line_9)        max="100"
        step="0.01"
        disabled
        style="cursor: default"
        data-attr:value="$_percentage"
    />
</label>
<pre style="line-height: 100%" data-text="$_contents"></pre>
```
 

This is using Datastar’s ability to patch signals directly. ***No need to generate HTML elements, as the contents are already bound to existing elements.*** We could also stream down the raster frames using base64 encoded images and update the src of an image tag. Either way works, you would just have to use `data-attr:src` on an image tag. Open your browser dev tool’s inspector tab for the contents of the `pre` tag. You'll see the frames being updated in real-time (in this case 30fps).[](/examples/animations)[](/examples/bulk_update)[](/star_federation)[](https://www.arcustech.com/)