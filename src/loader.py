from __future__ import annotations

import csv
import logging
from typing import TypedDict

logger = logging.getLogger(__name__)


class VideoRecord(TypedDict):
    """Структура одной строки CSV с метриками видео."""

    title: str
    ctr: float
    retention_rate: float
    views: str
    likes: str
    avg_watch_time: str


class FileLoadError(Exception):
    """Ошибка чтения/разбора CSV-файла."""


_NUMERIC_FIELDS: tuple[str, ...] = ("ctr", "retention_rate")


def _parse_row(row: dict[str, str]) -> VideoRecord | None:
    try:
        for field in _NUMERIC_FIELDS:
            row[field] = float(row[field])
    except (ValueError, KeyError) as exc:
        logger.warning("Пропущена строка с некорректными данными: %s (%s)", row, exc)
        return None
    return row  # type: ignore[return-value]


def load_csv_files(file_paths: list[str]) -> list[VideoRecord]:
    """Загружает и объединяет данные из CSV-файлов.

    Невалидные строки пропускаются с записью в лог.
    """
    data: list[VideoRecord] = []
    for file_path in file_paths:
        logger.debug("Читаем файл: %s", file_path)
        try:
            with open(file_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    parsed = _parse_row(row)
                    if parsed is not None:
                        data.append(parsed)
        except FileNotFoundError as exc:
            raise FileLoadError(f"Файл не найден: {file_path}") from exc
        except OSError as exc:
            raise FileLoadError(f"Ошибка при чтении файла {file_path}: {exc}") from exc
    logger.info("Загружено строк: %d из %d файлов", len(data), len(file_paths))
    return data
