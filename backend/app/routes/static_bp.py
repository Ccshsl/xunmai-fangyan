"""
路由层 - 静态文件服务
提供 /outputs/ 分析产物与 /static/ 前端静态资源
"""

from flask import Blueprint, send_from_directory

from app.config import Config

static_bp = Blueprint('static_bp', __name__)


@static_bp.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory(Config.OUTPUT_DIR, filename)


@static_bp.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(Config.STATIC_DIR, filename)