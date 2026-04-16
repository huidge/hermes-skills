# Hermes Skills Collection

A curated collection of skills for [Hermes Agent](https://github.com/hermes-agent).

## Overview

This repository contains **91+ skills** organized by category, covering:

- **apple** — Apple/macOS automation (iMessage, Reminders, Notes, FindMy)
- **autonomous-ai-agents** — Multi-agent orchestration (Claude Code, Codex, OpenCode)
- **creative** — ASCII art, diagrams, p5.js, manim animations
- **data-science** — Jupyter, market reports, data analysis
- **devops** — Cron jobs, webhooks, troubleshooting
- **gaming** — Minecraft servers, Pokemon emulation
- **mlops** — ML training, inference, evaluation, model management
- **productivity** — Google Workspace, Notion, Linear, PDF editing
- **research** — ArXiv, blog monitoring, investment analysis
- **software-development** — Architecture, patterns, Capacitor, TDD
- And more...

## Installation

Skills are automatically discovered by Hermes Agent from the `~/.hermes/skills/` directory.

To install a skill manually, copy its directory to `~/.hermes/skills/<category>/<skill-name>/`.

## Structure

```
skills/
├── README.md
├── category/
│   ├── DESCRIPTION.md          # Category description
│   └── skill-name/
│       ├── SKILL.md            # Main skill file (required)
│       ├── references/         # Reference materials
│       ├── templates/          # Templates
│       └── scripts/            # Helper scripts
```

## License

Individual skills may have their own licenses. See each SKILL.md for details.
