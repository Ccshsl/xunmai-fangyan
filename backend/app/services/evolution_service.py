"""
服务层 - 语言演变模拟数据业务
数据读取均通过 CacheManager 缓存
"""

from app.config import Config
from app.cache.cache_manager import cache
from app.services.dialect_service import get_all_dialects


def get_evolution_data(current_year):
    """
    准备演变模拟所需方言数据（内存缓存）
    返回 list[dict]：{city, dialect_area, province, initial_rate, current_rate}
    """
    def _loader():
        result = []
        for rec in get_all_dialects():
            rate = float(rec.get('youth_usage_rate') or 0)
            result.append({
                'city': rec.get('city', ''),
                'dialect_area': rec.get('dialect_area', ''),
                'province': rec.get('province', ''),
                'initial_rate': rate,
                'current_rate': rate,
            })
        return result

    key = f'evolution:data:{current_year}'
    return cache.get_or_set(key, _loader, Config.CACHE_DEFAULT_TIMEOUT)