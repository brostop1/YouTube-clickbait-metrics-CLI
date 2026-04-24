"""Отчёты (Strategy + Registry).

Импорты ниже важны: они регистрируют отчёты в `ReportRegistry`.
"""

from youtube_cli.reports.clickbait import ClickbaitReport as ClickbaitReport

__all__ = ["ClickbaitReport"]
