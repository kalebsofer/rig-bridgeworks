"""Shared DuckDB access to the pack extracts, used by tools/q.py and notebooks.

Each CSV under docs/pack becomes a view named after its file, with every column
as VARCHAR so mixed date formats and leading zeros survive. Cast explicitly.
Set RIG_DATA_DIR to read the extracts from another folder.

In a notebook, setup() returns a connection and registers the %%sql cell magic:

    %%sql
    SELECT count(*) FROM some_extract

    %%sql result
    SELECT ...          <- also saves the DataFrame as `result`
"""
import os
import re
from pathlib import Path

import duckdb


def data_dir():
    default = Path(__file__).resolve().parent.parent / "docs" / "pack"
    return Path(os.environ.get("RIG_DATA_DIR") or default)


def view_name(path):
    name = re.sub(r"\W+", "_", path.stem).strip("_").lower()
    return f"t_{name}" if name[:1].isdigit() else name


def discover():
    views = {}
    for path in sorted(data_dir().rglob("*.csv")):
        view = view_name(path)
        if view in views:
            raise ValueError(f"{views[view].as_posix()} and {path.as_posix()} both map to {view}")
        views[view] = path
    return views


def connect(views):
    con = duckdb.connect(":memory:")
    for view, path in views.items():
        quoted = path.as_posix().replace("'", "''")
        con.execute(
            f"CREATE VIEW {view} AS SELECT * FROM "
            f"read_csv('{quoted}', header=true, all_varchar=true)"
        )
    return con


def overview(con, views):
    """Rows and columns per view, as a DataFrame."""
    parts = [
        f"SELECT '{view}' AS view, count(*) AS rows, "
        f"(SELECT count(*) FROM (DESCRIBE {view})) AS columns FROM {view}"
        for view in views
    ]
    sql = " UNION ALL ".join(parts) or "SELECT NULL AS view, 0 AS rows, 0 AS columns WHERE false"
    return con.sql(sql).df()


def profile(con, view):
    """Row count, null rate and exact distinct count per column, without any values.

    This avoids SUMMARIZE for two reasons: its approx_unique is an estimate that
    can hide duplicate keys, and its min and max expose values from personal fields.
    """
    columns = [row[0] for row in con.execute(f"DESCRIBE {view}").fetchall()]
    parts = []
    for position, column in enumerate(columns):
        label = column.replace("'", "''")
        quoted = '"' + column.replace('"', '""') + '"'
        parts.append(
            f"SELECT {position} AS position, '{label}' AS column_name, count(*) AS rows, "
            f"round(100.0 * (count(*) - count({quoted})) / nullif(count(*), 0), 2) AS null_pct, "
            f"count(DISTINCT {quoted}) AS distinct_values FROM {view}"
        )
    sql = " UNION ALL ".join(parts)
    return con.sql(
        f"SELECT column_name, rows, null_pct, distinct_values FROM ({sql}) ORDER BY position"
    ).df()


def register_sql_magic(con):
    from IPython import get_ipython

    shell = get_ipython()

    def sql(line, cell):
        relation = con.sql(cell)
        if relation is None:
            return None
        frame = relation.df()
        if line.strip():
            shell.user_ns[line.strip()] = frame
        return frame

    shell.register_magic_function(sql, magic_kind="cell", magic_name="sql")


def setup():
    """Connect to the extracts for a notebook. Returns (con, views)."""
    views = discover()
    con = connect(views)
    register_sql_magic(con)
    print(f"{len(views)} views from {data_dir().as_posix()}")
    if not views:
        print("next: add the CSV extracts there, then rerun this cell")
    return con, views
