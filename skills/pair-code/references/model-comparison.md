# Model Comparison for Pair Programming

## Model Strengths

### Claude (Anthropic)

**Implementation strengths:**
- Careful, thorough code changes
- Strong understanding of context
- Good at following existing patterns
- Excellent documentation

**Review strengths:**
- Catches subtle bugs
- Good security awareness
- Thorough feedback
- Balanced criticism

**Best for:** Complex refactoring, security-sensitive code, documentation

### Gemini (Google)

**Implementation strengths:**
- Fast responses
- Creative solutions
- Good at boilerplate generation
- Strong with algorithms

**Review strengths:**
- Mathematical precision
- Edge case detection
- Performance considerations
- Concise feedback

**Best for:** Algorithm implementation, performance optimization, mathematical code

### OpenCode

**Implementation strengths:**
- Consistent output format
- Good at following templates
- Reliable for simple changes

**Review strengths:**
- Straightforward feedback
- Good for syntax checks

**Best for:** Simple changes, template-based generation

## Recommended Pairings

### High-Quality Code

**Claude + Claude** (default)
- Best for: Production code, security-sensitive changes
- Trade-off: Slower, more expensive

### Fast Iteration

**Gemini + Claude (haiku)**
- Command: `-i gemini -q`
- Best for: Rapid prototyping, simple fixes
- Trade-off: May miss subtle issues

### Diverse Perspectives

**Claude + Gemini**
- Command: `-r gemini`
- Best for: Getting different viewpoints
- Trade-off: Different review styles may conflict

### Budget Conscious

**Gemini + Claude (haiku)**
- Command: `-i gemini -q`
- Best for: High volume, simple changes
- Trade-off: Quality may vary

## When to Use Each Pairing

| Use Case | Pairing | Reason |
|----------|---------|--------|
| Security fix | Claude + Claude | Maximum scrutiny |
| Quick typo fix | Any + Claude -q | Speed matters |
| Algorithm | Gemini + Claude | Gemini strong at algorithms |
| Refactoring | Claude + Gemini | Get diverse perspective |
| Documentation | Claude + Claude | Claude excels at docs |
| Performance | Gemini + Claude | Gemini catches perf issues |

## Flipped Workflow Benefits

Using **Claude as implementer, Gemini as reviewer**:

1. **Different perspective**: Gemini catches things Claude misses
2. **Mathematical precision**: Gemini good at off-by-one errors
3. **Performance focus**: Gemini often suggests optimizations
4. **Concise feedback**: Gemini reviews are typically shorter

Example from real usage: Gemini caught a retry count logic error where `range(max_retries)` only produced 2 delays instead of the expected 3.
