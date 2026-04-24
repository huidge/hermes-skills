---
name: hermes-gateway-http-limitations
category: devops
description: Hermes gateway port 8642 is WebSocket-based only — NOT a REST API. Do NOT try to send WeChat/Weixin alerts via curl HTTP POST to the gateway. Understanding this prevents wasted time debugging "404 on all endpoints" when trying to send alerts from cron jobs.
---

# Hermes Gateway HTTP Limitations

## Key Finding
The hermes gateway (PID 34544 on macOS, `launchd` managed) listens on **port 8642** but it is **NOT a REST API server**. All attempts to send messages via `curl -X POST http://localhost:8642/...` return `404 Not Found`.

## Why
- Weixin/WeCom connect via **outbound WebSocket** to Tencent's servers
- The gateway is a WebSocket client connecting *out* to Tencent, not an HTTP server receiving *inbound* push requests
- `lsof -i :8642` shows the gateway holds the LISTEN socket, but its internal routing is WebSocket-based, not HTTP REST-based
- The only working Weixin send path is through the `send_message` tool in an active agent session (which calls `gateway.platforms.weixin` adapter internally)

## What This Means for Cron Job Alerts
When a cron job tries to send a WeChat alert (e.g., via `send_message` tool or directly calling the gateway from Python), it cannot use a simple HTTP POST. The cron delivery works because the **scheduler auto-injects the response into the gateway session** — the gateway then sends it via its existing WebSocket connection to Weixin.

## Verified Working Patterns
1. **Cron auto-delivery**: Set `deliver: "weixin:chat_id"` in the cron job config — the scheduler handles delivery through the gateway's WebSocket
2. **Active agent session**: Use `send_message(target="weixin:chat_id", message="...")` in an agent conversation — the agent calls `tools/send_message_tool.py` which routes through the gateway
3. **Alert file fallback**: Save alert to `~/.hermes/logs/alert_YYYYMMDD_HHMMSS.txt` — not real-time but preserves the alert

## Non-Working Patterns (DO NOT USE)
- `curl -X POST http://localhost:8642/api/send ...` → 404
- `curl -X POST http://localhost:8642/send_message ...` → 404  
- Any HTTP POST/GET to the gateway for sending messages

## Files Involved
- `~/.hermes/hermes-agent/tools/send_message_tool.py` — the actual send implementation
- `~/.hermes/hermes-agent/hermes_cli/web_server.py` — port 9119 web UI (FastAPI, separate from gateway port 8642)
- Gateway config: `hermes gateway status` shows Weixin is configured as WebSocket client

## How to Check Weixin Status
```bash
hermes status | grep -A5 "Weixin\|WeCom"
```