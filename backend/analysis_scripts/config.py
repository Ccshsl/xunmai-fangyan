"""
配置文件 - config.py
管理项目路径和参数
"""

import os

# 后端根目录 - 基于本文件位置动态计算（backend/analysis_scripts/）
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_ROOT)

# 数据目录
DATA_DIR = os.path.join(BACKEND_ROOT, 'data')

# 输出目录
OUTPUT_DIR = os.path.join(BACKEND_ROOT, 'outputs')

# 脚本目录
SCRIPTS_DIR = os.path.join(BACKEND_ROOT, 'analysis_scripts')

# 输入数据文件路径
DIALECT_POINTS_FILE = os.path.join(DATA_DIR, 'dialect_points.csv')
DIALECT_SIMILARITY_FILE = os.path.join(DATA_DIR, 'dialect_similarity.csv')
POPULATION_FILE = os.path.join(DATA_DIR, 'population_by_dialect.csv')
FEATURE_WORDS_FILE = os.path.join(DATA_DIR, 'feature_words.csv')

# 输出文件路径
CLEANED_POINTS_FILE = os.path.join(OUTPUT_DIR, 'dialect_points_cleaned.csv')
STATISTICS_SUMMARY_FILE = os.path.join(OUTPUT_DIR, 'statistics_summary.csv')
ISOGLOSS_MAP_FILE = os.path.join(OUTPUT_DIR, 'isogloss_map.png')
BUFFER_ANALYSIS_FILE = os.path.join(OUTPUT_DIR, 'buffer_analysis.png')
DIALECT_STATISTICS_FILE = os.path.join(OUTPUT_DIR, 'dialect_statistics.png')
DIALECT_DENDROGRAM_FILE = os.path.join(OUTPUT_DIR, 'dialect_dendrogram.png')
SIMILARITY_CLUSTERMAP_FILE = os.path.join(OUTPUT_DIR, 'similarity_clustermap.png')
LANGUAGE_EVOLUTION_FILE = os.path.join(OUTPUT_DIR, 'language_evolution.png')
EVOLUTION_COMPARISON_FILE = os.path.join(OUTPUT_DIR, 'evolution_comparison.png')
DIALECT_MAP_FILE = os.path.join(OUTPUT_DIR, 'dialect_map.html')
RISK_REPORT_FILE = os.path.join(OUTPUT_DIR, 'language_risk_report.csv')

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)