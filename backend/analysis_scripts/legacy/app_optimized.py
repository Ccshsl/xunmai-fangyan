# -*- coding: utf-8 -*-
"""
优化后的app.py - 使用缓存机制提升性能
"""
from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd
import os
import json
from functools import lru_cache

app = Flask(__name__)

# 配置路径
DATA_DIR = 'data'
OUTPUTS_DIR = 'outputs'
SCRIPTS_DIR = 'scripts'

# ==================== 全局缓存 ====================
# 缓存方言数据，避免每次请求都重新创建
_dialect_info_cache = None
_csv_data_cache = None
_statistics_cache = None

# ==================== 优化后的数据加载函数 ====================

def get_dialect_info():
    """获取方言详细信息（带缓存）"""
    global _dialect_info_cache
    if _dialect_info_cache is None:
        # 尝试从JSON文件加载
        json_path = os.path.join(DATA_DIR, 'dialect_data.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                _dialect_info_cache = json.load(f)
        else:
            # 如果JSON文件不存在，使用内置数据
            _dialect_info_cache = _get_builtin_dialect_info()
    return _dialect_info_cache

def _get_builtin_dialect_info():
    """内置方言数据（仅包含示例，实际使用时应从JSON加载）"""
    return {
        '北京': {
            'dialect_intro': '北京话是北京官话的代表，属于官话方言的分支之一。',
            'dialect_feature': '北京话最大的特点是儿化音丰富。',
            'dialect_history': '北京话源于辽金时期的女真语与汉语融合。',
            'dialect_culture': '北京话不仅是一种语言，更是一种文化符号。',
            'dialect_tags': ['儿化音', '轻声多', '口语化', '幽默感', '官话基础'],
            'feature_words': ['哪儿', '豆汁儿', '瓷实', '局气', '侃大山'],
            'common_phrases': ['您吃了吗？', '没事儿', '甭提了', '得嘞', '回头见'],
            'local_food': '北京烤鸭是老北京最具代表性的美食。',
            'folk_art': '京剧是北京最具代表性的传统艺术。',
            'historical_sites': '故宫是世界上现存规模最大的木质结构古建筑群。',
            'traditional_festival': '老北京庙会是最具特色的年俗活动。'
        }
    }

@lru_cache(maxsize=1)
def load_dialect_data():
    """加载方言数据（带缓存）"""
    try:
        df = pd.read_csv(os.path.join(OUTPUTS_DIR, 'dialect_points_cleaned.csv'), encoding='utf-8-sig')
        return df.to_dict('records')
    except Exception as e:
        print(f"加载数据失败: {e}")
        return []

@lru_cache(maxsize=1)
def load_statistics():
    """加载统计数据（带缓存）"""
    try:
        df = pd.read_csv(os.path.join(OUTPUTS_DIR, 'statistics_summary.csv'), encoding='utf-8-sig')
        return df.to_dict('records')
    except Exception as e:
        print(f"加载统计数据失败: {e}")
        return []

@lru_cache(maxsize=1)
def load_csv_dataframe():
    """加载CSV为DataFrame（带缓存）"""
    try:
        return pd.read_csv(os.path.join(OUTPUTS_DIR, 'dialect_points_cleaned.csv'), encoding='utf-8-sig')
    except Exception as e:
        print(f"加载数据失败: {e}")
        return pd.DataFrame()

def get_dialect_details(city, dialect_area="方言"):
    """获取方言详细介绍数据（带缓存）"""
    dialect_info = get_dialect_info()
    if city in dialect_info:
        return dialect_info[city]
    
    # 默认返回
    return {
        'dialect_intro': f'{city}方言是{dialect_area}的重要分支，具有独特的语音特点和丰富的词汇体系。',
        'dialect_feature': f'{city}方言在语音、词汇方面都有独特之处，体现了当地的文化特色。',
        'dialect_history': f'{city}方言历经长期发展演变，承载着丰富的历史文化信息。',
        'dialect_culture': f'{city}方言是当地文化的重要组成部分，反映了当地人的性格特点。',
        'dialect_tags': ['地域特色', '文化丰富', '历史悠久'],
        'feature_words': ['特色词1', '特色词2', '特色词3'],
        'common_phrases': ['你好！', '谢谢', '再见'],
        'local_food': f'{city}有着丰富的特色美食，体现了当地的饮食文化。',
        'folk_art': f'{city}有着独特的民间艺术和传统工艺。',
        'historical_sites': f'{city}有着丰富的历史遗迹和文化景点。',
        'traditional_festival': f'{city}保留着传统节日习俗。'
    }

def get_related_cities(dialect_area, current_city):
    """获取同一方言区的其他城市（带缓存）"""
    df = load_csv_dataframe()
    if df.empty:
        return []
    related = df[df['dialect_area'] == dialect_area]['city'].tolist()
    related = [c for c in related if c != current_city][:6]
    return related

# ==================== 路由定义 ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def dialect_map():
    return render_template('map.html')

@app.route('/statistics')
def statistics():
    stats = load_statistics()
    return render_template('statistics.html', stats=stats)

@app.route('/evolution')
def evolution():
    import datetime
    current_year = datetime.datetime.now().year
    
    df = load_csv_dataframe()
    dialect_data = []
    for _, row in df.iterrows():
        dialect_data.append({
            'city': row['city'],
            'dialect_area': row['dialect_area'],
            'province': row['province'],
            'initial_rate': float(row['youth_usage_rate']),
            'current_rate': float(row['youth_usage_rate'])
        })
    
    return render_template('evolution.html',
                         current_year=current_year,
                         future_year=current_year + 50,
                         dialect_data=dialect_data,
                         dialect_data_json=json.dumps(dialect_data, ensure_ascii=False))

@app.route('/migration')
def migration():
    return render_template('migration.html')

@app.route('/detail/<city_name>')
def dialect_detail(city_name):
    city_name = city_name.replace('%20', ' ')
    df = load_csv_dataframe()
    
    if df.empty:
        return "数据加载失败", 500
    
    city_data = df[df['city'] == city_name]
    
    if city_data.empty:
        return "城市不存在", 404
    
    row = city_data.iloc[0]
    details = get_dialect_details(city_name, row['dialect_area'])
    related = get_related_cities(row['dialect_area'], city_name)
    
    return render_template('detail.html',
                         city=city_name,
                         province=row['province'],
                         dialect_area=row['dialect_area'],
                         longitude=row['longitude'],
                         latitude=row['latitude'],
                         population_10k=row['population_10k'],
                         youth_usage_rate=row['youth_usage_rate'],
                         endanger_index=row['endanger_index'],
                         endanger_level=row['endanger_level'],
                         related_cities=related,
                         **details)

@app.route('/api/dialects')
def get_dialects():
    data = load_dialect_data()
    return jsonify(data)

@app.route('/api/statistics')
def get_statistics():
    data = load_statistics()
    return jsonify(data)

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory(OUTPUTS_DIR, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# ==================== 清除缓存函数 ====================

def clear_cache():
    """清除所有缓存"""
    global _dialect_info_cache, _csv_data_cache, _statistics_cache
    _dialect_info_cache = None
    _csv_data_cache = None
    _statistics_cache = None
    load_dialect_data.cache_clear()
    load_statistics.cache_clear()
    load_csv_dataframe.cache_clear()

if __name__ == '__main__':
    # 启动时预加载数据
    print("正在预加载数据...")
    get_dialect_info()
    load_dialect_data()
    load_statistics()
    print("数据预加载完成！")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
