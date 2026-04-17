---
name: skill-hub-gateway-setup
description: Configure Skill Hub Gateway (OpenClaw) - install skill, obtain API key via bootstrap flow, and set up environment variables
category: autonomous-ai-agents
version: 1.0
metadata:
  openclaw:
    skillKey: skill-hub-gateway
---

# Skill Hub Gateway Setup

## Trigger
When the user wants to configure Skill Hub Gateway for OpenClaw, obtain an API key, or integrate with the binaryworks.app skill marketplace.

## Context
Skill Hub Gateway provides OpenClaw agents access to 100+ AI capabilities through a unified API. Requires one-time bootstrap to obtain an API key.

## Prerequisites
- Node.js installed
- npm available
- OpenClaw CLI installed (`/usr/local/bin/openclaw`)

## Step-by-Step Setup

### Step 1: Install clawhub CLI
```bash
npm install -g clawhub
```

### Step 2: Install skill-hub-gateway skill
```bash
clawhub install skill-hub-gateway --force
```
Note: The skill is flagged as suspicious by VirusTotal (due to external API calls). `--force` is required for non-interactive install.

Installed location: `~/.openclaw/workspace/skills/skill-hub-gateway/`

### Step 3: Run bootstrap to get API key

The API uses a two-step bootstrap flow:

1. `POST /agent/install-code/issue` → get `install_code`
2. `POST /agent/bootstrap` → get `api_key`

Use the setup script at `~/.hermes/scripts/setup-skill-hub.mjs`:
```bash
node ~/.hermes/scripts/setup-skill-hub.mjs
```

Or call APIs manually:
```bash
# Step 1: Get install code
curl -X POST https://gateway-api.binaryworks.app/agent/install-code/issue \
  -H "Content-Type: application/json" \
  -d '{"channel":"local","owner_uid_hint":"owner_abc123"}'

# Step 2: Bootstrap (use install_code from step 1)
curl -X POST https://gateway-api.binaryworks.app/agent/bootstrap \
  -H "Content-Type: application/json" \
  -d '{"agent_uid":"agent_xyz789","install_code":"<install_code>"}'
```

### Step 4: Add to .env
Add these lines to `~/.hermes/.env`:
```
SKILL_HUB_API_KEY=<api_key>
SKILL_HUB_AGENT_UID=<agent_uid>
SKILL_HUB_OWNER_UID=<owner_uid>
SKILL_HUB_BASE_URL=https://gateway-api.binaryworks.app
```

### Step 5: Restart Gateway
```bash
hermes gateway restart
```

## Pitfalls

### UID Format Requirements
- **agent_uid**: Must match `^agent_[a-z0-9][a-z0-9_-]{5,63}$` — use underscore, not hyphen after prefix
- **owner_uid_hint**: Must match `^owner_[a-z0-9][a-z0-9_-]{5,63}$` — same pattern
- ❌ Wrong: `agent-abc123`, `owner-abc123`
- ✅ Correct: `agent_abc123`, `owner_abc123`

### ESM Module Issues
The setup script uses ES modules (`.mjs`). Don't use `require()` — use `import` statements:
```javascript
import os from 'os';
import crypto from 'crypto';
import path from 'path';
```

### VirusTotal Warning
The skill is flagged as suspicious because it makes external API calls. This is expected — the skill communicates with gateway-api.binaryworks.app. Review the code in `scripts/` directory if concerned.

### API Endpoints
- Base URL: `https://gateway-api.binaryworks.app`
- Site URL: `https://gateway.binaryworks.app`
- Manifest: `GET /skills/manifest.json` (for version checks)

## Verification
Test the API key:
```bash
curl -H "X-API-Key: <api_key>" https://gateway-api.binaryworks.app/skills/manifest.json
```

Should return a JSON response with skill manifest data.

## Related Files
- Setup script: `~/.hermes/scripts/setup-skill-hub.mjs`
- Config backup: `~/.hermes/config/skill-hub.env`
- Skill directory: `~/.openclaw/workspace/skills/skill-hub-gateway/`
- Chinese docs: `~/.openclaw/workspace/skills/skill-hub-gateway/SKILL.zh-CN.md`
