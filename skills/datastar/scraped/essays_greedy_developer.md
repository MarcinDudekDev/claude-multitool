# Source: https://data-star.dev/essays/greedy_developer

Greedy Developer? 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) EssaysHow we landed here, and where we’re headed next.[](/essays/greedy_developer)[](/essays/v1_and_beyond)[](/essays/the_road_to_v1)[](/essays/htmx_sucks)[](/essays/another_dependency)[](/essays/event_streams_all_the_way_down)[](/essays/im_a_teapot)[](/essays/grugs_around_the_fire)[](/essays/haikus)[](/essays/yes_you_want_a_build_step)[](/essays/why_another_framework)[]()[](/essays/v1_and_beyond)
# Greedy Developer?

## Context [#](#context)
 

A recent blog post titled [HTMX, Datastar, greedy developer](https://drshapeless.com/blog/posts/htmx,-datastar,-greedy-developer.html) and several [Hacker News](https://news.ycombinator.com/item?id=45536618) [threads](https://news.ycombinator.com/item?id=45536000) raised concerns about Datastar Pro, pricing, and whether features were “moved behind a paywall”. Here’s what has changed, who Pro is for, and how to achieve some of the same things with the free version.
## The facts [#](#the-facts)
 

Datastar remains MIT-licensed and free. For v1, we moved a handful of convenience plugins into [Datastar Pro](/datastar_pro). The old code is tagged in the repo. Fork if you want. 

The same outcomes are possible with the freely available version using standard APIs. We use the same API that everyone else does. Nothing you can build was taken from you; we set a support boundary. Judge the work by results: smaller bundles, faster apps, and lower egress and compute.

Here’s how you can replicate two Pro attributes using the free version:
```
<!-- Replaces the current URL on load and whenever $page changes. -->
<div data-effect="window.history.replaceState({}, '', '/page/' + $page)"></div>

<!-- Scrolls the element into view. -->
<div data-init="el.scrollIntoView()"></div>
```
 
## Timeline and philosophy [#](#timeline-and-philosophy)
 
- Datastar was available under the MIT license since the beginning.
- Mostly a solo project until Ben, and later Johnny, joined.
- We rewrote the code from scratch at least three times to achieve a rock-solid foundation that will last many years. No Datastar v2 is planned or necessary.
- Started life as a tiny ~3 KB core with docs on writing plugins.
- It still is plugin-first. The v1 line defines what we will support long-term.
## Who is Pro for? [#](#who-is-pro-for?)
 

Hobbyist, student, solo tinkerer? Keep using the free core. You don’t need Pro to build real apps. Pro makes sense if:
- The [Datastar Inspector](/datastar_pro#datastar-inspector) will save you time.
- You want the convenience that the [Pro plugins](/datastar_pro#pro-features) provide, even if we don’t think you *need* them.
- You want to support the project and prefer to purchase over donating (donations are tax deductible in the US).
- You don’t want to write or maintain plugins yourself.

Pro is a one-time lifetime license purchased from 501(c)(3) nonprofit. We don’t hold shares nor own equity. We steward the project. There is no buyout and no rug pull.
## Why one bundle [#](#why-one-bundle)
 

We are pricing plugins, [Inspector](/datastar_pro#datastar-inspector), [Rocket](/datastar_pro#rocket), and [Stellar CSS](/datastar_pro#stellar-css) together. One price keeps things simple and avoids FOMO. You pay once and get everything we ship under Pro, now and forever. No nickel-and-diming, no price matrix, no guessing what we might hold back. It also removes decision fatigue for teams and makes procurement easier. The goal is to fund the work and draw a clear support boundary, not carve the product into SKUs.
## Clear commitments [#](#clear-commitments)
 

The core stays free, small, and fast. Pro is convenience and tooling, not basic capabilities. Anything Pro can do, you can do with the free version and your own effort (just like everyone else, including us).
## Conclusion [#](#conclusion)
 

There’s a silent majority that sees the value in our work, and we sincerely thank you. We’ll spend more of our time on Pro since I never want to be accused of this shit again, even when it’s untrue. Building in the open can be rewarding, but the vitriol and entitlement around people telling us how to spend our time and effort is exhausting. 

While I disagree with DHH on many things, he nailed it with this...

Have questions? Hop into [Discord](https://discord.gg/bnRNgZjgPh) and see what we’re building for a return to normalcy in web dev.[]()[](/essays/v1_and_beyond)[](/star_federation)[](https://www.arcustech.com/)