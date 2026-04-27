from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Protocol

from src.loader import VideoRecord


@dataclass(frozen=True, slots=True)
class ClickbaitRow:
    """DTO одной строки отчёта по «кликбейтным» видео."""

    title: str
    ctr: float
    retention_rate: float


class Report(Protocol):
    """Контракт отчёта: принимает данные, возвращает строки таблицы."""

    def generate(self, data: list[VideoRecord]) -> list[dict[str, object]]: ...


class ClickbaitReport:
    """Отчёт о видео с высоким CTR и низким удержанием."""

    CTR_THRESHOLD: float = 15.0
    RETENTION_THRESHOLD: float = 40.0

    def generate(self, data: list[VideoRecord]) -> list[dict[str, object]]:
        filtered = [
            ClickbaitRow(
                title=row["title"],
                ctr=row["ctr"],
                retention_rate=row["retention_rate"],
            )
            for row in data
            if row["ctr"] > self.CTR_THRESHOLD and row["retention_rate"] < self.RETENTION_THRESHOLD
        ]
        filtered.sort(key=lambda r: r.ctr, reverse=True)
        return [asdict(row) for row in filtered]


class ReportRegistry:
    """Реестр доступных отчётов по их строковому имени."""

    _reports: dict[str, type[Report]] = {
        "clickbait": ClickbaitReport,
    }

    @classmethod
    def get_report(cls, report_name: str) -> Report:
        report_class = cls._reports.get(report_name)
        if report_class is None:
            raise ValueError(f"Неизвестный тип отчета: {report_name}")
        return report_class()

    @classmethod
    def available(cls) -> list[str]:
        return sorted(cls._reports)
