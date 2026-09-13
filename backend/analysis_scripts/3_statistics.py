"""
脚本3：统计分析 - 3_statistics.py
方言区人口统计、年轻人使用率分析、濒危方言识别
"""

import pandas as pd
import numpy as np
from config import *

def load_cleaned_data(filepath):
    """读取清洗后的数据"""
    return pd.read_csv(filepath, encoding='utf-8-sig')

def analyze_population(df):
    """各方言区使用人口统计"""
    pop_stats = df.groupby('dialect_area').agg(
        total_population=('population_10k', 'sum'),
        city_count=('city', 'count')
    ).sort_values('total_population', ascending=False)
    
    print("【方言区人口统计】")
    print(pop_stats)
    print()
    return pop_stats

def analyze_youth_rate(df):
    """各方言区年轻人使用率统计"""
    rate_stats = df.groupby('dialect_area').agg(
        avg_usage_rate=('youth_usage_rate', 'mean'),
        min_usage_rate=('youth_usage_rate', 'min'),
        max_usage_rate=('youth_usage_rate', 'max')
    ).sort_values('avg_usage_rate', ascending=False)
    
    print("【年轻人使用率统计】")
    print(rate_stats)
    print()
    return rate_stats

def identify_endangered_dialects(df, threshold=0.5):
    """识别濒危方言（年轻人使用率<50%）"""
    endangered = df[df['youth_usage_rate'] < threshold].sort_values('youth_usage_rate')
    
    print(f"【濒危方言识别】(使用率 < {threshold})")
    if len(endangered) > 0:
        print(endangered[['city', 'dialect_area', 'youth_usage_rate', 'endanger_level']])
    else:
        print("   暂无濒危方言")
    print()
    return endangered

def descriptive_statistics(df):
    """输出描述性统计"""
    print("【描述性统计】")
    stats = df[['population_10k', 'youth_usage_rate', 'endanger_index']].describe()
    print(stats)
    print()
    return stats

def main():
    print("=" * 60)
    print("脚本3：统计分析")
    print("=" * 60)
    
    print("\n[步骤1] 读取清洗后数据...")
    df = load_cleaned_data(CLEANED_POINTS_FILE)
    print(f"   数据条数: {len(df)}")
    
    print("\n[步骤2] 方言区人口统计...")
    pop_stats = analyze_population(df)
    
    print("\n[步骤3] 年轻人使用率分析...")
    rate_stats = analyze_youth_rate(df)
    
    print("\n[步骤4] 濒危方言识别...")
    endangered = identify_endangered_dialects(df)
    
    print("\n[步骤5] 描述性统计...")
    desc_stats = descriptive_statistics(df)
    
    print("\n[步骤6] 生成汇总报告...")
    summary = pd.DataFrame({
        '指标': ['方言点总数', '方言区数量', '总人口(万人)', '平均使用率', 
                '最高使用率', '最低使用率', '濒危方言数'],
        '数值': [
            len(df),
            df['dialect_area'].nunique(),
            df['population_10k'].sum(),
            f"{df['youth_usage_rate'].mean():.2f}",
            f"{df['youth_usage_rate'].max():.2f}",
            f"{df['youth_usage_rate'].min():.2f}",
            len(endangered)
        ]
    })
    print("【汇总统计】")
    print(summary)
    
    summary.to_csv(STATISTICS_SUMMARY_FILE, index=False, encoding='utf-8-sig')
    print(f"\n   已保存: {STATISTICS_SUMMARY_FILE}")
    
    print("\n" + "=" * 60)
    print("统计分析完成！")
    print("=" * 60)
    
    return pop_stats, rate_stats, endangered, desc_stats

if __name__ == "__main__":
    main()
