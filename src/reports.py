from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseReport(ABC):
    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class ClickbaitReport(BaseReport):
    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered_data = [
            row for row in data
            if row['ctr'] > 15 and row['retention_rate'] < 40
        ]
        sorted_data = sorted(filtered_data, key=lambda x: x['ctr'], reverse=True)
        return [
            {
                'title': row['title'],
                'ctr': row['ctr'],
                'retention_rate': row['retention_rate'],
            }
            for row in sorted_data
        ]


class ReportRegistry:
    _reports: Dict[str, type[BaseReport]] = {
        'clickbait': ClickbaitReport,
    }

    @classmethod
    def get_report(cls, report_name: str) -> BaseReport:
        report_class = cls._reports.get(report_name)
        if not report_class:
            raise ValueError(f"Неизвестный тип отчета: {report_name}")
        return report_class()
