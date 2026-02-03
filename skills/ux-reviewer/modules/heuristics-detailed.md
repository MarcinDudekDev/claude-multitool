# Nielsen's 10 Usability Heuristics (Detailed)

## 1. Visibility of System Status
**Keep users informed through appropriate feedback within reasonable time.**

Examples:
- Progress bars during file uploads
- "Saving..." indicators
- Loading spinners with context ("Loading products...")
- Success/error toast messages

**Bad:** Silent form submission with no feedback
**Good:** "Message sent successfully" toast + redirect

## 2. Match Between System and Real World
**Use language, concepts, and conventions familiar to the user.**

Examples:
- "Shopping Cart" not "Product Accumulator"
- Calendar using month/day format user expects
- Icons matching real-world objects (trash can for delete)

**Bad:** Technical jargon in error messages
**Good:** "We couldn't find that page" vs "404 Not Found"

## 3. User Control and Freedom
**Provide undo, redo, and clear exit paths.**

Examples:
- Undo delete with "Undo" link
- Cancel button on modals
- Back button works predictably
- "Are you sure?" for destructive actions

**Bad:** No way to cancel a multi-step wizard
**Good:** Gmail's "Undo Send" feature

## 4. Consistency and Standards
**Follow platform conventions. Same words/actions = same things.**

Examples:
- Blue underlined text = link
- × in corner = close
- Consistent button styles throughout app
- Same navigation position on all pages

**Bad:** Sometimes "Save" sometimes "Submit" for same action
**Good:** Consistent terminology and placement

## 5. Error Prevention
**Prevent errors before they happen.**

Examples:
- Disable "Submit" until form valid
- Confirmation dialogs for destructive actions
- Date pickers instead of free text
- Inline validation as user types

**Bad:** Let user type invalid email, show error on submit
**Good:** Real-time email format validation

## 6. Recognition Rather Than Recall
**Minimize memory load. Make options visible.**

Examples:
- Dropdown menus vs free text
- Recently used items shown
- Breadcrumbs showing location
- Autocomplete suggestions

**Bad:** Requiring users to remember SKU codes
**Good:** Searchable product list with images

## 7. Flexibility and Efficiency of Use
**Provide accelerators for expert users.**

Examples:
- Keyboard shortcuts (Cmd+S to save)
- Search with filters for power users
- Bulk actions
- Customizable dashboards

**Bad:** Force every user through 5-step wizard
**Good:** Wizard for new users, quick-add for experts

## 8. Aesthetic and Minimalist Design
**Remove unnecessary information. Every element should serve a purpose.**

Examples:
- Whitespace to reduce cognitive load
- Progressive disclosure (show more on demand)
- Remove decorative elements that distract
- Clear visual hierarchy

**Bad:** Dashboard with 50 metrics visible at once
**Good:** Show top 5 metrics, expandable for more

## 9. Help Users Recognize, Diagnose, and Recover from Errors
**Error messages in plain language with solutions.**

Examples:
- "Password must be at least 8 characters" not "Invalid input"
- Highlight which field has error
- Suggest fixes ("Did you mean gmail.com?")
- Don't clear form on error

**Bad:** "Error code: 0x8007045D"
**Good:** "File too large. Maximum size is 10MB. Try compressing it first."

## 10. Help and Documentation
**Provide searchable, task-focused help.**

Examples:
- Contextual help icons (?) next to complex fields
- Searchable FAQ/knowledge base
- Tooltips on hover
- Onboarding tutorials for new features

**Bad:** 100-page PDF manual
**Good:** In-app tooltips + searchable help center

## References
- https://www.nngroup.com/articles/ten-usability-heuristics/
- https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
