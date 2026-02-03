# Source: https://data-star.dev/examples/progressive_load

Progressive Load Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/progress_bar)[](/examples/sortable)
# Progressive Load 

Demonstrates how to progressively load different sections of a page using SSE events. DemoLoad

Each part is loaded randomly and progressively. 
## HTML [#](#html)
 
```
[ 1](#f64e0b9b78a6acd3_line_1)<div>
[ 2](#f64e0b9b78a6acd3_line_2)    <div class="actions">
[ 3](#f64e0b9b78a6acd3_line_3)        <button
[ 4](#f64e0b9b78a6acd3_line_4)            id="load-button"
[ 5](#f64e0b9b78a6acd3_line_5)            data-signals:load-disabled="false"
[ 6](#f64e0b9b78a6acd3_line_6)            data-on:click="$loadDisabled=true; @get('/examples/progressive_load/updates')"
[ 7](#f64e0b9b78a6acd3_line_7)            data-attr:disabled="$loadDisabled"
[ 8](#f64e0b9b78a6acd3_line_8)            data-indicator:progressive-Load
[ 9](#f64e0b9b78a6acd3_line_9)        >
            Load
        </button>
        <!-- Indicator element -->
    </div>
    <p>
        Each part is loaded randomly and progressively.
    </p>
</div>
<div id="Load">
    <header id="header">Welcome to my blog</header>
    <section id="article">
        <h4>This is my article</h4>
        <section id="articleBody">
            <p>
                Lorem ipsum dolor sit amet...
            </p>
        </section>
    </section>
    <section id="comments">
        <h5>Comments</h5>
        <p>
            This is the comments section. It will also be progressively loaded as you scroll down.
        </p>
        <ul id="comments-list">
            <li id="1">
                <img src="https://avatar.iran.liara.run/username?username=example" alt="Avatar" class="avatar"/>
                This is a comment...
            </li>
            <!-- More comments loaded progressively -->
        </ul>
    </section>
    <div id="footer">Hope you like it</div>
</div>
```
 
## Explanation [#](#explanation)
 

This is a response to [Dan Abramov's article on progressive JSON](https://overreacted.io/progressive-json/). I think it's overcomplicated and shows a lack of understanding of how powerful native hypermedia is.
### Note [#](#note)
 

This example shows how to progressively load a page using Datastar. The page is divided into sections. We already have examples of [infinite scroll](/examples/infinite_scroll) and [progress bar](/examples/progress_bar), but this example shows how to progressively load a page in a more structured way.

It's truly baffling to me the amount of complexity that React developers tend to introduce. Hypermedia is a powerful tool that allows you to progressively load content in a way that is simple and efficient. This example shows how to use Datastar's server-sent events (SSE) to progressively load a page in a way that is easy to understand and maintain.

Nothing is faster than direct HTML morphing without a virtual DOM. – let the browser do the heavy lifting. This example shows how to use Datastar to progressively load a page in a way that is simple and efficient while only using a one-time cost CDN shim.[](/examples/progress_bar)[](/examples/sortable)[](/star_federation)[](https://www.arcustech.com/)