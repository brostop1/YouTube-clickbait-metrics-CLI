"""Тесты reports/clickbait.py."""

from __future__ import annotations

from youtube_cli.data.models import VideoMetric
from youtube_cli.reports.clickbait import ClickbaitReport


def test_clickbait_filters_strict_thresholds() -> None:
    report = ClickbaitReport()

    rows = [
        VideoMetric("ok", 15.0, 39.9, 0, 0, 1.0),  # ctr not > 15
        VideoMetric("ok", 15.1, 40.0, 0, 0, 1.0),  # retention not < 40
        VideoMetric("hit", 15.1, 39.9, 0, 0, 1.0),  # should pass
    ]

    filtered = report.filter(rows)
    assert [r.title for r in filtered] == ["hit"]


def test_clickbait_sort_by_ctr_desc() -> None:
    report = ClickbaitReport()

    rows = [
        VideoMetric("a", 16.0, 10.0, 0, 0, 1.0),
        VideoMetric("b", 30.0, 10.0, 0, 0, 1.0),
        VideoMetric("c", 20.0, 10.0, 0, 0, 1.0),
    ]

    sorted_rows = report.sort(rows)
    assert [r.title for r in sorted_rows] == ["b", "c", "a"]


def test_clickbait_run_empty() -> None:
    report = ClickbaitReport()
    assert report.run([]) == []
