"""Тесты валидации VideoMetric."""

from __future__ import annotations

import pytest

from youtube_cli.data.models import VideoMetric


def _valid() -> VideoMetric:
    return VideoMetric(
        title="Sample",
        ctr=12.5,
        retention_rate=55.0,
        views=1000,
        likes=50,
        avg_watch_time=4.2,
    )


def test_video_metric_valid() -> None:
    v = _valid()
    assert v.title == "Sample"
    assert v.ctr == 12.5


def test_video_metric_boundary_ctr() -> None:
    VideoMetric("t", 0.0, 50.0, 0, 0, 1.0)
    VideoMetric("t", 100.0, 50.0, 0, 0, 1.0)


def test_video_metric_boundary_retention() -> None:
    VideoMetric("t", 10.0, 0.0, 0, 0, 1.0)
    VideoMetric("t", 10.0, 100.0, 0, 0, 1.0)


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"title": "", "ctr": 1.0, "retention_rate": 1.0, "views": 1, "likes": 0, "avg_watch_time": 1.0}, "title"),
        ({"title": "   ", "ctr": 1.0, "retention_rate": 1.0, "views": 1, "likes": 0, "avg_watch_time": 1.0}, "title"),
        ({"title": "t", "ctr": -0.1, "retention_rate": 1.0, "views": 0, "likes": 0, "avg_watch_time": 1.0}, "ctr"),
        ({"title": "t", "ctr": 100.1, "retention_rate": 1.0, "views": 0, "likes": 0, "avg_watch_time": 1.0}, "ctr"),
        ({"title": "t", "ctr": 1.0, "retention_rate": -1.0, "views": 0, "likes": 0, "avg_watch_time": 1.0}, "retention_rate"),
        ({"title": "t", "ctr": 1.0, "retention_rate": 100.1, "views": 0, "likes": 0, "avg_watch_time": 1.0}, "retention_rate"),
        ({"title": "t", "ctr": 1.0, "retention_rate": 1.0, "views": -1, "likes": 0, "avg_watch_time": 1.0}, "views"),
        ({"title": "t", "ctr": 1.0, "retention_rate": 1.0, "views": 0, "likes": -1, "avg_watch_time": 1.0}, "likes"),
        ({"title": "t", "ctr": 1.0, "retention_rate": 1.0, "views": 0, "likes": 0, "avg_watch_time": -0.1}, "avg_watch_time"),
    ],
)
def test_video_metric_validation_errors(kwargs: dict, match: str) -> None:
    base = {
        "title": "t",
        "ctr": 1.0,
        "retention_rate": 50.0,
        "views": 0,
        "likes": 0,
        "avg_watch_time": 1.0,
    }
    base.update(kwargs)
    with pytest.raises(ValueError, match=match):
        VideoMetric(**base)
