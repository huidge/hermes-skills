---
name: static-markdown-site
description: Build a minimal static site to display Markdown files — collapsible grouped sidebar, auto-sync from source directories, static HTML build, and GitHub deployment
---

# Static Markdown Site

Build a zero-framework static site that renders Markdown content with a collapsible grouped sidebar. Supports auto-syncing `.md` files from any source directory, static HTML build, and one-command GitHub deployment.

## When to Use

- You have a directory of `.md` files (reports, docs, notes) you want to browse as a website
- You want grouped sidebar navigation with collapsible sections
- You need a one-command workflow: sync → build → deploy

## Project Structure

```
md-site/
├── index.html              # entry point (loads marked.js from CDN)
├── build.py                # static HTML build (supports grouped manifest)
├── sync-reports.sh         # one-command: sync + build + git push
├── assets/
│   ├── style.css           # theme with CSS variables
│   └── app.js              # markdown loader + grouped sidebar logic
├── content/
│   ├── manifest.json        # grouped: [{group, pages: [{file, title}]}]
│   └── ...                  # synced .md files (preserves subdirectory structure)
└── docs/                    # static build output (use docs/ for GitHub Pages, dist/ otherwise)
```

## Key Design Decisions

### Grouped Manifest Format

The manifest supports two formats:

**Flat** (simple sites):
```json
[{ "file": "hello.md", "title": "Hello" }]
```

**Grouped** (auto-synced sites with directory structure):
```json
[
  { "group": "Getting Started", "pages": [{ "file": "hello.md", "title": "Hello" }] },
  { "group": "Daily", "pages": [{ "file": "daily/2026-04-15.md", "title": "2026-04-15" }] }
]
```

Both `app.js` and `build.py` detect the format automatically.

### Collapsible Sidebar Groups

- Click group label to expand/collapse (animated with `max-height` transition)
- State persisted in `localStorage` key `sidebar-groups`
- Visual indicator: `▾` arrow rotates 90° when collapsed
- Global sidebar collapse: `Ctrl+B` or `<` button, state in `sidebar-collapsed`

### CSS Variables for Easy Theming

```css
:root {
  --sidebar-width: 260px;
  --sidebar-gap: 100px;      /* gap between sidebar and content */
  --accent: #0969da;
  --bg-sidebar: #f8f9fb;
  --radius: 8px;
}
```

## Sync Script Pattern

`sync-reports.sh` does three things in sequence:

1. **Copy .md files** — `find + cp`, only if changed (`diff -q` check)
2. **Generate manifest** — Python heredoc walks `content/` directory, groups by path, skips demo pages
3. **Build + Deploy** — `python3 build.py`, then `git add -A && commit && push`

### Filtering Source Directories

To sync only specific directories and ignore certain files, define arrays at the top of the script:

```bash
SYNC_DIRS=("daily" "us-stock/daily" "weekly")
IGNORE_FILES=("readme.md" "hello.md")

# clean target dirs before sync (avoids stale files)
for dir in "${SYNC_DIRS[@]}"; do
  rm -rf "$CONTENT_DIR/$dir"
done

# copy only from specified dirs, skip ignored files
for dir in "${SYNC_DIRS[@]}"; do
  [ -d "$dir" ] || continue
  find "$dir" -name "*.md" -type f | while read -r src; do
    base=$(basename "$src" | tr '[:upper:]' '[:lower:]')
    skip=false
    for ign in "${IGNORE_FILES[@]}"; do
      [ "$base" = "$ign" ] && skip=true && break
    done
    $skip && continue
    # ... cp file
  done
done
```

Pass the dirs to the Python manifest generator so it only walks those subdirectories:
```bash
python3 - "$CONTENT_DIR" "${SYNC_DIRS[@]}" <<'PYEOF'
import os, sys
content_dir = sys.argv[1]
sync_dirs = sys.argv[2:]
for sdir in sync_dirs:
    walk_root = os.path.join(content_dir, sdir)
    # os.walk from walk_root...
PYEOF
```

### Python Pitfalls

- Python heredoc variable passing: use `python3 - \"$VAR1\" \"$VAR2\" <<'PYEOF'` with `sys.argv` — do NOT use shell variable expansion inside heredoc (causes `string indices must be integers` errors)
- Token handling: read from `~/.hermes/.env` via `grep`, embed in remote URL for passwordless push: `https://user:${TOKEN}@github.com/user/repo.git`
- The sync script replaces content — demo pages (hello.md, guide.md) must be manually added to the manifest's first group or they get lost on next sync

### GitHub Push with Embedded Token

```bash
TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
git remote add origin "https://user:${TOKEN}@github.com/user/repo.git"
git push -u origin main
```

## build.py Key Logic

- `load_manifest()` — reads manifest.json, auto-detects grouped vs flat format
- `flat_pages(groups)` — flattens groups into single page list
- Builds each page with grouped sidebar nav HTML
- Creates subdirectory structure in `dist/` matching source paths

## Deploy

Static site — deploy `dist/` or root to GitHub Pages, Netlify, Vercel, or any web server.

### GitHub Pages Path Restriction

GitHub Pages API only accepts `/` or `/docs` as source paths — `/dist` is NOT valid. If deploying via API:

```bash
# this fails with 422
curl -X POST .../pages -d '{"source":{"branch":"main","path":"/dist"}}'

# use /docs instead
curl -X POST .../pages -d '{"source":{"branch":"main","path":"/docs"}}'
```

So if using GitHub Pages, output builds to `docs/` instead of `dist/`. Update `build.py`:
```python
DIST = ROOT / "docs"  # not "dist"
```

Then enable Pages:
```bash
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/$OWNER/$REPO/pages \
  -d '{"build_type":"legacy","source":{"branch":"main","path":"/docs"}}'
```
