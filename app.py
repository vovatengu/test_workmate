import argparse
import sys
from tabulate import tabulate

from src.loader import load_csv_files, FileLoadError
from src.reports import ReportRegistry


def main():
    parser = argparse.ArgumentParser(description="Утилита для формирования отчетов по метрикам видео")
    parser.add_argument('--files', nargs='+', required=True, help='Список CSV файлов для анализа')
    parser.add_argument('--report', required=True, help='Название типа отчета (например: clickbait)')

    args = parser.parse_args()

    try:
        # 1. Загрузка данных
        data = load_csv_files(args.files)

        # 2. Получение объекта отчета
        report_processor = ReportRegistry.get_report(args.report)

        # 3. Генерация данных отчета
        report_data = report_processor.generate(data)

        # 4. Вывод в консоль
        print(tabulate(report_data, headers="keys", tablefmt="grid", floatfmt=".1f"))

    except FileLoadError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
