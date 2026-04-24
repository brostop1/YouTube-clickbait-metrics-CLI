"""Базовый класс отчёта."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from youtube_cli.data.models import VideoMetric


class Report(ABC):
    """Абстрактная стратегия отчёта."""

    @abstractmethod
    def filter(self, rows: list[VideoMetric]) -> list[VideoMetric]:
        """Возвращает отфильтрованные строки."""

    @abstractmethod
    def sort(self, rows: list[VideoMetric]) -> list[VideoMetric]:
        """Возвращает отсортированные строки."""

    @abstractmethod
    def get_columns(self) -> list[str]:
        """Имена колонок для табличного вывода."""

    def run(self, rows: list[VideoMetric]) -> list[list[Any]]:
        """filter → sort → строки для tabulate."""
        filtered = self.filter(rows)
        sorted_rows = self.sort(filtered)
        columns = self.get_columns()

        out: list[list[Any]] = []
        for r in sorted_rows:
            out.append([getattr(r, col) for col in columns])
        return out
