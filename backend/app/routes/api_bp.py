"""
路由层 - API 路由
返回 JSON，数据经服务层（已缓存）获取，对最终载荷再套一层响应缓存
"""

from flask import Blueprint, jsonify

from app.config import Config
from app.cache.cache_manager import cache
from app.services import dialect_service
from app.services import statistics_service

api_bp = Blueprint('api', __name__, url_prefix='/api')
_CACHE_TTL = Config.CACHE_DEFAULT_TIMEOUT


def _cached_response(key, loader):
    """响应缓存装饰逻辑：优先返回缓存载荷，否则加载并缓存"""
    payload = cache.get_or_set(key, loader, _CACHE_TTL)
    return jsonify(payload)


@api_bp.route('/dialects')
def get_dialects():
    return _cached_response(
        'api:dialects:v1',
        dialect_service.get_all_dialects,
    )


@api_bp.route('/statistics')
def get_statistics():
    return _cached_response(
        'api:statistics:v1',
        statistics_service.get_statistics_summary,
    )