"""
脚本8：语言演变模拟 - 8_evolution_sim.py
元胞自动机模型模拟方言演变
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import *

class LanguageEvolutionSimulator:
    """语言演变模拟类（元胞自动机模型）"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.initial_rates = df['youth_usage_rate'].values
        self.current_rates = df['youth_usage_rate'].values.copy()
        self.cities = df['city'].tolist()
        self.yearly_records = []
    
    def simulate_year(self, decay_rate=0.01, diffusion_rate=0.05):
        """模拟一年的变化"""
        new_rates = self.current_rates.copy()
        new_rates = new_rates * (1 - decay_rate)
        
        adjacency = self._create_adjacency()
        
        for i in range(len(self.cities)):
            neighbors = np.where(adjacency[i] == 1)[0]
            if len(neighbors) > 0:
                neighbor_avg_rate = np.mean(self.current_rates[neighbors])
                new_rates[i] = (1 - diffusion_rate) * new_rates[i] + diffusion_rate * neighbor_avg_rate
        
        new_rates = np.clip(new_rates, 0, 1)
        self.current_rates = new_rates
        
        return new_rates
    
    def _create_adjacency(self):
        """创建地理邻接关系"""
        n = len(self.cities)
        adjacency = np.zeros((n, n))
        
        neighbors = [
            (0, 4), (0, 9),
            (1, 10),
            (2, 8),
            (3, 4), (3, 5),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 11),
            (8, 11),
        ]
        
        for i, j in neighbors:
            adjacency[i, j] = 1
            adjacency[j, i] = 1
        
        return adjacency
    
    def run_simulation(self, years=50, decay_rate=0.01, diffusion_rate=0.05):
        """运行完整模拟"""
        self.yearly_records.append(self.current_rates.copy())
        
        for year in range(years):
            self.simulate_year(decay_rate, diffusion_rate)
            self.yearly_records.append(self.current_rates.copy())
        
        return np.array(self.yearly_records)
    
    def calculate_risk_level(self):
        """计算风险等级"""
        final_rates = self.current_rates
        
        conditions = [
            (final_rates >= 0.6),
            (final_rates >= 0.4) & (final_rates < 0.6),
            (final_rates < 0.4)
        ]
        choices = ['低危', '中危', '高危']
        risk_levels = np.select(conditions, choices, default='未知')
        
        return risk_levels
    
    def get_risk_report(self):
        """生成风险报告"""
        risk_levels = self.calculate_risk_level()
        final_rates = self.current_rates
        initial_rates = self.initial_rates
        
        report = pd.DataFrame({
            '城市': self.cities,
            '方言区': self.df['dialect_area'],
            '初始使用率': initial_rates,
            '50年后使用率': final_rates,
            '使用率变化': final_rates - initial_rates,
            '风险等级': risk_levels
        })
        
        return report

def plot_evolution(records, cities, dialect_areas):
    """绘制时间序列演变图（按方言区整合）"""
    plt.figure(figsize=(12, 8))
    
    # 创建方言区到索引的映射
    dialect_indices = {}
    for i, dialect in enumerate(dialect_areas):
        # 简化方言区名称
        dialect_short = dialect
        if '官话' in dialect:
            dialect_short = dialect.replace('官话', '') + '官'
        elif '片' in dialect:
            dialect_short = dialect[:2]
        elif len(dialect) > 4:
            dialect_short = dialect[:3]
        
        if dialect_short not in dialect_indices:
            dialect_indices[dialect_short] = []
        dialect_indices[dialect_short].append(i)
    
    # 为每个方言区计算平均使用率
    colors = plt.cm.tab20(np.linspace(0, 1, len(dialect_indices)))
    
    for idx, (dialect, indices) in enumerate(dialect_indices.items()):
        # 计算该方言区所有城市的平均使用率
        avg_records = records[:, indices].mean(axis=1)
        plt.plot(avg_records, label=dialect, linewidth=2, color=colors[idx])
    
    plt.title('方言年轻人使用率50年演变趋势（按方言区）', fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('平均使用率', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(LANGUAGE_EVOLUTION_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: {LANGUAGE_EVOLUTION_FILE}")

def plot_comparison(initial_rates, final_rates, cities, dialect_areas):
    """绘制初始vs50年后对比图（按方言区整合）"""
    # 创建方言区到数据的映射
    dialect_data = {}
    for city, dialect, initial, final in zip(cities, dialect_areas, initial_rates, final_rates):
        # 简化方言区名称
        dialect_short = dialect
        if '官话' in dialect:
            dialect_short = dialect.replace('官话', '') + '官'
        elif '片' in dialect:
            dialect_short = dialect[:2]
        elif len(dialect) > 4:
            dialect_short = dialect[:3]
        
        if dialect_short not in dialect_data:
            dialect_data[dialect_short] = {'initial': [], 'final': []}
        dialect_data[dialect_short]['initial'].append(initial)
        dialect_data[dialect_short]['final'].append(final)
    
    # 计算每个方言区的平均使用率
    dialect_names = list(dialect_data.keys())
    avg_initial = [np.mean(dialect_data[d]['initial']) for d in dialect_names]
    avg_final = [np.mean(dialect_data[d]['final']) for d in dialect_names]
    
    x = np.arange(len(dialect_names))
    width = 0.35
    
    plt.figure(figsize=(16, 8))
    plt.bar(x - width/2, avg_initial, width, label='初始使用率', color='skyblue')
    plt.bar(x + width/2, avg_final, width, label='50年后使用率', color='salmon')
    
    plt.title('方言使用率初始与50年后对比（按方言区）', fontsize=16)
    plt.xlabel('方言区', fontsize=12)
    plt.ylabel('平均使用率', fontsize=12)
    plt.xticks(x, dialect_names, rotation=45, fontsize=10)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(EVOLUTION_COMPARISON_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   已保存: {EVOLUTION_COMPARISON_FILE}")

def main():
    print("=" * 60)
    print("脚本8：语言演变模拟")
    print("=" * 60)
    
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    print("\n[步骤1] 读取数据...")
    df = pd.read_csv(CLEANED_POINTS_FILE, encoding='utf-8-sig')
    
    print("\n[步骤2] 创建演变模拟器...")
    simulator = LanguageEvolutionSimulator(df)
    
    print("\n[步骤3] 运行50年演变模拟...")
    # 基于真实调研数据调整参数：
    # - decay_rate=0.02: 年衰减率2%（基于吴语区调研数据显示的衰退速度）
    # - diffusion_rate=0.03: 扩散率3%（考虑现代人口流动加速方言融合）
    records = simulator.run_simulation(years=50, decay_rate=0.02, diffusion_rate=0.03)
    
    print("\n[步骤4] 生成风险报告...")
    risk_report = simulator.get_risk_report()
    print("【50年后风险评估报告】")
    print(risk_report)
    
    risk_report.to_csv(RISK_REPORT_FILE, index=False, encoding='utf-8-sig')
    print(f"\n   已保存: {RISK_REPORT_FILE}")
    
    print("\n[步骤5] 绘制演变趋势图...")
    plot_evolution(records, df['city'].tolist(), df['dialect_area'].tolist())
    
    print("\n[步骤6] 绘制对比图...")
    plot_comparison(simulator.initial_rates, simulator.current_rates, df['city'].tolist(), df['dialect_area'].tolist())
    
    print("\n" + "=" * 60)
    print("语言演变模拟完成！")
    print("=" * 60)
    
    return risk_report

if __name__ == "__main__":
    main()
