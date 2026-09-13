"""
应用配置 - 集中管理所有路径、端口、缓存参数
所有路径基于本文件位置动态计算，不做任何硬编码
"""

import os

# 后端根目录：backend/  （本文件位于 backend/app/config.py）
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 项目根目录
PROJECT_ROOT = os.path.dirname(BACKEND_ROOT)
# 前端根目录
FRONTEND_ROOT = os.path.join(PROJECT_ROOT, 'frontend')


class Config(object):
    """基类配置"""
    # 路径
    PROJECT_ROOT = PROJECT_ROOT
    BACKEND_ROOT = BACKEND_ROOT
    FRONTEND_ROOT = FRONTEND_ROOT

    DATA_DIR = os.path.join(BACKEND_ROOT, 'data')
    OUTPUT_DIR = os.path.join(BACKEND_ROOT, 'outputs')
    TEMPLATES_DIR = os.path.join(FRONTEND_ROOT, 'templates')
    STATIC_DIR = os.path.join(FRONTEND_ROOT, 'static')

    # 数据文件（服务层读取的清洗后数据）
    CLEANED_POINTS_FILE = os.path.join(OUTPUT_DIR, 'dialect_points_cleaned.csv')
    STATISTICS_SUMMARY_FILE = os.path.join(OUTPUT_DIR, 'statistics_summary.csv')

    # 服务
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True

    # 缓存
    CACHE_TYPE = 'memory'         # memory | file
    CACHE_DEFAULT_TIMEOUT = 3600  # 默认 TTL（秒）
    CACHE_FILE_DIR = os.path.join(OUTPUT_DIR, '.cache')

    # Flask
    JSON_AS_ASCII = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}