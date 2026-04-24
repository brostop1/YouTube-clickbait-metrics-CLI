"""Тесты cli/parser.py."""

from __future__ import annotations

import pytest

from youtube_cli.cli.parser import parse_args


def test_parser_requires_files_and_report() -> None:
    with pytest.raises(SystemExit) as exc:
        parse_args([])
    assert exc.value.code == 2


def test_parser_unknown_report_rejected() -> None:
    with pytest.raises(SystemExit) as exc:
        parse_args(["--files", "fixtures/valid.csv", "--report", "__nope__"])
    assert exc.value.code == 2


def test_parser_accepts_clickbait() -> None:
    ns = parse_args(["--files", "fixtures/valid.csv", "--report", "clickbait"])
    assert ns.report == "clickbait"
    assert ns.files == ["fixtures/valid.csv"]
