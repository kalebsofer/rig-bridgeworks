#!/usr/bin/env bash
# Sets up this workspace on this machine. Safe to re-run.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "== git"
if [ -d .git ]; then
  echo "   ok"
else
  git init --quiet -b main
  echo "   initialized"
fi

echo "== python"
uv sync --quiet
echo "   ok"

echo "== notebook output stripping"
uv run nbstripout --install --attributes .gitattributes
git config --get filter.nbstripout.clean > /dev/null
echo "   ok"

echo "== extracts"
uv run python tools/q.py --tables | sed -n 1p
echo "== done. Next: uv run jupyter lab work/01_eda.ipynb"
