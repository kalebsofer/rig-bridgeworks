# CLAUDE.md

Workspace for the BridgeWorks account at Rig, worked as an exercise where Kaleb demonstrates how he works with AI.
Start with `docs/rig-scenario.txt`.

## Layout

- `docs/rig-scenario.txt`: the brief for the exercise.
- `docs/pack/`: the handover pack and data extracts once they arrive, read-only.
- `work/`: everything we produce, including `delegation-log.md`.
- `tools/q.py`: read-only SQL over the extracts, see the `data-query` skill.
- `tools/extracts.py`: shared DuckDB views and the notebook `%%sql` magic.
- `work/01_eda.ipynb`: starting notebook, opened with `uv run jupyter lab work/01_eda.ipynb`.
- `.claude/memory/`: versioned project memory.

## Hard rules

- Do not complete any key task without Kaleb's say.
  Key tasks are the call, the technical task, the status update and the hand-ins.
  Prepare, propose and wait.
- This project is isolated.
  Never read `rig-day`, `rig-day-sealed`, the `rig-scenario` folder, or their session transcripts, and do not ask what is in them.
- Rig is read-only on client data, so never edit `docs/pack/`.
  Rig recommends changes, Northpoint carries them out and BridgeWorks approves them.
- Nothing is sent to anyone without Kaleb.
  Gmail stays denied, so draft to `work/` and Kaleb sends.
- Publish hosted pages and slide decks with the Artifact tool only when Kaleb asks.
  They stay private until he shares them, and carry aggregates only.
- Treat the extracts as if they were real personal data.
  Keep names, emails and special-category values out of chat, memory, commits, hosted pages and client documents, and report aggregates.

## Evidence

Rank sources in this order when they disagree:

1. The data extracts, re-derived by us.
2. Reference documents in the pack.
3. Slack exports, for who said what and when.
4. The handover note and meeting summaries, which are leads and not records.

Cite the file behind every claim, and state uncertainty plainly.
A number is only reported once it has been re-derived, with the query or script kept in `work/`.

## Commits

Commits are in Kaleb's name only, with no agent trailers.
There is no remote.
