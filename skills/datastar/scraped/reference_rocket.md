# Source: https://data-star.dev/reference/rocket

Rocket Reference 
  
  
    
      
    
    
      Copied!
    
  

[[](/guide)[](/reference)[](/examples)[](/how_tos)[](/datastar_pro)[]()[](/star_federation)[](/bundler)[](/essays)[](/examples)[](/how_tos)[](/datastar_pro)[](/reference)[](/shop)[](/videos)[](https://github.com/starfederation/datastar/) [](https://discord.gg/bnRNgZjgPh) [](https://www.youtube.com/@data-star) ReferenceUsage reference for attributes, actions, SSE events, etc.[](/reference/attributes)[](/reference/actions)[](/reference/rocket)[](#overview)[](#bridging-web-components-and-datastar)[](#signal-scoping)[](#defining-rocket-components)[](#signal-management)[](#component-signals)[](#global-signals)[](#props)[](#setup-scripts)[](#component-setup-scripts)[](#static-setup-scripts)[](#module-imports)[](#esm-imports)[](#iife-imports)[](#rocket-attributes)[](#light-dom-style-scoping)[``](#data-shadow-open)[``](#data-shadow-closed)[``](#data-if)[``](#data-else-if)[``](#data-else)[``](#data-for)[``](#data-key)[](#reactive-patterns)[](#computed-values)[](#effects-and-watchers)[](#element-references)[](#validation-with-codecs)[](#type-codecs)[](#validation-rules)[](#component-lifecycle)[](#optimistic-ui)[](#examples)[](/reference/sse_events)[](/reference/sdks)[](/reference/security)[](/reference/actions)[](/reference/sse_events)
# Rocket

Rocket is currently in alpha – available in the Datastar Pro repo.

Rocket is a [Datastar Pro](/datastar_pro) plugin that bridges [Web Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components) with Datastar’s reactive system. It allows you to create encapsulated, reusable components with reactive data binding.
> Rocket is a powerful feature, and should be used sparingly. For most applications, standard Datastar templates and global signals are sufficient. Reserve Rocket for cases where component encapsulation is essential, such as integrating third-party libraries or creating complex, reusable UI elements.
### Basic example [#](#basic-example)

Traditional web components require verbose class definitions and manual DOM management. Rocket eliminates this complexity with a declarative, template-based approach.

Here’s a Rocket component compared to a vanilla web component.
```
[ 1](#2658919688293c78_line_1)<template data-rocket:simple-counter
[ 2](#2658919688293c78_line_2)          data-props:count="int|min:0|=0"
[ 3](#2658919688293c78_line_3)          data-props:start="int|min:0|=0"
[ 4](#2658919688293c78_line_4)          data-props:step="int|min:1|max:10|=1"
[ 5](#2658919688293c78_line_5)>
[ 6](#2658919688293c78_line_6)  <script>
[ 7](#2658919688293c78_line_7)    $$count = $$start
[ 8](#2658919688293c78_line_8)  </script>
[ 9](#2658919688293c78_line_9)  <template data-if="$$errs?.start">
    <div data-text="$$errs.start[0].value"></div>
  </template>
  <template data-if="$$errs?.step">
    <div data-text="$$errs.step[0].value"></div>
  </template>
  <button data-on:click="$$count -= $$step">-</button>
  <span data-text="$$count"></span>
  <button data-on:click="$$count += $$step">+</button>
  <button data-on:click="$$count = $$start">Reset</button>
</template>
```

```
[  1](#1176d4430b63da30_line_1)class SimpleCounter extends HTMLElement {
[  2](#1176d4430b63da30_line_2)  static observedAttributes = ['start', 'step'];
[  3](#1176d4430b63da30_line_3)  
[  4](#1176d4430b63da30_line_4)  constructor() {
[  5](#1176d4430b63da30_line_5)    super();
[  6](#1176d4430b63da30_line_6)    this.innerHTML = `
[  7](#1176d4430b63da30_line_7)      <div class="error" style="display: none;"></div>
[  8](#1176d4430b63da30_line_8)      <button class="dec">-</button>
[  9](#1176d4430b63da30_line_9)      <span class="count">0</span>
[ 10](#1176d4430b63da30_line_10)      <button class="inc">+</button>
[ 11](#1176d4430b63da30_line_11)      <button class="reset">Reset</button>
[ 12](#1176d4430b63da30_line_12)    `;
[ 13](#1176d4430b63da30_line_13)    
[ 14](#1176d4430b63da30_line_14)    this.errorEl = this.querySelector('.error');
[ 15](#1176d4430b63da30_line_15)    this.decBtn = this.querySelector('.dec');
[ 16](#1176d4430b63da30_line_16)    this.incBtn = this.querySelector('.inc');
[ 17](#1176d4430b63da30_line_17)    this.resetBtn = this.querySelector('.reset');
[ 18](#1176d4430b63da30_line_18)    this.countEl = this.querySelector('.count');
[ 19](#1176d4430b63da30_line_19)    
[ 20](#1176d4430b63da30_line_20)    this.handleDec = () => { 
[ 21](#1176d4430b63da30_line_21)      const newValue = this.count - this.step;
[ 22](#1176d4430b63da30_line_22)      if (newValue >= 0) {
[ 23](#1176d4430b63da30_line_23)        this.count = newValue;
[ 24](#1176d4430b63da30_line_24)        this.updateDisplay();
[ 25](#1176d4430b63da30_line_25)      }
[ 26](#1176d4430b63da30_line_26)    };
[ 27](#1176d4430b63da30_line_27)    this.handleInc = () => { 
[ 28](#1176d4430b63da30_line_28)      this.count += this.step;
[ 29](#1176d4430b63da30_line_29)      this.updateDisplay();
[ 30](#1176d4430b63da30_line_30)    };
[ 31](#1176d4430b63da30_line_31)    this.handleReset = () => { 
[ 32](#1176d4430b63da30_line_32)      this.count = this.start; 
[ 33](#1176d4430b63da30_line_33)      this.updateDisplay(); 
[ 34](#1176d4430b63da30_line_34)    };
[ 35](#1176d4430b63da30_line_35)    
[ 36](#1176d4430b63da30_line_36)    this.decBtn.addEventListener('click', this.handleDec);
[ 37](#1176d4430b63da30_line_37)    this.incBtn.addEventListener('click', this.handleInc);
[ 38](#1176d4430b63da30_line_38)    this.resetBtn.addEventListener('click', this.handleReset);
[ 39](#1176d4430b63da30_line_39)  }
[ 40](#1176d4430b63da30_line_40)  
[ 41](#1176d4430b63da30_line_41)  connectedCallback() {
[ 42](#1176d4430b63da30_line_42)    const startVal = parseInt(this.getAttribute('start') || '0');
[ 43](#1176d4430b63da30_line_43)    const stepVal = parseInt(this.getAttribute('step') || '1');
[ 44](#1176d4430b63da30_line_44)    
[ 45](#1176d4430b63da30_line_45)    if (startVal < 0) {
[ 46](#1176d4430b63da30_line_46)      this.errorEl.textContent = 'start must be at least 0';
[ 47](#1176d4430b63da30_line_47)      this.errorEl.style.display = 'block';
[ 48](#1176d4430b63da30_line_48)      this.start = 0;
[ 49](#1176d4430b63da30_line_49)    } else {
[ 50](#1176d4430b63da30_line_50)      this.start = startVal;
[ 51](#1176d4430b63da30_line_51)      this.errorEl.style.display = 'none';
[ 52](#1176d4430b63da30_line_52)    }
[ 53](#1176d4430b63da30_line_53)    
[ 54](#1176d4430b63da30_line_54)    if (stepVal < 1 || stepVal > 10) {
[ 55](#1176d4430b63da30_line_55)      this.errorEl.textContent = 'step must be between 1 and 10';
[ 56](#1176d4430b63da30_line_56)      this.errorEl.style.display = 'block';
[ 57](#1176d4430b63da30_line_57)      this.step = Math.max(1, Math.min(10, stepVal));
[ 58](#1176d4430b63da30_line_58)    } else {
[ 59](#1176d4430b63da30_line_59)      this.step = stepVal;
[ 60](#1176d4430b63da30_line_60)      if (this.start === startVal) {
[ 61](#1176d4430b63da30_line_61)        this.errorEl.style.display = 'none';
[ 62](#1176d4430b63da30_line_62)      }
[ 63](#1176d4430b63da30_line_63)    }
[ 64](#1176d4430b63da30_line_64)    
[ 65](#1176d4430b63da30_line_65)    this.count = this.start;
[ 66](#1176d4430b63da30_line_66)    this.updateDisplay();
[ 67](#1176d4430b63da30_line_67)  }
[ 68](#1176d4430b63da30_line_68)  
[ 69](#1176d4430b63da30_line_69)  disconnectedCallback() {
[ 70](#1176d4430b63da30_line_70)    this.decBtn.removeEventListener('click', this.handleDec);
[ 71](#1176d4430b63da30_line_71)    this.incBtn.removeEventListener('click', this.handleInc);
[ 72](#1176d4430b63da30_line_72)    this.resetBtn.removeEventListener('click', this.handleReset);
[ 73](#1176d4430b63da30_line_73)  }
[ 74](#1176d4430b63da30_line_74)  
[ 75](#1176d4430b63da30_line_75)  attributeChangedCallback(name, oldValue, newValue) {
[ 76](#1176d4430b63da30_line_76)    if (name === 'start') {
[ 77](#1176d4430b63da30_line_77)      const startVal = parseInt(newValue || '0');
[ 78](#1176d4430b63da30_line_78)      if (startVal < 0) {
[ 79](#1176d4430b63da30_line_79)        this.errorEl.textContent = 'start must be at least 0';
[ 80](#1176d4430b63da30_line_80)        this.errorEl.style.display = 'block';
[ 81](#1176d4430b63da30_line_81)        this.start = 0;
[ 82](#1176d4430b63da30_line_82)      } else {
[ 83](#1176d4430b63da30_line_83)        this.start = startVal;
[ 84](#1176d4430b63da30_line_84)        this.errorEl.style.display = 'none';
[ 85](#1176d4430b63da30_line_85)      }
[ 86](#1176d4430b63da30_line_86)      this.count = this.start;
[ 87](#1176d4430b63da30_line_87)    } else if (name === 'step') {
[ 88](#1176d4430b63da30_line_88)      const stepVal = parseInt(newValue || '1');
[ 89](#1176d4430b63da30_line_89)      if (stepVal < 1 || stepVal > 10) {
[ 90](#1176d4430b63da30_line_90)        this.errorEl.textContent = 'step must be between 1 and 10';
[ 91](#1176d4430b63da30_line_91)        this.errorEl.style.display = 'block';
[ 92](#1176d4430b63da30_line_92)        this.step = Math.max(1, Math.min(10, stepVal));
[ 93](#1176d4430b63da30_line_93)      } else {
[ 94](#1176d4430b63da30_line_94)        this.step = stepVal;
[ 95](#1176d4430b63da30_line_95)        this.errorEl.style.display = 'none';
[ 96](#1176d4430b63da30_line_96)      }
[ 97](#1176d4430b63da30_line_97)    }
[ 98](#1176d4430b63da30_line_98)    if (this.isConnected) {
[ 99](#1176d4430b63da30_line_99)      this.updateDisplay();
    }
  }
  
  updateDisplay() {
    this.countEl.textContent = this.count;
  }
}

customElements.define('simple-counter', SimpleCounter);
```

## Overview [#](#overview)

Rocket allows you to turn HTML templates into fully reactive web components. The backend remains the source of truth, but your frontend components are now encapsulated and reusable without any of the usual hassle.

Add `data-rocket:my-component` to a `template` element to turn it into a Rocket component. Component signals are automatically [scoped](#signal-scoping) with `$$`, so component instances don’t interfere with each other.

You can use Rocket to wrap external libraries using [module imports](#module-imports), and create [references to elements](#element-references) within your component. Each component gets its own signal namespace that plays nicely with Datastar’s global signals. When you remove a component from the DOM, all its `$$` signals are cleaned up automatically.
### Bridging Web Components and Datastar [#](#bridging-web-components-and-datastar)

Web components want encapsulation; Datastar wants a global signal store. Rocket gives you both by creating isolated namespaces for each component. Each instance gets its own sandbox that doesn’t mess with other components on the page, or with global signals.

Multiple component instances work seamlessly, each getting its own numbered namespace. You still have access to global signals when you need them, but your component state stays isolated and clean.
### Signal Scoping [#](#signal-scoping)

Use `$$` for component-scoped signals, and `$` for global signals. Component signals are automatically cleaned up when you remove the component from the DOM - no memory leaks, no manual cleanup required.

Behind the scenes, your `$$count` becomes something like `$._rocket.my_counter.id1.count`, with each instance getting its own id-prefixed namespace. You never have to think about this complexity - just write `$$count` and Rocket handles the rest.
```
[ 1](#2e2215e24db173a2_line_1)// Your component template writes:
[ 2](#2e2215e24db173a2_line_2)<button data-on:click="$$count++">Increment</button>
[ 3](#2e2215e24db173a2_line_3)<span data-text="$$count"></span>
[ 4](#2e2215e24db173a2_line_4)
[ 5](#2e2215e24db173a2_line_5)// Rocket transforms it to (for instance #1):
[ 6](#2e2215e24db173a2_line_6)<button data-on:click="$._rocket.my_counter.id1.count++">Increment</button>
[ 7](#2e2215e24db173a2_line_7)<span data-text="$._rocket.my_counter.id1.count"></span>
[ 8](#2e2215e24db173a2_line_8)
[ 9](#2e2215e24db173a2_line_9)// The global Datastar signal structure:
$._rocket = {
  my_counter: {
    id1: { count: 0 }, // First counter instance
    id2: { count: 5 }, // Second counter instance
    id3: { count: 10 } // Third counter instance
  },
  user_card: {
    id4: { name: "Alice" }, // Different component type
    id5: { name: "Bob" }
  }
}
```

## Defining Rocket Components [#](#defining-rocket-components)

Rocket components are defined using a HTML `template` element with the `data-rocket:my-component` attribute, where `my-component` is the name of the resulting web component. The name must contain at least one hyphen, as per the [custom element](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements#name) specification.
```
<template data-rocket:my-counter>
  <script>
    $$count = 0  
  </script>
  <button data-on:click="$$count++">
    Count: <span data-text="$$count"></span>
  </button>
</template>
```

This gets compiled to a web component, meaning that usage is simply:
```
<my-counter></my-counter>
```

Rocket components *must* be defined before being used in the DOM.
```
<!-- Template element must appear first in the DOM. -->
<template data-rocket:my-counter></template>

<my-counter></my-counter>
```

## Signal Management [#](#signal-management)

Rocket makes it possible to work with both component-scoped and global signals (global to the entire page).
### Component Signals [#](#component-signals)

Component-scoped signals use the `$$` prefix and are isolated to each component instance.
```
[ 1](#b1dcfd1606f1f512_line_1)<template data-rocket:isolated-counter>
[ 2](#b1dcfd1606f1f512_line_2)  <script>
[ 3](#b1dcfd1606f1f512_line_3)    // These are component-scoped – each instance has its own values
[ 4](#b1dcfd1606f1f512_line_4)    $$count = 0
[ 5](#b1dcfd1606f1f512_line_5)    $$step = 1
[ 6](#b1dcfd1606f1f512_line_6)    $$maxCount = 10
[ 7](#b1dcfd1606f1f512_line_7)    $$isAtMax = computed(() => $$count >= $$maxCount)
[ 8](#b1dcfd1606f1f512_line_8)    
[ 9](#b1dcfd1606f1f512_line_9)    // Component actions
    action({
      name: 'increment',
      apply() {
        if ($$count < $$maxCount) {
          $$count += $$step
        }
      },
    })
  </script>
  
  <div>
    <p>Count: <span data-text="$$count"></span></p>
    <p data-show="$$isAtMax" class="error">Maximum reached!</p>
    <button data-on:click="@increment()" data-attr:disabled="$$isAtMax">+</button>
  </div>
</template>

<!-- Multiple instances work independently -->
<isolated-counter></isolated-counter>
<isolated-counter></isolated-counter>
```

### Global Signals [#](#global-signals)

Global signals use the `$` prefix and are shared across the entire page.
```
[ 1](#a20fd4ceffec643b_line_1)<template data-rocket:theme-toggle>
[ 2](#a20fd4ceffec643b_line_2)  <script>
[ 3](#a20fd4ceffec643b_line_3)    // Access global theme state
[ 4](#a20fd4ceffec643b_line_4)    if (!$theme) {
[ 5](#a20fd4ceffec643b_line_5)      $theme = 'light'
[ 6](#a20fd4ceffec643b_line_6)    }
[ 7](#a20fd4ceffec643b_line_7)    
[ 8](#a20fd4ceffec643b_line_8)    action({
[ 9](#a20fd4ceffec643b_line_9)      name: 'toggleTheme',
      apply() {
        $theme = $theme === 'light' ? 'dark' : 'light'
      },
    })
  </script>
  
  <button data-on:click="@toggleTheme()">
    <span data-text="$theme === 'light' ? '🌙' : '☀️'"></span>
    <span data-text="$theme === 'light' ? 'Dark Mode' : 'Light Mode'"></span>
  </button>
</template>

<!-- All instances share the same global theme -->
<theme-toggle></theme-toggle>
<theme-toggle></theme-toggle>
```

## Props [#](#props)

The `data-props:*` attribute allows you to define component props with codecs for validation and defaults.
```
[ 1](#ecd42f8fdb3d149b_line_1)<!-- Component definition with defaults -->
[ 2](#ecd42f8fdb3d149b_line_2)<template data-rocket:progress-bar
[ 3](#ecd42f8fdb3d149b_line_3)          data-props:value="int|=0"
[ 4](#ecd42f8fdb3d149b_line_4)          data-props:max="int|=100" 
[ 5](#ecd42f8fdb3d149b_line_5)          data-props:color="string|=blue"
[ 6](#ecd42f8fdb3d149b_line_6)>
[ 7](#ecd42f8fdb3d149b_line_7)  <script>
[ 8](#ecd42f8fdb3d149b_line_8)    $$percentage = computed(() => Math.round(($$value / $$max) * 100))
[ 9](#ecd42f8fdb3d149b_line_9)  </script>
  
  <div class="progress-container">
    <div class="progress-bar" 
        data-style="{
          width: $$percentage + '%',
          backgroundColor: $$color
        }">
    </div>
    <span data-text="$$percentage + '%'"></span>
  </div>
</template>

<!-- Usage -->
<progress-bar data-attr:value="'75'" data-attr:color="'green'"></progress-bar>
<progress-bar data-attr:value="'30'" data-attr:max="'50'"></progress-bar>
```

Rocket automatically transforms and validates values using the [codecs](#validation-with-codecs) defined in `data-props:*` attributes.
## Setup Scripts [#](#setup-scripts)

Setup scripts initialize component behavior and run when the component is created. Rocket supports both component (per-instance) and static (one-time) setup scripts.
### Component Setup Scripts [#](#component-setup-scripts)

Regular `<script>` tags run for each component instance.
```
[ 1](#6abe4866c0e34187_line_1)<template data-rocket:timer
[ 2](#6abe4866c0e34187_line_2)          data-props:seconds="int|=0"
[ 3](#6abe4866c0e34187_line_3)          data-props:running="boolean|=false"
[ 4](#6abe4866c0e34187_line_4)          data-props:interval="int|=1000"
[ 5](#6abe4866c0e34187_line_5)>
[ 6](#6abe4866c0e34187_line_6)  <script>
[ 7](#6abe4866c0e34187_line_7)    $$minutes = computed(() => Math.floor($$seconds / 60))
[ 8](#6abe4866c0e34187_line_8)    $$displayTime = computed(() => {
[ 9](#6abe4866c0e34187_line_9)      const m = String($$minutes).padStart(2, '0')
      const s = String($$seconds % 60).padStart(2, '0')
      return m + ':' + s
    })
    
    let intervalId
    effect(() => {
      if ($$running) {
        intervalId = setInterval(() => $$seconds++, $$interval)
      } else {
        clearInterval(intervalId)
      }
    })
    
    // Cleanup when component is removed
    onCleanup(() => {
      clearInterval(intervalId)
    })
  </script>
  
  <div>
    <h2 data-text="$$displayTime"></h2>
    <button data-on:click="$$running = !$$running" 
            data-text="$$running ? 'Stop' : 'Start'">
    </button>
    <button data-on:click="$$seconds = 0">Reset</button>
</div>
</template>
```

### Host Element Access [#](#host-element-access)

Rocket injects an `el` binding into every component setup script. It always points to the current custom element instance, even when you opt into Shadow DOM, so you can imperatively read attributes, toggle classes, or wire event listeners.
```
<template data-rocket:focus-pill>
  <script>
    el.setAttribute('role', 'button')
    el.addEventListener('focus', () => el.classList.add('is-focused'))
    el.addEventListener('blur', () => el.classList.remove('is-focused'))
  </script>
  
  <span><slot></slot></span>
</template>
```

Setup code executes inside an arrow function sandbox, so `this` has no meaning inside component scripts. Use `el` any time you need the host element—for example to call `el.shadowRoot`, `el.setAttribute`, or pass it into a third-party library.
### Static Setup Scripts [#](#static-setup-scripts)

Scripts with a `data-static` attribute only run once, when the component type is first registered. This is useful for shared constants or utilities.
```
[ 1](#37e9a26342f83c42_line_1)<template data-rocket:icon-button>
[ 2](#37e9a26342f83c42_line_2)  <script data-static>
[ 3](#37e9a26342f83c42_line_3)    const icons = {
[ 4](#37e9a26342f83c42_line_4)      heart: '❤️',
[ 5](#37e9a26342f83c42_line_5)      star: '⭐',
[ 6](#37e9a26342f83c42_line_6)      thumbs: '👍',
[ 7](#37e9a26342f83c42_line_7)      fire: '🔥'
[ 8](#37e9a26342f83c42_line_8)    }
[ 9](#37e9a26342f83c42_line_9)  </script>
  
  <script>
    $$icon = $$type || 'heart'
    $$emoji = computed(() => icons[$$icon] || '❓')
  </script>
  
  <button data-on:click="@click()">
    <span data-text="$$emoji"></span>
    <span data-text="$$label || 'Click me'"></span>
  </button>
</template>
```

## Module Imports [#](#module-imports)

Rocket allows you to wrap external libraries, loading them before the component initializes and the setup script runs. Use `data-import:*` for modern ES modules, and add the `__iife` modifier (`data-import:foo__iife`) for legacy globals.
### ESM Imports [#](#esm-imports)

The `data-import:*` attribute loads modern ES modules by default.
```
[ 1](#3cb46e28a5f4057e_line_1)<template data-rocket:qr-generator
[ 2](#3cb46e28a5f4057e_line_2)          data-props:text="string|trim|required!|=Hello World"
[ 3](#3cb46e28a5f4057e_line_3)          data-props:size="int|min:50|max:1000|=200"
[ 4](#3cb46e28a5f4057e_line_4)          data-import:qr="https://cdn.jsdelivr.net/npm/[[email protected]](/cdn-cgi/l/email-protection)/+esm"
[ 5](#3cb46e28a5f4057e_line_5)>
[ 6](#3cb46e28a5f4057e_line_6)  <script>
[ 7](#3cb46e28a5f4057e_line_7)    $$errorText = ''
[ 8](#3cb46e28a5f4057e_line_8)    
[ 9](#3cb46e28a5f4057e_line_9)    effect(() => {
      // Check for validation errors first
      if ($$hasErrs) {
        const messages = []
        if ($$errs?.text) {
          messages.push('Text is required')
        }
        if ($$errs?.size) {
          messages.push('Size must be 50-1000px')
        }
        $$errorText = messages.join(', ') || 'Validation failed'
        return
      }

      if (!$$canvas) {
        return
      }

      if (!qr) {
        $$errorText = 'QR library not loaded'
        return
      }
      
      try {
        qr.render({
          text: $$text,
          size: $$size
        }, $$canvas)
        $$errorText = ''
      } catch (err) {
        $$errorText = 'QR generation failed'
      }
    })
  </script>
  
  <div data-style="{width: $$size + 'px', height: $$size + 'px'}">
    <template data-if="!$$errorText">
      <canvas data-ref="canvas" style="display: block;"></canvas>
    </template>
    <template data-else>
      <div data-text="$$errorText" class="error"></div>
    </template>
  </div>
</template>
```

### IIFE Imports [#](#iife-imports)

Add the `__iife` modifier for legacy libraries that expose globals. The library must expose a global variable that matches the alias you specify after `data-import:`.
```
[ 1](#4f651ed891871e8b_line_1)<template data-rocket:chart
[ 2](#4f651ed891871e8b_line_2)          data-props:data="json|=[]"
[ 3](#4f651ed891871e8b_line_3)          data-props:type="string|=line"
[ 4](#4f651ed891871e8b_line_4)          data-import:chart__iife="https://cdn.jsdelivr.net/npm/[[email protected]](/cdn-cgi/l/email-protection)/dist/chart.umd.js"
[ 5](#4f651ed891871e8b_line_5)>
[ 6](#4f651ed891871e8b_line_6)  <script>
[ 7](#4f651ed891871e8b_line_7)    let chartInstance
[ 8](#4f651ed891871e8b_line_8)    
[ 9](#4f651ed891871e8b_line_9)    effect(() => {
      if (!$$canvas || !chart || !$$data.length) {
        return
      }

      if (chartInstance) {
        chartInstance.destroy()
      }
      
      const ctx = $$canvas.getContext('2d')
      chartInstance = new chart.Chart(ctx, {
        type: $$type,
        data: {
          datasets: [{
            data: $$data,
            backgroundColor: '#3b82f6'
          }]
        }
      })
    })
    
    onCleanup(() => {
      if (chartInstance) {
        chartInstance.destroy()
      }
    })
  </script>
  
  <canvas data-ref="canvas"></canvas>
</template>
```

## Rocket Attributes [#](#rocket-attributes)

In addition to the Rocket-specific `data-*` attributes defined above, the following attributes are available within Rocket components.

Rocket only transforms Datastar attributes such as `data-text`, `data-on`, and `data-attr`. Custom `data-*` attributes you add for your own semantics (e.g., `data-info="Hello Delaney!"`) are preserved verbatim in the rendered DOM.

By default, Rocket renders into the light DOM of the custom element, so the component’s content participates directly in the page layout and inherits global styles. The shadow attributes `data-shadow-*` let's you opt a component into using a Shadow DOM host instead. If you’re not familiar with Shadow DOM concepts like the [shadow root](https://developer.mozilla.org/en-US/docs/Web/API/ShadowRoot), it’s worth reading the MDN documentation first.
### Light DOM style scoping [#](#light-dom-style-scoping)

Light DOM Rocket components automatically scope any `<style>` blocks declared inside the component template and inside the component’s light DOM children. Selectors are rewritten to target only that component instance, so styles won’t leak across instances. Global stylesheets still apply as usual.

Use `:global(...)` in a selector to opt out of scoping for that selector. Shadow DOM components already have native style encapsulation, so scoping is only applied to light DOM components.
```
[ 1](#8ab1cd75449e1e8c_line_1)<template data-rocket:badge-list>
[ 2](#8ab1cd75449e1e8c_line_2)  <style>
[ 3](#8ab1cd75449e1e8c_line_3)    .badge { display: inline-flex; gap: 0.25rem; }
[ 4](#8ab1cd75449e1e8c_line_4)    .badge strong { color: #0a0; }
[ 5](#8ab1cd75449e1e8c_line_5)    :global(.accent) { color: #e11d48; }
[ 6](#8ab1cd75449e1e8c_line_6)  </style>
[ 7](#8ab1cd75449e1e8c_line_7)  <div class="badge">
[ 8](#8ab1cd75449e1e8c_line_8)    <strong data-text="$$label"></strong>
[ 9](#8ab1cd75449e1e8c_line_9)    <slot></slot>
  </div>
</template>

<badge-list data-attr:label="'Team'">
  <style>
    .badge { background: #fee; border: 1px solid #f99; }
    .badge em { font-style: normal; color: #900; }
  </style>
  <em class="accent">Alpha</em>
</badge-list>
```

### `data-shadow-open` [#](#data-shadow-open)

Use `data-shadow-open` to force an **open Shadow DOM** when you want style encapsulation but still need access to internal elements via `element.shadowRoot`, which is useful during debugging or integration.
```
[ 1](#5d544ed8a5147b0c_line_1)<template data-rocket:tag-pill
[ 2](#5d544ed8a5147b0c_line_2)          data-shadow-open
[ 3](#5d544ed8a5147b0c_line_3)          data-props:label="string|trim|required!">
[ 4](#5d544ed8a5147b0c_line_4)  <style>
[ 5](#5d544ed8a5147b0c_line_5)    .pill {
[ 6](#5d544ed8a5147b0c_line_6)      display: inline-flex;
[ 7](#5d544ed8a5147b0c_line_7)      align-items: center;
[ 8](#5d544ed8a5147b0c_line_8)      padding: 0.25rem 0.5rem;
[ 9](#5d544ed8a5147b0c_line_9)      border-radius: 999px;
      background: #0f172a;
      color: white;
      font-size: 0.75rem;
      gap: 0.25rem;
    }
    .dot {
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: #22c55e;
    }
  </style>
  <div class="pill">
    <span class="dot"></span>
    <span data-text="$$label"></span>
  </div>
</template>

<!-- Styles are fully encapsulated, but devtools and test harnesses can still inspect the .pill element via element.shadowRoot -->
<tag-pill data-attr:label="'Shadow-ready'"></tag-pill>
```

### `data-shadow-closed` [#](#data-shadow-closed)

Use `data-shadow-closed` to force a **closed Shadow DOM**. Choose this when you want the implementation to be fully encapsulated and inaccessible via `element.shadowRoot`, while still benefitting from Shadow DOM styling and slot projection.
```
[ 1](#96bc47f80919055c_line_1)<template data-rocket:status-tooltip
[ 2](#96bc47f80919055c_line_2)          data-shadow-closed
[ 3](#96bc47f80919055c_line_3)          data-props:text="string|trim|required!">
[ 4](#96bc47f80919055c_line_4)  <script>
[ 5](#96bc47f80919055c_line_5)    $$show = false
[ 6](#96bc47f80919055c_line_6)  </script>
[ 7](#96bc47f80919055c_line_7)
[ 8](#96bc47f80919055c_line_8)  <span data-on:mouseenter="$$show = true"
[ 9](#96bc47f80919055c_line_9)        data-on:mouseleave="$$show = false">
    <slot></slot>
    <span data-show="$$show" class="tooltip"
          data-text="$$text"></span>
  </span>
</template>

<!-- The tooltip DOM is hidden inside a closed shadow root -->
<status-tooltip data-attr:text="'Hello from Rocket'">
  Hover me
</status-tooltip>
```

### `data-if` [#](#data-if)

Conditionally outputs an element based on an expression. Must be placed on a `<template>` element in Rocket components.
```
<template data-if="$$items.count">
  <div data-text="$$items.count + ' items'"></div>
</template>
```

### `data-else-if` [#](#data-else-if)

Conditionally outputs an element based on an expression, if the preceding `data-if` condition is falsy. Must be on a `<template>`.
```
<template data-if="$$items.count">
  <div data-text="$$items.count + ' items found.'"></div>
</template>
<template data-else-if="$$items.count == 1">
  <div data-text="$$items.count + ' item found.'"></div>
</template>
```

### `data-else` [#](#data-else)

Outputs an element if the preceding `data-if` and `data-else-if` conditions are falsy. Must be on a `<template>`.
```
<template data-if="$$items.count">
  <div data-text="$$items.count + ' items found.'"></div>
</template>
<template data-else>
  <div>No items found.</div>
</template>
```

### `data-for` [#](#data-for)

Loops over any iterable (arrays, maps, sets, strings, and plain objects), and outputs the element for each item. Must be placed on a `<template>`.
```
<template data-for="item, index in $$items">
  <div>
    <span data-text="index + ': ' + item.name"></span>
  </div>
</template>
```

### `data-key` [#](#data-key)

Provides a stable key for each iteration when used alongside `data-for`. Keys enable DOM reuse (Solid-like keyed loops) and must live on the same `<template data-for>`.
```
<template data-for="item in $$items" data-key="item.id">
  <div data-text="item.label"></div>
</template>
```

The first alias (`item` above) is available to descendants just like any other binding. An optional second alias (`index` above) exposes the current key or numeric index. Nested loops are supported, and inner loop variables automatically shadow outer ones, so you can reuse names without conflicts.
```
<template data-for="items in $$itemSet">
  <div>
    <template data-for="item in items">
      <div>
        <span data-text="item.name"></span>
      </div>
    </template>
  </div>
</template>
```

## Reactive Patterns [#](#reactive-patterns)

Rocket provides `computed` and `effect` functions for declarative reactivity. These keep your component state automatically in sync with the DOM.
### Computed Values [#](#computed-values)

Computed values automatically update when their dependencies change.
```
[ 1](#94f9f423b0ed2499_line_1)<template data-rocket:shopping-cart
[ 2](#94f9f423b0ed2499_line_2)          data-props:items="json|=[]"
[ 3](#94f9f423b0ed2499_line_3)>
[ 4](#94f9f423b0ed2499_line_4)  <script>
[ 5](#94f9f423b0ed2499_line_5)    // Computed values automatically recalculate
[ 6](#94f9f423b0ed2499_line_6)    $$total = computed(() => 
[ 7](#94f9f423b0ed2499_line_7)      $$items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
[ 8](#94f9f423b0ed2499_line_8)    )
[ 9](#94f9f423b0ed2499_line_9)    
    $$itemCount = computed(() =>
      $$items.reduce((sum, item) => sum + item.quantity, 0)
    )
    
    $$isEmpty = computed(() => $$items.length === 0)
    
    // Actions that modify reactive state
    action({
      name: 'addItem',
      apply(_, item) {
        $$items = [...$$items, { ...item, quantity: 1 }]
      },
    })
    
    action({
      name: 'removeItem',
      apply(_, index) {
        $$items = $$items.filter((_, i) => i !== index)
      },
    })
  </script>
  
  <div>
    <h3>Shopping Cart</h3>
    <p data-show="$$isEmpty">Cart is empty</p>
    <p data-show="!$$isEmpty">
      Items: <span data-text="$$itemCount"></span> | 
      Total: $<span data-text="$$total.toFixed(2)"></span>
    </p>
    
    <template data-for="item, index in $$items">
      <div>
        <span data-text="item.name"></span> - 
        <span data-text="'$' + item.price"></span>
        <button data-on:click="@removeItem(index)">Remove</button>
      </div>
    </template>
  </div>
</template>
```

### Effects and Watchers [#](#effects-and-watchers)

Effects run side effects when reactive values change.
```
[ 1](#17f631a6c9c312c6_line_1)<template data-rocket:auto-saver
[ 2](#17f631a6c9c312c6_line_2)          data-props:data="string|="
[ 3](#17f631a6c9c312c6_line_3)          data-props:last-saved="string|="
[ 4](#17f631a6c9c312c6_line_4)          data-props:saving="boolean|=false"
[ 5](#17f631a6c9c312c6_line_5)>
[ 6](#17f631a6c9c312c6_line_6)  <script>
[ 7](#17f631a6c9c312c6_line_7)    let saveTimeout
[ 8](#17f631a6c9c312c6_line_8)    
[ 9](#17f631a6c9c312c6_line_9)    // Auto-save effect
    effect(() => {
      if (!$$data) {
        return
      }
      
      clearTimeout(saveTimeout)
      saveTimeout = setTimeout(async () => {
        $$saving = true
        try {
          await actions.post('/api/save', { data: $$data })
          $$lastSaved = new Date().toLocaleTimeString()
        } catch (error) {
          console.error('Save failed:', error)
        } finally {
          $$saving = false
        }
      }, 1000) // Debounce by 1 second
    })
    
    // Theme effect
    effect(() => {
      if ($theme) {
        document.body.className = $theme + '-theme'
      }
    })
    
    onCleanup(() => {
      clearTimeout(saveTimeout)
    })
  </script>
  
  <div>
    <textarea data-bind="data" placeholder="Start typing..."></textarea>
    <p data-show="$$saving">Saving...</p>
    <p data-show="$$lastSaved">Last saved: <span data-text="$$lastSaved"></span></p>
  </div>
</template>
```

## Element References [#](#element-references)

You can use `data-ref` to create references to elements within your component. Element references are available as `$$elementName` signals and automatically updated when the DOM changes.
```
[ 1](#35de3559a29a2674_line_1)<template data-rocket:canvas-painter
[ 2](#35de3559a29a2674_line_2)          data-props:color="string|=#000000"
[ 3](#35de3559a29a2674_line_3)          data-props:brush-size="int|=5"
[ 4](#35de3559a29a2674_line_4)>
[ 5](#35de3559a29a2674_line_5)  <script>
[ 6](#35de3559a29a2674_line_6)    let ctx
[ 7](#35de3559a29a2674_line_7)    let isDrawing = false
[ 8](#35de3559a29a2674_line_8)    
[ 9](#35de3559a29a2674_line_9)    // Get canvas context when canvas is available
    effect(() => {
      if ($$canvas) {
        ctx = $$canvas.getContext('2d')
        ctx.strokeStyle = $$color
        ctx.lineWidth = $$brushSize
        ctx.lineCap = 'round'
      }
    })
    
    // Update drawing properties
    effect(() => {
      if (ctx) {
        ctx.strokeStyle = $$color
        ctx.lineWidth = $$brushSize
      }
    })
    
    action({
      name: 'startDrawing',
      apply(_, e) {
        isDrawing = true
        const rect = $$canvas.getBoundingClientRect()
        ctx.beginPath()
        ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top)
      },
    })
    
    action({
      name: 'draw',
      apply(_, e) {
        if (!isDrawing) {
          return
        }

        const rect = $$canvas.getBoundingClientRect()
        ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top)
        ctx.stroke()
      },
    })
    
    action({
      name: 'stopDrawing',
      apply() {
        isDrawing = false
      },
    })
    
    action({
      name: 'clear',
      apply() {
        if (ctx) {
          ctx.clearRect(0, 0, $$canvas.width, $$canvas.height)
        }
      },
    })
  </script>
  
  <div>
    <div>
      <label>Color: <input type="color" data-bind="color"></label>
      <label>Size: <input type="range" min="1" max="20" data-bind="brushSize"></label>
      <button data-on:click="@clear()">Clear</button>
    </div>
    
    <canvas 
      data-ref="canvas" 
      width="400" 
      height="300"
      style="border: 1px solid #ccc"
      data-on:mousedown="@startDrawing"
      data-on:mousemove="@draw"
      data-on:mouseup="@stopDrawing"
      data-on:mouseleave="@stopDrawing">
    </canvas>
  </div>
</template>
```

## Validation with Codecs [#](#validation-with-codecs)

Rocket’s built-in codec system makes it possible to validate user input. By defining validation rules directly in your `data-props:*` attributes, data is automatically transformed and validated as it flows through your component.
### Type Codecs [#](#type-codecs)

Type codecs convert and validate prop values.
```
[ 1](#853daecf1fc675e7_line_1)<template data-rocket:validated-form
[ 2](#853daecf1fc675e7_line_2)          data-props:email="string|trim|required!|="
[ 3](#853daecf1fc675e7_line_3)          data-props:age="int|min:18|max:120|=0"
[ 4](#853daecf1fc675e7_line_4)          data-props:score="int|clamp:0,100|=0"
[ 5](#853daecf1fc675e7_line_5)>
[ 6](#853daecf1fc675e7_line_6)  <script>
[ 7](#853daecf1fc675e7_line_7)    // Signals are automatically validated by the codec system
[ 8](#853daecf1fc675e7_line_8)    // No need for manual codec setup - just use the signals directly
[ 9](#853daecf1fc675e7_line_9)    
    // Check for validation errors using the built-in $$hasErrs signal
    // No need to create computed - $$hasErrs is automatically available
  </script>
  
  <form>
    <div>
      <label>Email (required):</label>
      <input type="email" data-bind="email">
      <span data-show="$$errs?.email" class="error">Email is required</span>
    </div>
    
    <div>
      <label>Age (18-120):</label>
      <input type="number" data-bind="age">
      <span data-show="$$errs?.age" class="error">Age must be 18-120</span>
    </div>
    
    <div>
      <label>Score (0-100, auto-clamped):</label>
      <input type="number" data-bind="score">
      <span>Current: <span data-text="$$score"></span></span>
    </div>
    
    <button type="submit" data-attr:disabled="$$hasErrors">
      Submit
    </button>
  </form>
</template>
```

For date props, omitting an explicit default will use the current time. This is evaluated when the codec runs, producing a fresh `Date` instance based on the current time.
```
<template data-rocket:last-updated
          data-props:serverUpdateTime="date"
>
            <script>
    $$formatted = computed(() => $$serverUpdateTime.toLocaleString())
        </script>
  
        <span data-text="$$formatted"></span>
</template>
```

### Validation Rules [#](#validation-rules)

Codecs can either **transform** values (modify them) or **validate** them (check them without modifying).  Use the `!` suffix to make any codec validation-only.
- `min:10` - Transform: clamps value to minimum 10
- `min:10!` - Validate: rejects values below 10, keeps original on failure
- `trim` - Transform: removes whitespace
- `trim!` - Validate: rejects untrimmed stringsCodecTransformValidation **Type Conversion**`string`Converts to stringIs string?`int`Converts to integerIs integer?`float`Converts to numberIs numeric?`date`Converts ISO strings or timestamps to a `Date` object (defaults to the current time)Is valid date?`boolean`Converts to boolean. A missing attribute decodes to `false` by default, while a present-but-empty attribute (e.g. `<foo-bar baz>` on a `baz` prop) decodes to `true`.Is boolean?`json`Parses JSON stringValid JSON?`js`Parses JS object literal
**⚠️ [Avoid client values](https://xkcd.com/327/)**Valid JS syntax?`binary`Decodes base64Valid base64?**Validation**`required`-Not empty?`oneOf:a,b,c`Defaults to first option if invalidIs valid option?**Numeric Constraints**`min:n`Clamp to minimum value>= minimum?`max:n`Clamp to maximum value<= maximum?`clamp:min,max`Clamp between min and maxIn range?`round` / `round:n`Round to n decimal placesIs rounded?`ceil:n` / `floor:n`Ceiling/floor to n decimal placesIs ceiling/floor?**String Transforms**`trim`Remove leading/trailing whitespace-`upper` / `lower`Convert to upper/lowercase-`kebab` / `camel`Convert case styleCorrect case?`snake` / `pascal`Convert case styleCorrect case?`title` / `title:first`Title case (all words or first only)-**String Constraints**`minLength:n`-Length >= n?`maxLength:n`Truncates if too longLength <= n?`length:n`-Length equals n?`regex:pattern`-Matches regex?`startsWith:text`Adds prefix if missingStarts with text?`endsWith:text`Adds suffix if missingEnds with text?`includes:text`-Contains text?**Advanced Numeric**`lerp:min,max`Linear interpolation (0-1 to min-max)-`fit:in1,in2,out1,out2`Map value from one range to another-
## Component Lifecycle [#](#component-lifecycle)

Rocket components have a simple lifecycle with automatic cleanup.
```
[ 1](#2956cfd438f24eb_line_1)<template data-rocket:lifecycle-demo>
[ 2](#2956cfd438f24eb_line_2)  <script>
[ 3](#2956cfd438f24eb_line_3)    console.log('Component initializing...')
[ 4](#2956cfd438f24eb_line_4)    
[ 5](#2956cfd438f24eb_line_5)    $$mounted = true
[ 6](#2956cfd438f24eb_line_6)    
[ 7](#2956cfd438f24eb_line_7)    // Setup effects and timers
[ 8](#2956cfd438f24eb_line_8)    const intervalId = setInterval(() => {
[ 9](#2956cfd438f24eb_line_9)      console.log('Component is alive')
    }, 5000)
    
    // Cleanup when component is removed from DOM
    onCleanup(() => {
      console.log('Component cleanup')
      clearInterval(intervalId)
      $$mounted = false
    })
  </script>
  
  <div>
    <p data-show="$$mounted">Component is mounted</p>
  </div>
</template>
```

The lifecycle is as follows: 
- Rocket processes your template and registers the component.
- When you add it to the DOM, the instance is created and setup scripts run to initialize your signals.
- The component becomes reactive and responds to data changes.
- When you remove it from the DOM, all `onCleanup` callbacks run automatically.
## Optimistic UI [#](#optimistic-ui)

Rocket pairs seamlessly with Datastar’s server-driven model to provide instant visual feedback without shifting ownership of state to the browser. In the [Rocket flow example](/examples/rocket_flow), dragging a node instantly renders its optimistic position in the SVG while the original light-DOM host remains hidden. The component adds an `.is-pending` class to dim the node and connected edges, signaling that the drag is provisional. Once the backend confirms the new coordinates and updates the layout, the component automatically clears the pending style.

A dedicated prop such as `server-update-time="date"` makes this straightforward: each tab receives an updated timestamp from the server (via SSE or a patch), Rocket decodes it into a `Date` (defaulting to the current time when no value is provided), and internal effects react to reconcile every view. Unlike client-owned graph editors (e.g. React Flow), the server stays the single source of truth, while the optimistic UI remains a thin layer inside the component.
## Examples [#](#examples)

Check out the [Copy Button](/examples/rocket_copy_button) as a basic example, the [QR Code generator](/examples/rocket_qr_code) with validation, the [ECharts integration](/examples/rocket_echarts) for data visualization, the interactive [3D Globe](/examples/rocket_globe) with markers, and the [Virtual Scroll](/examples/rocket_virtual_scroll) example for handling large datasets efficiently.[](/reference/actions)[](/reference/sse_events)[](/star_federation)[](https://www.arcustech.com/)