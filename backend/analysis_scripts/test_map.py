"""
测试地图脚本 - 最简单的Folium地图
"""
import folium

# 创建最简单的地图
m = folium.Map(
    location=[35.0, 105.0],  # 中国中心点
    zoom_start=5,
    tiles='OpenStreetMap'
)

# 添加一个测试标记
folium.Marker(
    location=[39.9, 116.4],
    popup='北京'
).add_to(m)

# 保存地图
import os
output_dir = r'C:\Users\林宝澄\Desktop\寻脉方言系统\outputs'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'test_map.html')
m.save(output_path)
print(f"测试地图已保存到: {output_path}")