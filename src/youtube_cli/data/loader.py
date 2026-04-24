"""Загрузка и валидация CSV → List[VideoMetric]."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import TYPE_CHECKING

from youtube_cli.data.models import REQUIRED_CSV_COLUMNS, VideoMetric

if TYPE_CHECKING:
    from collections.abc import Iterable


def _validate_columns(fieldnames: list[str] | None, *, path: Path) -> None:
    if not fieldnames:
        raise ValueError(f"CSV file {path} has no header row")

    missing = [col for col in REQUIRED_CSV_COLUMNS if col not in fieldnames]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"CSV file {path} is missing required column(s): {missing_str}")


def _parse_row(row: dict[str, str], *, path: Path, row_number: int) -> VideoMetric:
    def req(col: str) -> str:
        value = row.get(col, "")
        if value is None:
            value = ""
        value = value.strip()
        if value == "":
            raise ValueError(f"missing value for column '{col}'")
        return value

    try:
        return VideoMetric(
            title=req("title"),
            ctr=float(req("ctr")),
            retention_rate=float(req("retention_rate")),
            views=int(req("views")),
            likes=int(req("likes")),
            avg_watch_time=float(req("avg_watch_time")),
        )
    except Exception as exc:  # noqa: BLE001 - превращаем в читаемую ошибку
        raise ValueError(f"{path}: row {row_number}: {exc}") from exc


def load_videos_from_files(paths: list[Path]) -> list[VideoMetric]:
    """Читает несколько CSV и возвращает список метрик по всем строкам."""
    if not paths:
        raise ValueError("no input files provided")

    all_rows: list[VideoMetric] = []

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        if not path.is_file():
            raise ValueError(f"not a file: {path}")

        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            _validate_columns(reader.fieldnames, path=path)

            for idx, row in enumerate(reader, start=2):
                if row is None:
                    continue
                # DictReader может вернуть {col: None, ...} для пустых строк.
                if all((v is None or str(v).strip() == "") for v in row.values()):
                    continue
                all_rows.append(_parse_row(row, path=path, row_number=idx))

    return all_rows
