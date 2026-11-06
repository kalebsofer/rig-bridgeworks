"""Read-only SQL over the pack extracts, for agents.

    uv run python tools/q.py --tables
    uv run python tools/q.py "SELECT count(*) FROM some_extract"
    uv run python tools/q.py --limit 200 --full "SELECT ..."

See tools/extracts.py for how the CSVs become views.
Prints a one-line aggregate, minified JSON rows, then a likely next command.
"""
import argparse
import json
import re
import sys

import duckdb

from extracts import connect, data_dir, discover

MAX_CELL = 120


def fail(code, message):
    print(json.dumps({"error": code, "message": message}, separators=(",", ":")), file=sys.stderr)
    sys.exit(2)


def cell(value, full):
    if isinstance(value, str) and not full and len(value) > MAX_CELL:
        return f"{value[:MAX_CELL]}...[{len(value)} chars]"
    if value is None or isinstance(value, (int, float, bool, str)):
        return value
    return str(value)


def show_tables(con, views):
    out = {}
    for view in views:
        columns = [row[0] for row in con.execute(f"DESCRIBE {view}").fetchall()]
        rows = con.execute(f"SELECT count(*) FROM {view}").fetchone()[0]
        out[view] = {"rows": rows, "columns": columns}
    print(f"{len(out)} views")
    print(json.dumps(out, separators=(",", ":")))
    if out:
        print(f'next: uv run python tools/q.py "SELECT ... FROM {next(iter(out))}"')
    else:
        print(f"next: add the CSV extracts under {data_dir().as_posix()}, then rerun --tables")


def run_query(con, sql, limit, full):
    sql = sql.strip().rstrip(";")
    writes = re.search(r"(?i)\b(copy|export|attach|install|load)\b", sql)
    if not re.match(r"(?is)^(select|with)\b", sql) or ";" in sql or writes:
        fail("read_only", "one SELECT or WITH statement only")
    try:
        cursor = con.execute(sql)
        names = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
    except duckdb.Error as exc:
        fail("sql_error", str(exc))

    shown = rows[:limit]
    suffix = f", showing {len(shown)}" if len(shown) < len(rows) else ""
    print(f"{len(rows)} results{suffix}")
    records = [dict(zip(names, (cell(v, full) for v in row))) for row in shown]
    print(json.dumps(records, separators=(",", ":")))
    if len(shown) < len(rows):
        print(f"next: rerun with --limit {len(rows)}, or aggregate in SQL")
    else:
        print("next: save the final query under work/ so the number can be re-derived")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sql", nargs="?")
    parser.add_argument("--tables", action="store_true")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    try:
        views = discover()
    except ValueError as exc:
        fail("duplicate_view", str(exc))
    con = connect(views)
    if args.tables:
        show_tables(con, views)
    elif not args.sql:
        fail("no_sql", "pass a SELECT or WITH statement, or --tables")
    elif not views:
        fail("no_extracts", f"no CSV files under {data_dir().as_posix()}")
    else:
        run_query(con, args.sql, args.limit, args.full)


if __name__ == "__main__":
    main()
