# YouTube Video Metrics Reporter

CLI приложение для обработки CSV-файлов с метриками видео и формирования отчетов.

## Установка
```bash
pip install -r requirements.txt
```

## Запуск
```bash
python app.py --files data/stats1.csv data/stats2.csv --report clickbait
```

## Тесты
```bash
pytest tests/ --cov=src
```
