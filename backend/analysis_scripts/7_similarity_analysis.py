"""
脚本7：相似度分析 - 7_similarity_analysis.py
方言相似度矩阵分析、层次聚类、谱系图
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from config import *

def load_similarity_matrix(filepath):
    """读取相似度矩阵"""
    return pd.read_csv(filepath, index_col=0, encoding='utf-8-sig')

def analyze_similarity(similarity):
    """分析相似度"""
    avg_similarity = similarity.mean().sort_values(ascending=False)
    print("【各地方言平均相似度】")
    print(avg_similarity)
    print()
    
    max_sim = 0
    max_pair = None
    cities = similarity.index.tolist()
    for i in range(len(cities)):
        for j in range(i+1, len(cities)):
            sim = similarity.iloc[i, j]
            if sim > max_sim and sim < 1.0:
                max_sim = sim
                max_pair = (cities[i], cities[j])
    print(f"【最相似方言对】{max_pair[0]} - {max_pair[1]}: {max_sim:.3f}")
    
    min_sim = 1.0
    min_pair = None
    for i in range(len(cities)):
        for j in range(i+1, len(cities)):
            sim = similarity.iloc[i, j]
            if sim < min_sim:
                min_sim = sim
                min_pair = (cities[i], cities[j])
    print(f"【差异最大方言对】{min_pair[0]} - {min_pair[1]}: {min_sim:.3f}")
    
    return avg_similarity

def plot_dendrogram(similarity):
    """绘制谱系图"""
    distance = 1 - similarity.values
    np.fill_diagonal(distance, 0)
    
    linked = linkage(distance, method='ward')
    
    plt.figure(figsize=(12, 8))
    dendrogram(linked, 
               labels=similarity.index.tolist(),
               orientation='top',
               distance_sort='descending',
               show_leaf_counts=True)
    plt.title('方言聚类谱系图', fontsize=14)
    plt.xlabel('方言点', fontsize=12)
    plt.ylabel('距离', fontsize=12)
    plt.savefig(DIALECT_DENDROGRAM_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: {DIALECT_DENDROGRAM_FILE}")

def plot_similarity_clustermap(similarity):
    """绘制相似度聚类热力图"""
    plt.figure(figsize=(12, 10))
    
    distance = 1 - similarity.values
    np.fill_diagonal(distance, 0)
    
    linked = linkage(distance, method='ward')
    
    from scipy.cluster.hierarchy import leaves_list
    order = leaves_list(linked)
    
    clustered_data = similarity.values[order, :][:, order]
    clustered_labels = similarity.index[order]
    
    plt.imshow(clustered_data, cmap='YlGnBu', interpolation='nearest')
    
    for i in range(len(clustered_labels)):
        for j in range(len(clustered_labels)):
            plt.text(j, i, f'{clustered_data[i, j]:.2f}', ha='center', va='center', fontsize=8, color='black')
    
    plt.colorbar()
    plt.title('方言相似度聚类热力图', fontsize=14)
    plt.xticks(range(len(clustered_labels)), clustered_labels, fontsize=8, rotation=90)
    plt.yticks(range(len(clustered_labels)), clustered_labels, fontsize=8)
    plt.tight_layout()
    plt.savefig(SIMILARITY_CLUSTERMAP_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: {SIMILARITY_CLUSTERMAP_FILE}")

def main():
    print("=" * 60)
    print("脚本7：相似度分析")
    print("=" * 60)
    
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    print("\n[步骤1] 读取相似度矩阵...")
    similarity = load_similarity_matrix(DIALECT_SIMILARITY_FILE)
    
    print("\n[步骤2] 分析相似度...")
    avg_similarity = analyze_similarity(similarity)
    
    print("\n[步骤3] 绘制聚类谱系图...")
    plot_dendrogram(similarity)
    
    print("\n[步骤4] 绘制相似度聚类热力图...")
    plot_similarity_clustermap(similarity)
    
    print("\n" + "=" * 60)
    print("相似度分析完成！")
    print("=" * 60)
    
    return avg_similarity

if __name__ == "__main__":
    main()
