import pytest
from src.reports import ClickbaitReport, ReportRegistry

def test_clickbait_report_filters_correctly(sample_data):
    report = ClickbaitReport()
    result = report.generate(sample_data)
    assert len(result) == 2
    titles = [r['title'] for r in result]
    assert 'Video A' in titles
    assert 'Video D' in titles
    assert 'Video B' not in titles
    assert 'Video C' not in titles

def test_clickbait_report_sorting(sample_data):
    report = ClickbaitReport()
    result = report.generate(sample_data)
    assert result[0]['title'] == 'Video D'
    assert result[1]['title'] == 'Video A'

def test_report_registry():
    report = ReportRegistry.get_report('clickbait')
    assert isinstance(report, ClickbaitReport)

def test_report_registry_unknown():
    with pytest.raises(ValueError):
        ReportRegistry.get_report('unknown_report')
