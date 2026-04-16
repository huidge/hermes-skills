---
name: common-development-patterns
description: 常见开发模式与问题解决 — 设计模式、并发处理、错误处理策略、安全防护、代码审查清单、性能调优方法论
category: software-development
---

# 常见开发模式与问题解决

## 触发条件
当用户需要：应用设计模式解决架构问题、处理并发/竞态条件、设计错误处理策略、做安全防护、代码审查、性能调优时使用。

## 一、常用设计模式

### 1. 创建型模式

```python
# === 工厂模式 (Factory) ===
# 场景: 根据类型创建不同对象，避免大量 if-else
class PaymentFactory:
    _creators = {}
    
    @classmethod
    def register(cls, method: str, creator):
        cls._creators[method] = creator
    
    @classmethod
    def create(cls, method: str, **kwargs):
        creator = cls._creators.get(method)
        if not creator:
            raise ValueError(f"Unknown payment method: {method}")
        return creator(**kwargs)

PaymentFactory.register("stripe", StripePayment)
PaymentFactory.register("alipay", AlipayPayment)
payment = PaymentFactory.create("stripe", amount=100)

# === 建造者模式 (Builder) ===
# 场景: 复杂对象的分步构建
from dataclasses import dataclass, field

@dataclass
class QueryBuilder:
    table: str
    _conditions: list = field(default_factory=list)
    _order_by: str = ""
    _limit: int = 100
    
    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self  # 链式调用
    
    def order(self, field: str, desc=False) -> "QueryBuilder":
        self._order_by = f"{field} {'DESC' if desc else 'ASC'}"
        return self
    
    def build(self) -> str:
        sql = f"SELECT * FROM {self.table}"
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        if self._order_by:
            sql += f" ORDER BY {self._order_by}"
        sql += f" LIMIT {self._limit}"
        return sql

query = (QueryBuilder("users")
    .where("status = 'active'")
    .where("age > 18")
    .order("created_at", desc=True)
    .build())
```

### 2. 结构型模式

```python
# === 适配器模式 (Adapter) ===
# 场景: 统一不同接口
class LegacyPaymentAdapter:
    def __init__(self, legacy_client):
        self.client = legacy_client
    
    def pay(self, amount: float, currency: str) -> dict:
        # 将新接口调用转换为旧系统接口
        result = self.client.process_transaction(
            txn_amount=int(amount * 100),  # 元 → 分
            curr_code=currency.upper()
        )
        return {"status": "success" if result.code == 0 else "failed"}

# === 装饰器模式 (Decorator) ===
# 场景: 给函数/方法添加横切关注点
import functools, time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(delay * (2 ** attempt))  # 指数退避
        return wrapper
    return decorator

def cache(ttl=300):
    def decorator(func):
        _cache = {}
        @functools.wraps(func)
        async def wrapper(*args):
            key = (func.__name__, args)
            if key in _cache and time.time() - _cache[key][1] < ttl:
                return _cache[key][0]
            result = await func(*args)
            _cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

@retry(max_attempts=3)
@cache(ttl=60)
async def fetch_user(user_id: str):
    return await db.users.find_one({"id": user_id})
```

### 3. 行为型模式

```python
# === 策略模式 (Strategy) ===
# 场景: 运行时切换算法
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_price: float) -> float:
        pass

class RegularPricing(PricingStrategy):
    def calculate(self, base_price):
        return base_price

class DiscountPricing(PricingStrategy):
    def __init__(self, discount=0.1):
        self.discount = discount
    def calculate(self, base_price):
        return base_price * (1 - self.discount)

class DynamicPricing(PricingStrategy):
    def calculate(self, base_price):
        hour = datetime.now().hour
        if 0 <= hour < 6:
            return base_price * 0.8   # 凌晨折扣
        elif 18 <= hour < 22:
            return base_price * 1.2   # 晚高峰溢价
        return base_price

class OrderService:
    def __init__(self, pricing: PricingStrategy):
        self.pricing = pricing
    
    def calculate_total(self, items):
        return sum(self.pricing.calculate(item.price) for item in items)

# 运行时切换
service = OrderService(DynamicPricing())

# === 观察者模式 (Observer) / 事件驱动 ===
# 场景: 解耦事件生产者和消费者
from typing import Callable
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)
    
    def on(self, event_type: str, handler: Callable):
        self._handlers[event_type].append(handler)
    
    async def emit(self, event_type: str, data: dict):
        for handler in self._handlers[event_type]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"Event handler error: {e}")

bus = EventBus()

# 注册处理
@bus.on("order.created")
async def send_notification(data):
    await email_service.send(data["user_email"], "订单已创建")

@bus.on("order.created")
async def update_inventory(data):
    await inventory_service.deduct(data["items"])

# 触发事件
await bus.emit("order.created", {"order_id": "123", "user_email": "a@b.com"})
```

## 二、并发与异步处理

### 1. Python 并发模式

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# === 异步 I/O 密集型 (推荐) ===
async def fetch_all_users():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user(session, uid) for uid in user_ids]
        return await asyncio.gather(*tasks)  # 并发执行

# === 限流并发 ===
async def fetch_with_limit(urls, max_concurrent=10):
    semaphore = asyncio.Semaphore(max_concurrent)
    async def fetch_one(url):
        async with semaphore:
            return await fetch(url)
    return await asyncio.gather(*[fetch_one(u) for u in urls])

# === 生产者-消费者 ===
async def producer_consumer():
    queue = asyncio.Queue(maxsize=100)
    
    async def producer():
        for item in data:
            await queue.put(item)
        await queue.put(None)  # 结束信号
    
    async def consumer(name):
        while True:
            item = await queue.get()
            if item is None:
                await queue.put(None)  # 传递结束信号
                break
            try:
                await process(item)
            finally:
                queue.task_done()
    
    await asyncio.gather(
        producer(),
        consumer("worker-1"),
        consumer("worker-2"),
        consumer("worker-3"),
    )

# === CPU 密集型: ProcessPoolExecutor ===
def cpu_intensive_task(data):
    return heavy_computation(data)

loop = asyncio.get_event_loop()
with ProcessPoolExecutor() as executor:
    results = await loop.run_in_executor(executor, cpu_intensive_task, data)
```

### 2. 竞态条件防护

```python
# === 分布式锁 (Redis) ===
import redis.asyncio as redis

class DistributedLock:
    def __init__(self, redis_client, key, timeout=10):
        self.redis = redis_client
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.token = str(uuid.uuid4())
    
    async def acquire(self):
        return await self.redis.set(
            self.key, self.token, nx=True, ex=self.timeout
        )
    
    async def release(self):
        # Lua 脚本保证原子性
        lua = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        end
        return 0
        """
        return await self.redis.eval(lua, 1, self.key, self.token)

# 使用
async def deduct_inventory(item_id):
    lock = DistributedLock(redis_client, f"inventory:{item_id}")
    if await lock.acquire():
        try:
            # 临界区: 读取-修改-写入
            stock = await get_stock(item_id)
            if stock > 0:
                await set_stock(item_id, stock - 1)
                return True
            return False
        finally:
            await lock.release()
    else:
        raise ConcurrentModificationError("请稍后重试")

# === 乐观锁 (版本号) ===
async def update_user_optimistic(user_id, data, expected_version):
    result = await db.users.update_one(
        {"id": user_id, "version": expected_version},
        {"$set": {**data, "version": expected_version + 1}}
    )
    if result.modified_count == 0:
        raise OptimisticLockError("数据已被其他请求修改")

# === CAS (Compare-And-Swap) ===
# Redis: SET key value XX (仅当 key 存在时设置)
# DB: UPDATE ... WHERE version = expected_version
```

## 三、错误处理策略

### 1. 分层错误处理

```python
# === 自定义异常层级 ===
class AppError(Exception):
    """应用基础异常"""
    def __init__(self, message, code="APP_ERROR", status=500, details=None):
        super().__init__(message)
        self.code = code
        self.status = status
        self.details = details or {}

class NotFoundError(AppError):
    def __init__(self, resource, identifier):
        super().__init__(
            f"{resource} not found: {identifier}",
            code="NOT_FOUND", status=404,
            details={"resource": resource, "id": identifier}
        )

class ValidationError(AppError):
    def __init__(self, errors: list):
        super().__init__(
            "Validation failed",
            code="VALIDATION_ERROR", status=422,
            details={"errors": errors}
        )

class BusinessRuleError(AppError):
    def __init__(self, rule, message):
        super().__init__(
            message,
            code="BUSINESS_RULE_VIOLATION", status=409,
            details={"rule": rule}
        )

# === 全局错误处理器 (FastAPI) ===
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status,
        content={
            "type": f"https://api.example.com/errors/{exc.code.lower()}",
            "title": exc.code,
            "status": exc.status,
            "detail": str(exc),
            "instance": str(request.url),
            "traceId": request.state.trace_id,
            **exc.details
        }
    )

@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error")
    return JSONResponse(
        status_code=500,
        content={
            "type": "https://api.example.com/errors/internal",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "An unexpected error occurred",
            "traceId": request.state.trace_id
        }
    )
```

### 2. 降级 & 熔断

```python
# === 熔断器 ===
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED -> OPEN -> HALF_OPEN
        self.last_failure_time = None
    
    async def call(self, func, *args, fallback=None, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            elif fallback:
                return await fallback(*args, **kwargs)
            else:
                raise CircuitOpenError("Service unavailable")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            if fallback:
                return await fallback(*args, **kwargs)
            raise

# 使用
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

async def get_recommendations(user_id):
    return await ai_service.recommend(user_id)

async def get_default_recommendations(user_id):
    return [{"id": "popular-1"}, {"id": "popular-2"}]

result = await breaker.call(
    get_recommendations, user_id,
    fallback=get_default_recommendations
)
```

## 四、安全防护

### 输入验证 (多层)
```python
from pydantic import BaseModel, EmailStr, validator

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    age: int
    
    @validator("name")
    def name_must_be_valid(cls, v):
        if len(v) < 1 or len(v) > 100:
            raise ValueError("Name must be 1-100 characters")
        if "<" in v or ">" in v or "script" in v.lower():
            raise ValueError("Invalid characters in name")
        return v.strip()
    
    @validator("age")
    def age_must_be_reasonable(cls, v):
        if not 0 <= v <= 150:
            raise ValueError("Invalid age")
        return v
```

### 常见安全漏洞防护
```
SQL 注入    → 参数化查询 / ORM (永远不要拼接 SQL)
XSS        → 输出编码 / CSP / HttpOnly Cookie
CSRF       → SameSite Cookie + Token
SSRF       → 白名单 URL / 禁止内网 IP
路径遍历    → 规范化路径 / 白名单目录
反序列化    → 避免 eval/pickle / 使用 JSON
权限绕过    → 每个端点独立鉴权 / 最小权限原则
```

## 五、代码审查清单

### 功能性
- [ ] 逻辑正确，边界条件处理
- [ ] 错误处理完整 (不吞异常)
- [ ] 并发安全 (竞态条件)
- [ ] 幂等性 (重试安全)

### 可维护性
- [ ] 命名清晰 (变量/函数/类)
- [ ] 单一职责 (函数 < 50 行)
- [ ] 无重复代码 (DRY)
- [ ] 注释说明 WHY 而非 WHAT

### 性能
- [ ] 无 N+1 查询
- [ ] 大数据集使用分页/流式处理
- [ ] 合理使用缓存
- [ ] 无不必要的序列化/反序列化

### 安全
- [ ] 输入验证
- [ ] 无硬编码密钥/密码
- [ ] 权限检查
- [ ] 敏感数据脱敏

### 测试
- [ ] 关键路径有测试覆盖
- [ ] 边界条件有测试
- [ ] 测试可独立运行 (无外部依赖)
