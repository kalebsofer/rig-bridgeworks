---
name: call-debrief
description: Turn Kaleb's notes from a client call into a record, and update the plan for anything that changed.
disable-model-invocation: true
argument-hint: [notes, or path to notes]
---

Process the call notes in $ARGUMENTS.

1. Write `work/call-<YYYY-MM-DD>.md`: decisions, actions with owner and date, new facts, and open questions.
2. Mark what was said versus what we have verified.
3. Compare with `work/fact-register.md` if it exists, and flag anything that contradicts it, or changes scope, dates or priorities.
4. Save durable changes to project memory, leaving out personal data.
5. Tell Kaleb what now needs to be done differently.
