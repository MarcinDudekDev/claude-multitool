# Source: https://data-star.dev/examples/click_to_edit

Click To Edit Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/bulk_update)[](/examples/click_to_load)
# Click To Edit 
Demo

First Name: John

Last Name: Doe

Email: [[email protected]](/cdn-cgi/l/email-protection)Edit Reset 
## Explanation [#](#explanation)
 

The click to edit pattern is a way to inline edit all or part of a record without a page refresh. This pattern starts with a UI that shows the details of a contact. The div has a button that will get the editing UI for the contact from `/edit`
```
[ 1](#183b8ea05a71a9b8_line_1)<div id="demo">
[ 2](#183b8ea05a71a9b8_line_2)    <p>First Name: John</p>
[ 3](#183b8ea05a71a9b8_line_3)    <p>Last Name: Doe</p>
[ 4](#183b8ea05a71a9b8_line_4)    <p>Email: [[email protected]](/cdn-cgi/l/email-protection)</p>
[ 5](#183b8ea05a71a9b8_line_5)    <div role="group">
[ 6](#183b8ea05a71a9b8_line_6)        <button
[ 7](#183b8ea05a71a9b8_line_7)            class="info"
[ 8](#183b8ea05a71a9b8_line_8)            data-indicator:_fetching
[ 9](#183b8ea05a71a9b8_line_9)            data-attr:disabled="$_fetching"
            data-on:click="@get('/examples/click_to_edit/edit')"
        >
            Edit
        </button>
        <button
            class="warning"
            data-indicator:_fetching
            data-attr:disabled="$_fetching"
            data-on:click="@patch('/examples/click_to_edit/reset')"
        >
            Reset
        </button>
    </div>
</div>
```
 

This returns a form that can be used to edit the contact
```
[ 1](#18135e807fc541f6_line_1)<div id="demo">
[ 2](#18135e807fc541f6_line_2)    <label>
[ 3](#18135e807fc541f6_line_3)        First Name
[ 4](#18135e807fc541f6_line_4)        <input
[ 5](#18135e807fc541f6_line_5)            type="text"
[ 6](#18135e807fc541f6_line_6)            data-bind:first-name
[ 7](#18135e807fc541f6_line_7)            data-attr:disabled="$_fetching"
[ 8](#18135e807fc541f6_line_8)        >
[ 9](#18135e807fc541f6_line_9)    </label>
    <label>
        Last Name
        <input
            type="text"
            data-bind:last-name
            data-attr:disabled="$_fetching"
        >
    </label>
    <label>
        Email
        <input
            type="email"
            data-bind:email
            data-attr:disabled="$_fetching"
        >
    </label>
    <div role="group">
        <button
            class="success"
            data-indicator:_fetching
            data-attr:disabled="$_fetching"
            data-on:click="@put('/examples/click_to_edit')"
        >
            Save
        </button>
        <button
            class="error"
            data-indicator:_fetching
            data-attr:disabled="$_fetching"
            data-on:click="@get('/examples/click_to_edit/cancel')"
        >
            Cancel
        </button>
    </div>
</div>
```
 
### There Is No Form [#](#there-is-no-form)
 

If you compare to htmx you’ll notice there is no form, you can use one, but it’s unnecessary. This is because you’re already using signals and when you `PUT` to `/edit`, the body is the entire contents of the signals, and it’s available to handle errors and validation holistically. There is also a profanity filter on the normal rendering of the contact that is not applied to the edit form. Controlling the rendering completely on the server allows you to have a single source of truth for the data and the rendering.
### There Is No Client Side Validation [#](#there-is-no-client-side-validation)
 

On the backend we’ve also added a quick sanitizer on the input to avoid bad actors (to some degree). You already have to deal with the data on the server so you might as well do the validation there. In this case, its just modifying how the text is rendered when not editing. This is a simple example, but you can see how to extend it to more complex forms.[](/examples/bulk_update)[](/examples/click_to_load)[](/star_federation)[](https://www.arcustech.com/)