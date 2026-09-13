"""
服务层 - 方言数据业务
所有数据读取均通过 CacheManager 缓存，禁止直接读文件
"""

import pandas as pd

from app.config import Config
from app.cache.cache_manager import cache
from app.data.dialect_info import get_dialect_details as _details_from_data
from app.utils.helpers import get_related_cities as _compute_related

# 缓存 key 与 TTL
_ALL_DIALECTS_KEY = 'dialect:all'
_DETAILS_KEY_TPL = 'dialect:details:%s:%s'
_CACHE_TTL = Config.CACHE_DEFAULT_TIMEOUT


def _load_cleaned_df():
    """读取清洗后 CSV（pandas），返回 DataFrame，空则返回空 DataFrame"""
    try:
        return pd.read_csv(Config.CLEANED_POINTS_FILE, encoding='utf-8-sig')
    except Exception as e:
        print(f"加载清洗CSV失败: {e}")
        return pd.DataFrame()


def get_all_dialects():
    """获取全部方言点位记录 list[dict]（内存缓存）"""
    def _loader():
        df = _load_cleaned_df()
        if df.empty:
            return []
        return df.to_dict('records')

    return cache.get_or_set(_ALL_DIALECTS_KEY, _loader, _CACHE_TTL)


def get_dialect_by_city(city):
    """根据城市名获取单条方言记录 dict，不存在返回 None"""
    all_records = get_all_dialects()
    for rec in all_records:
        if rec.get('city') == city:
            return rec
    return None


def get_dialect_details(city, dialect_area="方言"):
    """获取地区详情（内嵌字典，带模块级缓存）"""
    return _details_from_data(city, dialect_area)


def get_related_cities(dialect_area, exclude_city, limit=6):
    """获取同一方言区的其他城市（基于缓存的全部记录计算）"""
    all_records = get_all_dialects()
    return _compute_related(all_records, dialect_area, exclude_city, limit)