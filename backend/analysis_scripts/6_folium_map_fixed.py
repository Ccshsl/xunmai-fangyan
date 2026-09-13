"""
脚本6修复版：Folium交互地图 - 6_folium_map_fixed.py
修复空白问题，确保地图正常显示
"""

import folium
from folium.plugins import HeatMap, Fullscreen
import pandas as pd
from config import *

def load_data():
    df = pd.read_csv(CLEANED_POINTS_FILE, encoding='utf-8-sig')
    return df

def get_marker_color(endanger_level):
    colors = {
        '安全': 'green',
        '较安全': 'blue',
        '脆弱': 'orange',
        '濒危': 'red'
    }
    return colors.get(endanger_level, 'gray')

def create_popup_content(row):
    content = f"""
    <div style="width: 250px;">
        <h4 style="margin: 0 0 8px 0;">🏮 {row['city']}</h4>
        <p><strong>方言区:</strong> {row['dialect_area']}</p>
        <p><strong>省份:</strong> {row['province']}</p>
        <p><strong>使用人口:</strong> {row['population_10k']} 万人</p>
        <p><strong>年轻人使用率:</strong> {row['youth_usage_rate']:.1%}</p>
        <p><strong>濒危等级:</strong> <span style="color: {'green' if row['endanger_level']=='安全' else 'blue' if row['endanger_level']=='较安全' else 'orange' if row['endanger_level']=='脆弱' else 'red'};">{row['endanger_level']}</span></p>
    </div>
    """
    return content

def main():
    print("=" * 60)
    print("脚本6修复版：Folium交互地图")
    print("=" * 60)
    
    print("\n[步骤1] 读取数据...")
    df = load_data()
    
    print("\n[步骤2] 创建地图...")
    # 设置固定的地图ID，确保CSS能正确应用
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    
    # 创建地图时设置tiles为None，后续手动添加
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=5,
        tiles=None  # 不使用默认底图
    )
    
    # 添加OpenStreetMap底图（更稳定）
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap',
        name='OpenStreetMap'
    ).add_to(m)
    
    print("\n[步骤3] 添加热力图层...")
    heat_data = [[row['latitude'], row['longitude'], row['endanger_index']] 
                 for idx, row in df.iterrows()]
    HeatMap(heat_data, name='濒危指数热力图', opacity=0.5).add_to(m)
    
    print("\n[步骤4] 添加方言点标记...")
    for idx, row in df.iterrows():
        color = get_marker_color(row['endanger_level'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(create_popup_content(row), max_width=280),
            zindex_offset=1000
        ).add_to(m)
    
    print("\n[步骤5] 添加控制按钮...")
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)
    
    print("\n[步骤6] 保存地图...")
    m.save(DIALECT_MAP_FILE)
    print(f"   已保存: {DIALECT_MAP_FILE}")
    
    print("\n" + "=" * 60)
    print("Folium交互地图创建完成！")
    print("=" * 60)
    
    return m

if __name__ == "__main__":
    main()