"""
路由层 - 页面路由
只做参数接收与响应返回，业务逻辑全部委托给服务层
"""

import datetime
import json
from flask import Blueprint, render_template, abort

from app.services import dialect_service
from app.services import statistics_service
from app.services import evolution_service

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    return render_template('index.html')


@pages_bp.route('/map')
def dialect_map():
    return render_template('map.html')


@pages_bp.route('/statistics')
def statistics():
    stats = statistics_service.get_statistics_summary()
    return render_template('statistics.html', stats=stats)


@pages_bp.route('/evolution')
def evolution():
    current_year = datetime.datetime.now().year
    dialect_data = evolution_service.get_evolution_data(current_year)

    return render_template(
        'evolution.html',
        current_year=current_year,
        future_year=current_year + 50,
        dialect_data=dialect_data,
        dialect_data_json=json.dumps(dialect_data, ensure_ascii=False),
    )


@pages_bp.route('/migration')
def migration():
    return render_template('migration.html')


@pages_bp.route('/detail/<city_name>')
def dialect_detail(city_name):
    city_name = city_name.replace('%20', ' ')
    city_data = dialect_service.get_dialect_by_city(city_name)

    if city_data is None:
        abort(404)

    details = dialect_service.get_dialect_details(city_name, city_data.get('dialect_area'))
    related = dialect_service.get_related_cities(city_data.get('dialect_area'), city_name)

    return render_template(
        'detail.html',
        city=city_name,
        province=city_data.get('province', ''),
        dialect_area=city_data.get('dialect_area', ''),
        longitude=city_data.get('longitude', 0),
        latitude=city_data.get('latitude', 0),
        population_10k=city_data.get('population_10k', 0),
        youth_usage_rate=city_data.get('youth_usage_rate', 0),
        endanger_index=city_data.get('endanger_index', 0),
        endanger_level=city_data.get('endanger_level', ''),
        related_cities=related,
        **details,
    )


@pages_bp.route('/game')
def game():
    return render_template('game.html')


@pages_bp.route('/game-test')
def game_test():
    return render_template('game_test.html')