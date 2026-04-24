"""Точка входа приложения."""

from __future__ import annotations

import sys
from pathlib import Path

from youtube_cli.cli.parser import parse_args
from youtube_cli.data.loader import load_videos_from_files
import youtube_cli.reports  # noqa: F401 - регистрация отчётов
from youtube_cli.reports.registry import ReportRegistry
from youtube_cli.utils.output import print_table


def main(argv: list[str] | None = None) -> int:
    """Оркестрация CLI.

    Возвращает код выхода: 0 (ok), 1 (ошибка выполнения), 2 (ошибка аргументов).
    """
    try:
        args = parse_args(argv)
        paths = [Path(p) for p in args.files]
        rows = load_videos_from_files(paths)

        report_cls = ReportRegistry.get(args.report)
        report = report_cls()

        headers = report.get_columns()
        table_rows = report.run(rows)
        print_table(headers, table_rows)
        return 0
    except SystemExit as exc:
        # argparse уже печатает сообщение и использует код 2.
        code = exc.code if isinstance(exc.code, int) else 1
        return code
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
