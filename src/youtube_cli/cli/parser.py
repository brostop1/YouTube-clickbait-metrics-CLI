"""Разбор аргументов командной строки."""

from __future__ import annotations

import argparse
from argparse import Namespace

import youtube_cli.reports  # noqa: F401 - импорт для регистрации отчётов
from youtube_cli.reports.registry import ReportRegistry

def build_parser() -> argparse.ArgumentParser:
    """Возвращает настроенный парсер."""

    def report_name(value: str) -> str:
        value = value.strip()
        if not value:
            raise argparse.ArgumentTypeError("report name must be non-empty")
        available = ReportRegistry.list_available()
        if value not in available:
            available_str = ", ".join(available) if available else "<none>"
            raise argparse.ArgumentTypeError(
                f"unknown report '{value}'. Available: {available_str}"
            )
        return value

    parser = argparse.ArgumentParser(prog="youtube-cli")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to one or more CSV files",
    )
    parser.add_argument(
        "--report",
        required=True,
        type=report_name,
        help="Report name",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> Namespace:
    """Парсит argv и возвращает Namespace."""
    return build_parser().parse_args(argv)
