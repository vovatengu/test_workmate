from __future__ import annotations

import logging
from unittest.mock import patch

import pytest

from app import main


@patch("sys.argv", ["app.py", "--files", "data/stats1.csv", "--report", "clickbait"])
def test_main_runs_successfully(capsys: pytest.CaptureFixture[str]) -> None:
    try:
        main()
    except SystemExit as exc:
        if exc.code != 0:
            raise
    captured = capsys.readouterr()
    assert "Секрет который скрывают тимлиды" in captured.out


@pytest.mark.parametrize(
    ("argv", "expected_in_log"),
    [
        (
            ["app.py", "--files", "missing.csv", "--report", "clickbait"],
            "Файл не найден",
        ),
        (
            ["app.py", "--files", "data/stats1.csv", "--report", "unknown"],
            "Неизвестный тип отчета",
        ),
    ],
    ids=["missing-file", "unknown-report"],
)
def test_main_error_paths(
    argv: list[str],
    expected_in_log: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    with (
        caplog.at_level(logging.ERROR),
        patch("sys.argv", argv),
        pytest.raises(SystemExit) as exc_info,
    ):
        main()
    assert exc_info.value.code == 1
    assert expected_in_log in caplog.text
