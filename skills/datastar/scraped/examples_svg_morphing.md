# Source: https://data-star.dev/examples/svg_morphing

SVG Morphing Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/sortable)[](/examples/templ_counter)
# SVG Morphing 

Morphing elements within SVG elements is a little more invloved than standard HTML elements. This is because, as an XML dialect, SVG is [namespaced](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/Namespaces_crash_course). This means that `[<svg>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/svg)` elements (as well as `[<math>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/math)` elements) create their own namespace, separate from the HTML namespace. 

To morph an SVG element, you must either provide a `namespace` data line in the [`datastar-patch-elements`](/reference/sse_events#datastar-patch-elements) event:
```
event: datastar-patch-elements
data: namespace svg
data: elements <circle id="circle" cx="100" r="50" cy="75"></circle>


```
 

Or, alternatively, ensure that the target element is wrapped in an `<svg>` tag:
```
<svg id="circle">
    <circle cx="50" cy="100" r="50" fill="red" />
</svg>
```
 
## Basic Circle Color Change [#](#basic-circle-color-change)
 

This example demonstrates morphing an SVG circle’s color. Click the button to change  the circle from red to blue.DemoChange Color 
```
svgMorphingRouter.Get("/circle_color", func(w http.ResponseWriter, r *http.Request) {
    sse := datastar.NewSSE(w, r)
    color := svgColors[rand.N(len(svgColors))]
    sse.PatchElements(fmt.Sprintf(`<svg id="circle-demo"><circle cx="50" cy="50" r="40" fill="%s" /></svg>`, color))
})
```
 
## Circle Radius Change [#](#circle-radius-change)
 

This example shows how to morph the size of an SVG element. The circle will change  to a random radius when you click the button.DemoChange Radius 
```
svgMorphingRouter.Get("/circle_size", func(w http.ResponseWriter, r *http.Request) {
    sse := datastar.NewSSE(w, r)
    radius := 15 + rand.N(45) // Random radius between 15-60
    sse.PatchElements(fmt.Sprintf(`<svg id="size-demo"><circle cx="50" cy="50" r="%d" fill="green" /></svg>`, radius))
})
```
 
## Random Shape Transformation [#](#random-shape-transformation)
 

SVG morphing can handle changing between different shape types. This example morphs  to a random shape each time you click.DemoRandom Shape 
```
svgMorphingRouter.Get("/shape_transform", func(w http.ResponseWriter, r *http.Request) {
    sse := datastar.NewSSE(w, r)
    shape := svgShapes[rand.N(len(svgShapes))]
    sse.PatchElements(fmt.Sprintf(`<svg id="shape-demo">%s</svg>`, shape))
})
```
 
## Multiple Random Elements [#](#multiple-random-elements)
 

You can morph multiple SVG elements at once. This example updates three circles  with random colors and sizes each time you click.DemoRandomize All Circles 
```
[ 1](#5755852c6d11887d_line_1)svgMorphingRouter.Get("/multiple_elements", func(w http.ResponseWriter, r *http.Request) {
[ 2](#5755852c6d11887d_line_2)    sse := datastar.NewSSE(w, r)
[ 3](#5755852c6d11887d_line_3)    color1 := svgColors[rand.N(len(svgColors))]
[ 4](#5755852c6d11887d_line_4)    color2 := svgColors[rand.N(len(svgColors))]
[ 5](#5755852c6d11887d_line_5)    color3 := svgColors[rand.N(len(svgColors))]
[ 6](#5755852c6d11887d_line_6)    r1 := 10 + rand.N(20) // radius 10-30
[ 7](#5755852c6d11887d_line_7)    r2 := 10 + rand.N(20)
[ 8](#5755852c6d11887d_line_8)    r3 := 10 + rand.N(20)
[ 9](#5755852c6d11887d_line_9)    sse.PatchElements(fmt.Sprintf(`<svg id="multi-demo">
        <circle cx="30" cy="30" r="%d" fill="%s" />
        <circle cx="70" cy="30" r="%d" fill="%s" />
        <circle cx="50" cy="70" r="%d" fill="%s" />
    </svg>`, r1, color1, r2, color2, r3, color3))
})
```
 
## Animated Sequence [#](#animated-sequence)
 

This example demonstrates a sequence of SVG morphs that happen automatically  when triggered, creating a smooth animation effect.DemoStart Animation Sequence 
```
[ 1](#c0efbdb319b8c7b3_line_1)svgMorphingRouter.Get("/animated_morph", func(w http.ResponseWriter, r *http.Request) {
[ 2](#c0efbdb319b8c7b3_line_2)    sse := datastar.NewSSE(w, r)
[ 3](#c0efbdb319b8c7b3_line_3)    
[ 4](#c0efbdb319b8c7b3_line_4)    // First morph
[ 5](#c0efbdb319b8c7b3_line_5)    sse.PatchElements(`<svg id="animated-demo"><circle cx="50" cy="50" r="30" fill="red" /></svg>`)
[ 6](#c0efbdb319b8c7b3_line_6)    time.Sleep(500 * time.Millisecond)
[ 7](#c0efbdb319b8c7b3_line_7)    
[ 8](#c0efbdb319b8c7b3_line_8)    // Second morph
[ 9](#c0efbdb319b8c7b3_line_9)    sse.PatchElements(`<svg id="animated-demo"><circle cx="50" cy="50" r="45" fill="orange" /></svg>`)
    time.Sleep(500 * time.Millisecond)
    
    // Third morph
    sse.PatchElements(`<svg id="animated-demo"><circle cx="50" cy="50" r="60" fill="yellow" /></svg>`)
    time.Sleep(500 * time.Millisecond)
    
    // Reset
    sse.PatchElements(`<svg id="animated-demo"><circle cx="50" cy="50" r="20" fill="green" /></svg>`)
})
```
 
## Key Points [#](#key-points)
 
- SVG elements must be wrapped in an outer `<svg>` container
- The inner `<svg>` element should have the target ID
- All SVG element types (circle, rect, path, etc.) can be morphed
- Multiple SVG elements can be updated in a single morph operation
- CSS transitions work with SVG morphing for smooth animations[](/examples/sortable)[](/examples/templ_counter)[](/star_federation)[](https://www.arcustech.com/)