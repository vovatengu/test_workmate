from unittest.mock import patch
import pytest
from app import main

@patch('sys.argv', ['app.py', '--files', 'data/stats1.csv', '--report', 'clickbait'])
def test_main_runs_successfully(capsys):
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            raise
    captured = capsys.readouterr()
    assert "Секрет который скрывают тимлиды" in captured.out

@patch('sys.argv', ['app.py', '--files', 'missing.csv', '--report', 'clickbait'])
def test_main_file_not_found(capsys):
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Файл не найден" in captured.err

@patch('sys.argv', ['app.py', '--files', 'data/stats1.csv', '--report', 'unknown'])
def test_main_unknown_report(capsys):
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Неизвестный тип отчета" in captured.err
