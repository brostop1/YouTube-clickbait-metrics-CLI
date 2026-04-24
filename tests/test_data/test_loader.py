"""Тесты data/loader.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from youtube_cli.data.loader import load_videos_from_files


def test_load_valid_csv_from_fixtures() -> None:
    rows = load_videos_from_files([Path("fixtures/valid.csv")])
    assert len(rows) == 9
    
    first = rows[0]
    assert first.title == "Я бросил IT и стал фермером"
    assert first.ctr == 22.5
    assert first.retention_rate == 35
    assert first.views == 45200
    assert first.likes == 1240
    assert first.avg_watch_time == 4.2

def test_load_multiple_files_aggregates() -> None:
    rows = load_videos_from_files([Path("fixtures/valid.csv"), Path("fixtures/valid.csv")])
    assert len(rows) == 18


def test_missing_required_column_raises_value_error() -> None:
    with pytest.raises(ValueError, match="missing required column"):
        load_videos_from_files([Path("fixtures/invalid_missing_col.csv")])


def test_file_not_found_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_videos_from_files([Path("fixtures/does_not_exist.csv")])


def test_invalid_numeric_raises(tmp_path: Path) -> None:
    p = tmp_path / "bad.csv"
    p.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "t,10.0,50.0,not_an_int,1,4.2\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=r"row 2"):
        load_videos_from_files([p])
