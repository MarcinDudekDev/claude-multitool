# Source: https://data-star.dev/examples/web_component

Web Component Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/todomvc)[](/examples/rocket_copy_button)
# Web Component 
 DemoReversed    
## Explanation [#](#explanation)
 

This is an example of two-way binding with a web component that reverses a string. Normally, the web component would output the reversed value, but in this example, all it does is perform the logic and dispatch an event containing the result, which is then displayed.
```
<label>
    Reversed
    <input type="text" value="Your Name" data-bind:_name/>
</label>
<span data-signals:_reversed data-text="$_reversed"></span>
<reverse-component
    data-on:reverse="$_reversed = evt.detail.value"
    data-attr:name="$_name"
></reverse-component>
```
 

The `name` attribute value is bound to the `$_name` signal's value, and an event listener modifies the `$_reversed` signal's value sent in the `reverse` event. The web component observes changes to the `name` attribute and responds by reversing the string and dispatching a `reverse` event containing the resulting value.
```
[ 1](#d5473e5fc4db5bb1_line_1)class ReverseComponent extends HTMLElement {
[ 2](#d5473e5fc4db5bb1_line_2)    static get observedAttributes() {
[ 3](#d5473e5fc4db5bb1_line_3)        return ["name"];
[ 4](#d5473e5fc4db5bb1_line_4)    }
[ 5](#d5473e5fc4db5bb1_line_5)
[ 6](#d5473e5fc4db5bb1_line_6)    attributeChangedCallback(name, oldValue, newValue) {
[ 7](#d5473e5fc4db5bb1_line_7)        const value = [...newValue].toReversed().join("");
[ 8](#d5473e5fc4db5bb1_line_8)        this.dispatchEvent(new CustomEvent("reverse", { detail: { value } }));
[ 9](#d5473e5fc4db5bb1_line_9)    }
}

customElements.define("reverse-component", ReverseComponent);
```
[](/examples/todomvc)[](/examples/rocket_copy_button)[](/star_federation)[](https://www.arcustech.com/)