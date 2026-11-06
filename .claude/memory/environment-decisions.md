---
name: environment-decisions
description: Why there is no data MCP and how project memory is configured
metadata:
  type: project
---

There is no data MCP.
Queries run through `tools/q.py` on DuckDB, so they stay in the code that gets handed in.

JupySQL was removed on 2026-11-06 because it sends telemetry to PostHog through `ploomber-core`, and its JupyterLab extension is incompatible with Lab 4.6.
Notebooks use the small `%%sql` magic in `tools/extracts.py` instead, so check new dependencies for analytics clients before adding them.

Memory lives in `.claude/memory/` through `autoMemoryDirectory` in `.claude/settings.json`, so the path depends on the folder being `~/Code/rig-bridgeworks`.
The setting has had reports of being ignored, so if `/memory` shows another path, fall back to `~/Code/agent-config/link-claude-memory.sh`.

**How to apply:** Do not propose an MCP for the extracts.
