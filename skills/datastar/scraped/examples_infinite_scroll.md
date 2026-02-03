# Source: https://data-star.dev/examples/infinite_scroll

Infinite Scroll Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/form_data)[](/examples/inline_validation)
# Infinite Scroll 

The infinite scroll pattern provides a way to load content dynamically on user scrolling action.

Let’s focus on the final row (or the last element of your content):
```
<div data-on-intersect="@get('/examples/infinite_scroll/more')">
    Loading...
</div>
```
 

This last element contains a listener which, when scrolled into view, will trigger a request. The result is then appended after it. `data-on-intersect` is an attribute that triggers a request when the element is scrolled into view.DemoAgents NameEmailID Agent Smith 0[[email protected]](/cdn-cgi/l/email-protection)1982e3a7bb241055Agent Smith 1[[email protected]](/cdn-cgi/l/email-protection)65cd25028f98f158Agent Smith 2[[email protected]](/cdn-cgi/l/email-protection)7b95a7322f5da314Agent Smith 3[[email protected]](/cdn-cgi/l/email-protection)7324dc1e7e9474f0Agent Smith 4[[email protected]](/cdn-cgi/l/email-protection)628911027fcf803fAgent Smith 5[[email protected]](/cdn-cgi/l/email-protection)5edb980100c87e72Agent Smith 6[[email protected]](/cdn-cgi/l/email-protection)3564a48862bc4a0dAgent Smith 7[[email protected]](/cdn-cgi/l/email-protection)6eed105b82285faAgent Smith 8[[email protected]](/cdn-cgi/l/email-protection)664f427c6b2c4beaAgent Smith 9[[email protected]](/cdn-cgi/l/email-protection)28353a066812b268Loading...[](/examples/form_data)[](/examples/inline_validation)[](/star_federation)[](https://www.arcustech.com/)