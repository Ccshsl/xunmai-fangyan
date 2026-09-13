"""
脚本2：数据清洗 - 2_data_cleaning.py
读取并清洗方言点数据，处理缺失值和异常值
"""

import pandas as pd
import numpy as np
from config import *

def load_data(filepath):
    """读取方言点数据"""
    return pd.read_csv(filepath, encoding='utf-8-sig')

def analyze_missing_values(df):
    """检查并报告缺失值"""
    missing = df.isnull().sum()
    print("缺失值统计：")
    for col, count in missing.items():
        if count > 0:
            print(f"  {col}: {count} 个缺失值")
        else:
            print(f"  {col}: OK 无缺失")
    return missing

def analyze_outliers(df):
    """检查并报告异常值"""
    print("\n异常值检查：")
    
    lon_outliers = df[(df['longitude'] < 73) | (df['longitude'] > 135)]
    print(f"  经度异常值: {len(lon_outliers)} 个")
    
    lat_outliers = df[(df['latitude'] < 18) | (df['latitude'] > 54)]
    print(f"  纬度异常值: {len(lat_outliers)} 个")
    
    pop_outliers = df[(df['population_10k'] < 0) | (df['population_10k'] > 3000)]
    print(f"  人口异常值: {len(pop_outliers)} 个")
    
    rate_outliers = df[(df['youth_usage_rate'] < 0) | (df['youth_usage_rate'] > 1)]
    print(f"  使用率异常值: {len(rate_outliers)} 个")
    
    return lon_outliers, lat_outliers, pop_outliers, rate_outliers

def add_derived_fields(df):
    """添加派生字段"""
    df['endanger_index'] = 1 - df['youth_usage_rate']
    
    conditions = [
        (df['youth_usage_rate'] >= 0.7),
        (df['youth_usage_rate'] >= 0.5) & (df['youth_usage_rate'] < 0.7),
        (df['youth_usage_rate'] >= 0.3) & (df['youth_usage_rate'] < 0.5),
        (df['youth_usage_rate'] < 0.3)
    ]
    choices = ['安全', '较安全', '脆弱', '濒危']
    df['endanger_level'] = np.select(conditions, choices, default='未知')
    
    return df

def clean_data(df):
    """执行数据清洗"""
    cleaned = df.copy()
    
    if cleaned['population_10k'].isnull().any():
        cleaned['population_10k'].fillna(cleaned['population_10k'].median(), inplace=True)
    if cleaned['youth_usage_rate'].isnull().any():
        cleaned['youth_usage_rate'].fillna(cleaned['youth_usage_rate'].median(), inplace=True)
    
    cleaned = cleaned[(cleaned['longitude'] >= 73) & (cleaned['longitude'] <= 135)]
    cleaned = cleaned[(cleaned['latitude'] >= 18) & (cleaned['latitude'] <= 54)]
    
    cleaned['youth_usage_rate'] = np.clip(cleaned['youth_usage_rate'], 0, 1)
    
    return cleaned

def main():
    print("=" * 60)
    print("脚本2：数据清洗")
    print("=" * 60)
    
    print("\n[步骤1] 读取方言点数据...")
    df = load_data(DIALECT_POINTS_FILE)
    print(f"   原始数据: {len(df)} 条记录")
    print("\n数据概览：")
    print(df.head())
    
    print("\n[步骤2] 检查缺失值...")
    analyze_missing_values(df)
    
    print("\n[步骤3] 检查异常值...")
    analyze_outliers(df)
    
    print("\n[步骤4] 执行数据清洗...")
    cleaned_df = clean_data(df)
    print(f"   清洗后数据: {len(cleaned_df)} 条记录")
    
    print("\n[步骤5] 添加派生字段...")
    cleaned_df = add_derived_fields(cleaned_df)
    print("   添加字段: endanger_index(濒危指数), endanger_level(濒危等级)")
    
    print("\n[步骤6] 输出清洗后数据...")
    cleaned_df.to_csv(CLEANED_POINTS_FILE, index=False, encoding='utf-8-sig')
    print(f"   已保存: {CLEANED_POINTS_FILE}")
    
    print("\n清洗后数据概览：")
    print(cleaned_df[['city', 'dialect_area', 'youth_usage_rate', 'endanger_index', 'endanger_level']])
    
    print("\n" + "=" * 60)
    print("数据清洗完成！")
    print("=" * 60)
    
    return cleaned_df

if __name__ == "__main__":
    main()
