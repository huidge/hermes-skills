# Recent Skills (Apr 12-16, 2026)

20 skills recently added to the [Hermes Skills Collection](https://github.com/huidge/hermes-skills).

[中文文档](README_CN.md) | English

---

## Skills

### Cron Reminder WeChat Limitation
> **Trigger**: When creating cron jobs targeting WeChat

WeChat cannot receive auto-delivered cron job output. This skill warns users upfront and suggests alternatives (Telegram, Discord, local-only). Load when the user wants to schedule tasks for WeChat delivery.

---

### Hermes Agent
> **Category**: Autonomous AI Agents | **Trigger**: Configuration, troubleshooting, extending Hermes

Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and contributor reference.

---

### Daily Market Report (每日A股报告)
> **Category**: Data Science | **Trigger**: A股、市场报告、收盘汇总

每日A股收盘交易汇总报告生成流程 — 数据采集、资金流向分析、板块热点分析、技术面与消息面综合分析。自动生成结构化的每日市场报告。

---

### Eastmoney Scraper (东方财富数据采集)
> **Category**: Data Science | **Trigger**: A股数据、基金排名、板块资金流

从东方财富内部 API 抓取 A 股市场数据、基金排名和板块资金流向。无需 API Key，直接通过 HTTP 请求获取实时数据。

---

### US Stock Daily Report (美股日报)
> **Category**: Data Science | **Trigger**: 美股、美股行情、收盘报告

每日美股收盘行情汇总 — 主要指数（道琼斯、纳斯达克、标普500）、板块轮动、个股亮点、宏观消息面、技术分析。

---

### Cron Job Troubleshooting (定时任务排查)
> **Category**: DevOps | **Trigger**: cron job 失败、定时任务错误、调度问题

Debug cron job execution failures — check job status, session logs, gateway errors, and model availability。4 步排查法：检查状态 → 查看日志 → 验证网关 → 测试模型。

---

### Investment Analysis (投资分析)
> **Category**: Research | **Trigger**: 股票分析、基金投资、资产配置

股票与基金投资分析完整方法论 — 基本面分析（财报、估值）、技术分析（K线、指标）、板块轮动、市场情绪、基金定投策略、资产配置与风险管理。

---

### API Design Patterns (API 设计模式)
> **Category**: Software Development | **Trigger**: API 设计、RESTful、GraphQL、gRPC

API 设计最佳实践指南 — RESTful / GraphQL / gRPC 选型对比、统一错误处理、认证授权方案（JWT/OAuth2）、版本控制策略、限流与分页设计。

---

### Capacitor H5 to App (H5 转原生应用)
> **Category**: Software Development | **Trigger**: H5 打包、Web 转 App、Capacitor

将任意 H5 网页应用打包为原生 Android/iOS 应用。流程：下载静态资源 → Capacitor 项目搭建 → HTTP 明文后端配置 → 网络安全策略 → GitHub Actions 自动构建 → 资源更新脚本。

---

### Common Development Patterns (通用开发模式)
> **Category**: Software Development | **Trigger**: 设计模式、并发、错误处理、代码审查

常见开发模式与问题解决 — 设计模式（单例、工厂、观察者等）、并发处理（锁、协程、线程池）、错误处理策略、安全防护清单、代码审查要点、性能调优方法论。

---

### Database Design and Caching (数据库与缓存)
> **Category**: Software Development | **Trigger**: 数据库设计、缓存、Redis、Schema

数据库设计与缓存策略 — 关系型/NoSQL 选型指南、Schema 设计范式（1NF-BCNF）、索引优化策略、Redis 缓存模式（穿透/击穿/雪崩）、数据一致性方案。

---

### DevOps CI/CD & Containerization (DevOps 实践)
> **Category**: Software Development | **Trigger**: Docker、K8s、CI/CD、GitOps

DevOps 全链路实践 — Docker 容器化最佳实践、Kubernetes 编排（Deployment/Service/Ingress）、CI/CD 流水线设计（GitHub Actions/GitLab CI）、GitOps 工作流、监控与可观测性（Prometheus/Grafana）、基础设施即代码（Terraform）。

---

### Frontend Architecture (前端架构)
> **Category**: Software Development | **Trigger**: React、Vue、Next.js、前端框架选型

前端架构设计指南 — 框架选型对比（React/Next/Vue/Nuxt/Svelte）、渲染策略（SSR/SSG/ISR/CSR）、状态管理方案、组件设计原则、性能优化策略（代码分割、懒加载、缓存）。

---

### System Architecture Design (系统架构设计)
> **Category**: Software Development | **Trigger**: 架构设计、微服务、DDD

系统架构设计指南 — 单体 vs 微服务选型、分层架构、领域驱动设计（DDD：实体/值对象/聚合根/领域事件）、高可用方案（负载均衡/熔断/降容）、高扩展方案选型。

---

### Plan Mode (计划模式)
> **Category**: Software Development | **Trigger**: 先做计划再执行、plan mode

Hermes 计划模式 — 在执行前先审查上下文，将实施计划写入工作区的 `.hermes/plans/` 目录。不执行任何工作，仅输出计划供确认。

---

### Requesting Code Review (代码审查请求)
> **Category**: Software Development | **Trigger**: 提交前检查、代码审查、pre-commit

Pre-commit 验证流水线 — 静态安全扫描（依赖漏洞、密钥泄漏）、代码质量检查（lint、格式化）、测试覆盖率验证、变更影响分析。提交前自动运行。

---

### Subagent-Driven Development (子代理驱动开发)
> **Category**: Software Development | **Trigger**: 并行开发、多任务分发、delegate_task

执行实施计划时的并行任务策略 — 为每个独立任务派发 delegate_task 子代理，两阶段审查（规范合规性 + 代码质量），适合大型功能的拆分开发。

---

### Systematic Debugging (系统化调试)
> **Category**: Software Development | **Trigger**: Bug 排查、测试失败、异常行为

4 阶段根因调查方法论 — 收集信息（复现、日志、环境）→ 形成假设 → 验证假设（最小化复现）→ 定位根因。核心原则：不理解问题前不做修复。

---

### Test-Driven Development (测试驱动开发)
> **Category**: Software Development | **Trigger**: TDD、先写测试、test first

强制执行 RED-GREEN-REFACTOR 循环 — 先写失败的测试（RED），再写最小实现使测试通过（GREEN），最后重构优化。适用于任何功能开发或 bug 修复。

---

### Writing Plans (撰写实施计划)
> **Category**: Software Development | **Trigger**: 需求分析、任务拆分、实施计划

为多步骤任务创建完整的实施计划 — 拆分为可执行的小任务、指定精确文件路径、包含完整代码示例。适合复杂功能的前期规划。

---

## Installation

```bash
# Clone full collection
git clone https://github.com/huidge/hermes-skills.git ~/.hermes/skills

# Or checkout only recent skills
git clone -b recent-skills https://github.com/huidge/hermes-skills.git ~/.hermes/skills
```

## License

Individual skills may have their own licenses. See each SKILL.md for details.
