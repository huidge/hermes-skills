---
name: cron-reminder-wechat-limitation
description: WeChat cannot receive cron job auto-delivery. Warn users upfront.
triggers: [cron job on wechat, scheduled reminder wechat, 定时任务 wechat, 定时提醒]
---

# Cron Job Reminders on WeChat

## Problem
Cron jobs (`cronjob` tool) cannot auto-deliver messages back to WeChat/WeChat chats. The job executes successfully and generates output, but the response is only saved to `~/.hermes/cron/output/` — it never arrives in the chat.

This affects both `deliver="local"` (default) **and** `deliver="origin"`. Even explicitly setting `deliver="origin"` does not fix it. The issue is likely that WeChat requires the current session context to send messages, and cron jobs run in isolated sessions without that context.

## Workarounds
1. **Deliver immediately in the current chat** — if the user asks for a short-term reminder (minutes, not hours), just set a simple note and reply directly after doing other work. Not ideal but reliable.
2. **Suggest switching platforms** — Telegram and Discord both support cron job delivery via `deliver="origin"`. WeChat is a known exception.
3. **Use `send_message` manually from a script** — if the user really needs timed delivery on WeChat, you could write a script that sleeps and calls `send_message`, but this is fragile and not recommended.

## What to tell the user
When a WeChat user asks for a timed reminder or scheduled message, warn them upfront:
> "WeChat 不支持定时任务自动推送提醒。任务会执行但消息不会发到聊天里。需要的话我可以现在直接提醒你，或者建议换到 Telegram 等支持定时投递的平台。"
