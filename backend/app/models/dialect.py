"""
模型层 - 方言数据结构的静态类型定义
字段对齐清洗后 CSV（dialect_points_cleaned.csv）
"""

from dataclasses import dataclass
from typing import Optional, TypedDict


class DialectRecord(TypedDict):
    """清洗 CSV 中单条方言点位记录"""
    city: str
    dialect_area: str
    province: str
    longitude: float
    latitude: float
    population_10k: float
    youth_usage_rate: float
    endanger_index: float
    endanger_level: str


@dataclass
class DialectPoint:
    """方言点位数据类"""
    city: str
    dialect_area: str
    province: str
    longitude: float = 0.0
    latitude: float = 0.0
    population_10k: float = 0.0
    youth_usage_rate: float = 0.0
    endanger_index: float = 0.0
    endanger_level: str = ''

    @classmethod
    def from_dict(cls, data: dict) -> 'DialectPoint':
        return cls(
            city=data.get('city', ''),
            dialect_area=data.get('dialect_area', ''),
            province=data.get('province', ''),
            longitude=float(data.get('longitude') or 0),
            latitude=float(data.get('latitude') or 0),
            population_10k=float(data.get('population_10k') or 0),
            youth_usage_rate=float(data.get('youth_usage_rate') or 0),
            endanger_index=float(data.get('endanger_index') or 0),
            endanger_level=data.get('endanger_level', ''),
        )


class StatisticsRecord(TypedDict):
    """统计数据记录"""
    metric: str
    value: float