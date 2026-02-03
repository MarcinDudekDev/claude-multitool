# Source: https://data-star.dev/essays/why_another_framework

Why another framework? 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) EssaysHow we landed here, and where we’re headed next.[](/essays/greedy_developer)[](/essays/v1_and_beyond)[](/essays/the_road_to_v1)[](/essays/htmx_sucks)[](/essays/another_dependency)[](/essays/event_streams_all_the_way_down)[](/essays/im_a_teapot)[](/essays/grugs_around_the_fire)[](/essays/haikus)[](/essays/yes_you_want_a_build_step)[](/essays/why_another_framework)[](/essays/yes_you_want_a_build_step)[]()
# Why another framework?

## What’s different? [#](#what’s-different?)
 

There are many things I find wonderful about Alpine.js and htmx. However, there are a few things that I think could be improved. The biggest challenge it both is plugins (called `directives`/`magic` in Alpine and `extensions` in htmx). I tried writing in both of them and was disappointed by the breadth of monkey patching and lack of type safety. In general, you don’t have access to what other plugins do nor can you build a DAG of dependencies (i.e. you can’t structure the dependencies in a way that they flow in one direction without looping back on themselves). This means you have to be very careful about the order in which you load plugins and what they do. This is especially true if you want to use a plugin in a plugin. I think this is a big problem and I wanted to solve it. Because Datastar started with the notion that ***EVERYTHING*** is a plugin, you could theoretically build both Alpine and htmx inside Datastar. I don’t think that is a good idea, but it is possible.

Beyond that, I want the backend to be the *source of truth* when it comes to state. [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) is a great way to structure your applications, but you still need some client side state. Datastar does not use FormData; it lacks the ability to define nested data structures simply. So in general you send up JSON (automatically) and down HTML. This is more prescriptive than htmx, but again this is with just the included plugins. You can build your own plugins to do whatever you want.
## Background [#](#background)
 

I love what [Caleb Porzio](https://calebporzio.com/) has done with [Alpine.js](https://alpinejs.dev/) and what [Carson Gross](https://bigsky.software/cv/) has done with [htmx](https://htmx.org/). However, after trying to make extensions in both I became disappointed with the limitations. Both are pure JavaScript, which is fine but leads to having to either having to keep the whole state in your head and/or being prepared for lots of runtime errors. Personally I think the best way to do this is to use Typescript and have the build step and compiler catch as many errors as possible. Plus it makes it easier to extend and create optimized builds.
### Why not just use Vue/React/Svelte? [#](#why-not-just-use-vue/react/svelte?)
 

[htmx Essays](https://htmx.org/essays/) are a great place to start.
### Why not just use htmx + Alpine? [#](#why-not-just-use-htmx-+-alpine?)
 

There was a bit of a rant here before. TL;DR I tried to show htmx v2 could do all these things, and it wasn’t accepted by the community. I think htmx is great and I will continue to recommend it. In general, I think that some of the choices are throwing the baby out with the bathwater when it comes to things like Vite/TS/etc. The good news is that everything I and some other lurkers wanted is available in Datastar or can be added easily via plugins.[](/essays/yes_you_want_a_build_step)[]()[](/star_federation)[](https://www.arcustech.com/)