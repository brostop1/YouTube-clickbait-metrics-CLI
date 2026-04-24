"""Доменные модели метрик видео."""

from __future__ import annotations

from dataclasses import dataclass

# Диапазоны для процентных метрик (как в CSV: 0–100).
CTR_MIN: float = 0.0
CTR_MAX: float = 100.0
RETENTION_RATE_MIN: float = 0.0
RETENTION_RATE_MAX: float = 100.0

# Колонки CSV, необходимые для построения VideoMetric (единый источник для loader).
REQUIRED_CSV_COLUMNS: tuple[str, ...] = (
    "title",
    "ctr",
    "retention_rate",
    "views",
    "likes",
    "avg_watch_time",
)


@dataclass(frozen=True)
class VideoMetric:
    """Метрики одного видео после успешного парсинга строки CSV."""

    title: str
    ctr: float
    retention_rate: float
    views: int
    likes: int
    avg_watch_time: float

    def __post_init__(self) -> None:
        if not self.title.strip():
            msg = "title must be a non-empty string"
            raise ValueError(msg)
        if not CTR_MIN <= self.ctr <= CTR_MAX:
            msg = f"ctr must be between {CTR_MIN} and {CTR_MAX}, got {self.ctr!r}"
            raise ValueError(msg)
        if not RETENTION_RATE_MIN <= self.retention_rate <= RETENTION_RATE_MAX:
            msg = (
                "retention_rate must be between "
                f"{RETENTION_RATE_MIN} and {RETENTION_RATE_MAX}, "
                f"got {self.retention_rate!r}"
            )
            raise ValueError(msg)
        if self.views < 0:
            msg = "views must be >= 0"
            raise ValueError(msg)
        if self.likes < 0:
            msg = "likes must be >= 0"
            raise ValueError(msg)
        if self.avg_watch_time < 0:
            msg = "avg_watch_time must be >= 0"
            raise ValueError(msg)
