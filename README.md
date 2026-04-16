# Hermes Skills Collection

A curated collection of **91+ skills** for [Hermes Agent](https://github.com/hermes-agent) — organized by category, covering coding, ML/AI, research, creative content, productivity, and more.

[中文文档](README_CN.md) | English

## What are Skills?

Skills are reusable knowledge modules that teach Hermes Agent how to perform specific tasks. Each skill contains a `SKILL.md` with step-by-step instructions, commands, templates, and best practices. Skills are auto-discovered from `~/.hermes/skills/`.

## Categories

---

### Apple (macOS)
macOS-specific automation — only loads on Mac systems.

| Skill | Description |
|-------|-------------|
| apple-notes | Manage Apple Notes via `memo` CLI — create, view, search, edit notes |
| apple-reminders | Manage Apple Reminders via `remindctl` — list, add, complete, delete |
| findmy | Track Apple devices and AirTags via FindMy.app |
| imessage | Send and receive iMessages/SMS via `imsg` CLI |

### Autonomous AI Agents
Spawn and orchestrate autonomous coding agents and multi-agent workflows.

| Skill | Description |
|-------|-------------|
| claude-code | Delegate tasks to Claude Code (Anthropic's CLI agent) |
| codex | Delegate tasks to OpenAI Codex CLI agent |
| opencode | Delegate tasks to OpenCode CLI agent |
| hermes-agent | Complete guide to using and extending Hermes Agent |

### Creative
Content generation — ASCII art, diagrams, animations, music, and visual design.

| Skill | Description |
|-------|-------------|
| ascii-art | Generate ASCII art — pyfiglet (571 fonts), cowsay, image-to-ascii |
| ascii-video | Production pipeline for ASCII art video (MP4, GIF, real-time) |
| creative-ideation | Generate project ideas through creative constraints |
| excalidraw | Create hand-drawn style diagrams (.excalidraw files) |
| manim-video | 3Blue1Brown-style math/tech animations with Manim |
| p5js | Interactive and generative visual art with p5.js |
| popular-web-designs | 54 production-quality design systems (Airbnb, Apple, Cursor...) |
| songwriting-and-ai-music | Songwriting craft + AI music generation (Suno) |

### Data Science
Data analysis, market reports, Jupyter notebooks, and visualization.

| Skill | Description |
|-------|-------------|
| daily-market-report | 每日A股收盘交易汇总 — 资金流向、板块热点、技术面分析 |
| eastmoney-scraper | Scrape A-share market data from 东方财富 APIs |
| jupyter-live-kernel | Live Jupyter kernel for stateful, iterative Python exploration |
| us-stock-daily-report | 每日美股收盘行情 — 指数、板块轮动、个股亮点 |

### DevOps
Infrastructure, monitoring, and automation troubleshooting.

| Skill | Description |
|-------|-------------|
| cron-job-troubleshooting | Debug cron job failures — status, logs, gateway errors |
| webhook-subscriptions | Event-driven agent activation via webhooks |

### Domain Intelligence
Passive domain reconnaissance using Python stdlib — no API keys needed.

| Skill | Description |
|-------|-------------|
| domain-intel | Subdomain discovery, SSL inspection, WHOIS, DNS, bulk analysis |

### Email
Terminal-based email management.

| Skill | Description |
|-------|-------------|
| himalaya | IMAP/SMTP email via CLI — list, read, write, reply, search, multi-account |

### Gaming
Game server setup and automation.

| Skill | Description |
|-------|-------------|
| minecraft-modpack-server | Modded Minecraft server from CurseForge/Modrinth packs |
| pokemon-player | Autonomous Pokemon gameplay via headless emulation |

### GitHub
Repository, PR, issue, and CI/CD management.

| Skill | Description |
|-------|-------------|
| codebase-inspection | LOC counting, language breakdown, codebase stats |
| github-auth | GitHub authentication — tokens, SSH, credential helpers |
| github-code-review | Code review via git diffs and PR inline comments |
| github-issues | Create, manage, triage, and close GitHub issues |
| github-pr-workflow | Full PR lifecycle — branch, commit, open, monitor, merge |
| github-repo-management | Clone, create, fork, configure repos; secrets, releases |

### MCP (Model Context Protocol)
Connect to external MCP servers and tools.

| Skill | Description |
|-------|-------------|
| mcporter | CLI bridge for ad-hoc MCP server interaction |
| native-mcp | Built-in MCP client — auto-discover tools from servers |

### Media
Audio, video, GIFs, and content processing.

| Skill | Description |
|-------|-------------|
| gif-search | Search and download GIFs from Tenor |
| heartmula | Open-source music generation (Suno-like) |
| songsee | Audio spectrograms and feature visualizations |
| youtube-content | Fetch YouTube transcripts, summaries, analysis |

### MLOps
Full ML lifecycle — training, inference, evaluation, deployment.

**Training:**
| Skill | Description |
|-------|-------------|
| axolotl | Fine-tuning with YAML configs — 100+ models, LoRA/QLoRA, DPO/GRPO |
| unsloth | Fast fine-tuning — 2-5x faster, 50-80% less memory |
| peft | Parameter-efficient fine-tuning — LoRA, QLoRA, 25+ methods |
| trl-fine-tuning | RLHF fine-tuning — SFT, DPO, PPO/GRPO |
| grpo-rl-training | GRPO/RL training for reasoning models |
| pytorch-fsdp | Fully Sharded Data Parallel training |

**Inference:**
| Skill | Description |
|-------|-------------|
| vllm | High-throughput LLM serving with PagedAttention |
| llama-cpp | LLM inference on CPU/Apple Silicon/consumer GPUs |
| gguf | GGUF quantization for efficient CPU/GPU inference |
| guidance | Constrained generation — regex, grammars, structured output |
| outlines | Guarantee valid JSON/XML/code during generation |
| obliteratus | Remove LLM refusal behaviors via mechanistic interpretability |

**Models:**
| Skill | Description |
|-------|-------------|
| stable-diffusion | Text-to-image generation |
| whisper | Speech recognition — 99 languages, transcription |
| clip | Vision-language model — zero-shot image classification |
| segment-anything | Zero-shot image segmentation |
| audiocraft | Text-to-music (MusicGen) and sound effects (AudioGen) |

**Evaluation & Tracking:**
| Skill | Description |
|-------|-------------|
| lm-evaluation-harness | 60+ benchmarks (MMLU, HumanEval, GSM8K...) |
| weights-and-biases | Experiment tracking, visualization, hyperparameter sweeps |
| dspy | Declarative AI programming — optimize prompts, build RAG |
| huggingface-hub | HuggingFace CLI — search, download, upload models/datasets |

**Cloud:**
| Skill | Description |
|-------|-------------|
| modal | Serverless GPU cloud for ML workloads |

### Note-taking
| Skill | Description |
|-------|-------------|
| obsidian | Read, search, create notes in Obsidian vault |

### Productivity
Documents, presentations, spreadsheets, and workflow tools.

| Skill | Description |
|-------|-------------|
| google-workspace | Gmail, Calendar, Drive, Contacts, Sheets, Docs integration |
| linear | Linear issues, projects, teams via GraphQL API |
| nano-pdf | Edit PDFs with natural language instructions |
| notion | Notion API — pages, databases, blocks |
| ocr-and-documents | Extract text from PDFs, scanned docs, DOCX, PPTX |
| powerpoint | Create, edit, parse .pptx presentations |

### Red Teaming
| Skill | Description |
|-------|-------------|
| godmode | Jailbreak LLMs — 33 obfuscation techniques, multi-model racing |

### Research
Academic research, market data, content monitoring, and knowledge management.

| Skill | Description |
|-------|-------------|
| arxiv | Search and retrieve academic papers from arXiv |
| blogwatcher | Monitor blogs and RSS/Atom feeds for updates |
| investment-analysis | 股票与基金投资分析 — 基本面/技术面/资产配置 |
| llm-wiki | Build persistent, interlinked markdown knowledge base |
| polymarket | Query Polymarket prediction market data |
| research-paper-writing | End-to-end ML/AI paper writing pipeline |

### Smart Home
| Skill | Description |
|-------|-------------|
| openhue | Control Philips Hue lights, rooms, and scenes |

### Social Media
| Skill | Description |
|-------|-------------|
| xitter | X/Twitter via x-cli — post, search, like, retweet, bookmarks |

### Software Development
Architecture, patterns, testing, debugging, and best practices.

| Skill | Description |
|-------|-------------|
| api-design-patterns | API 设计最佳实践 — RESTful/GraphQL/gRPC |
| capacitor-h5-to-app | Package H5 web app into native Android/iOS app |
| common-development-patterns | 设计模式、并发、错误处理、安全、性能调优 |
| database-design-and-caching | 数据库设计、索引优化、Redis 缓存模式 |
| devops-cicd-containerization | Docker/K8s/CI/CD/GitOps/监控可观测性 |
| frontend-architecture | React/Next/Vue/Nuxt/Svelte 框架选型、渲染策略 |
| system-architecture-design | 单体 vs 微服务、DDD、高可用方案 |
| plan | Plan mode — write implementation plans, don't execute |
| writing-plans | Create comprehensive implementation plans with tasks |
| test-driven-development | RED-GREEN-REFACTOR TDD cycle |
| systematic-debugging | 4-phase root cause investigation |
| subagent-driven-development | Parallel task execution with delegate_task |
| requesting-code-review | Pre-commit verification pipeline |

### Inference.sh
| Skill | Description |
|-------|-------------|
| infsh | Run 150+ AI apps via inference.sh — image, video, LLM, search, 3D |

---

## Installation

Skills are auto-discovered from `~/.hermes/skills/`. To add a skill:

```bash
# Clone this repo
git clone https://github.com/huidge/hermes-skills.git ~/.hermes/skills

# Or copy a single skill
cp -r skills/software-development/tdd ~/.hermes/skills/software-development/
```

## Repository Structure

```
skills/
├── README.md
├── category/
│   ├── DESCRIPTION.md              # Category description
│   └── skill-name/
│       ├── SKILL.md                # Main skill file (required)
│       ├── references/             # Reference materials
│       ├── templates/              # Templates
│       └── scripts/                # Helper scripts
```

## Sync

This repo auto-syncs daily via cron job. Manual sync:

```bash
~/.hermes/sync-skills.sh
```

## Stats

- **26 categories**
- **91+ skills**
- **Domains**: Coding, ML/AI, Creative, Productivity, Research, Gaming, IoT, and more

## License

Individual skills may have their own licenses. See each SKILL.md for details.
