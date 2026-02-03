# Source: https://data-star.dev/examples/todomvc

TodoMVC Example 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ExamplesExamples of what Datastar can do.[](/examples/active_search)[](/examples/animations)[](/examples/bad_apple)[](/examples/bulk_update)[](/examples/click_to_edit)[](/examples/click_to_load)[](/examples/custom_event)[](/examples/custom_plugin)[](/examples/dbmon)[](/examples/delete_row)[](/examples/edit_row)[](/examples/event_bubbling)[](/examples/file_upload)[](/examples/form_data)[](/examples/infinite_scroll)[](/examples/inline_validation)[](/examples/lazy_load)[](/examples/lazy_tabs)[](/examples/on_signal_patch)[](/examples/progress_bar)[](/examples/progressive_load)[](/examples/sortable)[](/examples/svg_morphing)[](/examples/templ_counter)[](/examples/title_update)[](/examples/todomvc)[](/examples/web_component)[](/examples/rocket_copy_button)[](/examples/rocket_counter)[](/examples/rocket_echarts)[](/examples/rocket_flow)[](/examples/rocket_globe)[](/examples/rocket_password_strength)[](/examples/rocket_projection)[](/examples/rocket_qr_code)[](/examples/rocket_starfield)[](/examples/rocket_virtual_scroll)[](/examples/title_update)[](/examples/web_component)
# TodoMVC 
Demo
-  Learn any backend language 
-  Learn Datastar 
-  ??? 
-  Profit **3** items pending AllPendingCompleted Delete Reset 
## Explanation [#](#explanation)
 

This is a full implementation of TodoMVC using Datastar. It demonstrates complex state management, including adding, editing, deleting, and filtering todos, all handled through server-sent events.
## HTML [#](#html)
 
```
[ 1](#c2572da164a1ba0e_line_1)<section
[ 2](#c2572da164a1ba0e_line_2)    id="todomvc"
[ 3](#c2572da164a1ba0e_line_3)    data-init="@get('/examples/todomvc/updates')"
[ 4](#c2572da164a1ba0e_line_4)>
[ 5](#c2572da164a1ba0e_line_5)    <header id="todo-header">
[ 6](#c2572da164a1ba0e_line_6)        <input
[ 7](#c2572da164a1ba0e_line_7)            type="checkbox"
[ 8](#c2572da164a1ba0e_line_8)            data-on:click__prevent="@post('/examples/todomvc/-1/toggle')"
[ 9](#c2572da164a1ba0e_line_9)            data-init="el.checked = false"
        />
        <input
            id="new-todo"
            type="text"
            placeholder="What needs to be done?"
            data-signals:input
            data-bind:input
            data-on:keydown="
                evt.key === 'Enter' && $input.trim() && @patch('/examples/todomvc/-1') && ($input = '');
            "
        />
    </header>
    <ul id="todo-list">
        <!-- Todo items are dynamically rendered here -->
    </ul>
    <div id="todo-actions">
        <span>
            <strong>0</strong> items pending
        </span>
        <button class="small info" data-on:click="@put('/examples/todomvc/mode/0')">
            All
        </button>
        <button class="small" data-on:click="@put('/examples/todomvc/mode/1')">
            Pending
        </button>
        <button class="small" data-on:click="@put('/examples/todomvc/mode/2')">
            Completed
        </button>
        <button class="error small" aria-disabled="true">
            Delete
        </button>
        <button class="warning small" data-on:click="@put('/examples/todomvc/reset')">
            Reset
        </button>
    </div>
</section>
```
[](/examples/title_update)[](/examples/web_component)[](/star_federation)[](https://www.arcustech.com/)