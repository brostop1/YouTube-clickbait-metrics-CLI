"""Реестр отчётов."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Callable, Type

if TYPE_CHECKING:
    from youtube_cli.reports.base import Report


class ReportRegistry:
    """Маппинг имя отчёта → класс (Strategy + Registry)."""

    _lock = threading.Lock()
    _reports: dict[str, Type["Report"]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[Type["Report"]], Type["Report"]]:
        """Декоратор регистрации отчёта в реестре."""
        normalized = name.strip()
        if not normalized:
            raise ValueError("report name must be a non-empty string")

        def decorator(report_cls: Type["Report"]) -> Type["Report"]:
            with cls._lock:
                if normalized in cls._reports:
                    existing = cls._reports[normalized]
                    raise ValueError(
                        f"report '{normalized}' already registered: {existing.__name__}"
                    )
                cls._reports[normalized] = report_cls
            return report_cls

        return decorator

    @classmethod
    def get(cls, name: str) -> Type[Report]:
        normalized = name.strip()
        if not normalized:
            raise ValueError("report name must be a non-empty string")

        with cls._lock:
            report_cls = cls._reports.get(normalized)
            available = sorted(cls._reports.keys())

        if report_cls is None:
            available_str = ", ".join(available) if available else "<none>"
            raise ValueError(f"unknown report '{normalized}'. Available: {available_str}")

        return report_cls

    @classmethod
    def list_available(cls) -> list[str]:
        with cls._lock:
            return sorted(cls._reports.keys())
