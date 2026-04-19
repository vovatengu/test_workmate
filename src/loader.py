import csv
from typing import List, Dict, Any


class FileLoadError(Exception):
    pass


def load_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    data = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        row['ctr'] = float(row['ctr'])
                        row['retention_rate'] = float(row['retention_rate'])
                    except (ValueError, KeyError):
                        continue
                    data.append(row)
        except FileNotFoundError:
            raise FileLoadError(f"Файл не найден: {file_path}")
        except Exception as e:
            raise FileLoadError(f"Ошибка при чтении файла {file_path}: {e}")
    return data
