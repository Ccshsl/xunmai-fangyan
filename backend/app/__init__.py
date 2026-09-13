"""
寻脉方言系统 - Flask 应用工厂
create_app() 创建并配置应用：注册蓝图、初始化缓存、配置模板/静态路径、挂载缓存钩子
"""

from flask import Flask

from app.config import config_map
from app.cache.cache_manager import cache
from app.routes import register_blueprints


def create_app(config_name='default'):
    """
    应用工厂
    config_name: 'default' | 'development' | 'production'
    """
    config_cls = config_map.get(config_name, config_map['default'])
    app = Flask(
        __name__,
        static_folder=None,  # 静态资源统一由 static_bp 提供，避免路由重复注册
    )
    app.config.from_object(config_cls)

    # Jinja2 模板路径指向前端目录
    app.jinja_loader.searchpath = [config_cls.TEMPLATES_DIR]

    # 初始化缓存
    cache.init_app(app)

    # 注册蓝图
    register_blueprints(app)

    # 请求钩子：before_request 缓存命中检查（命中率统计已由 CacheManager 内部完成）
    @app.before_request
    def before_request_cache():
        pass

    # after_request：为 GET 响应设置 HTTP 缓存头
    @app.after_request
    def after_request_cache(response):
        from flask import request
        if request.method == 'GET':
            # 静态资源、API 响应可长缓存；页面缓存较短
            path = request.path
            if path.startswith('/static/') or path.startswith('/outputs/'):
                response.headers['Cache-Control'] = 'public, max-age=604800'  # 7 天
                response.headers['Expires'] = 'Fri, 31 Dec 9999 23:59:59 GMT'
            elif path.startswith('/api/'):
                response.headers['Cache-Control'] = 'public, max-age=300'
            else:
                response.headers['Cache-Control'] = 'no-cache'
            response.headers['Vary'] = 'Accept-Encoding'
        return response

    # 缓存状态端点（便于监控命中率）
    @app.route('/api/cache-stats')
    def cache_stats():
        from flask import jsonify
        return jsonify(cache.get_stats())

    return app