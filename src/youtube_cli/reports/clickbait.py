"""Отчёт clickbait: ctr > 15 и retention_rate < 40, сортировка по ctr ↓."""

from __future__ import annotations

from typing import TYPE_CHECKING

from youtube_cli.reports.base import Report
from youtube_cli.reports.registry import ReportRegistry

if TYPE_CHECKING:
    from youtube_cli.data.models import VideoMetric


@ReportRegistry.register("clickbait")
class ClickbaitReport(Report):
    """Видео с высоким CTR и низким удержанием."""

    def filter(self, rows: list[VideoMetric]) -> list[VideoMetric]:
        return [r for r in rows if r.ctr > 15 and r.retention_rate < 40]

    def sort(self, rows: list[VideoMetric]) -> list[VideoMetric]:
        return sorted(rows, key=lambda r: r.ctr, reverse=True)

    def get_columns(self) -> list[str]:
        return ["title", "ctr", "retention_rate", "views", "likes", "avg_watch_time"]
