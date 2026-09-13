"""
工具层 - 通用路径处理与格式化辅助函数
"""

import os

from app.config import PROJECT_ROOT


def safe_path(*parts):
    """拼接路径，过滤空段"""
    return os.path.normpath(os.path.join(*(str(p) for p in parts if p)))


def as_float(value, default=0.0):
    """安全转 float"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def format_percent(value, ndigits=2):
    """转百分数字符串，如 0.8567 -> '85.67%'"""
    return f"{as_float(value) * 100:.{ndigits}f}%"


def format_number(value, ndigits=2):
    """格式化数字"""
    return f"{as_float(value):,.{ndigits}f}"


def get_related_cities(all_records, dialect_area, exclude_city, limit=6):
    """
    从方言数据记录中获取同一方言区的其他城市（供服务层复用）
    all_records: list[dict]，每项需含 city 与 dialect_area
    """
    related = [r['city'] for r in all_records
               if r.get('dialect_area') == dialect_area and r.get('city') != exclude_city]
    return related[:limit]