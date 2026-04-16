# Recent Skills — 最新技能 (2026年4月12-16日)

[Hermes Skills Collection](https://github.com/huidge/hermes-skills) 最近新增的 **20 个技能**。

中文版 | [English](README.md)

---

## 技能列表

### Cron Reminder WeChat Limitation (微信定时任务限制)
> **分类**: 根目录 | **触发词**: 微信定时任务、WeChat cron job

微信无法接收 cron job 自动投递的输出。本技能在用户创建微信定时任务时提前预警，并建议替代方案（Telegram、Discord、仅本地保存）。

---

### Hermes Agent (Hermes 完整指南)
> **分类**: 自主 AI 代理 | **触发词**: 配置 Hermes、故障排查、扩展

Hermes Agent 完整使用与扩展指南 — CLI 用法、安装配置、多代理启动、网关平台、技能开发、语音工具、个人配置和贡献者参考。

---

### Daily Market Report (每日A股报告)
> **分类**: 数据科学 | **触发词**: A股、市场报告、收盘汇总

每日A股收盘交易汇总报告生成流程 — 数据采集、资金流向分析、板块热点分析、技术面与消息面综合分析。自动生成结构化的每日市场报告。

---

### Eastmoney Scraper (东方财富数据采集)
> **分类**: 数据科学 | **触发词**: A股数据、基金排名、板块资金流

从东方财富内部 API 抓取 A 股市场数据、基金排名和板块资金流向。无需 API Key，直接通过 HTTP 请求获取实时数据。

---

### US Stock Daily Report (美股日报)
> **分类**: 数据科学 | **触发词**: 美股、美股行情、收盘报告

每日美股收盘行情汇总 — 主要指数（道琼斯、纳斯达克、标普500）、板块轮动、个股亮点、宏观消息面、技术分析。

---

### Cron Job Troubleshooting (定时任务排查)
> **分类**: DevOps | **触发词**: cron job 失败、定时任务错误、调度问题

定时任务执行失败排查指南 — 检查任务状态 → 查看会话日志 → 验证网关错误 → 测试模型可用性。4 步定位问题根因。

---

### Investment Analysis (投资分析)
> **分类**: 科研 | **触发词**: 股票分析、基金投资、资产配置

股票与基金投资分析完整方法论 — 基本面分析（财报、估值）、技术分析（K线、指标）、板块轮动、市场情绪、基金定投策略、资产配置与风险管理。

---

### API Design Patterns (API 设计模式)
> **分类**: 软件开发 | **触发词**: API 设计、RESTful、GraphQL、gRPC

API 设计最佳实践指南：
- **选型对比**: RESTful vs GraphQL vs gRPC 适用场景
- **错误处理**: 统一错误码、HTTP 状态码规范
- **认证授权**: JWT / OAuth2 / API Key 方案选型
- **版本控制**: URL 路径 vs Header vs 参数方案
- **限流分页**: 令牌桶、滑动窗口、游标分页

---

### Capacitor H5 to App (H5 转原生应用)
> **分类**: 软件开发 | **触发词**: H5 打包、Web 转 App、Capacitor

将任意 H5 网页应用打包为原生 Android/iOS 应用：
1. 下载 H5 静态资源
2. Capacitor 项目搭建
3. HTTP 明文后端配置（network_security_config.xml）
4. GitHub Actions 自动构建
5. 资源热更新脚本

---

### Common Development Patterns (通用开发模式)
> **分类**: 软件开发 | **触发词**: 设计模式、并发、错误处理、代码审查

常见开发模式与问题解决百科：
- **设计模式**: 单例、工厂、观察者、策略、装饰器...
- **并发处理**: 锁机制、协程、线程池、异步模式
- **错误处理**: 异常层级、重试策略、熔断降级
- **安全防护**: SQL注入/XSS/CSRF 防护清单
- **性能调优**: 数据库优化、缓存策略、CDN、懒加载

---

### Database Design and Caching (数据库与缓存)
> **分类**: 软件开发 | **触发词**: 数据库设计、缓存、Redis、Schema

数据库设计与缓存策略：
- **选型指南**: 关系型 (MySQL/PostgreSQL) vs NoSQL (MongoDB/Redis)
- **Schema 范式**: 1NF → BCNF 设计原则
- **索引优化**: B+树、覆盖索引、联合索引、最左匹配
- **Redis 缓存**: 穿透/击穿/雪崩三板斧、缓存更新策略
- **一致性方案**: Cache-Aside / Write-Through / Write-Behind

---

### DevOps CI/CD & Containerization (DevOps 实践)
> **分类**: 软件开发 | **触发词**: Docker、K8s、CI/CD、GitOps

DevOps 全链路实践指南：
- **容器化**: Dockerfile 最佳实践、多阶段构建、镜像优化
- **编排**: Kubernetes Deployment/Service/Ingress/ConfigMap
- **CI/CD**: GitHub Actions / GitLab CI 流水线设计
- **GitOps**: ArgoCD / Flux 声明式部署
- **监控**: Prometheus + Grafana + AlertManager
- **IaC**: Terraform / Pulumi 基础设施即代码

---

### Frontend Architecture (前端架构)
> **分类**: 软件开发 | **触发词**: React、Vue、Next.js、前端框架选型

前端架构设计指南：
- **框架选型**: React vs Next.js vs Vue vs Nuxt vs Svelte 对比
- **渲染策略**: SSR / SSG / ISR / CSR 适用场景
- **状态管理**: Redux / Zustand / Pinia / Jotai 选型
- **组件设计**: 原子设计、组合模式、受控 vs 非受控
- **性能优化**: 代码分割、Tree Shaking、图片懒加载、Web Vitals

---

### System Architecture Design (系统架构设计)
> **分类**: 软件开发 | **触发词**: 架构设计、微服务、DDD

系统架构设计指南：
- **单体 vs 微服务**: 适用场景、演进路径、拆分策略
- **分层架构**: 四层架构 / 六边形架构 / CQRS
- **领域驱动设计**: 实体、值对象、聚合根、领域事件、限界上下文
- **高可用**: 负载均衡、熔断器、降级策略、多活架构
- **高扩展**: 水平扩展、读写分离、分库分表、消息队列

---

### Plan Mode (计划模式)
> **分类**: 软件开发 | **触发词**: 先做计划再执行、plan mode

Hermes 计划模式 — 在执行任何工作之前，先审查上下文，将实施计划写入 `.hermes/plans/` 目录。仅输出计划供用户确认，不执行任何操作。

---

### Requesting Code Review (代码审查请求)
> **分类**: 软件开发 | **触发词**: 提交前检查、代码审查、pre-commit

Pre-commit 验证流水线：
1. **安全扫描**: 依赖漏洞检测、密钥/Token 泄漏检查
2. **代码质量**: Lint 检查、格式化验证、复杂度分析
3. **测试覆盖**: 单元测试 + 集成测试通过率
4. **变更分析**: 影响范围评估、破坏性变更检测

---

### Subagent-Driven Development (子代理驱动开发)
> **分类**: 软件开发 | **触发词**: 并行开发、多任务分发、delegate_task

大型功能的并行开发策略 — 将实施计划拆分为独立任务，为每个任务派发 delegate_task 子代理并行执行。两阶段审查：先检查规范合规性，再审查代码质量。

---

### Systematic Debugging (系统化调试)
> **分类**: 软件开发 | **触发词**: Bug 排查、测试失败、异常行为

4 阶段根因调查方法论：
1. **收集信息**: 复现步骤、错误日志、环境信息
2. **形成假设**: 基于症状推断可能原因
3. **验证假设**: 最小化复现、二分排查
4. **定位根因**: 确认根本原因，再设计修复方案

核心原则：不理解问题前不做修复。

---

### Test-Driven Development (测试驱动开发)
> **分类**: 软件开发 | **触发词**: TDD、先写测试、test first

强制执行 RED-GREEN-REFACTOR 循环：
- **RED**: 先写一个失败的测试，明确期望行为
- **GREEN**: 写最小代码使测试通过，不追求完美
- **REFACTOR**: 在测试保护下优化代码结构

适用于任何功能开发或 bug 修复。

---

### Writing Plans (撰写实施计划)
> **分类**: 软件开发 | **触发词**: 需求分析、任务拆分、实施计划

为多步骤任务创建完整的实施计划 — 拆分为可执行的小任务、指定精确文件路径、包含完整代码示例。适合复杂功能的前期规划和大型重构。

---

## 安装

```bash
# 克隆完整集合（91+ skills）
git clone https://github.com/huidge/hermes-skills.git ~/.hermes/skills

# 或仅克隆最新技能分支
git clone -b recent-skills https://github.com/huidge/hermes-skills.git ~/.hermes/skills
```

## 许可证

各 skill 可能有独立许可证，详见各 SKILL.md 文件。
