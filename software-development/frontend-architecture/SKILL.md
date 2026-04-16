---
name: frontend-architecture
description: 前端架构设计 — 框架选型(React/Next/Vue/Nuxt/Svelte)、渲染策略(SSR/SSG/ISR/CSR)、状态管理、组件设计、性能优化
category: software-development
---

# 前端架构设计指南

## 触发条件
当用户需要：选择前端框架、设计组件架构、选渲染策略、做状态管理方案、优化前端性能、解决 SEO/首屏加载问题时使用。

## 一、框架选型 (2025-2026)

### 主流全栈框架对比

| 维度 | Next.js (React) | Nuxt (Vue) | SvelteKit | Remix |
|------|----------------|------------|-----------|-------|
| 底层库 | React | Vue 3 | Svelte | React |
| 构建工具 | Turbopack | Vite | Vite | Vite |
| 渲染模式 | SSR/SSG/ISR/CSR/PPR | SSR/SSG/ISR/CSR | SSR/SSG/CSR | SSR (嵌套路由) |
| 包体积 | 中等 | 中等 | 最小 | 中等 |
| 学习曲线 | 中 | 低 | 低 | 中 |
| 生态 | 最大 | 大 | 成长中 | 成长中 |
| 适用 | 企业应用/电商/SEO | 快速原型/中型项目 | 性能敏感/小项目 | 复杂交互表单 |

### 选型决策
```
团队熟悉 React → Next.js (生态最强，Vercel 支持)
团队熟悉 Vue → Nuxt (约定优于配置，开发快)
追求极致性能/小包 → SvelteKit (编译时优化)
复杂表单/数据变更密集 → Remix (Web Standards)
渐进式增强/简单页面 → HTMX + 服务端模板
```

## 二、渲染策略详解

### CSR / SSR / SSG / ISR / PPR

```
CSR (Client-Side Rendering):
  构建时 → 生成空 HTML + JS Bundle
  浏览器 → 下载 JS → 执行 → 渲染页面
  适合: 后台管理/工具类应用 (不需 SEO)

SSR (Server-Side Rendering):
  每次请求 → 服务端生成完整 HTML
  首屏快 (FCP 好), SEO 友好
  适合: 电商详情页/新闻 (内容频繁变化)

SSG (Static Site Generation):
  构建时 → 生成所有页面的静态 HTML
  最快 (CDN 缓存), 最省服务器
  适合: 博客/文档/落地页 (内容不常变)

ISR (Incremental Static Regeneration):
  SSG + 按需重新生成
  revalidate: 60 → 60秒后后台重新生成
  适合: 大量页面 + 偶尔更新 (电商商品列表)

PPR (Partial Prerendering, Next.js 14+):
  静态外壳 + 动态 Streaming 洞
  结合 SSG 速度 + SSR 灵活性
  适合: 混合静态/动态内容
```

### 选择公式
```
SEO 需求 + 数据实时性 → SSR
SEO 需求 + 数据稳定   → SSG/ISR
不需要 SEO           → CSR
大量页面 + 部分动态   → PPR
```

## 三、状态管理

### 按作用域分类

```
组件内状态:     useState / ref() / $state()
跨组件状态:     Context / provide/inject / Context API
全局客户端状态:  Zustand / Pinia / Svelte Store / Jotai
服务端状态:     TanStack Query / SWR / Apollo Client
URL 状态:       nuqs / useSearchParams / URL Sync
表单状态:       React Hook Form / TanStack Form / VeeValidate
```

### 服务端状态管理 (推荐优先使用)

```typescript
// TanStack Query (React) — 推荐
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

function Users() {
  const queryClient = useQueryClient()
  
  // 自动缓存、重试、后台刷新、去重
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 5 * 60 * 1000,  // 5分钟内不重新请求
  })

  const mutation = useMutation({
    mutationFn: (newUser) => fetch('/api/users', {
      method: 'POST', body: JSON.stringify(newUser)
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  if (isLoading) return <Skeleton />
  if (error) return <ErrorBoundary error={error} />

  return <UserList users={data} onCreate={mutation.mutate} />
}
```

### 全局状态选型

| 场景 | 推荐 | 理由 |
|------|------|------|
| 简单共享状态 | Zustand | 最简 API，无 Provider，~1KB |
| 复杂状态逻辑 | Redux Toolkit | 最佳 DevTools，可预测 |
| Vue 项目 | Pinia | Vue 官方推荐，TypeScript 友好 |
| 原子化状态 | Jotai / Recoil | 按需订阅，性能最优 |
| 服务端数据 | TanStack Query / SWR | 缓存/重试/乐观更新 |

## 四、组件设计模式

### 1. 容器/展示组件 (Container/Presentational)
```tsx
// Container: 获取数据, 处理逻辑
function UserListContainer() {
  const { data, isLoading } = useQuery(['users'], fetchUsers)
  const deleteUser = useMutation(deleteUserFn)
  
  if (isLoading) return <Spinner />
  return <UserList users={data} onDelete={deleteUser.mutate} />
}

// Presentational: 纯 UI, 通过 props 接收数据
function UserList({ users, onDelete }) {
  return (
    <ul>
      {users.map(u => <UserCard key={u.id} user={u} onDelete={onDelete} />)}
    </ul>
  )
}
```

### 2. 组合模式 (Compound Components)
```tsx
// <Select>
//   <Select.Trigger />
//   <Select.Content>
//     <Select.Item value="1">Option 1</Select.Item>
//   </Select.Content>
// </Select>
```

### 3. Headless UI (逻辑与样式分离)
```tsx
// 使用 Radix / Headless UI / React Aria
// 只提供行为和无障碍，样式完全自定义
import * as DropdownMenu from '@radix-ui/react-dropdown-menu'
```

### 4. Server Components (Next.js App Router)
```tsx
// Server Component (默认) — 可直接访问数据库/API
async function UserList() {
  const users = await db.users.findMany()  // 无 API 层
  return <UserTable users={users} />       // 零 JS 发送到客户端
}

// Client Component — 需要交互
'use client'
function LikeButton({ initialCount }) {
  const [count, setCount] = useState(initialCount)
  return <button onClick={() => setCount(c => c + 1)}>👍 {count}</button>
}
```

## 五、性能优化

### 核心指标
```
LCP (Largest Contentful Paint) < 2.5s  → 最大内容渲染
FID (First Input Delay) < 100ms       → 首次输入延迟 → 已被 INP 取代
INP (Interaction to Next Paint) < 200ms → 交互响应
CLS (Cumulative Layout Shift) < 0.1    → 布局偏移
FCP (First Contentful Paint) < 1.8s   → 首次内容渲染
TTFB (Time to First Byte) < 800ms     → 首字节时间
```

### 优化手段

```
# 1. 代码分割 & 懒加载
const HeavyComponent = lazy(() => import('./HeavyComponent'))

# 2. 图片优化
<Image
  src="/hero.jpg"
  width={800}
  height={400}
  loading="lazy"          // 非首屏图片延迟加载
  placeholder="blur"      // 模糊占位
  sizes="(max-width: 768px) 100vw, 50vw"
  format="webp"           // 现代格式
/>

# 3. 字体优化
- 使用 font-display: swap
- 子集化 (只包含需要的字符)
- preload 关键字体

# 4. 资源提示
<link rel="preload" href="/critical.css" as="style" />
<link rel="prefetch" href="/next-page.js" />
<link rel="preconnect" href="https://api.example.com" />

# 5. Bundle 分析
npx @next/bundle-analyzer  // 找出大依赖
npm install --save-dev webpack-bundle-analyzer

# 6. Tree Shaking
- 使用 ESM (import/export)
- 避免 import * as xxx
- 检查 sideEffects 字段

# 7. 缓存策略
Cache-Control: public, max-age=31536000, immutable  // 带 hash 的静态资源
Cache-Control: public, max-age=0, must-revalidate    // HTML 页面

# 8. Streaming & Suspense
<Suspense fallback={<Skeleton />}>
  <AsyncComponent />
</Suspense>
```

## 六、项目结构推荐

```
src/
├── app/                    # Next.js App Router / 文件路由
│   ├── (marketing)/        # 路由组
│   │   ├── page.tsx
│   │   └── pricing/
│   ├── (app)/
│   │   ├── dashboard/
│   │   └── settings/
│   ├── api/                # API Routes
│   ├── layout.tsx          # 根布局
│   └── globals.css
├── components/
│   ├── ui/                 # 基础 UI 组件 (Button, Input, Card)
│   ├── forms/              # 表单组件
│   └── features/           # 功能模块组件
│       ├── users/
│       └── orders/
├── lib/
│   ├── api.ts              # API 客户端
│   ├── auth.ts             # 认证工具
│   ├── db.ts               # 数据库客户端
│   └── utils.ts            # 通用工具函数
├── hooks/                  # 自定义 hooks
├── stores/                 # 状态管理
├── types/                  # TypeScript 类型定义
├── styles/                 # 样式 (如果不用 CSS Modules)
└── config/                 # 配置文件
```

## 七、CSS 方案选型

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|---------|
| Tailwind CSS | 快速开发, 一致性强 | HTML 致癌, 学习成本 | 大多数项目首选 |
| CSS Modules | 作用域隔离, 原生 | 组合不便 | 中型项目 |
| CSS-in-JS (styled) | 动态样式, 组件化 | 运行时开销 | React 组件库 |
| Vanilla Extract | 零运行时, 类型安全 | 配置复杂 | 性能敏感项目 |
| UnoCSS | 极快, 可定制 | 较新 | 追求极致性能 |

## 八、测试策略

```
单元测试:     Vitest / Jest — 工具函数、纯逻辑
组件测试:     Testing Library — 组件交互
E2E 测试:     Playwright / Cypress — 关键用户流程
视觉回归:     Chromatic / Percy — UI 截图对比
类型检查:     TypeScript — 编译时错误捕获

测试金字塔:
  E2E (10%) — 关键路径
  集成 (20%) — 组件 + API
  单元 (70%) — 纯函数、逻辑
```

## 九、安全清单

- [ ] XSS 防护: React 默认转义, dangerouslySetInnerHTML 审查
- [ ] CSRF: SameSite Cookie + Token
- [ ] CSP Header: 限制脚本来源
- [ ] 环境变量: NEXT_PUBLIC_ 前缀才会暴露到客户端
- [ ] 依赖审计: npm audit / Snyk
- [ ] 输入验证: zod / yup (客户端 + 服务端双重验证)
- [ ] 敏感数据不进 URL / localStorage
