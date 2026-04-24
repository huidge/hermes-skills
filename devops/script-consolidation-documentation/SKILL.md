---
name: script-consolidation-documentation
category: devops
description: Consolidate scattered utility scripts into a centralized directory with comprehensive documentation, then publish to version control.
---

# Script Consolidation & Documentation

## When to Use
Use this skill when you need to:
- Gather utility scripts scattered across multiple directories into one place
- Create comprehensive documentation for existing scripts
- Publish a curated scripts repository for team access
- Perform "script hygiene" — discovering what scripts actually exist and what they do

## Problem Addressed
Scripts often accumulate in various locations (`~/scripts/`, `~/.hermes/scripts/`, skill subdirectories, cron job locations) without centralized documentation. This skill provides a systematic approach to discover, curate, document, and publish them.

---

## Step-by-Step Process

### Step 1: Discovery — Find All Scripts

Search multiple common locations to build a complete inventory:

```bash
# Primary script directories
ls -la ~/.hermes/scripts/
ls -la ~/scripts/
ls -la ~/.local/bin/

# Skill-embedded scripts (commonly in scripts/ subdirectories)
find ~/.hermes/skills -name "*.py" -path "*/scripts/*" 2>/dev/null
find ~/.hermes/skills -name "*.sh" -path "*/scripts/*" 2>/dev/null
find ~/.hermes/skills -name "*.mjs" -path "*/scripts/*" 2>/dev/null

# Cron job scripts (check crontab and hermes cron)
crontab -l 2>/dev/null | grep -E '\.(py|sh|mjs)$' || true
hermes cron list
```

**Output needed**: Complete list of script paths with purpose (if recognizable from filename/context).

### Step 2: Curation — Select What to Include

**Include**:
- Standalone utility scripts (not tightly coupled to specific skill internals)
- Scripts referenced by cron jobs
- Monitoring/maintenance scripts
- Deployment/setup scripts
- Scripts with general reuse potential

**Exclude**:
- Internal skill templates (e.g., `templates/basic_grpo_training.py`)
- Empty `__init__.py` files
- Scripts that are clearly one-off experiments
- Large data files or binaries masquerading as scripts

**Rule of thumb**: If you'd feel comfortable sharing it with a teammate for reuse, include it.

### Step 3: Copy to Centralized Directory

Create a new summary directory in the skills repo root (or dedicated scripts repo):

```bash
# In ~/.hermes/skills/
mkdir -p scripts-summary

# Copy curated scripts
cp ~/.hermes/scripts/*.py scripts-summary/ 2>/dev/null || true
cp ~/.hermes/scripts/*.sh scripts-summary/ 2>/dev/null || true
cp ~/.hermes/scripts/*.mjs scripts-summary/ 2>/dev/null || true

# Also copy any skill-embedded scripts you identified as useful
# Example: cp ~/.hermes/skills/github/github-auth/scripts/gh-env.sh scripts-summary/
```

**Set executable permissions** (critical for shell scripts):
```bash
chmod +x scripts-summary/*.sh
```

### Step 4: Write Comprehensive README.md

Structure the README with these sections:

```markdown
# [Repository Name] — Scripts Collection

Brief one-liner describing the collection's purpose.

## Table of Contents
- [Category 1](#category-1)
- [Category 2](#category-2)

---

## Category 1 Name

### ScriptName.ext

**用途**: One-sentence purpose

**用法**:
```bash
# Basic usage
./scriptname [args]

# With options
./scriptname --option value /path/to/output
```

**工作原理** (optional): 1-2 sentences on how it works

**依赖**:
- dep1 >= version
- dep2

**关联 Cron Job** (if applicable): Job name — schedule

**注意事项**:
- Known gotchas or prerequisites
- Data source limitations
- Platform requirements (macOS/Linux)

---

## Appendix

### Script Inventory Table
| Script | Purpose | Dependencies | Cron? |
|--------|---------|--------------|-------|
| `daily-report.py` | A-share market report | akshare, pandas | ✅ |
| `cron_monitor.py` | Job health checker | — | ❌ |

### Quick Reference
Common one-liners for daily use.

```

### Step 5: Git Commit & Push

```bash
cd ~/.hermes/skills

# Stage new directory
git add scripts-summary/

# Commit with structured message
git commit -m "Add scripts-summary: centralized utility script repository

- Create scripts-summary/ with 7 curated utility scripts
- Document each script's usage, dependencies, and examples in README.md
- Set executable permissions on shell scripts
- Cover categories: market data, monitoring, watchdog, deployment, testing
"

# Push
git push origin main
```

---

## Key Decisions & Rationale

### Why a `scripts-summary/` subdirectory (not replace `~/.hermes/scripts/`)?
- Preserve existing cron job paths (they reference `~/.hermes/scripts/` directly)
- Non-breaking change — existing workflows continue
- Clear separation: "source of truth" vs "published documentation set"

### Why document **in the repo** instead of separate wiki?
- Versioned alongside code — docs evolve with scripts
- Easier to contribute via PR
- Single source of truth for developers

### Why categorize instead of alphabetical?
- Faster scanning — users look for "monitoring" not "cron_monitor"
- Groups related tools (market data scripts together)
- Better for README table of contents

---

## Common Pitfalls & Tips

### Pitfall 1: Forgetting to set executable bits
Shell scripts copied from elsewhere lose `+x` permission.

**Fix**:
```bash
chmod +x scripts-summary/*.sh
git add --chmod=+x scripts-summary/*.sh  # stage permission change
```

### Pitfall 2: Including skill-internal templates accidentally
Templates inside `templates/` or `references/` subdirectories are usually skill-specific, not general utilities.

**Rule**: Only copy files from `*/scripts/` directories, not `*/templates/` or `*/references/`.

### Pitfall 3: Forgetting to test scripts after copying
Scripts may have hardcoded paths (e.g., `~/market-reports/`).

**Fix**: Spot-check 2-3 key scripts:
```bash
head -5 scripts-summary/cron_monitor.py  # verify shebang + imports
grep -E '\.(py|sh|mjs)$' ~/.hermes/cron_jobs.json  # verify paths still valid
```

### Pitfall 4: README becomes outdated
Scripts change but README doesn't.

**Fix**: When updating a script, make it a habit to also update its README section in the same commit.

---

## Verification Checklist

- [ ] All scripts discovered (checked `~/.hermes/scripts/` + skill `*/scripts/` dirs)
- [ ] Curated list excludes internal templates/experiments
- [ ] Shell scripts have `+x` permission
- [ ] README includes each script with: purpose, usage, dependencies
- [ ] README has categorized table of contents
- [ ] Quick reference table added at bottom
- [ ] Git commit message is structured and descriptive
- [ ] Pushed to remote and verified on GitHub
- [ ] Local `~/.hermes/scripts/` paths still work (no breaking changes)

---

## Example Outcome

**Before**: Scripts scattered, undocumented, only original author knows what they do.

**After**:
```
~/.hermes/skills/
└── scripts-summary/
    ├── README.md                    # Central documentation
    ├── a-share-daily-report.py      # Market data
    ├── cron_monitor.py              # Monitoring
    ├── hermes-watchdog.sh           # Ops
    ├── sync-reports.sh              # Deployment
    └── test_weixin.py               # Testing
```

Team members can now:
1. Read README to understand available tools
2. Run scripts directly from `scripts-summary/`
3. Contribute improvements with clear context

---

## Variations

### A. Separate Scripts Repository
Instead of `scripts-summary/` inside skills repo, create standalone `huidge/hermes-scripts`:
```bash
mkdir ~/projects/hermes-scripts
cp ~/.hermes/scripts/*.py ~/projects/hermes-scripts/
cd ~/projects/hermes-scripts
git init && git remote add origin git@github.com:huidge/hermes-scripts.git
```

Use when: scripts are truly independent, not skill-specific.

### B. Include Usage Examples
Add `examples/` subdirectory with sample invocations:
```
scripts-summary/
├── examples/
│   ├── daily-report-output.md
│   └── cron-monitor-alert.json
```

### C. Add Shell Completions
Include `completions/` with bash/zsh completion scripts for frequently used CLI tools.

---

**Skill Version**: 1.0  
**Last Updated**: 2026-04-24  
**Use Case**: First applied to consolidate ~/.hermes/scripts/ contents into skills repo with full documentation
