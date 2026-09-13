"""
脚本4：空间分析 - 4_spatial_analysis.py
坐标系转换、缓冲区分析、等语线插值生成
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import Rbf
from config import *

def load_cleaned_data(filepath):
    """读取清洗后的数据"""
    return pd.read_csv(filepath, encoding='utf-8-sig')

def wgs84_to_webmercator(lon, lat):
    """坐标转换：WGS84 → Web墨卡托（EPSG:3857）"""
    R = 6378137.0
    x = R * np.radians(lon)
    y = R * np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))
    return x, y

def coordinate_conversion(df):
    """坐标转换：WGS84 → Web墨卡托"""
    df = df.copy()
    x_list, y_list = [], []
    for _, row in df.iterrows():
        x, y = wgs84_to_webmercator(row['longitude'], row['latitude'])
        x_list.append(x)
        y_list.append(y)
    df['mercator_x'] = x_list
    df['mercator_y'] = y_list
    return df

def generate_isogloss_map(df):
    """生成等语线图（基于IDW/RBF插值）"""
    lon_min, lon_max = df['longitude'].min() - 3, df['longitude'].max() + 3
    lat_min, lat_max = df['latitude'].min() - 3, df['latitude'].max() + 3
    
    grid_lon, grid_lat = np.meshgrid(
        np.linspace(lon_min, lon_max, 120),
        np.linspace(lat_min, lat_max, 120)
    )
    
    rbf = Rbf(
        df['longitude'],
        df['latitude'],
        df['youth_usage_rate'],
        function='linear'
    )
    grid_rate = rbf(grid_lon, grid_lat)
    
    grid_rate = np.clip(grid_rate, 0, 1)
    
    return grid_lon, grid_lat, grid_rate

def plot_isogloss_map(df, grid_lon, grid_lat, grid_rate):
    """绘制等语线图"""
    plt.figure(figsize=(12, 8))
    
    contour = plt.contourf(grid_lon, grid_lat, grid_rate, levels=12, cmap='RdYlGn_r', alpha=0.8)
    cbar = plt.colorbar(contour, label='年轻人使用率')
    
    for _, row in df.iterrows():
        color = 'red' if row['endanger_level'] in ['脆弱', '濒危'] else 'blue'
        plt.scatter(row['longitude'], row['latitude'], 
                    c=color, s=80, zorder=5, edgecolor='black', linewidth=0.8)
        plt.text(row['longitude'] + 0.2, row['latitude'] + 0.15, 
                 row['city'], fontsize=8)
    
    plt.title('方言年轻人使用率等语线图', fontsize=14, fontweight='bold')
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.grid(True, alpha=0.3)
    plt.savefig(ISOGLOSS_MAP_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: {ISOGLOSS_MAP_FILE}")

def plot_buffer_analysis(df, radius_degrees=2):
    """绘制缓冲区分析图（用圆形代替缓冲区）"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for _, row in df.iterrows():
        circle = plt.Circle((row['longitude'], row['latitude']), 
                           radius_degrees, color='lightblue', alpha=0.25, 
                           edgecolor='blue', linewidth=1)
        ax.add_patch(circle)
    
    color_map = {'安全': 'green', '脆弱': 'orange', '濒危': 'red'}
    for _, row in df.iterrows():
        color = color_map.get(row['endanger_level'], 'blue')
        ax.scatter(row['longitude'], row['latitude'], 
                   c=color, s=80, zorder=5, edgecolor='black', linewidth=0.8)
    
    for _, row in df.iterrows():
        ax.text(row['longitude'] + 0.2, row['latitude'] + 0.15, 
                row['city'], fontsize=8)
    
    ax.set_xlim(df['longitude'].min() - 4, df['longitude'].max() + 4)
    ax.set_ylim(df['latitude'].min() - 4, df['latitude'].max() + 4)
    ax.set_title(f'方言点缓冲区分析图（{radius_degrees}°半径）', fontsize=14, fontweight='bold')
    ax.set_xlabel('经度')
    ax.set_ylabel('纬度')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='濒危'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='脆弱'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='安全'),
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.savefig(BUFFER_ANALYSIS_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: {BUFFER_ANALYSIS_FILE}")

def main():
    print("=" * 60)
    print("脚本4：空间分析")
    print("=" * 60)
    
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    print("\n[步骤1] 读取清洗后数据...")
    df = load_cleaned_data(CLEANED_POINTS_FILE)
    print(f"   数据条数: {len(df)}")
    
    print("\n[步骤2] 坐标转换（WGS84 → Web墨卡托）...")
    df_web = coordinate_conversion(df)
    print(f"   原始坐标系: WGS84 (EPSG:4326)")
    print(f"   转换后坐标系: Web墨卡托 (EPSG:3857)")
    print(f"   示例 - 北京: ({df_web.iloc[0]['mercator_x']:.0f}, {df_web.iloc[0]['mercator_y']:.0f}) 米")
    
    print("\n[步骤3] 缓冲区分析...")
    buffer_radius = 2
    print(f"   缓冲区半径: {buffer_radius}° (约{buffer_radius * 111:.0f}公里)")
    print(f"   缓冲区覆盖点数: {len(df)}")
    
    print("\n[步骤4] 等语线插值生成...")
    grid_lon, grid_lat, grid_rate = generate_isogloss_map(df)
    print(f"   插值网格: {grid_lon.shape}")
    print(f"   使用率范围: {grid_rate.min():.3f} ~ {grid_rate.max():.3f}")
    
    print("\n[步骤5] 绘制等语线图...")
    plot_isogloss_map(df, grid_lon, grid_lat, grid_rate)
    
    print("\n[步骤6] 绘制缓冲区分析图...")
    plot_buffer_analysis(df, buffer_radius)
    
    print("\n" + "=" * 60)
    print("空间分析完成！")
    print("=" * 60)
    
    return df, df_web

if __name__ == "__main__":
    main()
