# Source: https://data-star.dev/examples/bulk_update

Bulk Update Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/bad_apple)[](/examples/click_to_edit)
# Bulk Update 
DemoNameEmailStatus Joe Smith[[email protected]](/cdn-cgi/l/email-protection)ActiveAngie MacDowell[[email protected]](/cdn-cgi/l/email-protection)ActiveFuqua Tarkenton[[email protected]](/cdn-cgi/l/email-protection)InactiveKim Yee[[email protected]](/cdn-cgi/l/email-protection)InactiveActivate Deactivate 
## HTML [#](#html)
 
```
[ 1](#b9f0b5177a76b3a2_line_1)<div
[ 2](#b9f0b5177a76b3a2_line_2)    id="demo"
[ 3](#b9f0b5177a76b3a2_line_3)    data-signals__ifmissing="{_fetching: false, selections: Array(4).fill(false)}"
[ 4](#b9f0b5177a76b3a2_line_4)>
[ 5](#b9f0b5177a76b3a2_line_5)    <table>
[ 6](#b9f0b5177a76b3a2_line_6)        <thead>
[ 7](#b9f0b5177a76b3a2_line_7)            <tr>
[ 8](#b9f0b5177a76b3a2_line_8)                <th>
[ 9](#b9f0b5177a76b3a2_line_9)                    <input
                        type="checkbox"
                        data-bind:_all
                        data-on:change="$selections = Array(4).fill($_all)"
                        data-effect="$selections; $_all = $selections.every(Boolean)"
                        data-attr:disabled="$_fetching"
                    />
                </th>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <input
                        type="checkbox"
                        data-bind:selections
                        data-attr:disabled="$_fetching"
                    />
                </td>
                <td>Joe Smith</td>
                <td>[[email protected]](/cdn-cgi/l/email-protection)</td>
                <td>Active</td>
            </tr>
            <!-- More rows... -->
        </tbody>
    </table>
    <div role="group">
        <button
            class="success"
            data-on:click="@put('/examples/bulk_update/activate')"
            data-indicator:_fetching
            data-attr:disabled="$_fetching"
        >
            <i class="pixelarticons:user-plus"></i>
            Activate
        </button>
        <button
            class="error"
            data-on:click="@put('/examples/bulk_update/deactivate')"
            data-indicator:_fetching
            data-attr:disabled="$_fetching"
        >
            <i class="pixelarticons:user-x"></i>
            Deactivate
        </button>
    </div>
</div>
```
 
## Explanation [#](#explanation)
 

This example shows how to implement a common pattern where rows are selected and then bulk updated. This is accomplished by putting a form around a table, with checkboxes in the table, and then including the checked values in `PUT`s to two different endpoints: activate and deactivate.

The server will either activate or deactivate the checked users and then re-render the table with updated rows.[](/examples/bad_apple)[](/examples/click_to_edit)[](/star_federation)[](https://www.arcustech.com/)