---
paths:
  - "work/**/*.py"
  - "work/**/*.sql"
  - "work/**/*.ipynb"
  - "tools/**"
---

# Data work

- Load from `docs/pack/` and never write there.
- Parse dates and normalize keys explicitly, and report how many rows each step drops or changes.
- Check key uniqueness before each join, and check row counts after it for fan-out.
- Every reported number has a reconciliation or test showing how we know it is right.
- Saved outputs carry aggregates or IDs, never names, contact details or special-category values.
- Scripts must re-run from a clean checkout with `uv run`.
- Git strips notebook outputs, but they stay on disk, so do not read them back into chat unless they are aggregates.
