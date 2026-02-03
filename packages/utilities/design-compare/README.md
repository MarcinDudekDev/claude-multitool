# design-compare

Compare design mockups with implementation screenshots using visual similarity metrics.

## Features

- Multiple comparison metrics (SSIM, perceptual hash, CLIP, pixel matching)
- Generates diff heatmap showing differences
- Side-by-side comparison output
- Configurable pass/fail threshold
- JSON output for automation

## Requirements

- Python 3.8+
- PIL/Pillow
- NumPy
- scikit-image (for SSIM)
- imagehash (for perceptual hash)
- torch + CLIP (optional, for semantic similarity)

## Installation

```bash
pip install pillow numpy scikit-image imagehash

# Optional: for CLIP embeddings
pip install torch clip

ln -s /path/to/design-compare ~/.local/bin/design-compare
```

## Usage

```bash
# Basic comparison
design-compare mockup.png screenshot.png

# Save diff heatmap
design-compare mockup.png screenshot.png --output diff.png

# Side-by-side comparison
design-compare mockup.png screenshot.png --side-by-side comparison.png

# JSON output for CI/CD
design-compare mockup.png screenshot.png --json

# Custom pass threshold
design-compare mockup.png screenshot.png --threshold 85

# Faster (skip CLIP)
design-compare mockup.png screenshot.png --no-clip
```

## Metrics

| Metric | Weight | Description |
|--------|--------|-------------|
| SSIM | 30% | Structural similarity |
| pHash | 20% | Perceptual hash |
| CLIP | 35% | Semantic similarity (AI) |
| Pixel match | 15% | Direct pixel comparison |

Custom weights:
```bash
design-compare mockup.png test.png --weights "ssim:0.5,phash:0.3,pixel_match:0.2"
```

## Output

```
Comparing: mockup.png vs screenshot.png

Scores:
  SSIM:        94.2%
  pHash:       96.8%
  CLIP:        91.5%
  Pixel match: 88.3%

Combined: 92.7%  ✓ PASS (threshold: 90%)
```

## License

MIT
