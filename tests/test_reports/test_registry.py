"""Тесты reports/registry.py."""

from __future__ import annotations

import pytest

from youtube_cli.reports.base import Report
from youtube_cli.reports.registry import ReportRegistry


def test_register_and_get() -> None:
    name = "__test_report__register_and_get"

    @ReportRegistry.register(name)
    class _R(Report):
        def filter(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def sort(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def get_columns(self) -> list[str]:
            return ["video_id"]

    assert ReportRegistry.get(name) is _R


def test_register_duplicate_raises() -> None:
    name = "__test_report__duplicate"

    @ReportRegistry.register(name)
    class _R1(Report):
        def filter(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def sort(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def get_columns(self) -> list[str]:
            return ["video_id"]

    with pytest.raises(ValueError, match="already registered"):

        @ReportRegistry.register(name)
        class _R2(Report):
            def filter(self, rows):  # type: ignore[no-untyped-def]
                return rows

            def sort(self, rows):  # type: ignore[no-untyped-def]
                return rows

            def get_columns(self) -> list[str]:
                return ["video_id"]

    assert ReportRegistry.get(name) is _R1


def test_get_unknown_report_lists_available() -> None:
    name = "__test_report__available_for_unknown"

    @ReportRegistry.register(name)
    class _R(Report):
        def filter(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def sort(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def get_columns(self) -> list[str]:
            return ["video_id"]

    with pytest.raises(ValueError, match="unknown report"):
        ReportRegistry.get("__does_not_exist__")

    # Сообщение должно помогать пользователю: показать доступные отчёты
    with pytest.raises(ValueError, match="Available"):
        ReportRegistry.get("__does_not_exist__")

    assert _R in [ReportRegistry.get(name)]


def test_list_available_sorted() -> None:
    a = "__test_report__a"
    b = "__test_report__b"

    @ReportRegistry.register(b)
    class _RB(Report):
        def filter(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def sort(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def get_columns(self) -> list[str]:
            return ["video_id"]

    @ReportRegistry.register(a)
    class _RA(Report):
        def filter(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def sort(self, rows):  # type: ignore[no-untyped-def]
            return rows

        def get_columns(self) -> list[str]:
            return ["video_id"]

    available = ReportRegistry.list_available()
    assert a in available and b in available
    assert available == sorted(available)
