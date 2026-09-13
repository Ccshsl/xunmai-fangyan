"""路由层 - 注册所有蓝图"""
from flask import Flask


def register_blueprints(app: Flask):
    """向 Flask 应用注册所有路由蓝图"""
    from app.routes.pages_bp import pages_bp
    from app.routes.api_bp import api_bp
    from app.routes.static_bp import static_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(static_bp)