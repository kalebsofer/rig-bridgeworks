---
name: data-query
description: Use when answering any question from the BridgeWorks extracts - counts, joins, duplicates, snapshot history, match rates - or when exploring the CSVs under docs/pack.
allowed-tools: Bash(uv run *)
---

# Data query

Query the extracts through `tools/q.py`, which is read-only and returns a count, minified JSON and a next step.

```bash
uv run python tools/q.py --tables
uv run python tools/q.py "SELECT count(*) FROM some_extract"
```

Kaleb's notebooks use the same views through `tools/extracts.py`, starting from `work/01_eda.ipynb` with `uv run jupyter lab work/01_eda.ipynb`.
Each CSV under `docs/pack/` is a view named after its file, so `--tables` lists what exists.
Every column is VARCHAR, so cast deliberately and check what fails to parse with `TRY_CAST` or `TRY_STRPTIME`.

## Workflow

1. Read any README alongside the extracts and run `--tables`.
2. Profile before answering: nulls, distinct keys, value formats.
3. Select only the columns you need, and aggregate personal fields rather than listing them.
4. Once a number matters, move the query into a script in `work/` so it can be re-derived.
5. Have `number-verifier` check it before it goes in any deliverable.
