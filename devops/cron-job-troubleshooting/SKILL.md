---
name: cron-job-troubleshooting
description: Debug cron job execution failures — check job status, session logs, gateway errors, model availability, and stale gateway code
category: devops
version: 1.2
---

# Cron Job Troubleshooting

## Trigger
When a cron job fails to execute, runs late, or produces unexpected results.

## Diagnostic Steps

### Step 1: Check Job Status
```bash
hermes cron list
# or programmatically:
cronjob(action='list')
```
Look for:
- `last_run_at: null` → job never executed
- `last_status: error` → job failed
- `last_delivery_error` → delivery issue
- `next_run_at` in the past → scheduler missed the trigger

### Step 2: Check Session Files
```bash
ls -la ~/.hermes/sessions/ | grep cron_<job_id>
```
- No session file → job never started
- Session file exists → read last 20 lines to see outcome

### Step 3: Check System Logs
```bash
hermes logs 2>&1 | grep -E "cron|error|API call failed" | tail -30
```
Common errors:
- `API call failed after 3 retries. Connection error` → model provider unavailable
- `PermissionDeniedError: 403` → model not available in region
- `WebSocket error` → platform connectivity issue

### Step 4: Check Gateway Error Log
```bash
tail -100 ~/.hermes/logs/gateway.error.log
```
Look for model/API errors, platform connection failures, idle timeouts.

### Step 5: Check Gateway Code Version vs Running Process
**Critical:** Python processes load modules into memory at startup. If `config.yaml` provider was changed AFTER the gateway started, the running gateway still uses the OLD in-memory `PROVIDER_REGISTRY`. This causes `Unknown provider` errors even when the provider IS in the current on-disk code.

```bash
# Check when gateway process started
ps -p $(pgrep -f "hermes.*gateway") -o lstart=

# Check latest code commit date
cd ~/.hermes/hermes-agent && git log -1 --format="%ci"

# Compare: if gateway started BEFORE the provider was added to the codebase,
# it won't recognize it. The gateway loads whatever code version existed at startup.
```

Symptom: `AuthError: Unknown provider 'X'` when provider X IS in current `auth.py` PROVIDER_REGISTRY.

Fix: Restart the gateway so it loads the latest code:
```bash
# Option 1: Kill gateway, let watchdog auto-restart
kill $(pgrep -f "hermes.*gateway run")

# Option 2: Direct restart
hermes gateway restart
```

**Prevention:** Always restart the gateway after changing `config.yaml` provider or running `hermes update`.

### Step 6: Test Model Availability
Try a simple query with the same model used by the cron job. If it fails, the model provider is the root cause.

### Step 7: Manual Trigger Test
```bash
cronjob(action='run', job_id='<job_id>')
```
This forces immediate execution and updates `last_run_at`/`last_status`.

## Common Root Causes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `last_run_at: null` | Model service down | Switch provider or wait |
| Session exists, no output | Skill error | Check skill, run manually |
| Late execution (>30min delay) | Model throttling | Retry later or switch model |
| Delivery error | Platform disconnected | Check platform config |
| `Unknown provider 'X'` but X exists in code | Gateway running stale code | Restart gateway to reload modules |

## Setting Up Proactive Monitoring

Create a cron job that monitors other jobs and sends alerts on failure.

### Monitor Job Template
```python
cronjob(
 action='create',
 name='系统健康检查',
 schedule='0 */6 * * *', # Every 6 hours
 deliver='weixin:USER_ID@im.wechat', # WeChat delivery
 prompt='''执行定时任务监控检查：

1. 使用 cronjob(action='list') 获取所有定时任务的状态
2. 检查每个任务的 last_run_at 和 last_status
3. 如果发现以下情况，生成告警消息：
 - last_status 不是 'ok'（任务失败）
 - last_run_at 为空（任务从未运行）
4. 将告警消息格式化为清晰的中文报告
5. 如果有告警，使用 send_message 发送到微信
6. 告警格式：🚨 定时任务告警 - [问题描述]

如果没有异常，不发送消息。''',
 skills=['cronjob']
)
```

### Finding your WeChat delivery target
Check your existing cron jobs for the `deliver` field format — it contains your WeChat user ID.

### Alert Triggers
| Condition | Detection | Alert Message |
|-----------|-----------|---------------|
| Job failed | `last_status != 'ok'` | "任务 [name] 上次运行失败" |
| Never ran | `last_run_at == null` | "任务 [name] 从未运行过" |

### Important Notes
- The monitor job itself should also be monitored (check it runs periodically)
- Use `deliver` parameter for auto-delivery to messaging platforms
- For WeChat: `deliver='weixin:USER_ID@im.wechat'`
- For Telegram: `deliver='telegram:CHAT_ID'`
- The monitor's `deliver` must match the platform format exactly

## Pitfalls
- `cronjob run` only triggers execution; it doesn't guarantee success if the underlying issue (model availability) persists
- Some providers have regional restrictions (403 errors)
- Gateway restart may be needed after fixing provider issues
- **Gateway restart IS required after changing config.yaml provider** — the running process uses the old in-memory PROVIDER_REGISTRY
- **Gateway restart IS required after `hermes update`** — new code on disk is not loaded by the running process
- Check `~/.hermes/logs/gateway.error.log` for detailed errors, not just `hermes logs`
- Monitor jobs can also fail if model service is down — consider having multiple checks or a fallback
- WeChat delivery requires proper `WEIXIN_HOME_CHANNEL` configuration in `.env`
