---
name: project-isolation
description: This project is walled off from rig-day, rig-day-sealed and rig-scenario, including their transcripts
metadata:
  type: feedback
---

Confirmed by Kaleb on 2026-11-06: this project is fully walled off from `rig-day`, `rig-day-sealed`, the `rig-scenario` folder and their session transcripts.

**Why:** It is a new project, and only the environment was meant to carry over, not context.

**How to apply:** Deny rules and `.claude/hooks/guard.py` enforce this, but they only stop accidents, so do not work around them.
If something from those folders is needed, Kaleb copies it in himself.
