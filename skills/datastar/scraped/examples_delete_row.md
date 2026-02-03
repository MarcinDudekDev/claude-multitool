# Source: https://data-star.dev/examples/delete_row

Delete Row Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/dbmon)[](/examples/edit_row)
# Delete Row 
DemoNameEmailActions Fuqua Tarkenton[[email protected]](/cdn-cgi/l/email-protection)DeleteReset 
## Explanation [#](#explanation)
 

This example shows how to implement a delete button that removes a table row upon completion. First let’s look at the table body:
```
[ 1](#1d650d6ce6c762e0_line_1)<table>
[ 2](#1d650d6ce6c762e0_line_2)    <thead>
[ 3](#1d650d6ce6c762e0_line_3)        <tr>
[ 4](#1d650d6ce6c762e0_line_4)            <th>Name</th>
[ 5](#1d650d6ce6c762e0_line_5)            <th>Email</th>
[ 6](#1d650d6ce6c762e0_line_6)            <th>Actions</th>
[ 7](#1d650d6ce6c762e0_line_7)        </tr>
[ 8](#1d650d6ce6c762e0_line_8)    </thead>
[ 9](#1d650d6ce6c762e0_line_9)    <tbody>
        <tr>
            <td>Joe Smith</td>
            <td>[[email protected]](/cdn-cgi/l/email-protection)</td>
            <td>
                <button
                    class="error"
                    data-on:click="confirm('Are you sure?') && @delete('/examples/delete_row/0')"
                    data-indicator:_fetching
                    data-attr:disabled="$_fetching"
                >
                    Delete
                </button>
            </td>
        </tr>
    </tbody>
</table>
```
 

The row has a normal confirm to `confirm()` the delete action.[](/examples/dbmon)[](/examples/edit_row)[](/star_federation)[](https://www.arcustech.com/)