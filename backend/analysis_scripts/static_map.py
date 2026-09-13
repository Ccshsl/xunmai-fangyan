"""
生成静态图片地图
"""
import pandas as pd
import matplotlib.pyplot as plt
from config import *

def main():
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 读取数据
    df = pd.read_csv(CLEANED_POINTS_FILE, encoding='utf-8-sig')
    
    # 创建地图
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 绘制中国区域背景
    ax.set_xlim(73, 135)
    ax.set_ylim(18, 54)
    
    # 绘制方言点
    for idx, row in df.iterrows():
        color = {'安全': 'green', '较安全': 'blue', '脆弱': 'orange', '濒危': 'red'}.get(row['endanger_level'], 'gray')
        ax.scatter(row['longitude'], row['latitude'], s=row['population_10k']*2, 
                   c=color, alpha=0.7, edgecolor='black', linewidth=1)
    
    # 添加城市标签（主要城市）
    major_cities = ['北京', '上海', '广州', '成都', '西安', '武汉', '南京', '杭州']
    for idx, row in df.iterrows():
        if row['city'] in major_cities:
            ax.text(row['longitude']+0.5, row['latitude']+0.5, row['city'], 
                    fontsize=10, ha='left', va='bottom')
    
    # 设置标题和图例
    ax.set_title('中国方言分布地图', fontsize=16, pad=20)
    ax.set_xlabel('经度', fontsize=12)
    ax.set_ylabel('纬度', fontsize=12)
    
    # 添加图例
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='安全'),
        Patch(facecolor='blue', label='较安全'),
        Patch(facecolor='orange', label='脆弱'),
        Patch(facecolor='red', label='濒危')
    ]
    ax.legend(handles=legend_elements, loc='lower right', title='濒危等级')
    
    # 保存图片
    plt.savefig(OUTPUT_DIR + '/static_dialect_map.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"静态地图已保存: {OUTPUT_DIR}/static_dialect_map.png")

if __name__ == "__main__":
    main()