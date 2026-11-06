from pathlib import Path

import pytest

import extracts


@pytest.fixture
def data(tmp_path, monkeypatch):
    monkeypatch.setenv("RIG_DATA_DIR", str(tmp_path))
    (tmp_path / "sub").mkdir()
    (tmp_path / "2024 Some-Export.csv").write_text("id,when\n001,2026-01-02\n002,\n")
    (tmp_path / "sub" / "other.csv").write_text("id\n001\n")
    return tmp_path


def test_view_names_are_valid_identifiers():
    assert extracts.view_name(Path("2024 Some-Export.csv")) == "t_2024_some_export"
    assert extracts.view_name(Path("Plain.csv")) == "plain"


def test_discover_finds_nested_csvs(data):
    assert set(extracts.discover()) == {"t_2024_some_export", "other"}


def test_discover_rejects_colliding_names(data):
    (data / "other-.csv").write_text("id\n")
    with pytest.raises(ValueError, match="both map to other"):
        extracts.discover()


def test_columns_stay_text_so_leading_zeros_survive(data):
    con = extracts.connect(extracts.discover())
    assert con.execute("SELECT min(id) FROM t_2024_some_export").fetchone()[0] == "001"


def test_overview_counts_rows_and_columns(data):
    views = extracts.discover()
    frame = extracts.overview(extracts.connect(views), views).set_index("view")
    assert frame.loc["t_2024_some_export", "rows"] == 2
    assert frame.loc["t_2024_some_export", "columns"] == 2


def test_overview_handles_no_extracts(tmp_path, monkeypatch):
    monkeypatch.setenv("RIG_DATA_DIR", str(tmp_path))
    views = extracts.discover()
    assert views == {}
    assert len(extracts.overview(extracts.connect(views), views)) == 0


def test_profile_is_exact_and_returns_no_values(data):
    views = extracts.discover()
    frame = extracts.profile(extracts.connect(views), "t_2024_some_export")
    assert list(frame.columns) == ["column_name", "rows", "null_pct", "distinct_values"]
    assert list(frame["column_name"]) == ["id", "when"]
    assert list(frame["distinct_values"]) == [2, 1]
    assert list(frame["null_pct"]) == [0.0, 50.0]


def test_profile_counts_duplicate_keys_exactly(tmp_path, monkeypatch):
    monkeypatch.setenv("RIG_DATA_DIR", str(tmp_path))
    rows = "".join(f"{i:06d}\n" for i in range(50_000))
    (tmp_path / "keys.csv").write_text("id\n" + rows + "000000\n")
    views = extracts.discover()
    frame = extracts.profile(extracts.connect(views), "keys")
    assert frame.loc[0, "rows"] == 50_001
    assert frame.loc[0, "distinct_values"] == 50_000
