# WCAG 2.1 AA Accessibility Checklist

## Perceivable

### 1.1 Text Alternatives
- [ ] All images have alt text (descriptive or empty for decorative)
- [ ] Complex images (charts/graphs) have long descriptions
- [ ] Icons have accessible labels

### 1.2 Time-based Media
- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] No auto-playing media with sound

### 1.3 Adaptable
- [ ] Content reads logically without CSS
- [ ] Form labels programmatically associated with inputs
- [ ] Tables have headers marked up correctly

### 1.4 Distinguishable
- [ ] **Color contrast:** 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt bold)
- [ ] Color not sole indicator (e.g., red error + icon/text)
- [ ] Text resizable to 200% without loss
- [ ] No horizontal scrolling at 320px width

## Operable

### 2.1 Keyboard Accessible
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Skip links to main content
- [ ] Focus order logical

### 2.2 Enough Time
- [ ] User can pause/stop/hide moving content
- [ ] Session timeouts warn user with option to extend
- [ ] No time limits on reading content

### 2.3 Seizures
- [ ] No content flashes more than 3 times/second

### 2.4 Navigable
- [ ] Pages have descriptive titles
- [ ] Focus visible (outline on focused elements)
- [ ] Link text descriptive ("Read more about pricing" not "Click here")
- [ ] Multiple ways to find pages (nav, search, sitemap)

### 2.5 Input Modalities
- [ ] **Touch targets:** Minimum 44×44 CSS pixels
- [ ] Pointer gestures have alternatives (pinch → buttons)
- [ ] Motion controls have alternatives (shake → button)

## Understandable

### 3.1 Readable
- [ ] Page language declared (`<html lang="en">`)
- [ ] Abbreviations explained on first use

### 3.2 Predictable
- [ ] Focus doesn't trigger unexpected changes
- [ ] Consistent navigation across pages
- [ ] Consistent identification (same icons = same actions)

### 3.3 Input Assistance
- [ ] Errors identified with text (not just color)
- [ ] Labels/instructions for form inputs
- [ ] Error suggestions provided
- [ ] Confirmation before destructive actions

## Robust

### 4.1 Compatible
- [ ] Valid HTML (no duplicate IDs)
- [ ] ARIA used correctly (aria-label, aria-expanded, etc.)
- [ ] Custom controls have correct roles

## Quick Contrast Checks

| Element | Minimum Ratio |
|---------|---------------|
| Normal text (<18pt) | 4.5:1 |
| Large text (18pt+ or 14pt bold) | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

## Touch Target Sizes

| Platform | Minimum Size |
|----------|--------------|
| iOS | 44×44 pt |
| Android | 48×48 dp |
| Web | 44×44 CSS px |

## Testing Tools
- **Contrast:** WebAIM Contrast Checker, Colour Contrast Analyser
- **Screen reader:** VoiceOver (Mac), NVDA (Windows), TalkBack (Android)
- **Automated:** axe DevTools, WAVE, Lighthouse
- **Keyboard:** Tab through entire page, check focus visibility

## References
- https://www.w3.org/WAI/WCAG21/quickref/
- https://webaim.org/standards/wcag/checklist
