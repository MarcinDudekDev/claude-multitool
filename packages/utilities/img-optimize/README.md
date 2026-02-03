# img-optimize

Local TinyPNG alternative for image optimization.

## Features

- Lossless optimization by default
- Lossy compression option for aggressive reduction
- Auto-resize for large images
- WebP generation
- Batch processing with recursive option
- Supports PNG, JPEG, WebP

## Requirements

- ImageMagick (`brew install imagemagick`)
- pngquant (`brew install pngquant`) - for PNG lossy
- jpegoptim (`brew install jpegoptim`) - for JPEG
- cwebp (`brew install webp`) - for WebP

## Installation

```bash
ln -s /path/to/img-optimize ~/.local/bin/img-optimize
```

## Usage

```bash
# Lossless optimization (default)
img-optimize image.png

# Lossy compression
img-optimize --lossy image.jpg

# Generate WebP versions too
img-optimize --webp image.png

# Replace originals (default creates .opt.ext)
img-optimize --replace image.png

# Process directory recursively
img-optimize -R ./images/

# Custom quality
img-optimize --lossy --quality 75 image.jpg
```

## Options

| Option | Description |
|--------|-------------|
| `-l, --lossy` | Enable lossy compression |
| `-q, --quality NUM` | Quality 1-100 (default: 85) |
| `-m, --max-dim NUM` | Max dimension before resize (default: 4000) |
| `-w, --webp` | Generate WebP versions |
| `-r, --replace` | Replace originals |
| `-R, --recursive` | Process directories recursively |
| `-v, --verbose` | Show detailed output |

## Output

By default, creates optimized files with `.opt` suffix:
- `image.png` → `image.opt.png`

With `--replace`, overwrites original.

## License

MIT
