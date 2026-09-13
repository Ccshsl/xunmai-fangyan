"""
脚本6：Folium交互地图 - 6_folium_map.py
创建交互式方言分布地图（恢复到基础版本）
"""

import folium
from folium.plugins import HeatMap, Fullscreen
import pandas as pd
from config import *

def load_data():
    """读取数据"""
    df = pd.read_csv(CLEANED_POINTS_FILE, encoding='utf-8-sig')
    return df

def get_marker_color(endanger_level):
    """根据濒危等级获取标记颜色"""
    colors = {
        '安全': 'green',
        '较安全': 'blue',
        '脆弱': 'orange',
        '濒危': 'red'
    }
    return colors.get(endanger_level, 'gray')

def create_popup_content(row):
    """创建弹出框内容"""
    return f"""
    <b>{row['city']}</b><br>
    方言区: {row['dialect_area']}<br>
    省份: {row['province']}<br>
    使用人口: {row['population_10k']} 万人<br>
    年轻人使用率: {row['youth_usage_rate']:.2%}<br>
    濒危指数: {row['endanger_index']:.2f}<br>
    濒危等级: {row['endanger_level']}
    """

def main():
    print("=" * 60)
    print("脚本6：Folium交互地图（基础版本）")
    print("=" * 60)
    
    print("\n[步骤1] 读取数据...")
    df = load_data()
    
    print("\n[步骤2] 创建地图...")
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
    
    print("\n[步骤3] 添加高德地图底图...")
    folium.TileLayer(
        tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='高德地图',
        name='高德地图'
    ).add_to(m)
    
    print("\n[步骤4] 添加热力图层...")
    heat_data = [[row['latitude'], row['longitude'], row['endanger_index']] 
                 for idx, row in df.iterrows()]
    HeatMap(heat_data, name='濒危指数热力图', opacity=0.5).add_to(m)
    
    print("\n[步骤5] 添加影响范围圆...")
    for idx, row in df.iterrows():
        radius = row['population_10k'] * 50
        folium.Circle(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.1,
            popup=f"{row['city']} 影响范围"
        ).add_to(m)
    
    print("\n[步骤6] 添加方言点标记...")
    for idx, row in df.iterrows():
        color = get_marker_color(row['endanger_level'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(create_popup_content(row), max_width=300),
            zindex_offset=1000
        ).add_to(m)
    
    print("\n[步骤7] 添加全屏按钮和图层控制...")
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)
    
    print("\n[步骤7.5] 添加图例...")
    # 添加图例
    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 10px; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.15); z-index: 1000;">
        <div style="font-weight: bold; margin-bottom: 10px; font-size: 14px;">📍 濒危等级图例</div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: green; margin-right: 8px;"></div>
            <span style="font-size: 12px;">安全</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: blue; margin-right: 8px;"></div>
            <span style="font-size: 12px;">较安全</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: orange; margin-right: 8px;"></div>
            <span style="font-size: 12px;">脆弱</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: red; margin-right: 8px;"></div>
            <span style="font-size: 12px;">濒危</span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    print("\n[步骤8] 保存地图...")
    m.save(DIALECT_MAP_FILE)
    print(f"   已保存: {DIALECT_MAP_FILE}")
    
    print("\n" + "=" * 60)
    print("Folium交互地图创建完成！")
    print("=" * 60)
    
    return m

if __name__ == "__main__":
    main()