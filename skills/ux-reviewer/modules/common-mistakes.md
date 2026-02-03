# Common UX Mistakes & Antipatterns

## TOP 10 UX GOTCHAS

| # | Mistake | Why It's Bad | Fix |
|---|---------|--------------|-----|
| 1 | **Hamburger menus on desktop** | Reduces engagement 50%+ | Visible navigation |
| 2 | **Asking users what they want** | Users lie/don't know | Observe behavior instead |
| 3 | **Icon-only buttons** | Unclear meaning | Add labels or tooltips |
| 4 | **Infinite scroll without position** | Can't bookmark, share, or return | Add pagination or "load more" |
| 5 | **Carousel/slider for content** | 1% click banner 2+ | Show all content or prioritize |
| 6 | **Placeholder text as labels** | Disappears when typing | Use visible labels above inputs |
| 7 | **Gray text on gray background** | Fails contrast, hard to read | 4.5:1 minimum contrast |
| 8 | **Disabling paste in password** | Breaks password managers | Allow paste always |
| 9 | **Centered body text** | Hard to read long lines | Left-align, max 70 chars/line |
| 10 | **Mystery meat navigation** | Users can't predict where links go | Clear, descriptive link text |

## Dark Patterns to Avoid

### Confirm-shaming
**Bad:** "No thanks, I don't want to save money"
**Good:** "No thanks" or "Maybe later"

### Hidden Costs
**Bad:** Show price without shipping until checkout
**Good:** "Starting at $X + shipping" upfront

### Trick Questions
**Bad:** "Uncheck to not unsubscribe from not receiving..."
**Good:** "Subscribe to newsletter" checkbox

### Roach Motel
**Bad:** Easy to sign up, 5 pages + phone call to cancel
**Good:** Cancel in same place as sign up

### Forced Continuity
**Bad:** Auto-charge after trial with no warning
**Good:** Email reminder 3 days before trial ends

### Misdirection
**Bad:** Big "Accept All Cookies" button, tiny "Manage"
**Good:** Equal visual weight for all options

## Form Mistakes

| Mistake | Fix |
|---------|-----|
| Required fields not marked | Use asterisk (*) or say "All fields required" |
| Error shown only after submit | Inline validation as user types |
| Clearing form on error | Preserve user input |
| Date format not specified | Show format or use date picker |
| Phone/CC requiring specific format | Auto-format as user types |

## Mobile-Specific Mistakes

| Mistake | Fix |
|---------|-----|
| Touch targets too small | Minimum 44×44px |
| Hover-only interactions | Add tap alternatives |
| Fixed position elements blocking content | Use sparingly, allow dismiss |
| Large unoptimized images | Serve responsive images |
| No viewport meta | Add `<meta name="viewport" content="width=device-width, initial-scale=1">` |

## Copy/Microcopy Mistakes

| Mistake | Example | Better |
|---------|---------|--------|
| Vague button text | "Submit" | "Create Account" |
| Technical errors | "Error 500" | "Something went wrong. Please try again." |
| No empty states | Blank page | "No items yet. Add your first!" |
| Generic confirmations | "Success" | "Your order #1234 is confirmed" |

## Research Mistakes

| Mistake | Why It Fails |
|---------|--------------|
| Asking "Would you use this?" | People say yes, don't mean it |
| Testing with coworkers | They know too much context |
| Leading questions | "Don't you think this is better?" |
| Small sample size | 5 users find 80% of issues |
| Not testing on real devices | Desktop != mobile experience |

## References
- https://www.nngroup.com/articles/
- https://www.deceptive.design/ (dark patterns)
- https://lawsofux.com/
