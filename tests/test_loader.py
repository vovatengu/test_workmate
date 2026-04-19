import pytest
from src.loader import load_csv_files, FileLoadError

def test_load_csv_files_success(csv_file_content):
    data = load_csv_files([csv_file_content])
    assert len(data) == 1
    assert data[0]['title'] == 'Test Vid'
    assert isinstance(data[0]['ctr'], float)

def test_load_csv_files_not_found():
    with pytest.raises(FileLoadError):
        load_csv_files(['non_existent_file.csv'])
