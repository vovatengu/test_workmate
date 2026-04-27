from __future__ import annotations

import pytest

from src.reports import ClickbaitReport, ReportRegistry


def test_clickbait_report_filters_correctly(sample_data: list[dict[str, object]]) -> None:
    result = ClickbaitReport().generate(sample_data)  # type: ignore[arg-type]
    titles = {row["title"] for row in result}
    assert titles == {"Video A", "Video D"}


def test_clickbait_report_sorting(sample_data: list[dict[str, object]]) -> None:
    result = ClickbaitReport().generate(sample_data)  # type: ignore[arg-type]
    assert [row["title"] for row in result] == ["Video D", "Video A"]


def test_clickbait_report_row_shape(sample_data: list[dict[str, object]]) -> None:
    result = ClickbaitReport().generate(sample_data)  # type: ignore[arg-type]
    assert result, "ожидаем хотя бы одну строку"
    assert set(result[0].keys()) == {"title", "ctr", "retention_rate"}


@pytest.mark.parametrize(
    ("ctr", "retention", "is_clickbait"),
    [
        (15.1, 39.9, True),
        (15.0, 39.9, False),
        (20.0, 40.0, False),
        (100.0, 0.0, True),
        (0.0, 100.0, False),
    ],
    ids=["just-above", "ctr-on-edge", "retention-on-edge", "extreme-clickbait", "extreme-good"],
)
def test_clickbait_threshold(ctr: float, retention: float, is_clickbait: bool) -> None:
    data = [{"title": "T", "ctr": ctr, "retention_rate": retention}]
    result = ClickbaitReport().generate(data)  # type: ignore[arg-type]
    assert bool(result) is is_clickbait


@pytest.mark.parametrize("name", ["clickbait"])
def test_report_registry_known(name: str) -> None:
    report = ReportRegistry.get_report(name)
    assert isinstance(report, ClickbaitReport)


@pytest.mark.parametrize("name", ["unknown_report", "", "Clickbait", "click_bait"])
def test_report_registry_unknown(name: str) -> None:
    with pytest.raises(ValueError, match="Неизвестный тип отчета"):
        ReportRegistry.get_report(name)


def test_report_registry_available_lists_known() -> None:
    assert "clickbait" in ReportRegistry.available()
