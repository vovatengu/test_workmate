from __future__ import annotations

import argparse
import logging
import sys

from tabulate import tabulate

from src.loader import FileLoadError, load_csv_files
from src.reports import ReportRegistry

logger = logging.getLogger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Утилита для формирования отчетов по метрикам видео",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Список CSV-файлов для анализа",
    )
    parser.add_argument(
        "--report",
        required=True,
        help=f"Название типа отчета (доступные: {', '.join(ReportRegistry.available())})",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Уровень логирования (по умолчанию WARNING)",
    )
    return parser


def main() -> None:
    args = _build_parser().parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )

    try:
        data = load_csv_files(args.files)
        report_processor = ReportRegistry.get_report(args.report)
        report_data = report_processor.generate(data)

        print(tabulate(report_data, headers="keys", tablefmt="grid", floatfmt=".1f"))
    except FileLoadError as exc:
        logger.error("%s", exc)
        sys.exit(1)
    except ValueError as exc:
        logger.error("%s", exc)
        sys.exit(1)
    except Exception:
        logger.exception("Непредвиденная ошибка")
        sys.exit(1)


if __name__ == "__main__":
    main()
