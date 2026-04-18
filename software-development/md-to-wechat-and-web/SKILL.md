---
name: md-to-wechat-and-web
description: Convert Markdown files to styled HTML web pages and WeChat public account articles with inline styles, batch processing support
---

# Markdown to Web + WeChat Converter

A unified Python CLI tool (`report.py`) for converting Markdown into styled web pages and/or WeChat public account (公众号) articles. Supports single files and batch processing.

## Script Location

```
market-reports/report.py
```

## Dependencies

```bash
pip install markdown
```

## Usage

```bash
# Single file, default: generates both html + wechat
python3 report.py weekly/2026-W16.md

# Only one format
python3 report.py weekly/2026-W16.md -f html
python3 report.py weekly/2026-W16.md -f wechat

# Batch: entire directory
python3 report.py daily/

# Batch: multiple directories + recursive
python3 report.py daily/ weekly/ -r

# Output to specific directory
python3 report.py weekly/ -o dist/

# Full combo
python3 report.py . -r -f wechat -o dist/
```

## CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `inputs` | File(s) or directory(ies) | required |
| `-f` | Format: `html`, `wechat`, `all` | `all` |
| `-r` | Recursive subdirectories | off |
| `-o` | Output directory | same as source |

## Output Files

For input `report.md`:
- `report.html` — web page version
- `report.wechat.html` — WeChat version

## Web Version Features

- External `<style>` block with CSS variables
- Blue gradient header with title/subtitle
- Card-based layout (each h2 section wrapped in a card)
- Auto color-codes: **red for gains (+X.XX%), green for losses (-X.XX%)** — A-share convention
- Responsive design for mobile
- Hover effects on table rows

## WeChat Version Features

WeChat editor rejects `<style>` blocks and external CSS. All styling must be **inline**.

### Key constraints handled:
- All styles as `style="..."` attributes on every element
- Width capped at 677px (WeChat reading area)
- Font stack: `-apple-system, 'PingFang SC', 'Microsoft YaHei'`
- No `<link>`, no `<script>`, no external resources
- Section headers get emoji prefixes (📊🔄📌🔍🔮⚠️)
- Tables: blue header row, first column left-aligned, numbers center-aligned
- **Color coding: red for gains, green for losses** (A-share market convention)
- Gradient horizontal rules (inline `background: linear-gradient`)

### WeChat publish workflow:
1. Open `.wechat.html` in browser
2. Ctrl/Cmd+A → Ctrl/Cmd+C
3. Paste into mp.weixin.qq.com editor

## Customization

### Adding section emojis
Edit `SECTION_EMOJIS` dict in `report.py`:
```python
SECTION_EMOJIS = {
    "主要指数": "📊",
    "板块轮动": "🔄",
    # add more...
}
```

### Changing colors
Edit `WC_STYLES` dict (WeChat) or `HTML_CSS` string (web) in `report.py`.

### Changing color scheme
Edit `colorize()` and `colorize_to_spans()` functions. Currently:
- `+X.XX%` → `#d93025` (red, A-share: up)
- `-X.XX%` → `#0d904f` (green, A-share: down)

## Pitfalls

- WeChat strips some CSS properties on paste — test with actual editor after changes
- Very long tables may overflow on mobile — consider splitting if needed
- `markdown` library auto-escapes some HTML entities in table cells — the colorize function runs post-conversion to avoid conflicts
- A-share convention: red=up, green=down (opposite of US markets)
