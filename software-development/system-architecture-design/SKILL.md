---
name: system-architecture-design
description: 系统架构设计指南 — 单体 vs 微服务、分层架构、领域驱动设计(DDD)、高可用/高扩展方案选型
category: software-development
---

# 系统架构设计指南

## 触发条件
当用户需要：设计新系统架构、评估现有架构、做技术选型决策、讨论微服务拆分、解决扩展性/可用性问题时使用。

## 一、架构风格选型决策树

### 1. 单体 vs 微服务 vs 模块化单体

| 维度 | 单体 Monolith | 模块化单体 Modular Monolith | 微服务 Microservices |
|------|--------------|---------------------------|---------------------|
| 适用阶段 | MVP / 小团队 (<10人) | 成长期 / 中型团队 | 大规模 / 多团队 (>50人) |
| 部署复杂度 | 低 | 中 | 高 (需 K8s/服务网格) |
| 数据一致性 | 简单 (ACID) | 简单 (ACID) | 复杂 (Saga/Eventual) |
| 技术栈 | 统一 | 统一但可隔离 | 每服务独立 |
| 运维成本 | 低 | 中 | 高 |
| 扩展方式 | 整体水平扩展 | 按模块拆分扩展 | 每服务独立扩展 |

**决策建议**：
- 新项目 → 从模块化单体开始，明确边界但保持部署简单
- 只有当：团队>50人、需要独立部署、技术栈异构 → 才考虑微服务
- Amazon/Netflix 的经验：先单体后微服务，渐进迁移

### 2. 分层架构 (Layered Architecture)

```
┌─────────────────────────────────────┐
│        Presentation Layer           │  ← API Controllers / Views
├─────────────────────────────────────┤
│        Application Layer            │  ← Use Cases / Service Orchestration
├─────────────────────────────────────┤
│        Domain Layer                 │  ← Business Logic / Entities / Value Objects
├─────────────────────────────────────┤
│        Infrastructure Layer         │  ← DB / Cache / MQ / External APIs
└─────────────────────────────────────┘
```

**核心原则**：
- 依赖方向：Presentation → Application → Domain ← Infrastructure
- Domain 层不依赖任何外部层 (依赖反转 DIP)
- Application 层编排用例，不包含业务逻辑
- Infrastructure 实现 Domain 定义的接口

## 二、领域驱动设计 (DDD) 核心模式

### 1. 战略设计
- **Bounded Context (限界上下文)**: 划分微服务边界的依据
- **Ubiquitous Language (通用语言)**: 团队和代码使用统一术语
- **Context Map**: 描述上下文间的关系 (ACL, OHS, PL, etc.)

### 2. 战术设计
```
Aggregate (聚合根)
├── Entity (实体，有唯一标识)
├── Value Object (值对象，不可变，按值比较)
├── Domain Event (领域事件)
└── Repository (仓储，持久化抽象)
```

### 3. 常见聚合模式
- **订单聚合**: Order → OrderItems, Payments, Shipping
- **用户聚合**: User → Profile, Preferences, Permissions
- **产品聚合**: Product → SKU, Pricing, Inventory

## 三、高可用 & 高扩展设计

### 1. 可用性等级 (SLA)
| SLA | 年停机时间 | 实现方式 |
|-----|-----------|---------|
| 99.9% | 8.76h | 负载均衡 + 健康检查 |
| 99.95% | 4.38h | 多可用区部署 |
| 99.99% | 52.6min | 多区域 + 自动故障转移 |
| 99.999% | 5.26min | 全冗余 + 混沌工程 |

### 2. 扩展模式
```
垂直扩展 (Scale Up)    → 加 CPU/内存，简单但有上限
水平扩展 (Scale Out)   → 加机器，需无状态设计
读写分离               → 主库写，从库读
分库分表 (Sharding)    → 按用户ID/地域/时间拆分
CQRS                   → 命令和查询分离，独立优化
```

### 3. 容错模式
- **Circuit Breaker (熔断器)**: 连续失败后断开，防止雪崩
- **Retry with Backoff**: 指数退避重试 + 抖动
- **Bulkhead (隔舱)**: 资源隔离，一个故障不影响其他
- **Rate Limiting**: 令牌桶/滑动窗口限流
- **Graceful Degradation**: 降级策略，核心功能优先

## 四、技术选型矩阵

### 后端框架选型
| 场景 | 推荐 | 理由 |
|------|------|------|
| 高并发 API / 实时应用 | Node.js (NestJS / Express) | 事件驱动，非阻塞 I/O，高并发性能好 |
| AI/ML 集成 / 数据处理 | Python (FastAPI) | 原生 Python 生态，自动 OpenAPI 文档 |
| 企业级 / 复杂业务 | Java (Spring Boot) / C# (.NET) | 成熟生态，强类型，事务管理 |
| 高性能微服务 | Go (Gin / Fiber) | 编译型，低内存占用，goroutine 并发 |
| 全栈 TypeScript | NestJS | Angular 风格架构，支持 REST/gRPC/WS |

### 前端框架选型
| 场景 | 推荐 | 理由 |
|------|------|------|
| 企业 SPA / 丰富生态 | React (Next.js) | 最大社区，组件库丰富，SSR/SSG/ISR |
| 快速原型 / 渐进式 | Vue (Nuxt) | 学习曲线低，约定优于配置，Vite 构建快 |
| 极致性能 / 小包 | Svelte (SvelteKit) | 编译时优化，无虚拟 DOM，包体积小 |
| 传统 MPA / 强交互 | HTMX + 服务端渲染 | 简单，无需构建步骤，SEO 友好 |

## 五、架构决策记录 (ADR) 模板

```markdown
# ADR-NNN: [决策标题]

## 状态: [提议 | 已接受 | 已弃用 | 已取代]

## 背景
[描述驱动决策的上下文和问题]

## 决策
[描述做出的具体决策]

## 后果
### 正面
- [优点1]
### 负面
- [缺点/风险1]
### 中性
- [需要关注的方面]
```

## 六、常见反模式 (避免)

1. **分布式单体**: 拆了服务但部署耦合，最差情况
2. **过早优化**: MVP 阶段就用微服务，增加不必要的复杂度
3. **上帝对象**: 一个类/服务承担过多职责
4. **紧耦合**: 服务间直接调用而非通过事件/消息
5. **忽略数据一致性**: 微服务间共享数据库
6. **缺少监控**: 没有可观测性 (logging/tracing/metrics) 就上分布式

## 七、实战分析流程

### 步骤 1: 需求分析
- 功能需求 vs 非功能需求 (性能/可用性/安全)
- 预估 QPS / DAU / 数据量
- 明确约束条件 (团队/预算/时间)

### 步骤 2: 领域建模
- 识别核心领域、支撑领域、通用领域
- 划分 Bounded Context
- 定义聚合根和实体关系

### 步骤 3: 架构选型
- 单体 vs 微服务 (根据团队规模和复杂度)
- 选择技术栈 (根据团队技能和场景)
- 确定数据存储策略

### 步骤 4: 详细设计
- API 设计 (RESTful / GraphQL)
- 数据库 schema 设计
- 缓存策略 (Cache-Aside / Write-Through)
- 消息队列选型 (Kafka / RabbitMQ / Redis Streams)

### 步骤 5: 可靠性设计
- 容错和降级方案
- 监控告警方案
- CI/CD 流水线设计
- 灾备和恢复方案

## 八、热门架构趋势 (2025-2026)

1. **Modular Monolith 回归**: 避免微服务复杂度，保持模块化清晰边界
2. **Edge Computing**: 边缘计算，降低延迟 (Cloudflare Workers, Deno Deploy)
3. **Serverless + Event-Driven**: FaaS + 事件驱动架构
4. **AI-First Architecture**: LLM 推理服务作为核心组件
5. **Platform Engineering**: 内部开发者平台 (IDP)，降低认知负担
6. **GitOps**: 基础设施和部署声明式管理 (ArgoCD / Flux)
