---
name: api-design-patterns
description: API 设计最佳实践 — RESTful / GraphQL / gRPC 选型、错误处理、认证授权、版本控制、限流分页
category: software-development
---

# API 设计最佳实践

## 触发条件
当用户需要：设计 API 接口、选择 API 风格、处理错误码、实现认证/授权、做 API 版本管理、设计分页/限流时使用。

## 一、API 风格选型

| 维度 | REST | GraphQL | gRPC |
|------|------|---------|------|
| 数据获取 | 多端点，固定结构 | 单端点，按需查询 | 强类型 Protobuf |
| 性能 | 缓存友好 | 避免 over/under-fetching | 最高性能 (HTTP/2) |
| 实时 | 需 WebSocket/SSE | Subscription | 双向流 |
| 学习曲线 | 低 | 中 | 高 |
| 适用场景 | 公共 API / CRUD | 复杂前端 / 多端 | 内部微服务通信 |
| 工具链 | OpenAPI/Swagger | Apollo/Relay | buf/protoc |

### 选型建议
- **面向外部开发者** → REST (最广泛支持，缓存友好)
- **前端需求多变** → GraphQL (前端自取所需)
- **微服务间通信** → gRPC (高性能，强类型)
- **混合方案**: REST 作为公共 API + gRPC 内部通信 + GraphQL BFF 层

## 二、RESTful API 设计规范

### 1. URL 设计
```
# 资源命名: 名词复数，kebab-case
GET    /api/v1/users              # 列表
GET    /api/v1/users/{id}         # 详情
POST   /api/v1/users              # 创建
PUT    /api/v1/users/{id}         # 全量更新
PATCH  /api/v1/users/{id}         # 部分更新
DELETE /api/v1/users/{id}         # 删除

# 嵌套资源 (最多2层)
GET    /api/v1/users/{id}/orders
GET    /api/v1/users/{id}/orders/{orderId}

# 操作型端点 (非 CRUD)
POST   /api/v1/users/{id}/activate
POST   /api/v1/orders/{id}/cancel
```

### 2. HTTP 状态码标准
```
200 OK               → GET/PUT/PATCH 成功
201 Created          → POST 创建成功
204 No Content       → DELETE 成功
400 Bad Request      → 参数校验失败
401 Unauthorized     → 未认证
403 Forbidden        → 无权限
404 Not Found        → 资源不存在
409 Conflict         → 资源冲突 (重复创建)
422 Unprocessable    → 业务规则校验失败
429 Too Many Requests → 限流
500 Internal Error   → 服务端错误
502 Bad Gateway      → 上游服务故障
503 Service Unavailable → 服务不可用
```

### 3. 错误响应格式 (RFC 7807 Problem Details)
```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The 'email' field must be a valid email address",
  "instance": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "message": "必须是有效的邮箱地址",
      "code": "INVALID_EMAIL_FORMAT"
    }
  ],
  "traceId": "abc-123-def-456"
}
```

### 4. 分页设计
```json
// Cursor-based (推荐，适合大数据集)
GET /api/v1/users?cursor=eyJpZCI6MTAwfQ&limit=20

{
  "data": [...],
  "pagination": {
    "hasNext": true,
    "nextCursor": "eyJpZCI6MTIwfQ",
    "prevCursor": "eyJpZCI6ODB9",
    "limit": 20
  }
}

// Offset-based (适合小数据集/后台管理)
GET /api/v1/users?page=2&per_page=20

{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total": 500,
    "total_pages": 25
  }
}
```

### 5. 过滤、排序、字段选择
```
# 过滤
GET /api/v1/users?status=active&role=admin&created_after=2025-01-01

# 排序
GET /api/v1/users?sort=-created_at,name    # - 前缀表示降序

# 字段选择 (减少传输)
GET /api/v1/users?fields=id,name,email

# 搜索
GET /api/v1/users?q=john&search_fields=name,email
```

## 三、认证与授权

### 1. 认证方案对比
| 方案 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| JWT | SPA / 移动端 / 微服务 | 无状态，自包含 | 无法主动失效，体积大 |
| Session + Cookie | 传统 Web | 服务端可控，安全性好 | 需共享 Session 存储 |
| OAuth 2.0 + OIDC | 第三方登录 / SSO | 标准化，生态好 | 实现复杂 |
| API Key | 内部服务 / 简单集成 | 简单 | 粒度粗，无法携带用户信息 |

### 2. JWT 最佳实践
```
Header: Authorization: Bearer <token>

Payload Claims:
{
  "sub": "user-id-123",        // Subject
  "iss": "auth.example.com",   // Issuer
  "aud": "api.example.com",    // Audience
  "exp": 1735689600,           // Expiration (短期: 15min)
  "iat": 1735688700,           // Issued At
  "jti": "unique-token-id",    // JWT ID (用于黑名单)
  "roles": ["admin", "user"],  // 自定义 claims
  "permissions": ["read:users", "write:orders"]
}

# 安全措施:
# 1. Access Token 短期 (15min) + Refresh Token 长期 (7d)
# 2. 使用 RS256 (非对称) 而非 HS256 (对称)
# 3. 敏感操作需重新验证
# 4. Refresh Token 单次使用 (Rotation)
```

### 3. RBAC 权限模型
```python
# 权限 = 操作 + 资源
permissions = {
    "admin": ["read:*", "write:*", "delete:*"],
    "editor": ["read:*", "write:posts", "write:comments"],
    "viewer": ["read:*"],
}

# API 中间件检查
@require_permission("write:users")
def create_user(request):
    ...
```

## 四、API 版本控制

### 策略对比
```
# 1. URL 路径 (推荐，最清晰)
/api/v1/users
/api/v2/users

# 2. 请求头 (优雅但调试不便)
Accept: application/vnd.myapi.v1+json

# 3. 查询参数 (简单但不标准)
/api/users?version=1

# 推荐: URL 路径 + 向后兼容 + Deprecation Header
Deprecation: true
Sunset: Sat, 01 Jan 2027 00:00:00 GMT
Link: </api/v2/users>; rel="successor-version"
```

## 五、限流设计

### 算法
```
# 1. 固定窗口 (简单)
100 requests / minute

# 2. 滑动窗口 (更精确)
100 requests / sliding 60 seconds

# 3. 令牌桶 (允许突发)
bucket: 100 tokens, refill: 10/sec

# 4. 漏桶 (平滑输出)
capacity: 100, leak rate: 10/sec
```

### 响应头
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1735689660
Retry-After: 30    # 429 时返回
```

## 六、GraphQL 设计要点

### Schema 设计原则
```graphql
# 用 Relay 风格的 Connection 实现分页
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
type UserEdge {
  node: User!
  cursor: String!
}
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Mutation 返回操作结果
type CreateUserPayload {
  user: User
  errors: [UserError!]
}
type UserError {
  field: [String!]!
  message: String!
}

# 避免 N+1: 使用 DataLoader
# 复杂度限制: 防止恶意查询
```

### 安全措施
- Query 深度限制 (max 10 层)
- Query 复杂度分析 (按字段加权)
- 请求超时限制
- Persisted Queries (只允许预注册查询)

## 七、OpenAPI 规范模板

```yaml
openapi: "3.1.0"
info:
  title: My API
  version: "1.0.0"
  description: API description
servers:
  - url: https://api.example.com/v1
    description: Production
paths:
  /users:
    get:
      operationId: listUsers
      tags: [Users]
      parameters:
        - name: limit
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
        - name: cursor
          in: query
          schema: { type: string }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items: { $ref: "#/components/schemas/User" }
                  pagination: { $ref: "#/components/schemas/Pagination" }
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    User:
      type: object
      required: [id, name, email]
      properties:
        id: { type: string, format: uuid }
        name: { type: string, minLength: 1, maxLength: 100 }
        email: { type: string, format: email }
```

## 八、API 安全清单

- [ ] 所有输入验证 (白名单而非黑名单)
- [ ] 参数化查询 (防 SQL 注入)
- [ ] 输出编码 (防 XSS)
- [ ] CORS 白名单配置
- [ ] HTTPS 强制
- [ ] Rate Limiting
- [ ] 请求体大小限制
- [ ] 敏感数据不进 URL (日志会记录)
- [ ] API Key / Token 轮换机制
- [ ] 请求 ID 追踪 (traceId)
- [ ] 审计日志
