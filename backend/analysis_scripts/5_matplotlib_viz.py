"""
脚本5：Matplotlib可视化 - 5_matplotlib_viz.py
生成6种以上统计图表（单独生成每个图表）
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import *

def load_data():
    """读取数据"""
    df = pd.read_csv(CLEANED_POINTS_FILE, encoding='utf-8-sig')
    similarity = pd.read_csv(DIALECT_SIMILARITY_FILE, index_col=0, encoding='utf-8-sig')
    return df, similarity

def plot_pie_chart(df):
    """饼图：方言区人口占比（优化版）"""
    plt.figure(figsize=(12, 12))
    
    # 按方言区分组求和
    pop_by_area = df.groupby('dialect_area')['population_10k'].sum()
    total = pop_by_area.sum()
    
    # 合并占比小于2%的小方言区
    threshold = 0.02  # 2%阈值
    small_areas = pop_by_area[pop_by_area / total < threshold]
    large_areas = pop_by_area[pop_by_area / total >= threshold]
    
    # 添加"其他"类别
    if len(small_areas) > 0:
        large_areas['其他'] = small_areas.sum()
    
    # 简化标签
    labels = []
    for name in large_areas.index:
        if name == '其他':
            labels.append('其他')
        elif '官话' in name:
            labels.append(name.replace('官话', '') + '官')
        elif '片' in name:
            labels.append(name[:2])
        elif len(name) > 4:
            labels.append(name[:3])
        else:
            labels.append(name)
    
    # 设置饼图参数，标签放在外部
    wedges, texts, autotexts = plt.pie(
        large_areas, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90,
        textprops={'fontsize': 10},
        labeldistance=1.1,  # 标签距离
        pctdistance=0.85,   # 百分比距离
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )
    
    plt.title('各方言区人口占比', fontsize=18)
    plt.savefig(OUTPUT_DIR + '/pie_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: pie_chart.png")

def plot_bar_chart(df):
    """条形图：年轻人使用率对比（按方言区整合）"""
    plt.figure(figsize=(14, 8))
    
    # 按方言区分组，计算平均使用率
    grouped_df = df.groupby('dialect_area')['youth_usage_rate'].mean().reset_index()
    
    # 简化方言区名称
    grouped_df['dialect_short'] = grouped_df['dialect_area'].apply(lambda x: 
        x.replace('官话', '') + '官' if '官话' in x else
        x[:2] if '片' in x else
        x[:3] if len(x) > 3 else x
    )
    
    # 按使用率排序
    sorted_df = grouped_df.sort_values('youth_usage_rate', ascending=False)
    
    plt.bar(sorted_df['dialect_short'], sorted_df['youth_usage_rate'], color='skyblue')
    plt.title('各方言区年轻人平均使用率', fontsize=16)
    plt.xlabel('方言区', fontsize=12)
    plt.ylabel('平均使用率', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + '/bar_chart_usage.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: bar_chart_usage.png")

def plot_box_plot(df):
    """箱线图：濒危指数分布"""
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['endanger_index'], vert=False, patch_artist=True)
    plt.title('濒危指数分布', fontsize=16)
    plt.xlabel('濒危指数', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + '/box_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: box_plot.png")

def plot_scatter_plot(df):
    """散点图：人口vs使用率"""
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(df['population_10k'], df['youth_usage_rate'], 
                          s=150, c=df['endanger_index'], cmap='RdYlGn_r', alpha=0.7)
    plt.title('人口规模与使用率关系', fontsize=16)
    plt.xlabel('人口(万人)', fontsize=12)
    plt.ylabel('年轻人使用率', fontsize=12)
    plt.colorbar(scatter, label='濒危指数')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + '/scatter_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: scatter_plot.png")

def plot_heatmap(similarity):
    """热力图：方言相似度矩阵"""
    plt.figure(figsize=(14, 12))
    
    if len(similarity) > 20:
        similarity = similarity.iloc[:20, :20]
    
    data = similarity.values
    plt.imshow(data, cmap='YlGnBu', interpolation='nearest')
    
    for i in range(len(similarity)):
        for j in range(len(similarity)):
            plt.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center', fontsize=8, color='black')
    
    plt.colorbar()
    plt.title('方言相似度矩阵', fontsize=16)
    plt.xticks(range(len(similarity)), similarity.columns, fontsize=8, rotation=45)
    plt.yticks(range(len(similarity)), similarity.index, fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + '/heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: heatmap.png")

def plot_bar_chart2(df):
    """条形图：濒危等级分布"""
    plt.figure(figsize=(10, 6))
    level_counts = df['endanger_level'].value_counts()
    colors = {'安全': 'green', '较安全': 'yellow', '脆弱': 'orange', '濒危': 'red'}
    plt.bar(level_counts.index, level_counts.values, color=[colors[l] for l in level_counts.index])
    plt.title('濒危等级分布', fontsize=16)
    plt.xlabel('濒危等级', fontsize=12)
    plt.ylabel('城市数量', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + '/bar_chart_level.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: bar_chart_level.png")

def plot_city_count_bar(df):
    """条形图：各方言区城市数量"""
    plt.figure(figsize=(12, 6))
    city_counts = df.groupby('dialect_area')['city'].count().sort_values(ascending=False)
    
    # 简化标签
    labels = []
    for name in city_counts.index:
        if '官话' in name:
            labels.append(name.replace('官话', '') + '官')
        elif '片' in name:
            labels.append(name[:2])
        elif len(name) > 4:
            labels.append(name[:3])
        else:
            labels.append(name)
    
    plt.bar(labels, city_counts.values, color='coral')
    plt.title('各方言区城市数量', fontsize=16)
    plt.xlabel('方言区', fontsize=12)
    plt.ylabel('城市数量', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + '/bar_chart_city_count.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: bar_chart_city_count.png")

def main():
    print("=" * 60)
    print("脚本5：Matplotlib可视化")
    print("=" * 60)
    
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    print("\n[步骤1] 读取数据...")
    df, similarity = load_data()
    
    print("\n[步骤2] 生成独立图表...")
    print("-" * 40)
    
    print("生成饼图...")
    plot_pie_chart(df)
    
    print("生成使用率条形图...")
    plot_bar_chart(df)
    
    print("生成箱线图...")
    plot_box_plot(df)
    
    print("生成散点图...")
    plot_scatter_plot(df)
    
    print("生成热力图...")
    plot_heatmap(similarity)
    
    print("生成濒危等级条形图...")
    plot_bar_chart2(df)
    
    print("生成城市数量条形图...")
    plot_city_count_bar(df)
    
    print("-" * 40)
    print(f"\n共生成7个独立图表，保存至: {OUTPUT_DIR}")
    
    print("\n" + "=" * 60)
    print("Matplotlib可视化完成！")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()
