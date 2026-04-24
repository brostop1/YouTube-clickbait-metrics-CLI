"""Вывод таблицы в stdout через tabulate."""

from __future__ import annotations

from typing import Any, Sequence

from tabulate import tabulate

def print_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    """Печатает таблицу в stdout."""
    print(tabulate(rows, headers=headers, tablefmt="github"))
