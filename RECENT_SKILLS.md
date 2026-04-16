# Recent Skills (Apr 12-16, 2026)

This branch tracks the most recently created/updated skills.

## Skills List (20 total)

### Apr 16
- `devops/cron-job-troubleshooting` — Debug cron job execution failures

### Apr 15
- `data-science/us-stock-daily-report` — 每日美股收盘行情汇总
- `data-science/daily-market-report` — 每日A股收盘交易汇总报告生成流程
- `software-development/capacitor-h5-to-app` — Package H5 web app into native Android/iOS app

### Apr 14
- `software-development/common-development-patterns` — 常见开发模式与问题解决
- `software-development/devops-cicd-containerization` — DevOps 实践 — Docker/K8s/CI/CD
- `software-development/frontend-architecture` — 前端架构设计 — 框架选型/渲染策略
- `software-development/database-design-and-caching` — 数据库设计与缓存策略
- `software-development/api-design-patterns` — API 设计最佳实践
- `software-development/system-architecture-design` — 系统架构设计指南
- `research/investment-analysis` — 股票与基金投资分析技能

### Apr 13
- `data-science/eastmoney-scraper` — Scrape A-share market data

### Apr 12
- `cron-reminder-wechat-limitation` — WeChat cron job auto-delivery limitation
- `autonomous-ai-agents/hermes-agent` — Complete guide to using Hermes Agent
- `software-development/writing-plans` — Plan mode for multi-step implementation
- `software-development/test-driven-development` — TDD workflow
- `software-development/systematic-debugging` — Systematic debugging methodology
- `software-development/subagent-driven-development` — Subagent-driven development
- `software-development/requesting-code-review` — Pre-commit verification pipeline
- `software-development/plan` — Plan mode for Hermes

## Quick View

```bash
# List all recent skills
ls -d */*/SKILL.md | while read f; do dir=$(dirname "$f"); cat RECENT_SKILLS.md | grep -q "$dir" && echo "$dir"; done
```
