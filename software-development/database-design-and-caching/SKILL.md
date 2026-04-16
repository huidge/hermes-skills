---
name: database-design-and-caching
description: 数据库设计与缓存策略 — 关系型/NoSQL 选型、Schema 设计范式、索引优化、Redis 缓存模式、数据一致性方案
category: software-development
---

# 数据库设计与缓存策略

## 触发条件
当用户需要：设计数据库表结构、选择数据库类型、优化慢查询、实现缓存层、解决数据一致性问题、做读写分离/分库分表时使用。

## 一、数据库选型决策

### 关系型 vs NoSQL

| 维度 | PostgreSQL | MySQL | MongoDB | Redis | ClickHouse |
|------|-----------|-------|---------|-------|-----------|
| 数据模型 | 关系 + JSONB | 关系 | 文档 | 键值/哈希/列表/有序集合 | 列式 |
| 事务 | 完整 ACID | 完整 ACID | 单文档原子 | 单命令原子 | 不支持 |
| 查询语言 | SQL (强大) | SQL | MQL | Redis命令 | SQL (分析优化) |
| 扩展性 | 垂直 + 逻辑复制 | 主从 + 分片 | 原生分片 | Cluster | 分布式 |
| 适用场景 | 通用/复杂查询 | Web应用/OLTP | 灵活Schema/日志 | 缓存/会话/队列 | OLAP/日志分析 |

### 选型建议
```
强一致性 + 复杂关联查询 → PostgreSQL (首选) / MySQL
灵活 Schema + 嵌套数据  → MongoDB / DynamoDB
缓存 + 会话 + 实时数据   → Redis
全文搜索                 → Elasticsearch
时序数据                 → TimescaleDB / InfluxDB
图数据                   → Neo4j / Amazon Neptune
分析型 (OLAP)            → ClickHouse / BigQuery
```

### PostgreSQL 优先选择的理由
- JSONB 支持 NoSQL 场景，无需额外引入文档数据库
- 全文搜索 (tsvector) 可替代简单 ES 场景
- 扩展生态: PostGIS(地理), pgvector(向量), TimescaleDB(时序)
- MVCC 并发性能优秀

## 二、Schema 设计原则

### 1. 范式 vs 反范式

```
# 第三范式 (3NF) — 默认选择
- 消除传递依赖
- 数据冗余最小
- 适合写多读少

# 反范式 — 特定场景
- 读多写少的报表字段
- 频繁 JOIN 的计算字段
- 示例: orders 表冗余 user_name 避免每次 JOIN
```

### 2. 常见表设计模式

```sql
-- 模式 1: 主表 + 扩展表 (大字段分离)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    bio TEXT,
    avatar_url VARCHAR(500),
    preferences JSONB DEFAULT '{}'
);

-- 模式 2: 软删除
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
-- 查询时: WHERE deleted_at IS NULL
-- 唯一约束: CREATE UNIQUE INDEX ... WHERE deleted_at IS NULL

-- 模式 3: 审计日志
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    record_id UUID,
    action VARCHAR(10),  -- INSERT/UPDATE/DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by UUID,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

-- 模式 4: 多租户隔离
-- 方案 A: schema 隔离 (中等隔离)
CREATE SCHEMA tenant_abc;
-- 方案 B: row-level 安全 (简单)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- 模式 5: 时序分区
CREATE TABLE events (
    id BIGSERIAL,
    event_type VARCHAR(50),
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2025_q1 PARTITION OF events
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
```

### 3. 索引策略

```sql
-- B-Tree (默认，等值/范围/排序)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at DESC);

-- 复合索引 (最左前缀，区分度高的字段在前)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 部分索引 (只索引活跃数据)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- 表达式索引
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- GIN (JSONB/全文搜索/数组)
CREATE INDEX idx_profile_prefs ON user_profiles USING GIN(preferences);
CREATE INDEX idx_search ON articles USING GIN(to_tsvector('english', title || ' ' || body));

-- GiST (范围/地理)
CREATE INDEX idx_location ON places USING GIST(location);

-- 覆盖索引 (INCLUDE 避免回表)
CREATE INDEX idx_orders_cover ON orders(user_id) INCLUDE (total_amount, status);

-- BRIN (大表时序数据，极小索引)
CREATE INDEX idx_events_time ON events USING BRIN(created_at);
```

**索引优化检查清单**:
- [ ] EXPLAIN ANALYZE 分析执行计划
- [ ] 消除 Sequential Scan (大表)
- [ ] 检查 Index Scan vs Bitmap Scan
- [ ] 注意 Index Only Scan (覆盖索引)
- [ ] 监控 pg_stat_user_indexes 找出未使用的索引
- [ ] 避免在高写入表上建过多索引

## 三、Redis 缓存模式

### 1. Cache-Aside (旁路缓存，推荐)

```python
async def get_user(user_id: str):
    # 1. 查缓存
    cached = await redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # 2. 缓存未命中，查数据库
    user = await db.users.find_one({"id": user_id})
    if user:
        # 3. 写入缓存 (设置 TTL)
        await redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

async def update_user(user_id: str, data: dict):
    # 1. 更新数据库
    await db.users.update_one({"id": user_id}, {"$set": data})
    # 2. 删除缓存 (而非更新，避免并发覆盖)
    await redis.delete(f"user:{user_id}")
```

### 2. Write-Through (写穿透)

```python
async def update_user(user_id: str, data: dict):
    # 同时更新 DB 和 Cache
    await db.users.update_one({"id": user_id}, {"$set": data})
    await redis.setex(f"user:{user_id}", 3600, json.dumps(data))
    # 优点: 缓存始终新鲜
    # 缺点: 写延迟增加，冷数据也会缓存
```

### 3. Write-Behind (写回/异步写入)

```python
async def update_user(user_id: str, data: dict):
    # 只写缓存
    await redis.setex(f"user:{user_id}", 3600, json.dumps(data))
    # 异步队列写入 DB
    await redis.lpush("write_queue:users", json.dumps({
        "user_id": user_id, "data": data, "ts": time.time()
    }))

# 后台消费者批量写入 DB
async def write_back_consumer():
    while True:
        items = await redis.brpop("write_queue:users", timeout=5)
        if items:
            batch = [json.loads(items[1])]
            # 批量写入 DB
            await db.users.bulk_write([...])
```

### 4. 缓存穿透 / 击穿 / 雪崩 防护

```python
# === 缓存穿透 (查询不存在的数据) ===
# 方案: 缓存空值 + 布隆过滤器
async def get_user(user_id: str):
    cached = await redis.get(f"user:{user_id}")
    if cached == "__NULL__":
        return None  # 缓存了空值
    if cached:
        return json.loads(cached)
    
    user = await db.users.find_one({"id": user_id})
    if user:
        await redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    else:
        await redis.setex(f"user:{user_id}", 300, "__NULL__")  # 空值短 TTL
    return user

# === 缓存击穿 (热 key 过期瞬间大量请求) ===
# 方案: 互斥锁 + 永不过期 + 异步刷新
async def get_hot_data(key: str):
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    
    # 获取互斥锁
    lock_key = f"lock:{key}"
    if await redis.set(lock_key, "1", nx=True, ex=10):
        try:
            data = await fetch_from_db(key)
            await redis.setex(key, 3600, json.dumps(data))
            return data
        finally:
            await redis.delete(lock_key)
    else:
        # 等待其他线程加载
        await asyncio.sleep(0.1)
        return await get_hot_data(key)  # 重试

# === 缓存雪崩 (大量 key 同时过期) ===
# 方案: TTL 加随机抖动
import random
ttl = 3600 + random.randint(0, 600)  # 3600~4200 秒
await redis.setex(key, ttl, value)
```

### 5. Redis 数据结构应用场景

| 数据结构 | 场景 | 示例 |
|---------|------|------|
| String | 缓存/计数器 | `INCR page_views:url` |
| Hash | 对象存储 | `HSET user:1 name "John" age 30` |
| List | 消息队列/最新列表 | `LPUSH notifications:1 "msg"` BRPOP 消费 |
| Set | 标签/去重/共同好友 | `SINTER followers:a followers:b` |
| Sorted Set | 排行榜/延迟队列 | `ZADD leaderboard 100 player:1` |
| Bitmap | 在线状态/签到 | `SETBIT online 123 1` |
| HyperLogLog | 基数统计 (UV) | `PFADD visitors user_id` |

## 四、读写分离与分库分表

### 读写分离
```
应用层 → Proxy (ProxySQL/PgBouncer)
         ├→ Master (写) ──复制──→ Slave1 (读)
         └──────────────────→ Slave2 (读)

注意事项:
1. 主从延迟 → 关键读走主库
2. 连接池分离 → 写池/读池独立配置
3. 故障自动切换 → VIP 漂移 / Patroni
```

### 分库分表策略
```
# 垂直拆分: 按业务模块
用户库 (users, profiles, auth)
商品库 (products, categories, inventory)
订单库 (orders, payments, shipping)

# 水平拆分: 按规则拆分同一张表
按用户 ID 取模: user_id % 16 → 16 张表
按时间: 按月/季度分区
按地域: 华东/华南/华北

# 分片键选择原则:
- 查询频率最高的字段
- 数据分布均匀
- 避免跨分片 JOIN
```

## 五、数据一致性方案

### 1. 事务 (单库)
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT;
```

### 2. Saga 模式 (分布式)
```
Order Saga:
  步骤1: 创建订单 (Order Service) → 成功
  步骤2: 扣减库存 (Inventory Service) → 成功
  步骤3: 扣款 (Payment Service) → 失败!
  补偿: 释放库存 → 取消订单
```

### 3. 事件驱动 (Event Sourcing + CQRS)
```
写入: 保存事件到 Event Store → 发布事件到 MQ
读取: 事件消费者更新读模型 (Materialized View)
最终一致性，高吞吐，完整审计轨迹
```

### 4. 本地消息表
```
1. 业务操作和消息写入同一个事务
2. 后台任务扫描未发送的消息
3. 发送成功后标记为已发送
4. 消费端保证幂等
```

## 六、性能优化清单

- [ ] 慢查询日志分析 (pg_stat_statements / slow_query_log)
- [ ] 连接池配置 (PgBouncer / HikariCP)
- [ ] 批量操作替代循环单条操作
- [ ] 避免 SELECT *，只取需要的字段
- [ ] 合理使用 JSONB 索引
- [ ] VACUUM / ANALYZE 定期维护
- [ ] 监控: 连接数 / QPS / 缓存命中率 / 锁等待
