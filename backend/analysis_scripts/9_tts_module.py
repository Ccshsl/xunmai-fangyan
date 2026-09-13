"""
脚本9：AI语音合成与教学模块 - 9_tts_module.py
1. 方言语音合成（使用百度TTS API）
2. 自动生成方言知识卡片
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import *
import os

try:
    from aip import AipSpeech
    BAIDU_TTS_AVAILABLE = True
except ImportError:
    BAIDU_TTS_AVAILABLE = False
    print("提示：未安装百度语音SDK，语音合成功能不可用")

# 百度TTS配置（需要用户自行申请API Key）
BAIDU_APP_ID = 'YOUR_APP_ID'
BAIDU_API_KEY = 'YOUR_API_KEY'
BAIDU_SECRET_KEY = 'YOUR_SECRET_KEY'

# 方言语音编码映射
DIALECT_VOICE_MAP = {
    '普通话': {'per': 0, 'lang': 'zh'},
    '粤语': {'per': 5, 'lang': 'zh'},
    '四川话': {'per': 11, 'lang': 'zh'},
    '闽南语': {'per': 13, 'lang': 'zh'},
    '东北话': {'per': 14, 'lang': 'zh'},
    '河南话': {'per': 15, 'lang': 'zh'},
    '陕西话': {'per': 16, 'lang': 'zh'},
    '湖南话': {'per': 17, 'lang': 'zh'},
    '山东话': {'per': 18, 'lang': 'zh'}
}

class DialectTTS:
    """方言语音合成类"""
    
    def __init__(self):
        if BAIDU_TTS_AVAILABLE and all([BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY]):
            self.client = AipSpeech(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
            self.available = True
        else:
            self.available = False
    
    def text_to_speech(self, text, dialect='普通话', output_file=None):
        """
        将文字合成为方言语音
        :param text: 要合成的文字
        :param dialect: 方言类型
        :param output_file: 输出音频文件路径
        :return: 音频数据或文件路径
        """
        if not self.available:
            return None, "语音合成功能不可用，请配置百度API Key"
        
        if dialect not in DIALECT_VOICE_MAP:
            print(f"警告：不支持的方言类型 '{dialect}'，使用普通话")
            dialect = '普通话'
        
        config = DIALECT_VOICE_MAP[dialect]
        
        result = self.client.synthesis(
            text,
            config['lang'],
            1,
            {
                'per': config['per'],
                'vol': 5,  # 音量
                'spd': 5,  # 语速
                'pit': 5   # 音调
            }
        )
        
        if not isinstance(result, dict):
            if output_file:
                with open(output_file, 'wb') as f:
                    f.write(result)
                return output_file, "success"
            return result, "success"
        else:
            return None, f"合成失败: {result.get('err_msg', '未知错误')}"
    
    def get_supported_dialects(self):
        """获取支持的方言列表"""
        return list(DIALECT_VOICE_MAP.keys())

class DialectTeachingModule:
    """方言教学模块"""
    
    def __init__(self):
        self.feature_words = None
        self.load_data()
    
    def load_data(self):
        """加载特征词数据"""
        try:
            self.feature_words = pd.read_csv(FEATURE_WORDS_FILE, encoding='utf-8-sig')
        except Exception as e:
            print(f"加载特征词数据失败: {e}")
    
    def generate_knowledge_card(self, city_index=0):
        """
        生成方言知识卡片
        :param city_index: 城市索引
        :return: 知识卡片内容字典
        """
        if self.feature_words is None:
            return None
        
        if city_index >= len(self.feature_words):
            return None
        
        row = self.feature_words.iloc[city_index]
        card = {
            '城市': row['城市'],
            '方言区': row['方言区'],
            '词汇对比': [
                {'普通话': '你', '方言': row['你']},
                {'普通话': '我', '方言': row['我']},
                {'普通话': '他', '方言': row['他']},
                {'普通话': '吃饭', '方言': row['吃饭']},
                {'普通话': '喝水', '方言': row['喝水']},
                {'普通话': '什么', '方言': row['什么']}
            ]
        }
        
        return card
    
    def generate_all_cards(self):
        """生成所有城市的知识卡片"""
        cards = []
        for i in range(len(self.feature_words)):
            card = self.generate_knowledge_card(i)
            if card:
                cards.append(card)
        return cards
    
    def save_card_image(self, card, output_file=None):
        """
        将知识卡片保存为图片
        :param card: 知识卡片字典
        :param output_file: 输出图片路径
        """
        if not output_file:
            output_file = OUTPUT_DIR + f"/knowledge_card_{card['城市']}.png"
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title(f"{card['城市']} - {card['方言区']} 方言知识卡片", fontsize=14, pad=20)
        ax.axis('off')
        
        # 创建表格数据
        table_data = [['普通话', '方言']]
        for item in card['词汇对比']:
            table_data.append([item['普通话'], item['方言']])
        
        # 创建表格
        table = ax.table(
            cellText=table_data,
            loc='center',
            cellLoc='center',
            colLabels=None
        )
        
        # 设置表格样式
        table.set_fontsize(14)
        table.scale(1, 2)
        
        # 设置表头样式
        for i in range(2):
            cell = table[0, i]
            cell.set_text_props(fontweight='bold', fontsize=12)
            cell.set_facecolor('#4a90d9')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_file
    
    def generate_learning_report(self):
        """生成学习报告"""
        if self.feature_words is None:
            return None
        
        report = {
            'total_cities': len(self.feature_words),
            'dialect_areas': self.feature_words['方言区'].unique().tolist(),
            'common_features': {
                '第二人称': self.feature_words['你'].value_counts().head(5).to_dict(),
                '第一人称': self.feature_words['我'].value_counts().head(5).to_dict(),
                '第三人称': self.feature_words['他'].value_counts().head(5).to_dict()
            }
        }
        
        return report

def main():
    print("=" * 60)
    print("脚本9：AI语音合成与教学模块")
    print("=" * 60)
    
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 初始化教学模块
    print("\n[步骤1] 初始化教学模块...")
    teaching_module = DialectTeachingModule()
    
    # 生成知识卡片
    print("\n[步骤2] 生成方言知识卡片...")
    cards = teaching_module.generate_all_cards()
    if cards:
        print(f"   共生成 {len(cards)} 张知识卡片")
        
        # 保存前5张卡片
        for i, card in enumerate(cards[:5]):
            output_file = teaching_module.save_card_image(card)
            print(f"   已保存: {os.path.basename(output_file)}")
    
    # 生成学习报告
    print("\n[步骤3] 生成学习报告...")
    report = teaching_module.generate_learning_report()
    if report:
        print("【学习报告摘要】")
        print(f"  覆盖城市数: {report['total_cities']}")
        print(f"  方言区数量: {len(report['dialect_areas'])}")
        print(f"  主要方言区: {', '.join(report['dialect_areas'][:5])}...")
        
        # 保存报告
        report_df = pd.DataFrame({
            '统计项': ['城市总数', '方言区数量'],
            '数值': [report['total_cities'], len(report['dialect_areas'])]
        })
        report_file = OUTPUT_DIR + '/learning_report.csv'
        report_df.to_csv(report_file, index=False, encoding='utf-8-sig')
        print(f"   已保存学习报告: {report_file}")
    
    # 语音合成演示
    print("\n[步骤4] 语音合成功能演示...")
    tts = DialectTTS()
    if tts.available:
        print(f"   支持的方言: {', '.join(tts.get_supported_dialects())}")
        
        # 示例：合成"你好，这是方言语音合成演示"
        test_text = "你好，这是方言语音合成演示"
        for dialect in ['普通话', '粤语', '四川话'][:3]:
            output_file = OUTPUT_DIR + f"/tts_{dialect}.mp3"
            result, msg = tts.text_to_speech(test_text, dialect, output_file)
            if result:
                print(f"   已合成 {dialect}: {os.path.basename(output_file)}")
            else:
                print(f"   {dialect}合成失败: {msg}")
    else:
        print("   提示：语音合成功能需要配置百度API Key")
        print("   请在脚本中设置 BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY")
        print("   申请地址: https://ai.baidu.com/tech/speech/tts")
    
    print("\n" + "=" * 60)
    print("AI语音合成与教学模块完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()