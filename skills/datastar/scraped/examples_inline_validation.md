# Source: https://data-star.dev/examples/inline_validation

Inline Validation Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/infinite_scroll)[](/examples/lazy_load)
# Inline Validation 
DemoEmail Address  

The only valid email address is "[[email protected]](/cdn-cgi/l/email-protection)".First Name  Last Name  Sign Up 
## HTML [#](#html)
 
```
[ 1](#dcc17718b9545b86_line_1)<div id="demo">
[ 2](#dcc17718b9545b86_line_2)    <label>
[ 3](#dcc17718b9545b86_line_3)        Email Address
[ 4](#dcc17718b9545b86_line_4)        <input
[ 5](#dcc17718b9545b86_line_5)            type="email"
[ 6](#dcc17718b9545b86_line_6)            required
[ 7](#dcc17718b9545b86_line_7)            aria-live="polite"
[ 8](#dcc17718b9545b86_line_8)            aria-describedby="email-info"
[ 9](#dcc17718b9545b86_line_9)            data-bind:email
            data-on:keydown__debounce.500ms="@post('/examples/inline_validation/validate')"
        />
    </label>
    <p id="email-info" class="info">The only valid email address is "[[email protected]](/cdn-cgi/l/email-protection)".</p>
    <label>
        First Name
        <input
            type="text"
            required
            aria-live="polite"
            data-bind:first-name
            data-on:keydown__debounce.500ms="@post('/examples/inline_validation/validate')"
        />
    </label>
    <label>
        Last Name
        <input
            type="text"
            required
            aria-live="polite"
            data-bind:last-name
            data-on:keydown__debounce.500ms="@post('/examples/inline_validation/validate')"
        />
    </label>
    <button
        class="success"
        data-on:click="@post('/examples/inline_validation')"
    >
        <i class="material-symbols:person-add"></i>
        Sign Up
    </button>
</div>
```
 
## Explanation [#](#explanation)
 

This example shows how to do inline field validation, in this case of an email address. To do this we need to create a form with an input that `POST`s back to the server with the value to be validated and updates the DOM with the validation results. Since it’s easy to replace the whole form, the logic for displaying the validation results is kept simple.[](/examples/infinite_scroll)[](/examples/lazy_load)[](/star_federation)[](https://www.arcustech.com/)