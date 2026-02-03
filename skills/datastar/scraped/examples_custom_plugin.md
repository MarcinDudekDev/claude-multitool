# Source: https://data-star.dev/examples/custom_plugin

Custom Plugin Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/custom_event)[](/examples/dbmon)
# Custom Plugin 
 DemoAlert using an action Alert using an attribute 
## Explanation [#](#explanation)
 

Custom actions, attributes, and watchers can be implemented using the plugin API (documentation is in progress). This example implements a simple alert action and attribute.
### Action [#](#action)
 

An `action` plugin can be implemented as follows.
```
action({
    name: 'alert',
    apply(ctx, value) {
        alert(value)
    }
})
```
 

Setting the `name` to `alert` results in the syntax `@alert`.
```
<button data-on:click="@alert('Hello from an action')">
    Alert using an action
</button>
```
 
### Attribute [#](#attribute)
 

An `attribute` plugin can be implemented as follows.
```
[ 1](#d2be753829b23dc2_line_1)attribute({
[ 2](#d2be753829b23dc2_line_2)    name: 'alert',
[ 3](#d2be753829b23dc2_line_3)    requirement: {
[ 4](#d2be753829b23dc2_line_4)        key: 'denied',
[ 5](#d2be753829b23dc2_line_5)        value: 'must',
[ 6](#d2be753829b23dc2_line_6)    },
[ 7](#d2be753829b23dc2_line_7)    returnsValue: true,
[ 8](#d2be753829b23dc2_line_8)    apply({ el, rx }) {
[ 9](#d2be753829b23dc2_line_9)        const callback = () => alert(rx())
        el.addEventListener('click', callback)
        return () => el.removeEventListener('click', callback)
    }
})
```
 

Setting the `name` to `alert` results in the syntax `data-alert`.

The attribute shouldn’t take a key and needs a value, so `key` is `denied` and `value` is a `must`. The attribute expects a value to be returned from the expression so we set `returnsValue` to `true`.

On `apply`, we create an event listener that alerts the value returned from the expression when the element is clicked. We return a function that removes the event listener on `cleanup`.
```
<button data-alert="'Hello from an attribute'">
    Alert using an attribute
</button>
```
[](/examples/custom_event)[](/examples/dbmon)[](/star_federation)[](https://www.arcustech.com/)