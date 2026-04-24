#!/bin/bash
# hermes-watchdog.sh — 心跳检测 hermes gateway，无响应时自动重启
# 每 2 分钟检查一次，连续 3 次失败才重启（避免瞬时网络波动误判）

HEALTH_URL="http://127.0.0.1:8642/health"
LOG="$HOME/.hermes/logs/watchdog.log"
FAIL_COUNT=0
MAX_FAIL=3
CHECK_INTERVAL=120  # 秒

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

restart_gateway() {
    log "WARN: 连续 $MAX_FAIL 次健康检查失败，正在重启 hermes gateway..."
    launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist 2>>"$LOG"
    sleep 3
    launchctl load ~/Library/LaunchAgents/ai.hermes.gateway.plist 2>>"$LOG"
    sleep 10  # 等待启动

    # 验证重启是否成功
    if curl -sf --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
        log "OK: gateway 重启成功"
        FAIL_COUNT=0
    else
        log "ERROR: gateway 重启后仍无响应！"
    fi
}

log "INFO: watchdog 启动，检查间隔 ${CHECK_INTERVAL}s，容错次数 $MAX_FAIL"

while true; do
    if curl -sf --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
        if [ $FAIL_COUNT -gt 0 ]; then
            log "OK: 恢复正常 (之前连续失败 $FAIL_COUNT 次)"
        fi
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
