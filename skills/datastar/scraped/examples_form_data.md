# Source: https://data-star.dev/examples/form_data

Form Data Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/file_upload)[](/examples/infinite_scroll)
# Form Data 
Demo

foo:  bar:  baz:

Submit GET request   Submit POST requestSubmit GET request from outside the form 
## Explanation [#](#explanation)
 

Setting the `contentType` option to `form` tells the `@get()` action to look for the closest form, perform validation on it, and send all form elements within it to the backend. A `selector` option can be provided to specify a form element. No signals are sent to the backend in this type of request.
```
[ 1](#96e836ed3e078205_line_1)<form id="myform">
[ 2](#96e836ed3e078205_line_2)    foo:<input type="checkbox" name="checkboxes" value="foo" />
[ 3](#96e836ed3e078205_line_3)    bar:<input type="checkbox" name="checkboxes" value="bar" />
[ 4](#96e836ed3e078205_line_4)    baz:<input type="checkbox" name="checkboxes" value="baz" />
[ 5](#96e836ed3e078205_line_5)    <button data-on:click="@get('/endpoint', {contentType: 'form'})">
[ 6](#96e836ed3e078205_line_6)        Submit GET request
[ 7](#96e836ed3e078205_line_7)    </button>
[ 8](#96e836ed3e078205_line_8)    <button data-on:click="@post('/endpoint', {contentType: 'form'})">
[ 9](#96e836ed3e078205_line_9)        Submit POST request
    </button>
</form>

<button data-on:click="@get('/endpoint', {contentType: 'form', selector: '#myform'})">
    Submit GET request from outside the form
</button>
```
 Demo

foo: Submit form 
## Explanation [#](#explanation)
 

In this example, the `@get()` action is placed inside a submit listener on the form element using `data-on:submit`.
```
<form data-on:submit="@get('/endpoint', {contentType: 'form'})">
    foo: <input type="text" name="foo" required />
    <button>
        Submit form
    </button>
</form>
```
[](/examples/file_upload)[](/examples/infinite_scroll)[](/star_federation)[](https://www.arcustech.com/)