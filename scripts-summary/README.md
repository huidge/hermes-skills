# Hermes 脚本仓库

本仓库汇总了 Hermes Agent 系统相关的所有实用脚本，包括定时任务处理、监控告警、服务部署等工具。

## 目录

- [市场数据脚本](#市场数据脚本)
- [系统运维脚本](#系统运维脚本)
- [监控告警脚本](#监控告警脚本)
- [部署配置脚本](#部署配置脚本)
- [测试脚本](#测试脚本)

---

## 市场数据脚本

### a-share-daily-report.py

**用途**: 生成 A 股每日收盘行情汇总报告

**数据源优先级**: 东方财富 API > AKShare (Sina + 同花顺) 兜底

**用法**:
```bash
# 输出到标准输出
python3 a-share-daily-report.py

# 保存到指定文件
python3 a-share-daily-report.py /path/to/output.md

# 在 cron 任务中自动运行（通过 hermes cron）
# 已在 hermes 中配置为每日 15:30 自动执行
```

**输出内容**:
- 主要指数表现（上证、深证、创业板、北证50）
- 市场概览（上涨/下跌/平家数）
- 涨跌停统计
- 资金流向分析
- 热点板块排行
- 成交量与成交额

**依赖**:
- akshare >= 1.14.0
- pandas

**关联 Cron Job**:
- `每日A股收盘汇总` - 每天下午 15:30 执行，通过微信推送报告

**注意事项**:
- 东方财富 push2 接口已废弃，当前使用 push2his + 实时接口
- 北证50 使用新浪接口作为兜底
- 数据更新时间一般为 15:30 之后

---

### check_cron_alerts.py

**用途**: 简单的定时任务监控脚本，检查 cron 任务是否有失败的告警

**用法**:
```bash
python3 check_cron_alerts.py
```

**工作原理**:
- 调用 `hermes cron list` 获取所有定时任务状态
- 检查是否有标记为失败的任务
- 输出失败任务列表

**典型输出**:
```
检查定时任务告警...
- 每日A股收盘汇总: 执行失败
- 系统健康检查: 执行失败
发现 2 个问题任务
```

**适用场景**:
- 集成到外部监控系统（如 Zabbix、Prometheus）
- 手动排查定时任务问题

---

## 系统运维脚本

### cron_monitor.py

**用途**: 高级定时任务监控守护进程，主动检测任务执行状态异常并发送告警

**用法**:
```bash
# 手动运行一次检查
python3 cron_monitor.py

# 作为守护进程持续运行（建议配合 systemd 或 screen）
python3 cron_monitor.py --daemon

# 查看帮助
python3 cron_monitor.py --help
```

**检测规则**:
1. **从未运行**: 任务从未执行过
2. **执行失败**: 上次运行状态不是 'ok'
3. **长时间未运行**: 超过 24 小时未执行（可根据调度频率调整）
4. **调度异常**: 根据 crontab 表达式判断是否错过了执行窗口

**告警方式**:
- 标准输出日志
- 可通过扩展集成微信/邮件通知

**依赖**:
- 读取 `~/.hermes/cron_jobs.json` 获取任务配置

---

### hermes-watchdog.sh

**用途**: Hermes Gateway 心跳检测守护进程，无响应时自动重启服务

**工作机制**:
- 每 2 分钟检查一次 `http://127.0.0.1:8642/health`
- 连续 3 次失败后才重启（避免瞬时网络波动误判）
- 通过 `launchctl` 管理 macOS 服务

**部署** (macOS):
```bash
# 1. 复制 plist 文件到 LaunchAgents
cp ~/.hermes/scripts/hermes-watchdog.plist ~/Library/LaunchAgents/

# 2. 加载服务
launchctl load ~/Library/LaunchAgents/ai.hermes.watchdog.plist

# 3. 查看日志
tail -f ~/.hermes/logs/watchdog.log
```

**日志位置**: `~/.hermes/logs/watchdog.log`

**恢复手动控制**:
```bash
# 停止 watchdog
launchctl unload ~/Library/LaunchAgents/ai.hermes.watchdog.plist

# 手动重启 gateway
hermes gateway restart
```

**健康检查端点**:
- URL: `http://127.0.0.1:8642/health`
- 返回: JSON `{"status":"ok"}` 或 HTTP 200

---

## 部署配置脚本

### sync-reports.sh

**用途**: 自动同步 `market-reports` 目录的 Markdown 报告变更到 GitHub

**用法**:
```bash
# 手动同步
~/.hermes/scripts/sync-reports.sh

# 或通过软链接调用
ln -s ~/.hermes/scripts/sync-reports.sh /usr/local/bin/sync-reports
sync-reports
```

**执行流程**:
1. 检查 `market-reports` 目录是否有未提交的变更
2. 自动 `git add -A`
3. 提交，commit message 格式: `市场报告更新 YYYY-MM-DD`
4. 推送到 `origin/main`

**前置条件**:
- `market-reports` 目录必须是 git 仓库
- 已配置 GitHub 远程 `origin`
- 已设置 SSH 密钥或 Git 凭据

**关联 Cron Job**:
- `market-reports-sync` - 每天 06:30 和 16:30 自动执行

**失败处理**:
- 如果推送失败，脚本会退出并显示错误信息
- 建议配合 `cron_monitor.py` 监控该任务状态

---

### setup-skill-hub.mjs

**用途**: 配置 Skill Hub Gateway（OpenClaw）认证，自动获取 API Key

**环境要求**:
- Node.js >= 18
- 网络可访问 `https://gateway-api.binaryworks.app`

**用法**:
```bash
# 交互式配置（推荐首次使用）
node setup-skill-hub.mjs

# 指定 owner UID（如果已知）
node setup-skill-hub.mjs --owner-uid <your-uid>
```

**功能**:
1. 从服务器获取 install code
2. 绑定当前 Agent UID
3. 获取并保存 API key 到 `~/.hermes/.env`

**生成的文件**:
- `~/.hermes/.env` - 环境变量文件，包含 `OPENCLAW_API_KEY`

**配置后的技能调用**:
```bash
hermes skills load skill-hub-gateway-setup
# 之后即可使用远程 Skill Hub 中的技能
```

**故障排查**:
```bash
# 检查 .env 文件
cat ~/.hermes/.env | grep OPENCLAW

# 测试连接
curl -H "X-API-Key: $OPENCLAW_API_KEY" https://gateway-api.binaryworks.app/ping
```

---

## 测试脚本

### test_weixin.py

**用途**: 验证微信通知功能配置是否正确

**用法**:
```bash
python3 test_weixin.py
```

**检查项**:
- [x] 配置文件 `~/.hermes/.env` 是否存在
- [x] 必需环境变量是否配置 (`WEIXIN_ACCOUNT_ID`, `WEIXIN_TOKEN`, `WEIXIN_BASE_URL`)
- [x] 网络连通性测试（可选）
- [x] 发送测试消息

**典型输出**:
```
测试微信通知功能配置
==================================================
✅ 微信配置检查通过
环境变量:
  WEIXIN_ACCOUNT_ID = o9cq80xxx
  WEIXIN_BASE_URL   = https://qyapi.weixin.qq.com
发送测试消息... ✅ 成功
```

**手动发送测试消息**:
```bash
python3 test_weixin.py --send "Hello from Hermes"
```

---

## 脚本管理规范

### 文件命名
- Python 脚本: `*.py`，使用 snake_case
- Shell 脚本: `*.sh`，使用 kebab-case
- Node.js 脚本: `*.mjs` 或 `*.cjs`

### 权限设置
```bash
# 所有脚本必须可执行
chmod +x ~/.hermes/scripts/*.sh
chmod +x ~/.hermes/scripts/*.py
chmod +x ~/.hermes/scripts/*.mjs
```

### 依赖管理
Python 脚本依赖已安装在 Hermes 虚拟环境中，无需额外安装：
```bash
# 激活虚拟环境
source ~/.hermes/venv/bin/activate

# 安装缺失依赖
pip install akshare pandas
```

### 日志位置
所有脚本日志统一输出到:
- `~/.hermes/logs/` - 按文件名分割
- 例如: `~/.hermes/logs/cron_monitor.log`

---

## 定时任务总览

| 任务名称 | 调度 | 技能 | 状态 |
|---------|------|------|------|
| 每日A股收盘汇总 | 30 15 * * 1-5 | a-share-report-akshare | ✅ |
| 每日美股收盘汇总 | 0 6 * * * | us-stock-daily-report | ✅ |
| 系统健康检查 | 0 */6 * * * | cronjob | ✅ |
| skills-sync-to-github | 0 10 * * * | - | ✅ |
| market-reports-sync | 30 6,16 * * * | - | ✅ |
| 每周A股行情周报 | 0 17 * * 5 | a-share-report-akshare | ✅ |

查看所有定时任务:
```bash
hermes cron list
```

---

## 故障排查

### 脚本执行权限错误
```bash
chmod +x /path/to/script.sh
```

### Python 模块找不到
```bash
# 确认虚拟环境已激活
source ~/.hermes/venv/bin/activate
pip install -r ~/.hermes/scripts/requirements.txt  # 如存在
```

### Cron 任务不执行
```bash
# 检查 cron 服务状态
hermes cron list

# 查看最近执行日志
hermes cron logs <job_id>

# 手动运行测试
hermes cron run <job_id>
```

### 微信推送失败
```bash
# 测试微信配置
python3 ~/.hermes/scripts/test_weixin.py

# 检查网关状态
hermes status | grep -i weixin
```

---

## 更新日志

- **2026-04-24**: 创建脚本汇总目录，编写文档
- **2026-04-21**: a-share-daily-report 优化数据源
- **2026-04-17**: hermes-watchdog 部署完成
- **2026-04-16**: cron_monitor 初始版本

---

**维护者**: Hermes Agent System
**文档版本**: v1.0
**最后更新**: 2026-04-24
