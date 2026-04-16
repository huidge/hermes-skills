---
name: devops-cicd-containerization
description: DevOps 实践 — Docker 容器化、Kubernetes 编排、CI/CD 流水线、GitOps、监控可观测性、基础设施即代码
category: software-development
---

# DevOps & CI/CD & 容器化指南

## 触发条件
当用户需要：编写 Dockerfile、配置 K8s 部署、搭建 CI/CD 流水线、做监控/日志/链路追踪、管理基础设施、排查部署问题时使用。

## 一、Docker 最佳实践

### 1. 多阶段构建 (Multi-stage Build)

```dockerfile
# === Node.js 应用 ===
# Stage 1: 构建
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: 运行 (最小镜像)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]

# === Python 应用 ===
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
USER 1001
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Dockerfile 优化清单

```dockerfile
# 基础镜像选择
FROM node:20-alpine      # Alpine 最小化 (~5MB base)
FROM python:3.12-slim    # Slim 去掉开发工具
# 避免: latest 标签, 完整 OS 镜像

# 层缓存优化
# 1. 先 COPY 依赖文件 → 再 COPY 源码
COPY package*.json ./    # 变化少, 缓存命中率高
RUN npm ci
COPY . .                 # 源码变化频繁

# 2. 合并 RUN 减少层数
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 安全加固
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser             # 非 root 运行
HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1

# .dockerignore (必不可少)
# node_modules
# .git
# *.md
# .env*
# dist
# .next
```

### 3. Docker Compose (开发环境)

```yaml
# docker-compose.yml
version: "3.8"
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder    # 开发用构建阶段
    ports: ["3000:3000"]
    volumes:
      - .:/app           # 热重载
      - /app/node_modules
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      db: { condition: service_healthy }
      cache: { condition: service_started }

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes: ["redisdata:/data"]

  mailhog:  # 开发用邮件测试
    image: mailhog/mailhog
    ports: ["8025:8025"]

volumes:
  pgdata:
  redisdata:
```

## 二、Kubernetes 核心概念

### 1. 部署清单 (Deployment)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    version: v1.2.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1         # 最多多1个 Pod
      maxUnavailable: 0   # 滚动更新时不减少可用 Pod
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
        - name: web-app
          image: registry.example.com/web-app:v1.2.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:         # 存活检查
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:        # 就绪检查
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url
---
apiVersion: v1
kind: Service
metadata:
  name: web-app-svc
spec:
  selector:
    app: web-app
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts: [app.example.com]
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-app-svc
                port:
                  number: 80
```

### 2. HPA 自动扩缩

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### 3. K8s 安全最佳实践

```yaml
# Pod Security
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    fsGroup: 1001
  containers:
    - name: app
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
      volumeMounts:
        - name: tmp
          mountPath: /tmp
  volumes:
    - name: tmp
      emptyDir: {}
```

## 三、CI/CD 流水线

### GitHub Actions 示例

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # === CI: 测试 ===
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test -- --coverage
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test_db
      - uses: codecov/codecov-action@v4

  # === CI: 安全扫描 ===
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          scan-ref: .
          severity: HIGH,CRITICAL

  # === CD: 构建 & 推送镜像 ===
  build:
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=semver,pattern={{version}}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # === CD: 部署 ===
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to K8s
        uses: azure/k8s-deploy@v4
        with:
          manifests: k8s/
          images: ${{ needs.build.outputs.image-tag }}
          namespace: production
```

### GitOps (ArgoCD)

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/k8s-manifests
    targetRevision: main
    path: apps/web-app/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true      # 删除 Git 中不存在的资源
      selfHeal: true    # 自动修复配置偏移
    syncOptions:
      - CreateNamespace=true
```

## 四、可观测性 (Observability)

### 三大支柱

```
1. Logs (日志)
   结构化日志 → JSON 格式
   { "level": "error", "msg": "DB connection failed", "traceId": "abc123", "ts": "2025-01-15T10:30:00Z" }
   工具: ELK Stack / Loki + Grafana

2. Metrics (指标)
   系统: CPU/Memory/Disk/Network
   应用: QPS/Latency/Error Rate/Saturation (RED 方法)
   业务: DAU/订单量/转化率
   工具: Prometheus + Grafana / Datadog

3. Traces (链路追踪)
   请求经过的所有服务串联
   工具: Jaeger / Zipkin / OpenTelemetry
```

### OpenTelemetry 集成

```python
# Python 自动注入
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        # 业务逻辑...
```

### 告警规则示例 (Prometheus)

```yaml
groups:
  - name: app-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "错误率超过 5%"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 延迟超过 1 秒"
      
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 15m
        labels:
          severity: critical
```

## 五、基础设施即代码 (IaC)

### Terraform 示例

```hcl
# main.tf — AWS ECS Fargate
provider "aws" {
  region = "ap-east-1"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["ap-east-1a", "ap-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  enable_nat_gateway = true
}

resource "aws_ecs_cluster" "main" {
  name = "my-cluster"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "web-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  container_definitions = jsonencode([{
    name  = "web-app"
    image = "${aws_ecr_repository.app.repository_url}:latest"
    portMappings = [{ containerPort = 3000 }]
  }])
}
```

## 六、常见问题排查清单

### 部署失败
```
1. kubectl describe pod <name> — 查看 Events
2. kubectl logs <name> --previous — 查看上次崩溃日志
3. 检查: 资源限制 / 镜像拉取 / ConfigMap/Secret / RBAC
```

### 性能问题
```
1. kubectl top pods — 资源使用
2. 检查 HPA 是否生效
3. 数据库连接池是否耗尽
4. 慢查询日志
5. 链路追踪找到瓶颈服务
```

### 网络问题
```
1. kubectl exec -it <pod> -- curl <target-svc>
2. 检查 NetworkPolicy / Service / Endpoints
3. DNS 解析: nslookup <svc>.<ns>.svc.cluster.local
4. Ingress 配置检查
```
