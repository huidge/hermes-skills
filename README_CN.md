# Hermes Skills Collection (中文版)

[Hermes Agent](https://github.com/hermes-agent) 的 **91+ 个精选技能集合** — 涵盖编程、机器学习、科研、创意内容、效率工具等领域。

## 什么是 Skills？

Skills（技能）是可复用的知识模块，用于指导 Hermes Agent 完成特定任务。每个 skill 包含 `SKILL.md` 文件，内含分步指引、命令模板和最佳实践。Skills 会自动从 `~/.hermes/skills/` 目录中发现并加载。

---

## 技能分类

### Apple (macOS)
macOS 专属自动化 — 仅在 Mac 系统上加载。

| 技能 | 功能说明 |
|------|---------|
| apple-notes | 通过 `memo` CLI 管理 Apple 备忘录 — 创建、查看、搜索、编辑 |
| apple-reminders | 通过 `remindctl` 管理 Apple 提醒事项 — 列表、添加、完成、删除 |
| findmy | 通过 FindMy.app 追踪 Apple 设备和 AirTag |
| imessage | 通过 `imsg` CLI 发送和接收 iMessage/短信 |

### 自主 AI 代理
编排自主编程代理和多代理工作流。

| 技能 | 功能说明 |
|------|---------|
| claude-code | 委派任务给 Claude Code（Anthropic 的 CLI 代理） |
| codex | 委派任务给 OpenAI Codex CLI 代理 |
| opencode | 委派任务给 OpenCode CLI 代理 |
| hermes-agent | Hermes Agent 完整使用与扩展指南 |

### 创意内容
内容生成 — ASCII 艺术、图表、动画、音乐和视觉设计。

| 技能 | 功能说明 |
|------|---------|
| ascii-art | 生成 ASCII 艺术 — pyfiglet（571 种字体）、cowsay、图片转 ASCII |
| ascii-video | ASCII 视频制作流水线（MP4、GIF、实时渲染） |
| creative-ideation | 通过创意约束生成项目灵感 |
| excalidraw | 创建手绘风格图表（.excalidraw 文件） |
| manim-video | 3Blue1Brown 风格的数学/技术动画 |
| p5js | 使用 p5.js 创建交互式和生成式视觉艺术 |
| popular-web-designs | 54 套生产级设计系统（Airbnb、Apple、Cursor...） |
| songwriting-and-ai-music | 歌曲创作技巧 + AI 音乐生成（Suno） |

### 数据科学
数据分析、市场报告、Jupyter 笔记本和可视化。

| 技能 | 功能说明 |
|------|---------|
| daily-market-report | 每日A股收盘交易汇总 — 资金流向、板块热点、技术面分析 |
| eastmoney-scraper | 从东方财富 API 抓取 A 股市场数据 |
| jupyter-live-kernel | 有状态的 Jupyter 内核，支持迭代式 Python 探索 |
| us-stock-daily-report | 每日美股收盘行情 — 指数、板块轮动、个股亮点 |

### DevOps
基础设施、监控和自动化故障排查。

| 技能 | 功能说明 |
|------|---------|
| cron-job-troubleshooting | 排查定时任务失败 — 状态、日志、网关错误 |
| webhook-subscriptions | 通过 webhook 实现事件驱动的代理激活 |

### 域名情报
使用 Python 标准库进行被动域名侦察 — 无需 API Key。

| 技能 | 功能说明 |
|------|---------|
| domain-intel | 子域名发现、SSL 检查、WHOIS、DNS、批量分析 |

### 邮件
终端邮件管理。

| 技能 | 功能说明 |
|------|---------|
| himalaya | 通过 CLI 管理 IMAP/SMTP 邮件 — 列表、阅读、撰写、回复、搜索、多账户 |

### 游戏
游戏服务器搭建和自动化。

| 技能 | 功能说明 |
|------|---------|
| minecraft-modpack-server | 从 CurseForge/Modrinth 整合包搭建模组 Minecraft 服务器 |
| pokemon-player | 通过无头模拟器自动游玩 Pokemon |

### GitHub
仓库、PR、Issue 和 CI/CD 管理。

| 技能 | 功能说明 |
|------|---------|
| codebase-inspection | 代码行数统计、语言构成、代码库分析 |
| github-auth | GitHub 认证 — Token、SSH、凭证助手 |
| github-code-review | 通过 git diff 和 PR 行内评论进行代码审查 |
| github-issues | 创建、管理、分类和关闭 GitHub Issue |
| github-pr-workflow | 完整 PR 生命周期 — 分支、提交、创建、监控、合并 |
| github-repo-management | 克隆、创建、fork、配置仓库；管理密钥、发布 |

### MCP（模型上下文协议）
连接外部 MCP 服务器和工具。

| 技能 | 功能说明 |
|------|---------|
| mcporter | 临时 MCP 服务器交互的 CLI 桥接工具 |
| native-mcp | 内置 MCP 客户端 — 自动发现服务器提供的工具 |

### 媒体
音频、视频、GIF 和内容处理。

| 技能 | 功能说明 |
|------|---------|
| gif-search | 从 Tenor 搜索和下载 GIF |
| heartmula | 开源音乐生成模型（类 Suno） |
| songsee | 音频频谱图和特征可视化 |
| youtube-content | 获取 YouTube 字幕、摘要和分析 |

### MLOps
完整机器学习生命周期 — 训练、推理、评估、部署。

**训练：**
| 技能 | 功能说明 |
|------|---------|
| axolotl | YAML 配置驱动的微调 — 100+ 模型、LoRA/QLoRA、DPO/GRPO |
| unsloth | 快速微调 — 速度提升 2-5 倍，内存节省 50-80% |
| peft | 参数高效微调 — LoRA、QLoRA、25+ 种方法 |
| trl-fine-tuning | RLHF 微调 — SFT、DPO、PPO/GRPO |
| grpo-rl-training | 推理模型的 GRPO/RL 训练 |
| pytorch-fsdp | 完全分片数据并行训练 |

**推理：**
| 技能 | 功能说明 |
|------|---------|
| vllm | 基于 PagedAttention 的高吞吐 LLM 推理服务 |
| llama-cpp | 在 CPU/Apple Silicon/消费级 GPU 上运行 LLM 推理 |
| gguf | GGUF 量化 — 高效 CPU/GPU 推理 |
| guidance | 约束生成 — 正则表达式、文法、结构化输出 |
| outlines | 生成时保证有效的 JSON/XML/代码结构 |
| obliteratus | 通过机制可解释性移除 LLM 拒绝行为 |

**模型：**
| 技能 | 功能说明 |
|------|---------|
| stable-diffusion | 文本到图像生成 |
| whisper | 语音识别 — 支持 99 种语言、转录 |
| clip | 视觉-语言模型 — 零样本图像分类 |
| segment-anything | 零样本图像分割 |
| audiocraft | 文本到音乐（MusicGen）和音效生成（AudioGen） |

**评估与追踪：**
| 技能 | 功能说明 |
|------|---------|
| lm-evaluation-harness | 60+ 项基准测试（MMLU、HumanEval、GSM8K...） |
| weights-and-biases | 实验追踪、可视化、超参数搜索 |
| dspy | 声明式 AI 编程 — 自动优化 prompt、构建 RAG |
| huggingface-hub | HuggingFace CLI — 搜索、下载、上传模型/数据集 |

**云端：**
| 技能 | 功能说明 |
|------|---------|
| modal | ML 工作负载的无服务器 GPU 云平台 |

### 笔记
| 技能 | 功能说明 |
|------|---------|
| obsidian | 读取、搜索和创建 Obsidian 笔记 |

### 效率工具
文档、演示文稿、电子表格和工作流工具。

| 技能 | 功能说明 |
|------|---------|
| google-workspace | Gmail、日历、Drive、通讯录、Sheets、Docs 集成 |
| linear | 通过 GraphQL API 管理 Linear Issue、项目和团队 |
| nano-pdf | 使用自然语言指令编辑 PDF |
| notion | Notion API — 页面、数据库、块操作 |
| ocr-and-documents | 从 PDF、扫描文档、DOCX、PPTX 提取文本 |
| powerpoint | 创建、编辑、解析 .pptx 演示文稿 |

### 红队测试
| 技能 | 功能说明 |
|------|---------|
| godmode | LLM 越狱 — 33 种混淆技术、多模型竞速 |

### 科研
学术研究、市场数据、内容监控和知识管理。

| 技能 | 功能说明 |
|------|---------|
| arxiv | 从 arXiv 搜索和获取学术论文 |
| blogwatcher | 监控博客和 RSS/Atom 订阅源更新 |
| investment-analysis | 股票与基金投资分析 — 基本面/技术面/资产配置 |
| llm-wiki | 构建持久化的、相互链接的 Markdown 知识库 |
| polymarket | 查询 Polymarket 预测市场数据 |
| research-paper-writing | 端到端 ML/AI 论文撰写流水线 |

### 智能家居
| 技能 | 功能说明 |
|------|---------|
| openhue | 控制 Philips Hue 灯光、房间和场景 |

### 社交媒体
| 技能 | 功能说明 |
|------|---------|
| xitter | 通过 x-cli 操作 X/Twitter — 发帖、搜索、点赞、转推、收藏 |

### 软件开发
架构、模式、测试、调试和最佳实践。

| 技能 | 功能说明 |
|------|---------|
| api-design-patterns | API 设计最佳实践 — RESTful/GraphQL/gRPC |
| capacitor-h5-to-app | 将 H5 网页应用打包为原生 Android/iOS 应用 |
| common-development-patterns | 设计模式、并发处理、错误处理、安全防护、性能调优 |
| database-design-and-caching | 数据库设计、索引优化、Redis 缓存模式 |
| devops-cicd-containerization | Docker/K8s/CI/CD/GitOps/监控可观测性 |
| frontend-architecture | React/Next/Vue/Nuxt/Svelte 框架选型、渲染策略 |
| system-architecture-design | 单体 vs 微服务、DDD、高可用方案 |
| plan | 计划模式 — 撰写实施计划，不执行 |
| writing-plans | 创建包含任务拆分的完整实施计划 |
| test-driven-development | RED-GREEN-REFACTOR TDD 测试驱动开发 |
| systematic-debugging | 4 阶段根因调查方法论 |
| subagent-driven-development | 使用 delegate_task 并行执行任务 |
| requesting-code-review | 提交前验证流水线 |

### Inference.sh
| 技能 | 功能说明 |
|------|---------|
| infsh | 通过 inference.sh 运行 150+ AI 应用 — 图像、视频、LLM、搜索、3D |

---

## 安装

Skills 会从 `~/.hermes/skills/` 自动发现。添加方式：

```bash
# 克隆本仓库
git clone https://github.com/huidge/hermes-skills.git ~/.hermes/skills

# 或复制单个 skill
cp -r skills/software-development/tdd ~/.hermes/skills/software-development/
```

## 仓库结构

```
skills/
├── README.md
├── category/
│   ├── DESCRIPTION.md              # 分类描述
│   └── skill-name/
│       ├── SKILL.md                # 技能主文件（必需）
│       ├── references/             # 参考资料
│       ├── templates/              # 模板
│       └── scripts/                # 辅助脚本
```

## 同步

本仓库通过 cron job 每日自动同步。手动同步：

```bash
~/.hermes/sync-skills.sh
```

## 数据统计

- **26 个分类**
- **91+ 个技能**
- **覆盖领域**: 编程、ML/AI、创意、效率、科研、游戏、物联网等

## 许可证

各 skill 可能有独立许可证，详见各 SKILL.md 文件。
