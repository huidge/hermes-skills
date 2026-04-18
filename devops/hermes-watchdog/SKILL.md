---
name: hermes-watchdog
description: Set up a watchdog for hermes gateway — heartbeat detection and auto-restart when the process hangs or becomes unresponsive.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, watchdog, heartbeat, auto-restart, launchd, macos]
---

# Hermes Watchdog

Launchd only restarts hermes on process **exit** — it won't detect a hung or unresponsive gateway. This watchdog adds heartbeat detection via the `/health` endpoint.

## When to Use

- Hermes gateway process is running but unresponsive (cron jobs stop executing, API calls fail)
- Mac sleep/wake causes the gateway to enter a bad state without crashing
- You need 24/7 reliability for cron jobs and scheduled tasks

## How It Works

1. A bash script polls `http://127.0.0.1:8642/health` every 2 minutes
2. If the health endpoint fails 3 consecutive times (6 min), it force-restarts the gateway via launchctl
3. A launchd plist keeps the watchdog itself alive (KeepAlive: true)

## Setup

### 1. Create the watchdog script

```bash
cat > ~/.hermes/scripts/hermes-watchdog.sh << 'SCRIPT'
#!/bin/bash
HEALTH_URL="http://127.0.0.1:8642/health"
LOG="$HOME/.hermes/logs/watchdog.log"
FAIL_COUNT=0
MAX_FAIL=3
CHECK_INTERVAL=120

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

restart_gateway() {
    log "WARN: 连续 $MAX_FAIL 次健康检查失败，正在重启 hermes gateway..."
    launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist 2>>"$LOG"
    sleep 3
    launchctl load ~/Library/LaunchAgents/ai.hermes.gateway.plist 2>>"$LOG"
    sleep 10
    if curl -sf --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
        log "OK: gateway 重启成功"
    else
        log "ERROR: gateway 重启后仍无响应！"
    fi
    FAIL_COUNT=0
}

log "INFO: watchdog 启动，检查间隔 ${CHECK_INTERVAL}s，容错次数 $MAX_FAIL"

while true; do
    if curl -sf --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
        FAIL_COUNT=0
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        log "WARN: 健康检查失败 ($FAIL_COUNT/$MAX_FAIL)"
        if [ $FAIL_COUNT -ge $MAX_FAIL ]; then
            restart_gateway
            FAIL_COUNT=0
        fi
    fi
    sleep $CHECK_INTERVAL
done
SCRIPT

chmod +x ~/.hermes/scripts/hermes-watchdog.sh
```

### 2. Create the launchd plist

```bash
cat > ~/Library/LaunchAgents/ai.hermes.watchdog.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.hermes.watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/huidge/.hermes/scripts/hermes-watchdog.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/huidge/.hermes/logs/watchdog.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/huidge/.hermes/logs/watchdog.stderr.log</string>
</dict>
</plist>
PLIST
```

### 3. Load the service

```bash
launchctl load ~/Library/LaunchAgents/ai.hermes.watchdog.plist
```

## Verification

```bash
# Check watchdog process is running
ps aux | grep hermes-watchdog | grep -v grep

# Check watchdog logs
tail -f ~/.hermes/logs/watchdog.log
```

## Pitfalls

- **Health endpoint port**: Check `~/.hermes/config.yaml` for `port:` — default is 8642 but may differ
- **False positives**: The 3-retry threshold prevents restarts from transient network blips. Don't set MAX_FAIL below 2
- **Mac sleep**: After wake, the watchdog may detect failures and restart — this is desired behavior
- **launchd KeepAlive**: The watchdog plist uses `KeepAlive: true` (not just on failure) since it's a long-running loop script
