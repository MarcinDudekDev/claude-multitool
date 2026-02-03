# Source: https://data-star.dev/examples/animations

Animations Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/active_search)[](/examples/bad_apple)
# Animations 

Datastar is designed to allow you to use CSS transitions and the new View Transitions API to add smooth animations and transitions to your web page using only CSS and HTML. Below are a few examples of various animation techniques.
## Color Throb [#](#color-throb)
 

The simplest animation technique in Datastar is to keep the id of an element stable across a content swap. If the id of an element is kept stable, Datastar will swap it in such a way that CSS transitions can be written between the old version of the element and the new one.

Consider this divDemobrown on orange 

With SSE, we just update the style every second
```
<div
    id="color-throb"
    style="color: var(--blue-8); background-color: var(--orange-5);"
>
    blue on orange
</div>
```
 
## View Transitions [#](#view-transitions)
 

The swapping of the button below is happening on the backend. Each click is causing a transition of state. The animated opacity animation is provided automatically by the View Transition API (not yet supported by Firefox). Doesn’t matter if the targeted elements are different types, it will still “do the right thing”.DemoSwap It! 
## Fade Out On Swap [#](#fade-out-on-swap)
 

If you want to fade out an element that is going to be removed when the request ends, just send an SSE event with the opacity set to 0 and set a transition duration. This will fade out the element before it is removed.DemoFade out then delete on click 
## Fade In On Addition [#](#fade-in-on-addition)
 

Building on the previous example, we can fade in the new content the same way, starting from an opacity of 0 and transitioning to an opacity of 1.DemoFade me in on click[](/examples/active_search)[](/examples/bad_apple)[](/star_federation)[](https://www.arcustech.com/)