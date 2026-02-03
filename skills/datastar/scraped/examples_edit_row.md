# Source: https://data-star.dev/examples/edit_row

Edit Row Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/delete_row)[](/examples/event_bubbling)
# Edit Row 
DemoNameEmailActions Joe Smith[[email protected]](/cdn-cgi/l/email-protection)EditAngie MacDowell[[email protected]](/cdn-cgi/l/email-protection)EditFuqua Tarkenton[[email protected]](/cdn-cgi/l/email-protection)EditKim Yee[[email protected]](/cdn-cgi/l/email-protection)EditReset 
## Explanation [#](#explanation)
 

This example shows how to implement editable rows. First let’s look at the row prior to editing:
```
<tr>
    <td>Joe Smith</td>
    <td>[[email protected]](/cdn-cgi/l/email-protection)</td>
    <td>
        <button data-on:click="@get('/examples/edit_row/0')">
            Edit
        </button>
    </td>
</tr>
```
 

This will trigger a whole table replacement as we are going to remove the edit buttons from other rows as well as change out the inputs to allow editing.

Finally, here is what the row looks like when the data is being edited:
```
[ 1](#ad2428b964e077d8_line_1)<tr>
[ 2](#ad2428b964e077d8_line_2)    <td>
[ 3](#ad2428b964e077d8_line_3)        <input type="text" data-bind:name>
[ 4](#ad2428b964e077d8_line_4)    </td>
[ 5](#ad2428b964e077d8_line_5)    <td>
[ 6](#ad2428b964e077d8_line_6)        <input type="text" data-bind:email>
[ 7](#ad2428b964e077d8_line_7)    </td>
[ 8](#ad2428b964e077d8_line_8)    <td>
[ 9](#ad2428b964e077d8_line_9)        <button data-on:click="@get('/examples/edit_row/cancel')">
            Cancel
        </button>
        <button data-on:click="@patch('/examples/edit_row/0')">
            Save
        </button>
    </td>
</tr>
```
 

Here we have a few things going on, clicking the cancel button will bring back the read-only version of the row. Finally, there is a save button that issues a `PATCH` to update the contact.[](/examples/delete_row)[](/examples/event_bubbling)[](/star_federation)[](https://www.arcustech.com/)