# Source: https://data-star.dev/essays/v1_and_beyond

V1 and Beyond 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) EssaysHow we landed here, and where we’re headed next.[](/essays/greedy_developer)[](/essays/v1_and_beyond)[](/essays/the_road_to_v1)[](/essays/htmx_sucks)[](/essays/another_dependency)[](/essays/event_streams_all_the_way_down)[](/essays/im_a_teapot)[](/essays/grugs_around_the_fire)[](/essays/haikus)[](/essays/yes_you_want_a_build_step)[](/essays/why_another_framework)[](/essays/greedy_developer)[](/essays/the_road_to_v1)
# V1 and Beyond

## The road of despair [#](#the-road-of-despair)
 
> Two elements must therefore be rooted out once for all – the fear of future suffering, and the recollection of past suffering; since the latter no longer concerns me, and the former concerns me not yet. Seneca

Holy 💩 it is finally done. Last time we talked about the road to V1, what I didn’t tell you is that on the drive up to give that talk I was honestly struck by a bit of despair. I came very close to just deleting the site and docs and just keeping the source up out of convenience, without promoting it anymore. I was fighting with everyone on almost every topic. Something had to give. I was 💯 convinced the right way forward for the hypermedia-first framework. Here are the highlights and where we are today.
- Rewrite in TypeScript. This has been [covered](/essays/why_another_framework) [previously](https://data-star.dev/essays/why_another_framework). Even more so than when I wrote the original essay I feel vindicated by this choice. The htmx community was extremely bearish on TS and yet for me the ability to do static analysis meant less runtime checking. I think the fact we are ~40% smaller than htmx (when you include morphing) with so many more features proves this out. It seems like they’re conflating building the framework in TS with the need for TS in user applications.
- Make everything a plugin. Extensions do not cut it. Other than signals, literally everything else is a plugin. Datastar takes [data-*](https://html.spec.whatwg.org/#embedding-custom-non-visible-data-with-the-data-*-attributes) key-value pairs and parses them into parts and makes them reactive. That’s it. The core is less than 250 lines of code, and while terse, it is pretty straightforward. Pick what you want, leave the rest. We are probably best known for our take on SSE but that’s really just my opinion showing through. There is literally nothing stopping you from porting htmx or Alpine.js to Datastar: the inverse is not the case.
- Signals are table stakes. I’m glad they are now a known thing in the frontend community. By being smart with how we create expressions we have access to the fastest known approach (confirmed by the mad genius behind [alien signals](https://github.com/stackblitz/alien-signals)). 
- No vendored core. This is something I really wanted, but didn’t have the stomach for. Luckily since then I’ve gotten the support to tackle this. We have a purpose-built implementation for every line of code now. No deps, no libraries… just solve our case and not be forced to conform to other library constraints. In doing so we’ve not only shrunk the code, but added features and will take on anybody’s metrics in real-world applications.
- No SDK needed. When Datastar was on the front page of Hacker News, the only real arguments I got from the wider hypermedia advocates was the reliance on SSE. While I think the whole need for an SDK is completely overblown (it’s two events, people!), it’s clear that it was an issue for others. Now we have direct support for HTML, JSON, and JavaScript for simple cases. This means caching and static sites are natively supported. 

While it’s going to be a very 🌶️ take, I think there is **zero reason to use htmx going forward**. We are smaller, faster and more future-proof. In my opinion htmx is now a deprecated approach but Datastar would not exist but for the work of Carson and the surrounding team. They laid the groundwork and hopefully the plugin-first approach means we don’t have to go through this again and have another JS framework of the week.

But driving through the green pastures of rural Utah I didn’t know all this. I thought I’d present my little framework that no one really needed (but me) and go back to being an unknown dev.  Felt like I was screaming into the void about [preventing the collapse of civilization](https://www.youtube.com/watch?v=ZSRHeXYDLko), but for web developers. 

While I spent my youth as a performer (topic for another day), I’m not a good public speaker and flubbed my talk. i said “um” about a thousand times and spoke at 1% the speed of light; but the substance of the talk was solid. At the end I said I challenge anybody to prove me wrong and the audience got up and left. At least I said my piece and can have a nice drive back listening to audiobooks. It was pretty clear; I was alienating both the MPA and SPA crowds with my approach, so time to just dog food it on my own work. 

I needed it anyway to simplify the creation of real time and collaborative workflows. While I was hoping for more engagement as a gut check I never wanted to be a JS framework guy, hell I barely consider myself a real web dev.
## I am a jerk [#](#i-am-a-jerk)
  

During my talk I said my plan was to hit V1 for the talk and be done, damn I’m sure glad I didn’t in retrospect. After the talk a plethora of devs came into the #datastar channel on the htmx server, enough so to warrant creating our own server. This most unifying story between all of them that stayed was I was very forceful in telling them they were wrong. 

That’s not out of the ordinary for the internet, but out of the ordinary I would systematically try to prove why it was the case empirically. Over time it was clear that my ideas were correct but how you interface with the API was wrong. I’ve learned a lot about meeting people where they are at while maintaining your project’s ethos. It’s an interesting balancing act. After over 9 months since the talk we are in a place I could only dream of. As a user of Datastar on the daily I’m convinced this is by far the easiest approach to web dev ever released, let alone all the performance benefits. I wouldn’t have gotten here without the help of the community that has formed around this silly little project.

My default attitude of telling you why you’re wrong is terrible for community building if you just look at the numbers from a marketing perspective. Many have told me *“you attract more bees with honey than vinegar”*. In that analogy we are trying to clean the house and vinegar is gonna actually clean versus just making your house sticky. If your ideas can withstand debate and implementation then you’ll have a home here. 

I fail constantly but try to embrace and live by stoic principles. *“The blazing fire makes flames and brightness out of everything thrown into it”* is one of my favorite quotes. Our ideas and implementation should stand the arrows you unleash upon it. If someone can show my errors I thank them. I have noticed that that mentality is not shared by all. 

There have been many times in the last year that I’ve had put-up-or-shut-up interactions with well-known names in this space. Once it comes time to actually compare metrics or production deployments the silence becomes deafening or the excuses stack up. While it’s unfortunate I hope it over time becomes fuel for the fire and truth in the end will withstand the emotional whims of the egos in this space.
## The Deek [#](#the-deek)
  

Probably the biggest trajectory change came from Ben Croker. I first encountered him on the [HX-Pod podcast](https://hx-pod.transistor.fm/episodes/building-a-framework-on-top-of-htmx-sprig-with-htmx-contributor-ben-croker) on the drive through Utah. He seemed passionate and yet frustrated with htmx in the interview. It wasn’t long after he filed an issue in the Datastar repo asking for a terrible feature. The actual feature doesn’t matter (even if he claims it does) but he dealt with my hard-headed need for everything to be justified with actual real-world reasoning.

His responses  were measured and thoughtful in a way that works very well with my [wild magic](https://www.marginalia.nu/log/68-wizards-vs-sorcerers/) ways. He cared about the documentation, usability, and wanted to truly understand what made this project special. Nowadays he’s touched every plugin, every line of docs, and understands how the codebase works overall better than I do. His passion was infectious and I couldn’t imagine most of the project’s success without his direct involvement.
## Punch you in the taint [#](#punch-you-in-the-taint)
 

Let’s say my approach to answering questions is **“colorful”**.  

I constantly end up forcefully telling people they are wrong, especially in regards to things like optimistic updates and messing with my history. [Anders Murphy](https://andersmurphy.com/) is an example of someone that took that to heart and over time has become easily the largest community contributor and the owner of demos like [multiplayer Game of Life](https://example.andersmurphy.com) and [A Billion Checkboxes](https://checkboxes.andersmurphy.com). All this while having a simpler codebase and [orders of magnitude less complexity](https://andersmurphy.com/2025/04/15/why-you-should-use-brotli-sse.html) than the [alternatives](https://news.ycombinator.com/item?id=41079814). Now if only he could make a damn CRUD app like I told him to!
## Johnny Five is alive [#](#johnny-five-is-alive)
 

Another powerhouse is [Johnathan Stevers](https://github.com/jmstevers). He has written multiple SDKs, has helped make Datastar both the fastest signals and morphing strategy known currently. In a short time he has become a pivotal part of the small core team. Wish I was half as talented, let alone that he is less than half my age. It’s truly exciting to see where his career will go and what occult shenanigans we’ll have to do to keep him around once he is done with school.
## So many Voices [#](#so-many-voices)
  

I can’t believe we already have over 1,200 users in our Discord server, over [2,400 stars](https://github.com/starfederation/datastar/stargazers) and have [our own podcast](https://www.youtube.com/@data-star) that’s getting well over 1,000 views per episode. Most of the discussions aren’t about Datastar at this point, but about larger topics as it just gets out of the way. If you haven’t [joined the Discord](https://discord.gg/bnRNgZjgPh) I highly recommend it. We have accreted myriad smart people that care about craftsmanship in many dimensions.  My hope is we become the [Handmade Hero](https://hero.handmade.network/) of web dev.
## The road ahead [#](#the-road-ahead)
 
> Never let the future disturb you. You will meet it, if you have to, with the same weapons of reason which today arm you against the present. Marcus Aurelius

V1 is done but it’s only the beginning. I was ready to throw in the proverbial towel and now that seems like a past life. We’ve taken the complicated steps of forming an official 501c3 nonprofit and are working constantly on a set of tools to both make open source sustainable yet with a binding charter to improve developer enjoyment while having real-world environmental impact. 

We have Stellar in the works. It’s somewhere between [OpenProps](https://open-props.style/) and [UnoCSS](https://unocss.dev/). For me at least it completely removes the need for Tailwind and vibes very nicely with Datastar. So far it’s smaller, faster, has no build step, and works with just the browser. We have plans for more plugins and even Project Darkstar, an effort to make the same leaps Datastar did with current web development with what [Web Transport](https://developer.mozilla.org/en-US/docs/Web/API/WebTransport) will enable for future feature sets.
## The shorn yak [#](#the-shorn-yak)
 

Datastar has been an interesting ride. The core is done and will not see much change unless and until the browser APIs update. I see most development going toward fixing other areas of web development, because this part is now so painless that the other areas of the job are causing itches I didn’t know existed before. This yak at least; is now shorn.

I originally left my TS clearance job to make a database of my dreams, part of that was the desire to have a UI/UX like [MySQL Workbench](https://www.mysql.com/products/workbench/) built directly into the server. This is a really important feature as I was trying to build a bi-temporal event sourcing magnum opus. I’m glad for the journey and the friends I made along the way but also excited to get back to what caused Datastar to exist in the first place. The work doesn’t stop, but the daily churn certainly will.
## Go forth and ship [#](#go-forth-and-ship)
 

I never wanted Datastar to win a popularity contest. I do want people to be aware of it as an alternative to the collective madness that has been modern web dev. While it’s a multi-faceted problem [this blog](https://overreacted.io/react-for-two-computers/) is now my canary in the coal mine that has [ceased to be](https://www.youtube.com/watch?v=4vuW6tQ0218). This level of complexity and foot guns can’t be the zeitgeist in a future I want to live in. Stop fucking over complicating the web. Put the state in the right place and all this just ceases to be a real-world issue. When I try to have actual discussions with most influencer types it's about vibes and social proofs. I’ve been shocked at the lack of technical challenges to my approach. In fact until very recently I left badly performing code in the engine.ts just to see if anyone actually read and understood what Datastar does. My only advice to other devs is stolen:
> “Don’t take criticism from those you wouldn’t take advice from” Derek Collison

I don’t care about trying to convince the most fervent SPA devs. Most of the time they gish gallop or set up false dilemmas. I am all about the devs that feel the web has gotten too complicated for what we get out of it currently. 

I'm hopeful that we are truly bringing sanity back to the web and look forward to a bright future where the madness of RSC fueled blight is a long distance memory in the sands of time. There are no delusions of grandeur here; when the features on the browser become more powerful we too shall fade away. But until then, we are *currently* the best choice for building real time and collaborative applications that are performant, easy to use and maintainable. 
> 

I met a traveller from an antique land,

Who said—“Two vast and trunkless legs of stone

Stand in the desert... Near them, on the sand,

Half sunk a shattered visage lies, whose frown,

And wrinkled lip, and sneer of cold command,

Tell that its sculptor well those passions read

Which yet survive, stamped on these lifeless things,

The hand that mocked them, and the heart that fed;

And on the pedestal, these words appear:

My name is Ozymandias, King of Kings;

Look on my Works, ye Mighty, and despair!

Nothing beside remains. Round the decay

Of that colossal Wreck, boundless and bare

The lone and level sands stretch far away.”Ozymandias by Percy Bysshe Shelley
## We made it y’all [#](#we-made-it-y’all)
 

Thank you to everyone that has contributed to Datastar, whether it’s been code, documentation, or just spreading the good word (not a cult). I’m excited to see where we go from here and hope you’ll join  us on this journey.

Also of note I want to thank my family. My wife and kids don’t exactly understand this open source thing but they are great and supportive for the whole experience. Lucky to have so much love in my life.

*P.S. If anyone has a podcast or YouTube channel and wants to talk about any of this stuff let me know!  Not a great public speaker but passionate about being the change I want to see and sharing the insights I’ve learned along the way.*[](/essays/greedy_developer)[](/essays/the_road_to_v1)[](/star_federation)[](https://www.arcustech.com/)