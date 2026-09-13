"""
服务层 - 统计业务
数据读取均通过 CacheManager 缓存
"""

import pandas as pd

from app.config import Config
from app.cache.cache_manager import cache

_STATS_KEY = 'statistics:summary'
_CACHE_TTL = Config.CACHE_DEFAULT_TIMEOUT


def get_statistics_summary():
    """获取统计汇总数据 list[dict]（内存缓存）"""
    def _loader():
        try:
            df = pd.read_csv(Config.STATISTICS_SUMMARY_FILE, encoding='utf-8-sig')
        except Exception as e:
            print(f"加载统计数据失败: {e}")
            return []
        if df.empty:
            return []
        return df.to_dict('records')

    return cache.get_or_set(_STATS_KEY, _loader, _CACHE_TTL)