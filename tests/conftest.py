import pytest
import csv

@pytest.fixture
def sample_data():
    return [
        {'title': 'Video A', 'ctr': 18.2, 'retention_rate': 35.0, 'views': 100},
        {'title': 'Video B', 'ctr': 10.0, 'retention_rate': 30.0, 'views': 200},
        {'title': 'Video C', 'ctr': 20.0, 'retention_rate': 50.0, 'views': 300},
        {'title': 'Video D', 'ctr': 25.0, 'retention_rate': 20.0, 'views': 400},
    ]

@pytest.fixture
def csv_file_content(tmp_path):
    file_path = tmp_path / "test.csv"
    data = [
        {'title': 'Test Vid', 'ctr': '18.5', 'retention_rate': '30.0', 'views': '100', 'likes': '10', 'avg_watch_time': '5.0'}
    ]
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'ctr', 'retention_rate', 'views', 'likes', 'avg_watch_time'])
        writer.writeheader()
        writer.writerows(data)
    return str(file_path)
